# Servicio Técnico Mabe Quito (mabequito.click)

- Carpeta `mabe-quito/` (raíz): sitio listo para subir a la raíz del dominio (403 páginas).
- `fuente/`: generador en Python. Regenerar: `python3 gen.py site` (necesita `img/` y `assets/`).
- Fotos de técnicos con uniforme "Servicio Autorizado": apagadas por defecto. Solo se activan con `MABE_AUTH=1 python3 gen.py site` si el negocio es servicio autorizado de Mabe.
- Etiqueta de Search Console: crear `gsc-meta.txt` con la etiqueta `<meta name="google-site-verification" ...>` antes de generar.
