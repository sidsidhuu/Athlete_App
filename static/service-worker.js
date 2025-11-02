// /static/service-worker.js
const CACHE_NAME = 'ssa-cache-v5';
const OFFLINE_PAGE = '/static/offline.html';
const PRECACHE = [
  '/',
  '/static/manifest.json',
  '/static/icon-192x192.png',
  '/static/icon-512x512.png',
  '/static/abhinav_profile.jpg',
  '/static/styles.css',   // if exists
  '/static/script.js',   // if exists
  OFFLINE_PAGE
];

// --- tiny IDB helper ---
const IDB_DB = 'ssa-queue';
const IDB_STORE = 'outbox';
function idbOpen() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(IDB_DB, 1);
    req.onupgradeneeded = () => {
      req.result.createObjectStore(IDB_STORE, { keyPath: 'id', autoIncrement: true });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}
async function idbAdd(item) {
  const db = await idbOpen();
  return new Promise((res, rej) => {
    const tx = db.transaction(IDB_STORE, 'readwrite');
    const store = tx.objectStore(IDB_STORE);
    const r = store.add(item);
    r.onsuccess = () => { res(r.result); db.close(); };
    r.onerror = () => { rej(r.error); db.close(); };
  });
}
async function idbGetAll() {
  const db = await idbOpen();
  return new Promise((res, rej) => {
    const tx = db.transaction(IDB_STORE, 'readonly');
    const store = tx.objectStore(IDB_STORE);
    const r = store.getAll();
    r.onsuccess = () => { res(r.result); db.close(); };
    r.onerror = () => { rej(r.error); db.close(); };
  });
}
async function idbDelete(id) {
  const db = await idbOpen();
  return new Promise((res, rej) => {
    const tx = db.transaction(IDB_STORE, 'readwrite');
    const store = tx.objectStore(IDB_STORE);
    const r = store.delete(id);
    r.onsuccess = () => { res(true); db.close(); };
    r.onerror = () => { rej(r.error); db.close(); };
  });
}

// --- Install: precache ---
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE))
  );
  self.skipWaiting();
});

// --- Activate: clean old caches ---
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.map(key => key === CACHE_NAME ? null : caches.delete(key))
    ))
  );
  self.clients.claim();
});

// --- Fetch: network-first for API, cache-first for static resources ---
self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  // Ignore non-GET
  if (req.method !== 'GET') return;

  // API calls: network-first with cache fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(req).then(resp => {
        // clone response to cache
        const copy = resp.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(req, copy)).catch(()=>{});
        return resp;
      }).catch(() => caches.match(req).then(cached => cached || new Response(JSON.stringify({ error: 'offline' }), { status: 503 })))
    );
    return;
  }

  // For navigation requests and app shell, try network, fallback to cache/offline page
  if (req.mode === 'navigate' || req.headers.get('accept') && req.headers.get('accept').includes('text/html')) {
    event.respondWith(
      fetch(req).then(resp => {
        const copy = resp.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(req, copy)).catch(()=>{});
        return resp;
      }).catch(() => caches.match(req).then(cached => cached || caches.match(OFFLINE_PAGE)))
    );
    return;
  }

  // For other static resources: cache-first
  event.respondWith(
    caches.match(req).then(cached => cached || fetch(req).then(resp => {
      const copy = resp.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(req, copy)).catch(()=>{});
      return resp;
    }).catch(() => new Response(null, { status: 404 })))
  );
});

// --- Message: queue requests from client ---
self.addEventListener('message', event => {
  if (!event.data) return;
  if (event.data.type === 'QUEUE_REQUEST') {
    idbAdd(event.data.request).then(() => {
      self.registration.sync.register('background-sync').catch(()=>{});
    });
  }
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});

// --- Background Sync: flush queue ---
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(flushOutbox());
  }
});

async function flushOutbox() {
  const items = await idbGetAll();
  for (const item of items) {
    try {
      const opts = { method: item.method || 'POST', headers: item.headers || { 'Content-Type': 'application/json' }, body: item.body ? JSON.stringify(item.body) : undefined };
      const res = await fetch(item.url, opts);
      if (res && (res.status === 200 || res.status === 201 || res.status === 204)) {
        await idbDelete(item.id);
      }
    } catch (err) {
      console.warn('flush failed, keep item', item.id, err);
    }
  }
}

// --- Periodic Sync ---
self.addEventListener('periodicsync', event => {
  if (event.tag === 'refresh-data' || event.tag === 'periodic-sync') {
    event.waitUntil(periodicRefresh());
  }
});

async function periodicRefresh() {
  try {
    const res = await fetch('/api/performance/today');
    if (res && res.ok) {
      const data = await res.json();
      // cache the latest API response
      const cache = await caches.open(CACHE_NAME);
      await cache.put('/api/performance/today', new Response(JSON.stringify(data)));
      console.log('Periodic refresh done');
    }
  } catch (err) {
    console.warn('Periodic refresh failed', err);
  }
}

// --- Push Notifications ---
self.addEventListener('push', event => {
  const payload = event.data ? event.data.json ? event.data.json() : { body: event.data.text() } : { body: 'New notification' };
  const title = payload.title || 'SSA';
  const options = {
    body: payload.body || 'New update',
    icon: '/static/abhinav_profile.jpg',
    badge: '/static/abhinav_profile.jpg',
    data: payload.url || '/'
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  const url = event.notification.data || '/';
  event.waitUntil(clients.openWindow(url));
});
