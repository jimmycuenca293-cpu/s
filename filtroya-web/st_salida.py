# Archivos de salida: buscador y banner, formulario de solicitud, API, mapa del sitio, sitemaps, robots, llms y datos (se ejecuta al final de st_paginas.py).
mapa = lambda t, its: f'<h2 style="font-size:22px;margin:22px 0 10px">{esc(t)}</h2><ul class="spec-list">' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in its) + "</ul>"
cuerpo = (mapa("Países", [(f"Servicio técnico Samsung en {P['nombre']}", R_PAIS(pk)) for pk, P in PAISES.items()]) + mapa("Ciudades", [(f"Servicio técnico Samsung en {c['n']}", R_CIU(c)) for c in CIU])
          + mapa("Zonas", [(f"Servicio técnico Samsung en {z}, {c['n']}", R_Z(c, z)) for c, z in ZONAS_P]) + mapa("Mantenimiento por ciudad", [(f"Mantenimiento en {c['n']}", R_MANT(c)) for c in CIU]) + mapa("Voltaje por país", [(f"Voltaje en {P['nombre']}", R_VOLT(pk)) for pk, P in PAISES.items()])
          + mapa("Servicios por país", [(f"Servicio técnico de {pal(k, s)[1]} Samsung en {P['nombre']}", R_SERV(k, s)) for k, P in PAISES.items() for s in SERV_PAIS[k]]) + mapa("Guías de fallas", [(g["tit"], R_G(g)) for g in GUIAS]) + mapa("Cómo leer el modelo y códigos de error", [(t, f"{sl}.html") for sl, t in GUIAS_MOD] + [("Códigos de error de lavadoras Samsung", "codigos-de-error-lavadora-samsung.html")])
          + mapa("Por departamento", [(f"Servicio técnico Samsung en {d} ({PAISES[k]['nombre']})", R_DEP(k, d)) for k, d in DEP_HUBS]) + mapa("Preguntas y respuestas por país", [(f"Preguntas frecuentes en {P['nombre']}", f"preguntas-frecuentes-servicio-samsung-{pk}.html") for pk, P in PAISES.items()] + [(f"Respuestas rápidas en {P['nombre']}", f"respuestas-ia-servicio-tecnico-samsung-{pk}.html") for pk, P in PAISES.items()])
          + mapa("Ayuda", [("Solicitar visita", "solicitar-visita.html"), ("Cobertura", "cobertura-servicio-tecnico-samsung.html"), ("Preguntas frecuentes", "preguntas-frecuentes-servicio-tecnico-samsung.html"), ("Respuestas rápidas", "respuestas-para-ia-servicio-tecnico-samsung.html"), ("Quiénes somos", "quienes-somos.html"), ("Contacto", "contacto.html")]))
pagina("mapa-del-sitio.html", "Mapa del sitio | Servicio técnico Samsung", "Todas las páginas del sitio: países, ciudades, servicios y guías de fallas.", "mapa del sitio servicio tecnico samsung", [("Inicio", "index.html"), ("Mapa del sitio", None)],
       hero_simple("Mapa del sitio", "Todas las páginas", "Países, ciudades, servicios y guías.") + qa("¿Qué hay en este sitio?", "Servicio técnico Samsung por país y ciudad, páginas por equipo, guías de fallas y respuestas rápidas.") + seccion("Páginas", cuerpo), [], [], prio="0.4", tipo="guias")

