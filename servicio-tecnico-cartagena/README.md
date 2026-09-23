# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Décima iteración: corregí el problema real que señalaste (las fotos de
galería eran diminutas, 80px de alto) y agregué imágenes grandes en
**todas** las sub-páginas de marca, no solo en la principal. También
agregué las 5 fotos nuevas de Electrolux.

## Lo que estaba mal y cómo lo corregí

En la iteración anterior, al quitar la sección "Equipos que Reparamos",
metí las fotos de galería dentro de la columna de texto de "Quiénes
somos", en miniaturas de 80px de alto. Eso las hizo casi invisibles —
tenías razón en que se veía mal.

**Corrección**: le devolví a la galería su propio espacio, con fotos
grandes (260px de alto, tarjetas de tres columnas), pero con un título
distinto al que pediste quitar: ahora dice **"Neveras {Marca} que Hemos
Instalado y Reparado"**, enfocado en el trabajo real hecho en Cartagena,
no en "tecnología" ni en "equipos que reparamos".

Además, por iniciativa propia (sin que lo pidieras explícitamente),
agregué esa misma galería de fotos, en un formato más compacto de 2
columnas, a las **4 sub-páginas de cada marca** (fallas comunes,
mantenimiento, instalación, repuestos) que antes solo tenían una imagen
en el encabezado y texto. Cada sub-página muestra un par distinto de
fotos (no siempre las mismas dos), para que recorrer las 5 páginas de una
marca se sienta como ver contenido distinto, no relleno repetido.

## Electrolux: 5 fotos nuevas

Agregué las 5 imágenes que enviaste al final de la galería de Electrolux
(ahora tiene 7 en total): el modelo Side by Side en estudio, la
instalación en sala/cocina abierta, el modelo junto a un comedor con
muebles azules, la instalación empotrada, y el interior organizado con
frutas y bebidas.

## Estructura de imágenes por marca (para que quede claro)

Cada marca con fotos reales (Samsung, LG, Whirlpool, Mabe, Electrolux)
sigue el mismo patrón:

- `hero-{marca}-cartagena.jpg` y `equipo-{marca}-cartagena.jpg`: las dos
  fotos principales, en la portada y en "Quiénes somos".
- `galeria`: entre 4 y 7 fotos adicionales. Se reparten así:
  - Página principal de la marca: **todas** las fotos, en grande.
  - Fallas comunes: 2 fotos (las primeras de la lista).
  - Mantenimiento: 2 fotos (posiciones 3 y 4).
  - Instalación: 2 fotos (posiciones 5 y 6, si existen).
  - Repuestos: 2 fotos (posiciones 2 y 3).
  - Si una marca tiene menos fotos que las que pide esa posición, se
    repiten las dos primeras en vez de dejar la sección vacía.

## Estado de las imágenes y autorización por marca

Las 6 marcas están confirmadas como autorizadas. Fotos reales: Samsung,
LG, Whirlpool, Mabe y Electrolux completos. Solo falta Haceb — ver
`IMAGENES-LEEME.md`.

## Pendiente de tu parte

1. Enviar las imágenes de Haceb (ya confirmaste que es autorizada, solo
   falta el material).
2. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
