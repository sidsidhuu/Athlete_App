// static/service-worker.js (paste exactly)
const CACHE_NAME = 'ssa-app-v1';
const OFFLINE_URL = '/static/offline.html';
const PRECACHE = [
  '/',
  '/static/manifest.json',
  '/static/icon-192x192.png',
  '/static/icon-512x512.png',
  '/static/abhinav_profile.jpg',
  OFFLINE_URL
];

// Install: precache
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE)));
  self.skipWaiting();
});

// Activate: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.map(k => k === CACHE_NAME ? null : caches.delete(k))))
  );
  self.clients.claim();
});

// Fetch: network first for navigation, cache-first for others
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  // Navigation (HTML) requests -> network-first, fallback to offline page
  if (event.request.mode === 'navigate' || (event.request.headers.get('accept') || '').includes('text/html')) {
    event.respondWith(
      fetch(event.request).then(response => {
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, response.clone()));
        return response;
      }).catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }

  // Static assets -> cache-first
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        // put into cache for future
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, response.clone()));
        return response;
      }).catch(() => {
        // if not in cache, return a 503 response
        return new Response('Offline', { status: 503, statusText: 'Offline' });
      });
    })
  );
});

// Periodic Sync: fetch latest data in background
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'fetch-latest-data') {
    event.waitUntil(fetchAndCacheData());
  }
});

async function fetchAndCacheData() {
  try {
    const response = await fetch('/api/refresh'); // Use existing refresh endpoint
    const data = await response.json();
    const cache = await caches.open(CACHE_NAME);
    await cache.put('/latest-data', new Response(JSON.stringify(data)));
    console.log('✅ Background data updated!');
  } catch (error) {
    console.error('❌ Periodic Sync failed:', error);
  }
}
