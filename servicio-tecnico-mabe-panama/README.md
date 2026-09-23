# Servicio Técnico Mabe Panamá — sitio SEO completo

Sitio nuevo, construido desde cero para **Servicio Técnico Mabe Panamá**
(Ciudad de Panamá), reutilizando la misma arquitectura probada del sitio de
Cartagena (secciones SEO, JSON-LD, blog, zonas, validaciones), pero con
contenido 100% propio para esta marca y ciudad.

- **Dominio**: https://serviciotecnicomabepanama.click/
- **WhatsApp / teléfono**: +507 6933-7976
- **71 páginas** generadas y validadas (0 errores de HTML, 0 errores de
  JSON-LD, 0 enlaces/imágenes rotas, 0 texto duplicado, 0 regresiones del
  bug de scroll).

## Qué incluye

- **4 tipos de electrodomésticos**, cada uno con su propia página principal
  + 5 subpáginas + 8 páginas de zona:
  - Neveras y Refrigeradoras
  - Lavadoras
  - Secadoras
  - Centros de Lavado
  - Subpáginas por tipo: Resumen (index), Fallas Comunes, Mantenimiento
    Preventivo, Instalación, Repuestos Originales, Preguntas Frecuentes.
- **8 zonas reales de Ciudad de Panamá**: San Francisco, Bella Vista, El
  Cangrejo, Costa del Este, Punta Pacífica, Obarrio, Marbella, San
  Miguelito — cada una con página propia y también cruzada con cada tipo de
  electrodoméstico (8 zonas × 4 tipos = 32 páginas de zona).
- **3 páginas de servicio genéricas**: mantenimiento preventivo,
  instalación, reparación de motores/compresores.
- **Blog**, página general de preguntas frecuentes, y página pilar de
  fallas comunes.
- **Botón de WhatsApp** en todas las páginas, con mensajes predefinidos
  según la página (número +507 6933-7976).
- **JSON-LD**: `LocalBusiness`, `Service`, `FAQPage`, `BreadcrumbList`, y
  `speakable` para respuestas de asistentes de voz / IA.
- Mismo blindaje contra el bug de "salto al footer" que en el sitio de
  Cartagena.

## Estado de las imágenes

- **Neveras y Refrigeradoras**: fotos reales del equipo (reutilizadas de
  las fotos de Mabe que ya nos diste para Cartagena, ya que es la misma
  marca/producto): logo, hero, equipo, y galería de 7 fotos.
- **Lavadoras, Secadoras, Centros de Lavado**: por ahora tienen el logo de
  Mabe real, pero las fotos de hero/equipo/galería son marcadores de
  posición (placeholders) generados automáticamente, a la espera de las
  fotos que dijiste que ibas a enviar.

Cuando envíes las fotos de lavadoras, secadoras y centros de lavado (o
fotos distintas para neveras específicas de Panamá), las agrego de
inmediato y regenero el sitio.

## Pendiente de tu parte

1. Enviar las fotos de lavadoras, secadoras y centros de lavado (y decirme
   si las fotos de neveras que ya usé están bien o prefieres otras).
2. Confirmar el correo de contacto (por ahora uso
   `contacto@serviciotecnicomabepanama.click`).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
