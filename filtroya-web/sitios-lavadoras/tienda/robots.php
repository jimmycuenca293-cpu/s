<?php require __DIR__ . '/api/sitio.php'; header('Content-Type: text/plain; charset=utf-8'); ?>
# Asistentes de IA y buscadores: bienvenidos (así pueden leer y recomendar la tienda)
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: Bingbot
User-agent: *
Allow: /
Disallow: /admin.php
Disallow: /api/
Disallow: /gracias.php
Disallow: /opinion.php
Disallow: /carrito.php

Sitemap: <?= sitio()['base'] ?>/sitemap.xml
