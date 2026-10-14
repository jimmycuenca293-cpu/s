<?php
// ============================================================
//  TecniGuía — configuración de la versión PERSONAL (solo tú)
//  1. Copia este archivo como  config.php  (en la misma carpeta api/).
//  2. Llena los datos de tu base de datos de Hostinger y tu clave de Anthropic.
//  Nunca compartas config.php: tiene tus claves.
// ============================================================

// Una sola cuenta: la primera que se crea. Después se cierra el registro.
define('MODO_PERSONAL', true);

// --- Base de datos (hPanel → Bases de datos → MySQL) ---
define('DB_DSN',  'mysql:host=localhost;dbname=u123456789_tecniguia;charset=utf8mb4');
define('DB_USER', 'u123456789_tecniguia');
define('DB_PASS', 'TU_CONTRASEÑA_DE_LA_BASE_DE_DATOS');

// --- Inteligencia artificial (console.anthropic.com → API Keys) ---
define('ANTHROPIC_API_KEY', 'sk-ant-...');

// Modelo y esfuerzo para cada nivel: 'complex' = precisión máxima, 'default' = normal, 'quick' = rápido.
define('MODELOS', [
    'complex' => 'claude-opus-5-5',
    'default' => 'claude-opus-5-5',
    'quick'   => 'claude-opus-5-5',
]);
define('ESFUERZO', [
    'complex' => 'high',
    'default' => 'medium',
    'quick'   => 'low',
]);

// --- Datos que la versión personal no usa (déjalos así) ---
define('NOMBRE_APP', 'TecniGuía');
define('WHATSAPP_SOPORTE', '');
define('ADMIN_EMAILS', []);
define('DIAS_PRUEBA', 0);
define('LIMITE_DIARIO', 0);
define('PRECIO_ENTRADA_USD', 4.00);
define('PRECIO_SALIDA_USD', 20.00);
define('ANTHROPIC_BASE_URL', null);
define('MAX_BODY', 40 * 1024 * 1024);