# buscador + banner de ciudades
items = [[P["nombre"], R_PAIS(pk), "País", f"{len(CIU_PAIS[pk])} ciudades", ""] for pk, P in PAISES.items()] + [[c["n"], R_CIU(c), "Ciudad", c["pais"], c["pk"]] for c in CIU]
items += [[cap(pal(k, s)[1]), R_SERV(k, s), "Servicio", PAISES[k]["nombre"], k] for k in PAISES for s in SERV_PAIS[k]] + [[g["tit"], R_G(g), "Guía de fallas", "", ""] for g in GUIAS]
items += [[f"{cap(pal(c['pk'], sv)[1])} en {c['n']}", R_CS(c, sv), "Reparación", c["pais"], c["pk"]] for c in CIU for sv in SERV_PAIS[c["pk"]]]
items += [[f"{z} · {c['n']}", R_Z(c, z), "Zona", c["pais"], c["pk"]] for c, z in ZONAS_P]
js = ("(function(){var D=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";"
      "function n(s){return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').trim()}var X=D.map(function(r){return n(r[0]+' '+r[2]+' '+r[3])});"
      "function buscar(q,P){q=n(q);if(!q)return[];var t=q.split(/ +/),o=[];for(var i=0;i<D.length;i++){if(P&&D[i][4]&&D[i][4]!==P)continue;var ok=true,sc=0;for(var j=0;j<t.length;j++){var p=X[i].indexOf(t[j]);if(p<0){ok=false;break}sc+=p===0?0:1}if(ok){var e=n(D[i][0]);o.push([sc+(e.indexOf(q)===0?-2:0)+(D[i][2]==='Ciudad'||D[i][2]==='País'?0:.5),i])}}o.sort(function(a,b){return a[0]-b[0]});return o.slice(0,14).map(function(x){return D[x[1]]})}"
      "function pintar(caja,r,q){if(!q.trim()){caja.hidden=true;return}var g={},h='';r.forEach(function(x){(g[x[2]]=g[x[2]]||[]).push(x)});Object.keys(g).forEach(function(k){h+='<h6>'+k+'</h6>'+g[k].map(function(x){return '<a href=\"'+x[1]+'\"><span>'+x[0]+'</span><small>'+x[3]+'</small></a>'}).join('')});caja.innerHTML=h||'<p>No encontramos «'+q.replace(/</g,'')+'». Prueba con tu ciudad, tu país o el equipo.</p>';caja.hidden=false}"
      "document.querySelectorAll('[data-aq-q]').forEach(function(i){var c=i.parentNode.querySelector('.aq-res');var P=i.getAttribute('data-aq-pais')||'';i.addEventListener('input',function(){pintar(c,buscar(i.value,P),i.value)});i.addEventListener('focus',function(){if(i.value)pintar(c,buscar(i.value,P),i.value)});i.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=c.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape')c.hidden=true})});"
      "(function(){var t=document.querySelector('[data-tk]');if(!t)return;var K=t.getAttribute('data-tk');var c=D.filter(function(r){return K==='paises'?r[2]==='País':(r[2]==='Ciudad'&&r[4]===K)}).map(function(r){return r[0]});if(!c.length)return;var h=c.map(function(n){return '<span>'+n+'</span>'}).join('');t.innerHTML=h+h;t.style.setProperty('--d',Math.max(25,Math.round(c.length*3))+'s')})();"
      "document.addEventListener('click',function(e){document.querySelectorAll('.aq-res').forEach(function(c){if(!c.parentNode.contains(e.target))c.hidden=true});document.querySelectorAll('.aq-nav details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});})();")
(OUT / "buscar.js").write_text(js, encoding="utf-8")

(OUT / "solicitar.js").write_text("""(function(){var f=document.getElementById('sv-form');if(!f)return;var P=document.getElementById('sv-pais'),C=document.getElementById('sv-ciudad'),R=document.getElementById('sv-res');
function ciu(){C.innerHTML=(window.SV_CIU[P.value]||[]).map(function(c){return '<option>'+c+'</option>'}).join('')}P.addEventListener('change',ciu);ciu();
function FY(f){if(Array.isArray(f)){f.forEach(FY);return}if(!f||!f.url||!f.datos)return;try{fetch(f.url,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(f.datos),keepalive:true}).catch(function(){})}catch(e){}}
f.addEventListener('submit',function(e){e.preventDefault();var d={};new FormData(f).forEach(function(v,k){d[k]=v});if(!d.nombre||!d.tel||String(d.tel).replace(/\\D/g,'').length<7){R.innerHTML='<p style="color:#b91c1c">Escribe tu nombre y un celular válido.</p>';return}
R.textContent='Enviando…';fetch('/api/solicitud.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json()}).then(function(j){if(!j.ok)throw new Error(j.mensaje||'Error');FY(j.form);
var m=encodeURIComponent('Hola, acabo de solicitar una visita ('+j.ref+') para mi '+d.equipo+' Samsung en '+d.ciudad);R.innerHTML='<div class="st-ok"><b>¡Solicitud recibida!</b><br>Tu referencia es '+j.ref+'. Te contactaremos pronto. Si es urgente, escríbenos por WhatsApp.<br><a class="st-btn wa" style="margin-top:10px" target="_blank" rel="noopener" href="https://wa.me/'+(window.SV_WA||'')+'?text='+m+'">Escribir por WhatsApp</a></div>';f.reset();ciu()}).catch(function(){R.innerHTML='<p style="color:#b91c1c">No pudimos enviar el formulario. Escríbenos por WhatsApp y te atendemos.</p>'})})})();
""".replace("window.SV_WA||''", f"'{WA_DEF}'"), encoding="utf-8")

