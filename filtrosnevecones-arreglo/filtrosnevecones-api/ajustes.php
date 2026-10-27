<?php
// Ajustes de la tienda. Lo que escribas aquí manda sobre config.php. Este archivo no se ve desde internet.
return [
    'whatsapp' => '3013810242',
    'negocio'  => ['telefono' => '301 381 0242'],

    // Correo donde te llegan los datos de cada pedido
    'correo_avisos' => 'serviciotecnicoyrepuestoscali@gmail.com',

    // Correo que SALE de la tienda (el buzón que creaste en Hostinger > Correos).
    // Pon aquí la clave de ESE buzón (la que usas para entrar a su webmail), entre las comillas de 'clave'. Es lo único que falta.
    'smtp' => [
        'host'    => 'smtp.hostinger.com',
        'puerto'  => 465,
        'usuario' => 'pedidos@filtrosaguanevecones.com',
        'clave'   => '',
    ],
];
