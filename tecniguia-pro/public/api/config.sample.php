<?php
// ============================================================
//  TecniGuía Pro — configuración
//  1. Copia este archivo como  config.php  (en la misma carpeta).
//  2. Llena los datos de tu base de datos de Hostinger y tu clave de Anthropic.
//  Nunca compartas config.php: tiene tus claves.
// ============================================================

// --- Base de datos (hPanel → Bases de datos → MySQL) ---
define('DB_DSN',  'mysql:host=localhost;dbname=u123456789_tecniguia;charset=utf8mb4');
define('DB_USER', 'u123456789_tecniguia');
define('DB_PASS', 'TU_CONTRASEÑA_DE_LA_BASE_DE_DATOS');

// --- Inteligencia artificial (console.anthropic.com → API Keys) ---
define('ANTHROPIC_API_KEY', 'sk-ant-...');

// Modelo para cada nivel. 'complex' = precisión máxima, 'default' = normal, 'quick' = rápido.
define('MODELOS', [
    'complex' => 'claude-opus-5-5',
    'default' => 'claude-opus-5-5',
    'quick'   => 'claude-opus-5-5',
]);
// Esfuerzo de razonamiento para cada nivel: low, medium, high, xhigh, max.
define('ESFUERZO', [
    'complex' => 'high',
    'default' => 'medium',
    'quick'   => 'low',
]);
// Precio del modelo en dólares por millón de tokens (para estimar tus costos en el panel).
define('PRECIO_ENTRADA_USD', 4.00);
define('PRECIO_SALIDA_USD', 20.00);

// --- Tu negocio ---
define('NOMBRE_APP', 'TecniGuía');
define('WHATSAPP_SOPORTE', '+57 300 000 0000');      // a donde te escriben para pagar o pedir ayuda
define('ADMIN_EMAILS', ['tucorreo@gmail.com']);      // estos correos ven el panel de administración
define('DIAS_PRUEBA', 7);                            // días gratis al registrarse
define('LIMITE_DIARIO', 80);                         // consultas de IA por técnico por día

// --- Avanzado (normalmente no se toca) ---
define('ANTHROPIC_BASE_URL', null);                  // null = servidor oficial de Anthropic
define('MAX_BODY', 40 * 1024 * 1024);                // tamaño máximo de una petición (fotos incluidas)
