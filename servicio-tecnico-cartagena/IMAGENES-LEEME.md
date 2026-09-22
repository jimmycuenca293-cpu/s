# Cómo reemplazar las imágenes

Todas las imágenes están organizadas **por carpetas**, una por marca, para que
el sitio cargue rápido (sin depender de servidores externos) y sea fácil de
mantener. Ahora mismo cada archivo es un **placeholder** (fondo de color con
texto) que debes reemplazar por fotos reales, manteniendo el mismo nombre y
la misma carpeta.

```
images/
  logo/
    logo.svg          → logo de tu empresa (se usa en el menú y el pie de página)
    favicon.svg        → ícono de la pestaña del navegador
  home/
    hero-servicio-tecnico-cartagena.jpg   → foto principal de portada (técnico trabajando)
    equipo-tecnico-cartagena.jpg          → foto del equipo / técnicos certificados
  samsung/
    hero-samsung-cartagena.jpg            → técnico reparando una nevera Samsung
    equipo-samsung-cartagena.jpg          → primer plano de la reparación / repuestos
    logo-samsung.svg                      → logo de la marca (ya incluido, no es necesario tocarlo)
  lg/            (mismo patrón)
  electrolux/    (mismo patrón)
  whirlpool/     (mismo patrón)
  mabe/          (mismo patrón)
  haceb/         (mismo patrón)
```

## Recomendaciones para las fotos reales

1. **Usa fotos propias**, idealmente del técnico trabajando, del antes/después
   de una reparación, o de la nevera reparada. Esto es mucho más creíble para
   los clientes y para Google que fotos genéricas de internet.
2. **Formato y peso**: usa `.jpg` o, mejor aún, `.webp` (más liviano). Antes
   de subir cada foto, compres primero (herramientas gratuitas: Squoosh.app,
   TinyPNG). Apunta a menos de 200 KB por imagen.
3. **Tamaño recomendado**:
   - Fotos "hero" (portada): 1200×900 px aprox.
   - Fotos "equipo/reparación": 1000×720 px aprox.
4. **Mantén el mismo nombre de archivo** al reemplazar, así no tienes que
   tocar el HTML. Si usas `.webp` en vez de `.jpg`, avísame o busca y
   reemplaza la extensión en los archivos `.html` correspondientes.
5. El texto `alt` de cada imagen ya está optimizado para SEO (describe la
   marca, el servicio y "Cartagena"). Si cambias la foto por una muy distinta
   en contenido, ajusta también el `alt` para que siga describiendo lo que
   se ve.

## Sobre las imágenes del sitio anterior

El sitio original cargaba **todas sus imágenes desde un dominio de terceros**
(`turepuestoslg.click`), un sitio de venta de repuestos que no es tuyo. Esto
es un riesgo importante:

- Si ese sitio cambia o elimina las imágenes, las tuyas se rompen sin previo aviso.
- Depender de un servidor externo añade una conexión extra y **hace más
  lenta** la carga de tu página (peor SEO y peor experiencia de usuario).
- No tenías control sobre el peso ni el formato de esas imágenes.

Por eso esta nueva versión sirve todas las imágenes **desde tu propio
dominio**, en carpetas separadas, para que cargue más rápido y no dependa de
nadie más.
