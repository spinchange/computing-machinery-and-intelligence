const CACHE_NAME = 'turing-1950-v1';

const ASSETS = [
  './',
  'index.html',
  'style.css',
  'app.js',
  'fonts.css',
  'manifest.json',
  'icon.svg',
  'icon-192.png',
  'icon-512.png',
  'og-preview.png',
  'llms.txt',
  'llms-full.txt',
  'fonts/cinzel-normal-500.woff2',
  'fonts/cinzel-normal-700.woff2',
  'fonts/inter-normal-400.woff2',
  'fonts/inter-normal-500.woff2',
  'fonts/inter-normal-600.woff2',
  'fonts/inter-normal-700.woff2',
  'fonts/jetbrains-mono-normal-400.woff2',
  'fonts/jetbrains-mono-normal-500.woff2',
  'fonts/newsreader-italic-400700.woff2',
  'fonts/newsreader-normal-400700.woff2'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });
        return networkResponse;
      }).catch(() => {
        // Offline fallback for HTML requests
        if (event.request.headers.get('accept')?.includes('text/html')) {
          return caches.match('./');
        }
      });
    })
  );
});
