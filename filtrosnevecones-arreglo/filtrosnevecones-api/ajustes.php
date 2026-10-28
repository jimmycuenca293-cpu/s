<?php
// Ajustes de la tienda. Lo que escribas aquí manda sobre config.php. Este archivo no se ve desde internet.
return [
    'whatsapp' => '3013810242',
    'negocio'  => ['telefono' => '301 381 0242'],

    // Correo(s) donde te llegan los datos de cada pedido. Puedes poner varios separados por coma: 'uno@gmail.com, otro@gmail.com'
    'correo_avisos' => 'jimmycuenca293@gmail.com, serviciotecnicoyrepuestoscali@gmail.com',

    // Formulario de cada pedido (FormSubmit): llega a 'correo_avisos' en cuanto el cliente le da a pagar. La primera vez FormSubmit manda un correo con «Activate Form».
    'formulario' => ['activo' => true, 'proveedor' => 'formsubmit'],

    // Hoja de pedidos en Google (opcional, la más segura): pega aquí la URL que te da Apps Script y la misma clave que pusiste en el script.
    // Pasos en el archivo hoja-de-pedidos-google.txt
    'hoja' => ['url' => '', 'clave' => ''],

    // Llaves de Wompi (panel de Wompi > Desarrolladores): con ellas el carrito cobra VARIOS productos juntos, confirma los pagos solo y te manda el correo de «pedido pagado».
    // Sin ellas, cada producto se paga con su link de pago, de uno en uno. Llena las tres cosas con las llaves de PRODUCCIÓN (pub_prod_...).
    'wompi' => ['public_key' => '', 'integridad' => '', 'eventos' => ''],

    // Correo que SALE de la tienda (el buzón que creaste en Hostinger > Correos).
    // Pon aquí la clave de ESE buzón (la que usas para entrar a su webmail), entre las comillas de 'clave'. Es lo único que falta.
    'smtp' => [
        'host'    => 'smtp.hostinger.com',
        'puerto'  => 465,
        'usuario' => 'pedidos@filtrosaguanevecones.com',
        'clave'   => '',
    ],
];
