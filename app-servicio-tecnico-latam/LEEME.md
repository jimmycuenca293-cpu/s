# App Soporte Técnico Autorizado (marca + ubicación)
Dominio: https://soporte-tecnico-autorizado.com
- `config.json`: dominio, GSC, GTM, WhatsApp por país, colores por marca.
- `tecnicos.csv`: técnicos reales (marca, país, ciudad, zona, lat, lon, whatsapp, nombre). Hoy hay uno por ciudad con el número del país.
- `python3 _fuente/build.py --estricto` → carpeta `site/` (sube su contenido a la raíz del dominio con HTTPS).
- URLs: /soporte-tecnico-autorizado-{marca}-{ubicación}/ en todas las páginas.
- Search Console: enviar /sitemap.xml (índice con un sitemap por marca).
