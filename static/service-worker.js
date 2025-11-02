// ✅ SSA - Smart Sports Athlete Service Worker
// Version: 2.0
// Purpose: Offline support + background sync + periodic sync + notifications

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

// 🧱 STEP 1 — INSTALL PHASE (Cache essential files)
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log("🗂️ Caching essential files...");
      return cache.addAll(urlsToCache);
    })
  );
});

// 🧱 STEP 2 — ACTIVATE PHASE (Clean old cache versions)
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
  console.log("⚙️ Service Worker Activated: " + CACHE_NAME);
});

// 🧱 STEP 3 — OFFLINE SUPPORT (Serve cached content)
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // Use cache first, then fetch new
      return response || fetch(event.request).catch(() => {
        console.warn("🚫 Offline fallback triggered for:", event.request.url);
        return caches.match("/"); // fallback to homepage if offline
      });
    })
  );
});

// 🧱 STEP 4 — BACKGROUND SYNC (Handle pending requests)
self.addEventListener("sync", event => {
  if (event.tag === "background-sync") {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  // You can store pending requests in IndexedDB and resend them here
  console.log("🔄 Background sync triggered - re-sending pending data...");
}

// 🧱 STEP 5 — PERIODIC SYNC (Auto fetch updates periodically)
self.addEventListener("periodicsync", event => {
  if (event.tag === "refresh-data") {
    event.waitUntil(refreshData());
  }
});

async function refreshData() {
  console.log("🔁 Periodic Sync triggered: Fetching latest data...");
  try {
    const response = await fetch("/api/refresh");
    const data = await response.json();
    console.log("✅ Data refreshed:", data);
  } catch (err) {
    console.error("❌ Periodic Sync failed:", err);
  }
}

// 🧱 STEP 6 — PUSH NOTIFICATIONS (Show notifications)
self.addEventListener("push", event => {
  const options = {
    body: event.data ? event.data.text() : "New notification",
    icon: "/static/abhinav_profile.jpg",
    badge: "/static/abhinav_profile.jpg"
  };
  event.waitUntil(self.registration.showNotification("SSA", options));
});

// 🧱 STEP 7 — NOTIFICATION CLICK HANDLER
self.addEventListener("notificationclick", event => {
  event.notification.close();
  event.waitUntil(clients.openWindow("/"));
});
