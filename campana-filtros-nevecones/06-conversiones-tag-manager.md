# Conversiones con Google Tag Manager (GTM-5WSNHV66)

La tienda ya envía estos eventos al `dataLayer`:
| Evento | Cuándo | Úsalo como |
|---|---|---|
| `purchase` (página de gracias, con valor e ID de transacción) | Pago aprobado en Wompi | **Conversión principal: Compra** |
| `whatsapp` | Clic en botón de WhatsApp | Conversión secundaria |
| `pago_wompi` | Clic para ir a pagar | Secundaria (no cuenta como compra) |

## Pasos
1. Google Ads → Objetivos → Conversiones → Nueva → Sitio web → **Compra**. Valor: usar el del evento. Anota el *ID* y la *etiqueta*.
2. En GTM crea la etiqueta **Seguimiento de conversiones de Google Ads** con ese ID/etiqueta, activador: evento personalizado `purchase`. Variables: valor de la transacción e ID de transacción (variables de capa de datos).
3. Agrega la etiqueta **Vinculador de conversiones** en todas las páginas.
4. Crea una segunda conversión para `whatsapp` marcada como "secundaria".
5. Vista previa en GTM, haz una compra de prueba y confirma el estado "Registrando conversiones".
6. Vincula Search Console y Google Analytics 4 con la cuenta de Ads.
