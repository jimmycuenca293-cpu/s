# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Séptima iteración: **encontré y corregí la causa real** del salto al pie de
página, agregué Mabe, y sumé fotos a las páginas de marca que antes eran
solo texto.

## El bug del salto al pie de página — causa real encontrada

Reportaste, con razón, que el problema seguía pasando en **todos** los
enlaces internos. Investigué más a fondo y encontré la causa real: **las 98
páginas del sitio compartían el mismo `id="contacto"`** en su sección final
(justo antes del pie de página). Cada página tenía su propia sección con
ese identificador repetido.

Si en algún momento el navegador (o la vista previa) queda con `#contacto`
en la URL —por ejemplo, después de tocar el botón "Contacto" del menú— y
luego se navega a *cualquier otra página* del sitio sin borrar ese
fragmento, el navegador busca un elemento con `id="contacto"` en la nueva
página... y lo encuentra, porque **todas las páginas tenían uno**, siempre
la sección justo antes del footer. Por eso parecía que "todo enviaba al pie
de página": técnicamente no era un enlace roto, era un identificador
duplicado en el sitio entero que un fragmento de URL "pegado" podía
enganchar en cualquier página.

**La solución**: le di a cada una de las 98 páginas un `id` único para su
sección de contacto (`contacto-inicio`, `contacto-samsung`,
`contacto-lg-fallas`, `contacto-mabe-manga`, etc.). Ahora, aunque un
fragmento de URL quede pegado de una navegación anterior, no puede
coincidir con ninguna sección de una página distinta a la que pertenece.

Lo probé de forma automatizada reproduciendo exactamente tu escenario: clic
en "Contacto" (salta a la sección de contacto del inicio) → clic en la
tarjeta de Mabe → clic en la pestaña "Fallas Comunes". Las tres
navegaciones quedan arriba del todo (`scrollY: 0`), sin excepción.

## Qué más se agregó en esta iteración

1. **Mabe completo**: logo, fotos del técnico y galería, con el azul oficial
   de Mabe (`#2597BE`) tomado de tu logo.
2. **Fotos en las páginas de marca que antes eran solo texto**: las páginas
   de Fallas Comunes, Mantenimiento, Instalación y Repuestos de cada marca
   ahora tienen una foto real junto al texto del encabezado (antes eran
   una sola columna de texto sin imagen). Se aplicó a las 6 marcas × 4
   páginas = 24 páginas.

## Estado de las imágenes por marca

Samsung, LG, Whirlpool y Mabe completos. Electrolux y Haceb pendientes —
ver `IMAGENES-LEEME.md`.

## Pendiente de tu parte

1. Enviar las imágenes de Electrolux y Haceb, y decirme si cada una es
   autorizada oficialmente por el fabricante.
2. Confirmar si LG, Whirlpool o Mabe te autorizaron oficialmente (para
   agregar la etiqueta "Autorizado" como en Samsung).
3. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
