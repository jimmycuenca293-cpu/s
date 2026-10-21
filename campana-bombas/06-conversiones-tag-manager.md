# Conversiones con Google Tag Manager (GTM-5SCP73SQ)

La tienda de bombas está en el mismo dominio y usa el mismo contenedor que la de filtros. Manda el evento **`whatsapp`** al `dataLayer` cada vez que alguien toca un botón o enlace de WhatsApp. Incluye:
- `ubicacion`: `boton_flotante` o `enlace`
- `boton`: texto del botón
- `pagina`: ruta donde estaba (las bombas empiezan por `/bombas-de-agua/`)
- `marca`: Samsung o LG

## Si ya tienes la conversión de la campaña de filtros
No hay que crear nada nuevo: el activador `whatsapp` y la etiqueta de conversión de Google Ads ya funcionan para las bombas. Solo verifica en la vista previa de GTM que, al tocar un botón en una página de `/bombas-de-agua/`, aparece el evento `whatsapp` y la etiqueta se dispara.

## Si todavía no la tienes
1. Google Ads → Objetivos → Conversiones → Nueva → Sitio web → categoría **Cliente potencial**. Anota el ID y la etiqueta.
2. En Tag Manager crea el activador **Evento personalizado** con el nombre `whatsapp`.
3. Crea la etiqueta **Seguimiento de conversiones de Google Ads** con ese ID y etiqueta, y asóciala al activador.
4. Agrega la etiqueta **Vinculador de conversiones** en todas las páginas.
5. Vista previa de GTM: toca un botón de WhatsApp en la tienda y confirma que aparece `whatsapp` y que la etiqueta se dispara.
6. Vincula Search Console y Google Analytics 4 con la cuenta de Ads.

## Separar bombas de filtros en los informes
Como las dos tiendas comparten la conversión, en Google Ads las verás sumadas. Para separarlas, usa los informes por campaña (cada una tiene la suya) o crea en Tag Manager una variable con `pagina` que contenga `/bombas-de-agua/`.

Nota: esto mide los toques al botón, no las ventas cerradas. Cuando cierres una venta, anótala y compara con las conversiones de Ads para saber cuánto cuesta cada venta.
