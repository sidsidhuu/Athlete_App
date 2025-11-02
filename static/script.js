// Periodic Sync Registration
if ('serviceWorker' in navigator && 'PeriodicSyncManager' in window) {
  navigator.serviceWorker.ready.then(async (reg) => {
    const status = await navigator.permissions.query({ name: 'periodic-background-sync' });
    if (status.state === 'granted') {
      try {
        await reg.periodicSync.register('refresh-data', {
          minInterval: 24 * 60 * 60 * 1000 // 1 day
        });
        console.log("✅ Periodic Sync registered successfully!");
      } catch (err) {
        console.error("❌ Periodic Sync registration failed:", err);
      }
    }
  });
}