# API: solicitud de visita (correo por SMTP a todos los destinatarios + formulario desde el navegador)
api = OUT / "api"; api.mkdir(exist_ok=True); (OUT / "data").mkdir(exist_ok=True)
shutil.copy(AQUI / "src" / "api" / "lib.php", api / "lib.php")
(api / ".htaccess").write_text('<FilesMatch ".*">\n  Require all denied\n</FilesMatch>\n<FilesMatch "^solicitud\\.php$">\n  Require all granted\n</FilesMatch>\nOptions -Indexes\n', encoding="utf-8")
(OUT / "data" / ".htaccess").write_text("Require all denied\n", encoding="utf-8")
(api / "solicitud.php").write_text(r"""<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); echo '{"ok":false}'; exit; }
$j = json_decode((string) file_get_contents('php://input'), true);
if (!is_array($j)) { http_response_code(400); echo '{"ok":false,"mensaje":"Datos inválidos"}'; exit; }
if (!empty($j['web'])) { echo '{"ok":true,"ref":"OK","form":[]}'; exit; }
$lim = fn(string $k, int $n): string => mb_substr(trim(strip_tags((string) ($j[$k] ?? ''))), 0, $n);
$d = ['Nombre' => $lim('nombre', 80), 'Celular' => $lim('tel', 30), 'Correo del cliente' => $lim('email', 100), 'País' => $lim('pais', 40), 'Ciudad' => $lim('ciudad', 60), 'Equipo' => $lim('equipo', 60), 'Modelo' => $lim('modelo', 60), 'Problema' => $lim('problema', 600)];
if (mb_strlen($d['Nombre']) < 2 || strlen(preg_replace('/\D/', '', $d['Celular'])) < 7 || $d['Ciudad'] === '' || $d['Equipo'] === '') { http_response_code(422); echo '{"ok":false,"mensaje":"Faltan datos"}'; exit; }
if ($d['Correo del cliente'] !== '' && !filter_var($d['Correo del cliente'], FILTER_VALIDATE_EMAIL)) $d['Correo del cliente'] = '';
// Límite sencillo: máximo 8 solicitudes por hora desde la misma IP
$dir = __DIR__ . '/../data'; if (!is_dir($dir)) @mkdir($dir, 0755, true);
$lf = $dir . '/limite-' . md5((string) ($_SERVER['REMOTE_ADDR'] ?? '')) . '.txt';
$t = is_file($lf) ? array_filter(array_map('intval', explode(',', (string) file_get_contents($lf))), fn($x) => $x > time() - 3600) : [];
if (count($t) >= 8) { http_response_code(429); echo '{"ok":false,"mensaje":"Demasiadas solicitudes"}'; exit; }
$t[] = time(); @file_put_contents($lf, implode(',', $t));
$ref = 'SV-' . date('ymd') . '-' . strtoupper(bin2hex(random_bytes(3)));
$asunto = "Nueva solicitud de visita $ref — {$d['Equipo']} — {$d['Ciudad']}, {$d['País']}";
$filas = '';
foreach (['Nombre', 'Celular', 'Correo del cliente', 'País', 'Ciudad', 'Equipo', 'Modelo', 'Problema'] as $k) if ($d[$k] !== '') $filas .= '<tr><td style="padding:6px 10px;color:#5a6873">' . h($k) . '</td><td style="padding:6px 10px"><b>' . h($d[$k]) . '</b></td></tr>';
$html = '<h2 style="margin:0 0 8px">Nueva solicitud de visita</h2><p>Referencia <b>' . h($ref) . '</b>. Contacta al cliente para coordinar.</p><table style="border-collapse:collapse">' . $filas . '</table>';
$ok = false; $m = '';
foreach (correos_destino() as $dest) { if (enviar_correo($dest, $asunto, $html, $m)) $ok = true; }
if ($d['Correo del cliente'] !== '') enviar_correo($d['Correo del cliente'], "Recibimos tu solicitud $ref", '<h2 style="margin:0 0 8px">Recibimos tu solicitud</h2><p>Hola ' . h($d['Nombre']) . ', recibimos tu solicitud de visita (' . h($ref) . ') para tu ' . h($d['Equipo']) . ' Samsung en ' . h($d['Ciudad']) . '. Te contactaremos pronto para coordinar.</p>', $m2);
$forms = [];
foreach (correos_destino() as $dest) {
    $pl = form_payload($asunto, ['Solicitud' => $ref] + $d);
    $pl['url'] = preg_replace('~/ajax/.*$~', '/ajax/', $pl['url']) . rawurlencode($dest);
    unset($pl['datos']['_cc']);
    $forms[] = $pl;
}
@file_put_contents($dir . '/solicitudes.log', date('c') . " $ref " . json_encode($d, JSON_UNESCAPED_UNICODE) . ($ok ? '' : ' [correo no enviado]') . "\n", FILE_APPEND);
echo json_encode(['ok' => true, 'ref' => $ref, 'correo' => $ok, 'form' => $forms], JSON_UNESCAPED_UNICODE);
""", encoding="utf-8")
cfg = (AQUI / "src" / "api" / "config.sample.php").read_text(encoding="utf-8")
cfg = (cfg.replace("'dominio' => 'https://filtrosnevecones.com'", f"'dominio' => '{DOMINIO}'").replace("'nombre'    => 'Filtros Nevecones Colombia'", f"'nombre'    => '{NOMBRE}'").replace("'telefono'  => '310 714 7299'", f"'telefono'  => '{wa_vis('colombia')}'")
       .replace("'whatsapp' => '3107147299'", f"'whatsapp' => '{WA_DEF}'").replace("'gtm' => 'GTM-5WSNHV66'", f"'gtm' => '{GTM}'").replace("w-s2eiVewLzOHFjK7HAR9UUeqFoNMS14k_Gfrqt_ND4", TOKENS[0] if TOKENS else ""))
