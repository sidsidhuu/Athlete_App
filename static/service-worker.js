const CACHE_NAME = "ssa-cache-v1";
const urlsToCache = [
  "/",
  "/static/icon-192x192.png",
  "/static/icon-512x512.png"
];

// Install service worker
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

// Serve from cache when offline
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
