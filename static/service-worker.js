const CACHE_NAME = "ssa-cache-v2";
const urlsToCache = [
  "/",
  "/static/abhinav_profile.jpg",
  "/static/manifest.json",
  "/static/styles.css",
  "/static/script.js",
  "/static/service-worker.js",
  "/dashboard",
  "/profile",
  "/performance",
  "/settings"
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

// Background sync for offline actions
self.addEventListener("sync", event => {
  if (event.tag === "background-sync") {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // Implement background sync logic here
  console.log("Background sync triggered");
}

// Push notifications
self.addEventListener("push", event => {
  const options = {
    body: event.data ? event.data.text() : "New notification",
    icon: "/static/abhinav_profile.jpg",
    badge: "/static/abhinav_profile.jpg"
  };
  event.waitUntil(
    self.registration.showNotification("SSA", options)
  );
});

// Handle notification click
self.addEventListener("notificationclick", event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow("/")
  );
});