if os.environ.get("CORREO_AVISOS"):
    cfg = cfg.replace("'correo_avisos'    => 'serviciotecnicoyrepuestoscali@gmail.com'", f"'correo_avisos'    => '{os.environ['CORREO_AVISOS']}'", 1)
if os.environ.get("SMTP_CLAVE"):
    cfg = cfg.replace("'clave'   => '',", f"'clave'   => '{os.environ['SMTP_CLAVE']}',", 1)
(api / "config.sample.php").write_text(cfg, encoding="utf-8")
if os.environ.get("SMTP_CLAVE"):
    (api / "config.php").write_text(cfg, encoding="utf-8")

# datos estructurados, llms, robots, sitemaps, .htaccess
DATA = {"negocio": {"nombre": NOMBRE, "tipo": "Servicio técnico independiente especializado en electrodomésticos Samsung (no es Samsung Electronics)", "url": DOMINIO + "/", "atencion": "A domicilio", "diagnostico": "Primero el diagnóstico; el valor se confirma antes de reparar", "actualizado": HOY},
        "paises": {P["nombre"]: {"url": f"{DOMINIO}/{R_PAIS(pk)}", "whatsapp": "+" + wa_num(pk), "ciudades": [{"ciudad": c["n"], "zonas": {z: f"{DOMINIO}/{R_Z(c, z)}" for z in c["zonas"]}, "mantenimiento": f"{DOMINIO}/{R_MANT(c)}", "clima": CLIMA[c["s"]]["clima"], "altitud_m": CLIMA[c["s"]]["alt"], "url": f"{DOMINIO}/{R_CIU(c)}", "servicios": {pal(pk, sv)[1]: f"{DOMINIO}/{R_CS(c, sv)}" for sv in SERV_PAIS[pk]}} for c in CIU_PAIS[pk]]} for pk, P in PAISES.items()},
        "servicios": {SERVICIOS[s]["tit"]: {"lineas": SERVICIOS[s]["lineas"], "fallas": SERVICIOS[s]["sintomas"], "paginas": {P["nombre"]: f"{DOMINIO}/{R_SERV(k, s)}" for k, P in PAISES.items() if s in SERV_PAIS[k]}} for s in SERVICIOS}}
