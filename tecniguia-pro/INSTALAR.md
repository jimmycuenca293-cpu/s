# TecniGuía Pro: cómo instalarla en tu Hostinger

Sigue los pasos en orden. Toma unos 30 minutos la primera vez.

Al final vas a tener:

- **tudominio.com** (o un subdominio): la app donde los técnicos se registran y trabajan.
- **tudominio.com/admin.html**: tu panel para activar, suspender y ver el costo de cada técnico.

---

## 1. Crear tu cuenta de la API de Claude (la inteligencia artificial)

1. Entra a **https://console.anthropic.com** y crea una cuenta con tu correo.
2. Ve a **Billing** (facturación) y carga saldo con tu tarjeta. Es prepago: empieza con poco (por ejemplo US$ 20) mientras pruebas.
3. En **Limits** pon un **límite de gasto mensual** para no llevarte sorpresas.
4. Ve a **API Keys**, toca **Create Key**, ponle de nombre "TecniGuía" y **copia la clave** (empieza por `sk-ant-`). Guárdala; solo se muestra una vez.

> Cada diagnóstico que hagan tus técnicos gasta de este saldo. En el panel ves cuánto gasta cada uno.

---

## 2. Escoger dónde va la app

Recomendado: un **subdominio**, por ejemplo `app.tudominio.com`, para no mezclarla con tu página web actual.

En hPanel: **Dominios → Subdominios → Crear subdominio**. Escribe `app` y crea. Hostinger le asigna una carpeta (por ejemplo `public_html/app`).

---

## 3. Crear la base de datos

1. hPanel → **Bases de datos → Administración**.
2. Crea una base nueva: ponle nombre (ej. `tecniguia`), usuario (ej. `tecniguia`) y una contraseña segura. **Anota los tres datos completos** como los muestra Hostinger (llevan un prefijo, ej. `u123456789_tecniguia`).
3. Al lado de la base creada toca **phpMyAdmin → Entrar**.
4. En phpMyAdmin: pestaña **Importar → Seleccionar archivo →** escoge `schema.sql` (viene en el zip) → **Importar** (abajo).
5. Deben aparecer 4 tablas: `usuarios`, `visitas`, `uso`, `intentos`.

---

## 4. Subir los archivos

1. hPanel → **Archivos → Administrador de archivos**.
2. Entra a la carpeta del subdominio (ej. `public_html/app`). Si no usas subdominio, entra a `public_html`.
3. Sube `tecniguia-pro.zip` y luego clic derecho → **Extraer** ahí mismo.
4. Si los archivos quedaron dentro de una subcarpeta `public`, entra a ella, selecciona todo (incluye los archivos ocultos `.htaccess`) y **muévelo** a la carpeta del subdominio.

Debe quedar así dentro de la carpeta:

```
index.html
admin.html
terminos.html
.htaccess
api/   (auth.php, ia.php, visitas.php, admin.php, lib.php, config.sample.php, vendor/ …)
```

---

## 5. Poner tus datos (config.php)

1. Entra a la carpeta `api/`.
2. Clic derecho en `config.sample.php` → **Copiar** → nómbralo `config.php`.
3. Abre `config.php` (clic derecho → Editar) y cambia:

| Dato | Qué poner |
|---|---|
| `DB_DSN` | Cambia solo `dbname=...` por el nombre completo de tu base (ej. `u123456789_tecniguia`) |
| `DB_USER` | El usuario de la base (ej. `u123456789_tecniguia`) |
| `DB_PASS` | La contraseña de la base |
| `ANTHROPIC_API_KEY` | La clave que copiaste en el paso 1 |
| `WHATSAPP_SOPORTE` | Tu WhatsApp, donde los técnicos te escriben para pagar |
| `ADMIN_EMAILS` | Tu correo. Con ese correo te registras y ves el panel |
| `DIAS_PRUEBA` | Días gratis al registrarse (viene 7) |
| `LIMITE_DIARIO` | Consultas de IA por técnico por día (viene 80) |

4. Guarda.

> Nunca le pases a nadie el archivo `config.php`: tiene tus claves.

---

## 6. Ajustar PHP

hPanel → **Avanzado → Configuración de PHP**:

1. **Versión de PHP**: 8.2 o 8.3.
2. En **Opciones de PHP** cambia:
   - `max_execution_time` → **300** (el diagnóstico con precisión máxima puede tardar 1 a 2 minutos)
   - `memory_limit` → **256M**
   - `post_max_size` → **64M**
   - `upload_max_filesize` → **64M**
3. Guarda.

---

## 7. Activar el candado (SSL)

hPanel → **Seguridad → SSL** → instala el SSL gratis para tu dominio o subdominio. La app obliga a usar `https://`.

---

## 8. Probar

1. Abre `https://app.tudominio.com`.
2. Toca **Crear cuenta** y regístrate **con el correo que pusiste en `ADMIN_EMAILS`**. Arriba debe decir "Administrador".
3. Haz una visita de prueba con la foto de una etiqueta.
4. Abre `https://app.tudominio.com/admin.html`: debes ver tu cuenta y el costo de esa prueba.

---

## Cómo cobrar

1. Un técnico se registra y tiene `DIAS_PRUEBA` días gratis.
2. Cuando la prueba termina, la app le muestra tu WhatsApp para activar.
3. Te paga (Nequi, Daviplata, transferencia…).
4. En el **panel**, buscas su correo, escoges 30 días (o 90, 6 meses, 1 año) y tocas **Activar**. Los días se suman a los que le queden.
5. Si deja de pagar, no hagas nada: al vencer se pausa sola. Para cortar antes, **Suspender**.
6. ¿Olvidó la contraseña? En el panel toca **Clave temporal** y se la mandas por WhatsApp.

## Cuánto cobrar

Mira en el panel el **costo de IA por técnico** después de una o dos semanas de pruebas reales. Tu precio mensual debe cubrir ese costo con buen margen. Si el costo te queda alto, en `config.php` puedes cambiar los modelos (`MODELOS`) por unos más económicos, por ejemplo `claude-sonnet-5-5`; revisa antes que la calidad de los diagnósticos se mantenga.

---

## Problemas comunes

| Lo que pasa | Solución |
|---|---|
| "Falta api/config.php" | No creaste `config.php` (paso 5). |
| No deja crear cuenta / error de servidor | Revisa `DB_DSN`, `DB_USER` y `DB_PASS`, y que importaste `schema.sql`. |
| "El servicio de IA no está configurado" | La clave de Anthropic está mal copiada. |
| "El servicio de IA no respondió" | Revisa que tengas saldo en console.anthropic.com. |
| El diagnóstico se corta a los 30 s o 60 s | Sube `max_execution_time` (paso 6). |
| Error con fotos grandes | Sube `post_max_size` y `upload_max_filesize` (paso 6). |

## Actualizar la app más adelante

Sube los archivos nuevos encima de los viejos **sin borrar `api/config.php`**. Tus técnicos y sus visitas se quedan en la base de datos.
