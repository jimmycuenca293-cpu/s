# TecniGuía personal: cómo subirla a tu Hostinger

Esta es **tu** TecniGuía, solo para ti, con todo lo de la versión de Claude: foto de la etiqueta, video y sonido con espectrograma, visita guiada con doble verificación, foto del multímetro, revisión de tarjetas, calculadoras, voz, cronómetro, memoria de casos, garantías y cuentas del mes.

Solo existe una cuenta, la tuya. Después de crearla nadie más se puede registrar.

Toma unos 30 minutos la primera vez.

---

## 1. Tu clave de la IA (Claude)

1. Entra a **https://console.anthropic.com** y crea una cuenta.
2. **Billing**: carga saldo (prepago; empieza con poco, por ejemplo US$ 10–20).
3. **Limits**: pon un límite de gasto mensual.
4. **API Keys → Create Key**, ponle "TecniGuía" y **copia la clave** (empieza por `sk-ant-`). Solo se muestra una vez.

> Cada diagnóstico gasta de ese saldo. Con "Precisión máxima" cuesta más; desmárcala cuando no la necesites.

---

## 2. Dónde va la app

Recomendado: un **subdominio** como `tecniguia.tudominio.com`, para no tocar tu página web.

hPanel → **Dominios → Subdominios** → crea `tecniguia`. Hostinger le da una carpeta (ej. `public_html/tecniguia`).

---

## 3. Base de datos

1. hPanel → **Bases de datos → Administración** → crea una base (nombre, usuario y contraseña). **Anota los tres datos completos** tal como los muestra Hostinger (ej. `u123456789_tecniguia`).
2. Toca **phpMyAdmin → Entrar** → pestaña **Importar** → escoge `schema.sql` (viene en el zip) → **Importar**.

---

## 4. Subir los archivos

1. hPanel → **Administrador de archivos** → entra a la carpeta del subdominio.
2. Sube `tecniguia-personal.zip` → clic derecho → **Extraer**.
3. Deben quedar en esa carpeta: `index.html`, `.htaccess`, `terminos.html` y la carpeta `api/`.

---

## 5. Tus datos (config.php)

1. Entra a `api/`.
2. Copia `config.sample.php` con el nombre `config.php`.
3. Edita `config.php` y cambia:
   - `DB_DSN`: solo la parte `dbname=...` con el nombre de tu base.
   - `DB_USER` y `DB_PASS`: usuario y contraseña de la base.
   - `ANTHROPIC_API_KEY`: la clave del paso 1.
4. Guarda.

---

## 6. PHP

hPanel → **Avanzado → Configuración de PHP**:

- Versión **8.2 o 8.3**.
- `max_execution_time` → **300**
- `memory_limit` → **256M**
- `post_max_size` y `upload_max_filesize` → **64M**

---

## 7. SSL

hPanel → **Seguridad → SSL** → instala el SSL gratis del subdominio.

---

## 8. Crear tu cuenta

1. Abre `https://tecniguia.tudominio.com`.
2. Te aparece **Crear mi cuenta**: pon tu nombre, tu correo y una contraseña.
3. Listo. Desde ese momento la pantalla solo deja **Entrar**, y solo con tu correo.
4. En el celular: abre el enlace y agrégalo a la pantalla de inicio (Chrome: menú ⋮ → "Agregar a pantalla principal").

---

## Problemas comunes

| Lo que pasa | Solución |
|---|---|
| "Falta api/config.php" | No creaste `config.php` (paso 5). |
| Error al crear la cuenta | Revisa los datos de la base en `config.php` y que importaste `schema.sql`. |
| "El servicio de IA no está configurado" | La clave de Anthropic está mal copiada. |
| "El servicio de IA no respondió" | Revisa tu saldo en console.anthropic.com. |
| El diagnóstico se corta | Sube `max_execution_time` a 300 (paso 6). |
| Olvidaste la contraseña | En phpMyAdmin borra tu fila de la tabla `usuarios` (tus visitas se borran con ella) y vuelve a crear la cuenta. Descarga antes un respaldo desde Historial. |
