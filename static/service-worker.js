const CACHE_NAME = "ssa-cache-v4";
const urlsToCache = [
  "/",
  "/dashboard",
  "/profile",
  "/performance",
  "/settings",
  "/notes",
  "/notes/new",
  "/static/styles.css",
  "/static/script.js",
  "/static/manifest.json",
  "/static/abhinav_profile.jpg",
  "/static/icon-192x192.png",
  "/static/icon-512x512.png",
  "/static/offline.html",
  "/static/widget.html",
  "/static/note_taking.html"
];

// Install: pre-cache
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

// Activate: clean old caches
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(key => {
        if (key !== CACHE_NAME) return caches.delete(key);
      }))
    )
  );
});

// Fetch: network-first strategy with offline fallback
self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      })
      .catch(() => {
        // Return offline page for navigation requests
        if (event.request.mode === 'navigate') {
          return caches.match('/static/offline.html');
        }
        return caches.match(event.request);
      })
  );
});

// Background sync for offline requests
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(syncOfflineRequests());
  }
});

// Push notifications
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New update available!',
    icon: '/static/icon-192x192.png',
    badge: '/static/icon-192x192.png'
  };
  event.waitUntil(
    self.registration.showNotification('SSA Update', options)
  );
});

// Periodic sync for updating athlete data
self.addEventListener("periodicsync", event => {
  if (event.tag === "update-athlete-data") {
    event.waitUntil(updateAthleteData());
  }
});

// Handle messages from main thread
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'QUEUE_REQUEST') {
    queueRequest(event.data.request);
  }
});

// Queue requests for later sync
function queueRequest(request) {
  // Store in IndexedDB or similar for offline sync
  console.log('Queued request for offline sync:', request);
}

// Sync offline requests when back online
function syncOfflineRequests() {
  // Process queued requests
  console.log('Syncing offline requests...');
}

// Periodic sync function to update athlete data
async function updateAthleteData() {
  console.log("Periodic Sync: updating athlete data...");
  // Example fetch: update cached performance data
  const response = await fetch("/api/performance/latest");
  const data = await response.json();
  const cache = await caches.open(CACHE_NAME);
  await cache.put("/api/performance/latest", new Response(JSON.stringify(data)));
}
