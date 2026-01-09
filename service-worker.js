// Service Worker para Recetario Épico
const CACHE_NAME = 'recetario-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json'
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache).catch(() => {
        // Si falla agregar algunos archivos, continúa
        console.log('Algunos archivos no pudieron ser cacheados');
      });
    })
  );
  self.skipWaiting();
});

// Activar Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Estrategia: Network first, fallback to cache
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Clonar la respuesta
        const clonedResponse = response.clone();
        
        // Actualizar cache en background
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, clonedResponse);
        });
        
        return response;
      })
      .catch(() => {
        // Si falla la red, usar cache
        return caches.match(event.request).then((response) => {
          return response || new Response('No disponible offline', { status: 503 });
        });
      })
  );
});
