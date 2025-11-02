const CACHE_NAME = "ssa-cache-v3";
const urlsToCache = [
  "/",
  "/dashboard",
  "/profile",
  "/performance",
  "/settings",
  "/static/styles.css",
  "/static/script.js",
  "/static/manifest.json",
  "/static/abhinav_profile.jpg",
  "/static/icon-192x192.png",
  "/static/icon-512x512.png"
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

// Fetch: network-first strategy
self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
