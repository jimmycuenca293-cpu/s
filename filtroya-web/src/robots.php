<?php require __DIR__ . '/api/sitio.php'; header('Content-Type: text/plain; charset=utf-8'); ?>
User-agent: *
Allow: /
Disallow: /admin.php
Disallow: /api/
Disallow: /gracias.php
Disallow: /opinion.php

Sitemap: <?= sitio()['base'] ?>/sitemap.xml