(OUT / "datos-servicio-tecnico.json").write_text(json.dumps(DATA, ensure_ascii=False, indent=1), encoding="utf-8")
ll = [f"# {NOMBRE}", "", f"> Servicio técnico independiente especializado en electrodomésticos Samsung (no somos Samsung Electronics). Visita a domicilio en {len(CIU)} ciudades de {len(PAISES)} países: neveras, lavadoras, secadoras, lavavajillas, estufas, hornos y microondas; televisores en Costa Rica. Primero el diagnóstico; el valor se confirma antes de reparar. Actualizado el {FECHA_LARGA}.", "", "## Países y ciudades"]
ll += [f"- [{P['nombre']}]({DOMINIO}/{R_PAIS(pk)}): " + ", ".join(c["n"] for c in CIU_PAIS[pk]) + f". WhatsApp +{wa_num(pk)}" for pk, P in PAISES.items()]
ll += ["", "## Servicios"] + [f"- [{cap(pal(k, s)[1])} en {P['nombre']}]({DOMINIO}/{R_SERV(k, s)}): {SERVICIOS[s]['lineas']}." for k, P in PAISES.items() for s in SERV_PAIS[k]] + ["", "## Guías de fallas"] + [f"- [{g['tit']}]({DOMINIO}/{R_G(g)}): {g['res']}" for g in GUIAS]
ll += ["", "## Datos", f"- [Datos estructurados]({DOMINIO}/datos-servicio-tecnico.json)", f"- [Respuestas rápidas]({DOMINIO}/respuestas-para-ia-servicio-tecnico-samsung.html)", f"- [llms-full.txt]({DOMINIO}/llms-full.txt)"]
(OUT / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
LF = ll[:3] + ["", "## Preguntas y respuestas", ""] + [x for q, a in G_IA for x in (f"**{q}**", a, "")] + ["## Guías (texto completo)", ""] + [x for g in GUIAS for x in (f"### {g['tit']}", g["res"], re.sub(r"<[^>]+>", " ", g["cuerpo"]), "")]
(OUT / "llms-full.txt").write_text("\n".join(LF) + "\n", encoding="utf-8")
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /data/\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot", "Amazonbot", "meta-externalagent", "cohere-ai", "DuckAssistBot", "MistralAI-User", "YouBot", "Applebot"))
                                + f"Sitemap: {DOMINIO}/sitemap.xml\n" + "".join(f"Sitemap: {DOMINIO}/sitemap-{g}.xml\n" for g in ("paises", "ciudades", "zonas", "servicios", "guias")), encoding="utf-8")
grupos = {g: [] for g in ("paises", "ciudades", "zonas", "servicios", "guias")}
for n, pr, _t, _d, tp in PAGINAS:
    grupos[tp].append((n, pr))
for g, l in grupos.items():
    (OUT / f"sitemap-{g}.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{DOMINIO}/{'' if n == 'index.html' else n}</loc><lastmod>{HOY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n" for n, pr in l) + "</urlset>\n", encoding="utf-8")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <sitemap><loc>{DOMINIO}/sitemap-{g}.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n" for g in grupos) + "</sitemapindex>\n", encoding="utf-8")
(OUT / ".htaccess").write_text("""DirectoryIndex index.html index.php
ErrorDocument 404 /404.html
Options -Indexes
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteCond %{HTTP:X-Forwarded-Proto} !https
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
<FilesMatch "\\.(sqlite|sqlite-wal|sqlite-shm|log)$">
  Require all denied
</FilesMatch>
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json application/xml text/plain image/svg+xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Strict-Transport-Security "max-age=31536000" env=HTTPS
</IfModule>
""", encoding="utf-8")
print(f"listo: {OUT} · {len(PAGINAS)} páginas · {len(CIU)} ciudades · {len(PAISES)} países")
