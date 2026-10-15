<?php
// Copia este archivo como config.php y llena tus datos. config.php nunca se muestra en la web.
return [
    // Tu dominio, con https (se usa en los correos automáticos)
    'dominio' => 'https://filtrosdeaguanevecon.com',

    // Datos del negocio (salen en la tienda, en los correos y en los términos)
    'negocio' => [
        'nombre'    => 'PuroFiltro',
        'titular'   => 'Nombre del titular',            // persona o empresa dueña del negocio
        'documento' => 'C.C. o NIT 000.000.000-0',
        'direccion' => 'Dirección del negocio',     // opcional: si la dejas así no sale en la tienda
        'telefono'  => '321 799 6144',                   // sale en la tienda, en los términos y en los correos
        'correo'    => 'pedidos@filtrosdeaguanevecon.com',          // correo de atención al cliente
        'horario'   => 'lunes a sábado, de 8:00 a. m. a 6:00 p. m.',
    ],

    // A este correo te llega cada pedido PAGADO, con todos los datos para despacharlo
    'correo_avisos'    => 'tucorreo@gmail.com',
    // Correo desde el que salen los mensajes. Créalo en Hostinger (Correos) con tu dominio.
    'correo_remitente' => 'pedidos@filtrosdeaguanevecon.com',

    // Clave para entrar a tudominio.com/admin.php y ver los pedidos. Pon una larga.
    'admin_clave' => '',

    // Wompi: panel de Wompi > Desarrolladores. Con llaves de prueba (pub_test_) no se cobra de verdad.
    'wompi' => [
        'public_key' => 'pub_test_XXXXXXXXXXXXXXXX',
        'integridad' => 'test_integrity_XXXXXXXXXXXXXXXX',  // "Secreto de integridad"
        'eventos'    => 'test_events_XXXXXXXXXXXXXXXX',     // "Secreto de eventos"
    ],

    // Quién está detrás de la tienda (sale en "Quiénes somos" y como autor de las guías: Google confía más en expertos)
    'tecnico' => [
        'nombre'       => 'Tu nombre',
        'anos'         => '',            // años de experiencia, ej. '12'
        'especialidad' => 'neveras, nevecones, lavadoras y secadoras',
        'historia'     => '',            // un párrafo contando cómo empezaste (opcional)
    ],

    // Tus redes y perfiles (Facebook, Instagram, TikTok, Perfil de Google, Mercado Libre...). Ayuda a Google y a las IA a reconocer la tienda.
    'redes' => [
        // 'https://www.facebook.com/tutienda',
        // 'https://www.instagram.com/tutienda',
    ],

    // Google: código de verificación de Search Console (solo lo que va en content="...") y Google Analytics 4 (G-XXXXXXX)
    'google_verificacion' => 'HN_wbFxOz4Yeyfr0Oao1VfSO6mPB_I4k_uMqoVR5jZo',
    'ga4' => '',
    // Google Tag Manager: carga Analytics y Google Ads. Eventos que manda la tienda: "whatsapp" (clic en WhatsApp) y "pago_wompi" (va a pagar)
    'gtm' => 'GTM-N39G66VJ',
    // WhatsApp de atención (botón flotante en toda la tienda), 10 dígitos
    'whatsapp' => '3217996144',

    // Clave para la tarea programada que manda los recordatorios de cambio de filtro
    'cron_clave' => '',
];
