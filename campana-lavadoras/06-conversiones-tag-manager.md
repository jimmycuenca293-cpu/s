# Conversiones con Google Tag Manager (GTM-5SCP73SQ)

La tienda manda el evento **`whatsapp`** al `dataLayer` cada vez que alguien toca un botón o enlace de WhatsApp. Incluye:
- `ubicacion`: `boton_flotante` o `enlace`
- `boton`: texto del botón
- `pagina`: ruta donde estaba
- `marca`: Samsung o LG

## Pasos
1. Google Ads → Objetivos → Conversiones → Nueva → Sitio web → categoría **Cliente potencial** (o «Enviar formulario de cliente potencial»). Anota el ID y la etiqueta.
2. En Tag Manager crea el activador **Evento personalizado** con el nombre `whatsapp`.
3. Crea la etiqueta **Seguimiento de conversiones de Google Ads** con ese ID y etiqueta, y asóciala al activador.
4. Agrega la etiqueta **Vinculador de conversiones** en todas las páginas.
5. Vista previa de GTM: toca un botón de WhatsApp en la tienda y confirma que aparece `whatsapp` y que la etiqueta se dispara.
6. Vincula Search Console y Google Analytics 4 con la cuenta de Ads.

Nota: esto mide los toques al botón, no las ventas cerradas. Cuando cierres una venta, anótala y compara con las conversiones de Ads para saber cuánto cuesta cada venta.
