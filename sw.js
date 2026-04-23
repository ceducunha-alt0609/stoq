const CACHE_NAME = "stoq-cache-v2.0.0";
const APP_SHELL = [
  "./",
  "./index.html",
  "./offline.html",
  "./404.html",
  "./manifest.json",
  "./robots.txt",
  "./browserconfig.xml",
  "./icons/icon-72.png",
  "./icons/icon-96.png",
  "./icons/icon-128.png",
  "./icons/icon-144.png",
  "./icons/icon-152.png",
  "./icons/icon-192.png",
  "./icons/icon-384.png",
  "./icons/icon-512.png",
  "./icons/favicon-32.png",
  "./icons/favicon.ico",
  "./splash/splash-iphone-x.png",
  "./splash/splash-iphone-8.png",
  "./splash/splash-iphone-se.png",
  "./splash/splash-ipad-pro.png",
  "./splash/splash-ipad-air.png"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  const isSameOrigin = url.origin === self.location.origin;
  const acceptsHTML = request.headers.get("accept")?.includes("text/html");

  if (request.mode === "navigate" || acceptsHTML) {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (isSameOrigin && response.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
          }
          return response;
        })
        .catch(async () => {
          const cached = await caches.match(request);
          return cached || caches.match("./offline.html");
        })
    );
    return;
  }

  if (isSameOrigin) {
    event.respondWith(
      caches.match(request).then(cached => {
        if (cached) return cached;
        return fetch(request)
          .then(response => {
            if (response && response.ok) {
              const copy = response.clone();
              caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
            }
            return response;
          })
          .catch(() => caches.match("./offline.html"));
      })
    );
  }
});
