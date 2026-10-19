<?php
// Copia este archivo como config.php y llena tus datos. config.php nunca se muestra en la web.
return [
    // Tu dominio, con https (se usa en los correos automáticos)
    'dominio' => 'https://filtrosparalavadoras.click',

    // Datos del negocio (salen en la tienda, en los correos y en los términos)
    'negocio' => [
        'nombre'    => 'Filtros LG',
        'titular'   => 'Nombre del titular',            // persona o empresa dueña del negocio
        'documento' => 'C.C. o NIT 000.000.000-0',
        'direccion' => 'Dirección del negocio',     // opcional: si la dejas así no sale en la tienda
        'telefono'  => '320 510 2995',                   // sale en la tienda, en los términos y en los correos
        'correo'    => 'pedidos@filtrosparalavadoras.click',          // correo de atención al cliente
        'horario'   => 'lunes a sábado, de 8:00 a. m. a 6:00 p. m.',
    ],

    // A este correo te llega cada pedido PAGADO, con todos los datos para despacharlo
    'correo_avisos'    => 'serviciotecnicoyrepuestoscali@gmail.com',
    // Correo desde el que salen los mensajes. Créalo en Hostinger (Correos) con tu dominio.
    'correo_remitente' => 'pedidos@filtrosparalavadoras.click',
    // Envío de correos por SMTP con el buzón que creaste en Hostinger (Correos). Es lo que hace que SÍ te lleguen los datos del cliente.
    // Usuario = el correo completo del buzón (pedidos@filtrosparalavadoras.click) y clave = la del buzón. Host de Hostinger: smtp.hostinger.com, puerto 465.
    'smtp' => [
        'host'    => 'smtp.hostinger.com',
        'puerto'  => 465,
        'usuario' => 'pedidos@filtrosparalavadoras.click',
        'clave'   => '',
    ],

    // Datos del pedido a tu correo «como un formulario» (servicio FormSubmit), además del correo normal. Funciona aunque el correo del hosting falle.
    // La primera vez te llega un correo de FormSubmit para activarlo: toca el botón «Activate Form». Pon 'activo' => false para apagarlo.
    'formulario' => ['activo' => true, 'proveedor' => 'formsubmit'],
    // FormSubmit: la primera vez te llega un correo para activarlo (toca «Activate Form»). Alternativa, Web3Forms con tu clave; cambia la línea de arriba por:
    // 'formulario' => ['activo' => true, 'proveedor' => 'web3forms', 'clave' => '738e4767-832d-4e86-89ca-a94d3979fec0'],

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
    'google_verificacion' => '',
    'ga4' => '',
    // Google Tag Manager: carga Analytics y Google Ads. Eventos que manda la tienda: "whatsapp" (clic en WhatsApp) y "pago_wompi" (va a pagar)
    'gtm' => 'GTM-5SCP73SQ',
    // WhatsApp de atención (botón flotante en toda la tienda), 10 dígitos
    'whatsapp' => '3205102995',

    // Clave para la tarea programada que manda los recordatorios de cambio de filtro
    'cron_clave' => '',
];
