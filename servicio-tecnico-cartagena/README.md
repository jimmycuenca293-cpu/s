# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Undécima iteración: **las 6 marcas ya tienen fotos reales** (Haceb
completó la lista), redistribuí las fotos de galería para que cada una
viva junto a su sección correspondiente (no agrupadas), y agregué un
refuerzo técnico contra el salto de scroll que reportaste de nuevo.

## El salto de scroll — lo que encontré esta vez

Volví a probarlo de la forma más exigente posible: con Playwright abrí el
sitio real (los archivos estáticos, los mismos que estás descargando en
el zip) y reproduje en automático 15 navegaciones distintas — clic en
tarjeta de marca, en cada pestaña de sub-página, en zona, en marca+zona,
en servicio, en blog, en la guía de fallas, en preguntas frecuentes, e
incluso el caso exacto que más te preocupa: hacer clic en "Contacto"
(que sí debe bajar a esa sección, por diseño) y luego navegar a otra
página. **En los 15 casos, la página nueva carga con `scrollY: 0`**, es
decir, arriba del todo, donde está el `<h1>` con el título. No encontré
el bug en los archivos reales.

Aun así, **agregué una protección extra** que no dependía de que existiera
el bug o no: cada página ahora tiene un script en el `<head>` (antes de
que cargue cualquier otra cosa) que desactiva la restauración automática
de scroll del navegador y fuerza la posición a 0 si la URL no trae un
ancla específica (como `#contacto-samsung`). Esto es una capa de defensa
adicional, gratuita, que no puede empeorar nada.

**Mi conclusión honesta**: si sigues viendo el salto específicamente en la
vista previa de este chat (el link de Artifact), es probable que sea un
comportamiento de cómo esa vista previa maneja la navegación entre
páginas de un sitio multi-archivo, no un defecto del sitio en sí — porque
en un navegador real, con los archivos reales (los del zip, o subidos a
tu dominio), el comportamiento es correcto según la prueba automatizada.
Te recomiendo verificarlo abriendo el zip descargado con
`python3 -m http.server` (instrucciones abajo) o subiéndolo a tu hosting
real: ese es el comportamiento que verán tus clientes.

## Fotos de galería: redistribuidas por sección, no agrupadas

Corregí lo que señalaste: había juntado todas las fotos de galería en una
sola sección grande ("Neveras que Hemos Instalado y Reparado"). La quité
por completo. Ahora cada foto vive junto al contenido de su propia
sección:

- Página principal de la marca: una foto junto a "Fallas Comunes" y otra
  junto a "Reseñas de Clientes" (en lados opuestos, para variar).
- Sub-página de Fallas Comunes: una foto junto a "Preguntas sobre Fallas".
- Sub-página de Mantenimiento: una foto junto a "Frecuencia Recomendada".
- Sub-página de Instalación: una foto junto a "Tiempo Estimado".
- Sub-página de Repuestos: una foto junto a "Por Qué Elegir Repuestos
  Originales".

Si una marca tiene pocas fotos, se reutiliza la primera en vez de dejar
una sección sin imagen.

## Haceb: ya está completo

Agregué las 5 imágenes que enviaste: logo oficial, técnico revisando una
nevera French Door, técnico junto a su vehículo de servicio, el producto
en estudio, y la foto de "Un hogar, mil historias felices" con el
técnico y los clientes. El verde lima real de Haceb (`#ABC500`) se tomó
directamente de esa última imagen.

**Con esto, las 6 marcas están 100% completas: autorizadas y con fotos
reales.**

## Pendiente de tu parte

1. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).
2. Si el salto de scroll persiste, avísame en qué estás viendo el sitio
   exactamente (¿el link de vista previa, o el zip abierto en tu
   navegador?) para poder aislar la causa con precisión.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
