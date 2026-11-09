# Medir los toques al botón de WhatsApp

El sitio manda el evento **`whatsapp`** al `dataLayer` cada vez que alguien toca un botón o enlace de WhatsApp (con la página y el texto del botón). Para que Google Ads lo cuente como conversión:

1. En **Google Tag Manager** crea un contenedor para el sitio. Anota el ID (GTM-XXXXXXX).
2. Pídeme que regenere el sitio con ese ID (`GTM_ID=GTM-XXXXXXX python3 gen.py site`) o agrega el fragmento de GTM en el encabezado de todas las páginas.
3. En GTM crea el activador **Evento personalizado** con el nombre `whatsapp`.
4. En Google Ads → Objetivos → Conversiones → Nueva → Sitio web → categoría **Cliente potencial**. Anota el ID y la etiqueta.
5. En GTM crea la etiqueta **Seguimiento de conversiones de Google Ads** con ese ID y etiqueta, asociada al activador `whatsapp`, y la etiqueta **Vinculador de conversiones** en todas las páginas.
6. Vista previa de GTM: toca un botón de WhatsApp en el sitio y confirma que aparece `whatsapp` y que la etiqueta se dispara.
7. Vincula Search Console y Google Analytics 4 con la cuenta de Ads.

Nota: esto mide los toques al botón, no las ventas cerradas. Cuando cierres una venta, anótala y compara con las conversiones de Ads para saber cuánto cuesta cada servicio.
