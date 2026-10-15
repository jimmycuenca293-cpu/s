# 6. Conversiones en Google Tag Manager (GTM-N39G66VJ)

La tienda ya manda estos eventos:

| Evento | Cuándo | Datos |
|---|---|---|
| `whatsapp` | El cliente toca el botón de WhatsApp | ubicacion, pagina |
| `pago_wompi` | El cliente toca "Pagar" y va a la página de pago | value (total), currency (COP), transaction_id (pedido) |

1. En Google Ads crea 2 conversiones (Objetivos → Conversiones → Nueva → Sitio web → manual): **Compra (pago_wompi)** como principal y **Contacto WhatsApp** como secundaria. Copia el ID y la etiqueta de cada una.
2. En Tag Manager → **Activadores → Nuevo → Evento personalizado**: uno con nombre `pago_wompi` y otro con `whatsapp`.
3. **Etiquetas → Nueva → Seguimiento de conversiones de Google Ads** para cada una, con su activador. En la de pago_wompi: valor = variable de capa de datos `value`, moneda `COP`, ID de transacción = `transaction_id`.
4. Agrega la etiqueta **Vinculador de conversiones** con el activador "All Pages".
5. Prueba con **Vista previa** de Tag Manager y luego **Enviar → Publicar**.
