# Archivos de salida: buscador y banner, formulario de solicitud, API, mapa del sitio, sitemaps, robots, llms y datos (se ejecuta al final de st_paginas.py).
mapa = lambda t, its: f'<h2 style="font-size:22px;margin:22px 0 10px">{esc(t)}</h2><ul class="spec-list">' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in its) + "</ul>"
for pk, P in PAISES.items():
    cs_ = CIU_PAIS[pk]
    cuerpo = (mapa("Ciudades", [(f"Servicio técnico Samsung en {c['n']}", R_CIU(c)) for c in cs_])
              + mapa("Zonas", [(f"Servicio técnico Samsung en {z}, {c['n']}", R_Z(c, z)) for c, z in ZONAS_P if c["pk"] == pk]) + mapa("Mantenimiento por ciudad", [(f"Mantenimiento en {c['n']}", R_MANT(c)) for c in cs_]) + mapa("Voltaje", [(f"Voltaje en {P['nombre']}", R_VOLT(pk))])
              + mapa("Equipos", [(f"Servicio técnico de {pal(pk, s_)[1]} Samsung en {P['nombre']}", R_SERV(pk, s_)) for s_ in SERV_PAIS[pk]]) + mapa("Guías de fallas", [(loc(g["tit"], pk), R_G(g, pk)) for g in GUIAS_PK(pk)] + [("Códigos de error de lavadoras Samsung", R_COD_LISTA(pk))] + [(f"Cómo leer el modelo de tu {pal(pk, sv)[0]} Samsung", R_MOD(pk, sv)) for sv in SERV_PAIS[pk]])
              + mapa("Blog", [("Blog del centro de servicio técnico Samsung", f"{pk}/blog/index.html")] + [(t, u) for k, sl, t, u, d in BLOG if k == pk]) + mapa("Líneas Samsung", [(f"{cap(pal(k, sv)[1])} Samsung {ln} en {P['nombre']}", u) for k, sv, ln, u in LINEAS_P if k == pk]) + mapa("Fallas frecuentes por ciudad", [(pr["tit"].format(S=cap(pal(c["pk"], pr["sv"])[0]), s=pal(c["pk"], pr["sv"])[0], c=c["n"]), R_PROB(c, pr)) for c, pr in PROB_P if c["pk"] == pk])
              + mapa("Por departamento", [(f"Servicio técnico Samsung en {d} ({P['nombre']})", R_DEP(k, d)) for k, d in DEP_HUBS if k == pk]) + mapa("Contacto por ciudad", [(h, u) for k, c_, t_, u, h in CONT_P if k == pk]) + mapa("Ayuda", [("Solicitar visita", R_SOL(pk)), ("Preguntas frecuentes", R_FAQ(pk)), ("Respuestas rápidas", R_IA(pk)), ("Quiénes somos", R_INST(pk, "quienes-somos")), ("Contacto", R_INST(pk, "contacto"))]))
    pagina(R_MAPA(pk), f"Mapa del sitio | Servicio técnico Samsung en {P['nombre']}", f"Todas las páginas del servicio técnico Samsung en {P['nombre']}: ciudades, zonas, equipos y guías de fallas.", f"mapa del sitio servicio tecnico samsung {P['nombre'].lower()}", [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Mapa del sitio", None)],
           hero_simple(f"{P['bandera']} Mapa del sitio", f"Todas las páginas de {P['nombre']}", "Ciudades, equipos y guías.") + qa(f"¿Qué hay en la sección de {P['nombre']}?", f"Servicio técnico Samsung en {len(cs_)} ciudades de {esc(P['nombre'])}, páginas por equipo, guías de fallas y respuestas rápidas.") + seccion("Páginas", cuerpo), [], [], prio="0.4", pk=pk, tipo="guias")

# buscador + banner de ciudades
CL = lambda u: u[:-10] if u.endswith("index.html") else u
items = []
for _pk, _P in PAISES.items():
    _it = [[_P["nombre"], R_PAIS(_pk), "País", f"{len(CIU_PAIS[_pk])} ciudades", _pk]] + [[c["n"], R_CIU(c), "Ciudad", c["pais"], _pk] for c in CIU_PAIS[_pk]]
    _it += [[cap(pal(_pk, s_)[1]), R_SERV(_pk, s_), "Servicio", _P["nombre"], _pk] for s_ in SERV_PAIS[_pk]] + [[loc(g["tit"], _pk), R_G(g, _pk), "Guía de fallas", "", _pk] for g in GUIAS_PK(_pk)]
    _it += [[f"{cap(pal(_pk, sv)[1])} en {c['n']}", R_CS(c, sv), "Reparación", c["pais"], _pk] for c in CIU_PAIS[_pk] for sv in SERV_PAIS[_pk]]
    _it += [[f"{z} · {c['n']}", R_Z(c, z), "Zona", c["pais"], _pk] for c, z in ZONAS_P if c["pk"] == _pk]
    _it += [[f"{cap(pal(k, sv)[1])} Samsung {ln}", u, "Línea", _P["nombre"], _pk] for k, sv, ln, u in LINEAS_P if k == _pk]
    _it += [[t, u, "Blog", _P["nombre"], _pk] for k, sl, t, u, d in BLOG if k == _pk]
    _it += [[h, u, "Contacto", _P["nombre"], _pk] for k, c_, t_, u, h in CONT_P if k == _pk]
    _it += [[pr["tit"].format(S=cap(pal(c["pk"], pr["sv"])[0]), s=pal(c["pk"], pr["sv"])[0], c=c["n"]), R_PROB(c, pr), "Falla", c["pais"], _pk] for c, pr in PROB_P if c["pk"] == _pk]
    items.append((_pk, [[a, CL(b), c_, d_, e_] for a, b, c_, d_, e_ in _it]))
home_items = [[P["nombre"], CL(R_PAIS(pk)), "País", f"{len(CIU_PAIS[pk])} ciudades", ""] for pk, P in PAISES.items()]


def mk_js(its):
    return ("(function(){var D=" + json.dumps(its, ensure_ascii=False, separators=(",", ":")) + ";"
          "function n(s){return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').trim()}var X=D.map(function(r){return n(r[0]+' '+r[2]+' '+r[3])});"
          "function buscar(q,P){q=n(q);if(!q)return[];var t=q.split(/ +/),o=[];for(var i=0;i<D.length;i++){if(P&&D[i][4]&&D[i][4]!==P)continue;var ok=true,sc=0;for(var j=0;j<t.length;j++){var p=X[i].indexOf(t[j]);if(p<0){ok=false;break}sc+=p===0?0:1}if(ok){var e=n(D[i][0]);o.push([sc+(e.indexOf(q)===0?-2:0)+(D[i][2]==='Ciudad'||D[i][2]==='País'?0:.5),i])}}o.sort(function(a,b){return a[0]-b[0]});return o.slice(0,14).map(function(x){return D[x[1]]})}"
          "function pintar(caja,r,q){if(!q.trim()){caja.hidden=true;return}var g={},h='';r.forEach(function(x){(g[x[2]]=g[x[2]]||[]).push(x)});Object.keys(g).forEach(function(k){h+='<h6>'+k+'</h6>'+g[k].map(function(x){return '<a href=\"'+(window.ST_ROOT||'')+x[1]+'\"><span>'+x[0]+'</span><small>'+x[3]+'</small></a>'}).join('')});caja.innerHTML=h||'<p>No encontramos «'+q.replace(/</g,'')+'». Prueba con tu ciudad, tu país o el equipo.</p>';caja.hidden=false}"
          "document.querySelectorAll('[data-aq-q]').forEach(function(i){var c=i.parentNode.querySelector('.aq-res');var P=i.getAttribute('data-aq-pais')||'';i.addEventListener('input',function(){pintar(c,buscar(i.value,P),i.value)});i.addEventListener('focus',function(){if(i.value)pintar(c,buscar(i.value,P),i.value)});i.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=c.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape')c.hidden=true})});"
          "(function(){var t=document.querySelector('[data-tk]');if(!t)return;var K=t.getAttribute('data-tk');var c=D.filter(function(r){return K==='paises'?r[2]==='País':(r[2]==='Ciudad'&&r[4]===K)}).map(function(r){return r[0]});if(!c.length)return;var h=c.map(function(n){return '<span>'+n+'</span>'}).join('');t.innerHTML=h+h;t.style.setProperty('--d',Math.max(25,Math.round(c.length*3))+'s')})();"
          "document.addEventListener('click',function(e){document.querySelectorAll('.aq-res').forEach(function(c){if(!c.parentNode.contains(e.target))c.hidden=true});document.querySelectorAll('.aq-nav details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});})();")



(OUT / "buscar.js").write_text(mk_js(home_items), encoding="utf-8")
for _pk, _it in items:
    (OUT / _pk).mkdir(parents=True, exist_ok=True)
    (OUT / _pk / "buscar.js").write_text(mk_js(_it), encoding="utf-8")


(OUT / "solicitar.js").write_text("""(function(){var f=document.getElementById('sv-form');if(!f)return;var P=document.getElementById('sv-pais'),C=document.getElementById('sv-ciudad'),R=document.getElementById('sv-res');
function ciu(){C.innerHTML=(window.SV_CIU[P.value]||[]).map(function(c){return '<option>'+c+'</option>'}).join('')}P.addEventListener('change',ciu);ciu();
function FY(f){if(Array.isArray(f)){f.forEach(FY);return}if(!f||!f.url||!f.datos)return;try{fetch(f.url,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(f.datos),keepalive:true}).catch(function(){})}catch(e){}}
f.addEventListener('submit',function(e){e.preventDefault();var d={};new FormData(f).forEach(function(v,k){d[k]=v});if(!d.nombre||!d.tel||String(d.tel).replace(/\\D/g,'').length<7){R.innerHTML='<p style="color:#b91c1c">Escribe tu nombre y un celular válido.</p>';return}
R.textContent='Enviando…';fetch('/api/solicitud.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json()}).then(function(j){if(!j.ok)throw new Error(j.mensaje||'Error');FY(j.form);
var m=encodeURIComponent('Hola, acabo de solicitar una visita ('+j.ref+') para mi '+d.equipo+' Samsung en '+d.ciudad);R.innerHTML='<div class="st-ok"><b>¡Solicitud recibida!</b><br>Tu referencia es '+j.ref+'. Te contactaremos pronto. Si es urgente, escríbenos por WhatsApp.<br><a class="st-btn wa" style="margin-top:10px" target="_blank" rel="noopener" href="https://wa.me/'+(window.SV_WA||'')+'?text='+m+'">Escribir por WhatsApp</a></div>';f.reset();ciu()}).catch(function(){R.innerHTML='<p style="color:#b91c1c">No pudimos enviar el formulario. Escríbenos por WhatsApp y te atendemos.</p>'})})})();
""".replace("window.SV_WA||''", "(window.SV_WA||{})[d.pais]||''"), encoding="utf-8")

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

# datos estructurados, llms, robots y sitemaps: cada país tiene los suyos dentro de su carpeta; la raíz solo apunta a ellos
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]; v = VOLT[pk]
    DATA = {"negocio": {"nombre": NOMBRE, "tipo": "Servicio técnico independiente especializado en electrodomésticos Samsung (no es Samsung Electronics)", "pais": P["nombre"], "url": U(R_PAIS(pk)), "whatsapp": "+" + wa_num(pk), "atencion": "A domicilio", "diagnostico": "Primero el diagnóstico; el valor se confirma antes de reparar", "actualizado": HOY},
            "ciudades": [{"ciudad": c["n"], "zonas": {z: U(R_Z(c, z)) for z in c["zonas"]}, "mantenimiento": U(R_MANT(c)), "clima": CLIMA[c["s"]]["clima"], "altitud_m": CLIMA[c["s"]]["alt"], "url": U(R_CIU(c)), "servicios": {pal(pk, sv)[1]: U(R_CS(c, sv)) for sv in SERV_PAIS[pk]}} for c in cs],
            "servicios": {SERVICIOS[s_]["tit"]: {"lineas": SERVICIOS[s_]["lineas"], "fallas": SERVICIOS[s_]["sintomas"], "pagina": U(R_SERV(pk, s_))} for s_ in SERV_PAIS[pk]}}
    (OUT / pk / "datos-servicio-tecnico.json").write_text(json.dumps(DATA, ensure_ascii=False, indent=1), encoding="utf-8")
    L = [f"# Servicio técnico Samsung en {P['nombre']}", "", f"> Servicio técnico independiente especializado en electrodomésticos Samsung en {P['nombre']} (no somos Samsung Electronics). Visita a domicilio en {len(cs)} ciudades; primero el diagnóstico y el valor se confirma antes de reparar. WhatsApp +{wa_num(pk)}. Actualizado el {FECHA_LARGA}.", "",
         "## Equipos que reparamos"] + [f"- [{cap(pal(pk, s_)[1])}]({U(R_SERV(pk, s_))}): {SERVICIOS[s_]['lineas']}." for s_ in SERV_PAIS[pk]]
    L += ["", "## Ciudades"] + [f"- [{c['n']}]({U(R_CIU(c))})" + (" (cobertura ampliada, con coordinación previa)" if c["amp"] else "") for c in cs]
    L += ["", "## Guías de fallas"] + [f"- [{loc(g['tit'], pk)}]({U(R_G(g, pk))}): {loc(g['res'], pk)}" for g in GUIAS_PK(pk)]
    L += ["", "## Datos útiles", f"- Red eléctrica: {v[0]} a {v[1]}, enchufes {v[2]}.", f"- [Voltaje y electrodomésticos Samsung en {P['nombre']}]({U(R_VOLT(pk))})", f"- [Preguntas frecuentes]({U(R_FAQ(pk))})", f"- [Respuestas rápidas]({U(R_IA(pk))})", f"- [Datos estructurados]({DOMINIO}/{pk}/datos-servicio-tecnico.json)", f"- [llms-full.txt]({DOMINIO}/{pk}/llms-full.txt)", "", "## Preguntas y respuestas"]
    QA_ = []
    for c in cs:
        for sv in SERV_PAIS[pk]:
            QA_ += [f"**¿Reparan {pal(pk, sv)[1]} Samsung en {c['n']}?** Sí, con visita a domicilio" + (" (cobertura ampliada)" if c["amp"] else "") + f"; el valor se confirma tras el diagnóstico. WhatsApp +{wa_num(pk)}.", ""]
    (OUT / pk / "llms.txt").write_text("\n".join(L + QA_) + "\n", encoding="utf-8")
    LF = L[:3] + ["", "## Preguntas y respuestas", ""] + QA_ + ["## Guías (texto completo)", ""] + [x for g in GUIAS_PK(pk) for x in (f"### {loc(g['tit'], pk)}", loc(g["res"], pk), loc(re.sub(r"<[^>]+>", " ", g["cuerpo"]), pk), "")]
    (OUT / pk / "llms-full.txt").write_text("\n".join(LF) + "\n", encoding="utf-8")
ll = [f"# {NOMBRE}", "", f"> Servicio técnico independiente especializado en electrodomésticos Samsung (no somos Samsung Electronics). Cada país tiene su propia sección con sus ciudades y su WhatsApp. Actualizado el {FECHA_LARGA}.", "", "## Información por país"]
ll += [f"- [{P['nombre']}]({DOMINIO}/{pk}/llms.txt)" for pk, P in PAISES.items()]
(OUT / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /data/\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot", "Amazonbot", "meta-externalagent", "cohere-ai", "DuckAssistBot", "MistralAI-User", "YouBot", "Applebot"))
                                + f"Sitemap: {DOMINIO}/sitemap.xml\n" + "".join(f"Sitemap: {DOMINIO}/sitemap-{pk}.xml\n" for pk in PAISES), encoding="utf-8")
grupos = {pk: [] for pk in PAISES}
grupos["inicio"] = []
for n, pr, _t, _d, tp in PAGINAS:
    grupos[n.split("/")[0] if n.split("/")[0] in PAISES else "inicio"].append((n, pr))
for g, l in grupos.items():
    (OUT / (f"sitemap-{g}.xml")).write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{U(n)}</loc><lastmod>{HOY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n" for n, pr in l) + "</urlset>\n", encoding="utf-8")
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
# ---- detección de país y ciudad (zona horaria sin permiso; ubicación exacta solo si el cliente la permite)
import csv as _c
_COD = {"colombia": "co", "panama": "pa", "costa-rica": "cr", "paraguay": "py", "guatemala": "gt", "el-salvador": "sv", "ecuador": "ec", "chile": "cl"}
_NORM = lambda x: slug(x)
_coord = {}
_csv = AQUI.parent / "app-servicio-tecnico-latam" / "tecnicos.csv"
if _csv.exists():
    for _r in _c.DictReader(open(_csv, encoding="utf-8")):
        if _r["marca"] == "samsung":
            try:
                _coord.setdefault((_r["pais"], _NORM(_r["ciudad"])), (float(_r["lat"]), float(_r["lon"])))
            except ValueError:
                pass
_extra = {("co", "giron"): (7.07, -73.17), ("co", "piedecuesta"): (6.99, -73.05), ("co", "rionegro"): (6.155, -75.374), ("co", "la-estrella"): (6.158, -75.643), ("co", "sabaneta"): (6.151, -75.616), ("co", "dosquebradas"): (4.84, -75.67),
          ("co", "santa-rosa-de-cabal"): (4.868, -75.62), ("co", "jamundi"): (3.26, -76.54), ("co", "buga"): (3.9, -76.3), ("co", "duitama"): (5.82, -73.03), ("co", "ipiales"): (0.83, -77.64), ("co", "san-andres"): (12.58, -81.7),
          ("co", "fusagasuga"): (4.34, -74.36), ("co", "facatativa"): (4.81, -74.36), ("co", "bogota"): (4.711, -74.072), ("pa", "ciudad-de-panama"): (8.983, -79.517), ("cr", "san-jose"): (9.928, -84.091), ("py", "asuncion"): (-25.264, -57.576),
          ("gt", "ciudad-de-guatemala"): (14.635, -90.507), ("sv", "san-salvador"): (13.693, -89.218), ("ec", "quito"): (-0.18, -78.468), ("ec", "guayaquil"): (-2.17, -79.92), ("cl", "santiago-de-chile"): (-33.449, -70.669)}
_geo = []
for _c_ in CIU:
    _k = (_COD[_c_["pk"]], _NORM(_c_["n"]))
    _ll = _coord.get(_k) or _extra.get(_k) or _coord.get((_k[0], _NORM(_c_["n"].replace("de Chile", "").strip())))
    if _ll:
        _geo.append([_c_["pk"], _c_["n"], CL(R_CIU(_c_)), round(_ll[0], 3), round(_ll[1], 3), 1 if _c_["amp"] else 0])
_pp = {pk: [P["nombre"], CL(R_PAIS(pk))] for pk, P in PAISES.items()}
(OUT / "geo.js").write_text("""(function(){var C=""" + json.dumps(_geo, ensure_ascii=False, separators=(",", ":")) + """,P=""" + json.dumps(_pp, ensure_ascii=False, separators=(",", ":")) + """;
var TZ={'America/Bogota':'colombia','America/Panama':'panama','America/Costa_Rica':'costa-rica','America/Asuncion':'paraguay','America/Guatemala':'guatemala','America/El_Salvador':'el-salvador','America/Guayaquil':'ecuador','Pacific/Galapagos':'ecuador','America/Santiago':'chile','America/Punta_Arenas':'chile'};
var LG={'es-co':'colombia','es-pa':'panama','es-cr':'costa-rica','es-py':'paraguay','es-gt':'guatemala','es-sv':'el-salvador','es-ec':'ecuador','es-cl':'chile'};
function K(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
var m=document.querySelector('meta[name="st-pais"]'),aqui=m?m.content:'';
var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
var det=K('st_pais')||TZ[tz]||LG[(navigator.language||'').toLowerCase()]||'';
function dist(a,b,c,d){var R=6371,r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h))}
function cerca(lat,lon){var b=null,bd=1e9,dd=null,dm=1e9;C.forEach(function(c){var d=dist(lat,lon,c[3],c[4]);if(d<bd){bd=d;b=c}if(!c[5]&&d<dm){dm=d;dd=c}});if(b&&b[5]&&dd&&dm-bd<25){b=dd;bd=dm}return b?{c:b,d:bd}:null}
function barra(html){var d=document.createElement('div');d.className='st-geo';d.setAttribute('role','region');d.setAttribute('aria-label','Tu ubicación');d.innerHTML=html;document.body.insertBefore(d,document.body.firstChild);return d}
function usar(btn,msg){if(!navigator.geolocation){msg.textContent='Tu navegador no permite ubicación.';return}btn.disabled=true;msg.textContent='Buscando tu ubicación…';
navigator.geolocation.getCurrentPosition(function(p){var r=cerca(p.coords.latitude,p.coords.longitude);if(!r){msg.textContent='No pudimos ubicarte.';btn.disabled=false;return}K('st_pais',r.c[0]);
if(r.d>800){msg.innerHTML='Estás lejos de nuestras ciudades. La más cercana es '+r.c[1]+' ('+Math.round(r.d)+' km). <a href="'+r.c[2]+'">Ver '+r.c[1]+'</a>';btn.disabled=false;return}
msg.textContent='Estás cerca de '+r.c[1]+'. Te llevamos a su página…';location.href=r.c[2]},function(){msg.textContent='No se pudo obtener la ubicación. Elige tu país abajo.';btn.disabled=false},{enableHighAccuracy:true,timeout:12000,maximumAge:300000})}
window.STUbicacion=usar;
document.addEventListener('DOMContentLoaded',function(){
 document.querySelectorAll('[data-geo]').forEach(function(b){var msg=b.parentNode.querySelector('[data-geo-msg]')||document.createElement('span');b.addEventListener('click',function(){usar(b,msg)})});
 if(K('st_geo_x')==='1')return;
 if(det&&P[det]&&det!==aqui){var b=barra('<span>Parece que estás en <b>'+P[det][0]+'</b>.</span> <a class="st-btn sol" href="'+P[det][1]+'">Ver servicio técnico Samsung en '+P[det][0]+'</a> <button type="button" class="st-btn" data-ub>Usar mi ubicación exacta</button> <span data-um></span> <button type="button" class="st-x" aria-label="Cerrar">×</button>');
  b.querySelector('[data-ub]').addEventListener('click',function(){usar(this,b.querySelector('[data-um]'))});b.querySelector('.st-x').addEventListener('click',function(){K('st_geo_x','1');b.remove()});
  var cards=document.querySelectorAll('.st-pais');cards.forEach(function(a){if(a.getAttribute('href')===P[det][1]){a.classList.add('st-pais-det');var g=a.parentNode;g.insertBefore(a,g.firstChild)}})}
 else if(!aqui&&!det){}
 try{if(navigator.permissions&&!aqui){navigator.permissions.query({name:'geolocation'}).then(function(r){if(r.state==='granted'){var b=document.querySelector('[data-geo]');if(b)usar(b,b.parentNode.querySelector('[data-geo-msg]')||document.createElement('span'))}})}}catch(e){}
});})();
""", encoding="utf-8")
for _pk in PAISES:
    _cg = [g for g in _geo if g[0] == _pk]
    (OUT / _pk / "geo.js").write_text("""(function(){var C=""" + json.dumps(_cg, ensure_ascii=False, separators=(",", ":")) + """,R=window.ST_ROOT||'';
function dist(a,b,c,d){var r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 12742*Math.asin(Math.sqrt(h))}
function cerca(lat,lon){var b=null,bd=1e9,dd=null,dm=1e9;C.forEach(function(c){var d=dist(lat,lon,c[3],c[4]);if(d<bd){bd=d;b=c}if(!c[5]&&d<dm){dm=d;dd=c}});if(b&&b[5]&&dd&&dm-bd<25){b=dd;bd=dm}return b?{c:b,d:bd}:null}
function usar(btn,msg){if(!navigator.geolocation){msg.textContent='Tu navegador no permite ubicación.';return}btn.disabled=true;msg.textContent='Buscando tu ubicación…';
navigator.geolocation.getCurrentPosition(function(p){var r=cerca(p.coords.latitude,p.coords.longitude);btn.disabled=false;if(!r){msg.textContent='No pudimos ubicarte.';return}
if(r.d>150){msg.innerHTML='Tu ubicación está lejos de nuestras ciudades. La más cercana es '+r.c[1]+' ('+Math.round(r.d)+' km). <a href="'+R+r.c[2]+'">Ver '+r.c[1]+'</a>';return}
msg.textContent='Estás en '+r.c[1]+'. Abriendo su página…';location.href=R+r.c[2]},function(){btn.disabled=false;msg.textContent='No se pudo obtener la ubicación. Elige tu ciudad en el menú.'},{enableHighAccuracy:true,timeout:12000,maximumAge:300000})}
document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('[data-geo]').forEach(function(b){var m=b.parentNode.querySelector('[data-geo-msg]')||(function(){var s=document.createElement('p');s.className='st-aviso';s.setAttribute('data-geo-msg','');b.parentNode.parentNode.insertBefore(s,b.parentNode.nextSibling);return s})();b.addEventListener('click',function(){usar(b,m)})})});})();
""", encoding="utf-8")
# ---- imágenes con nombre descriptivo (SEO de imágenes) y sitemap de imágenes
RN = {"nevera-family-hub": "nevera-samsung-side-by-side-family-hub", "nevera-superior-inox": "nevera-samsung-superior-inox", "lavadora-superior": "lavadora-samsung-carga-superior", "secadora-torre": "torre-lavado-secado-samsung-apilada", "secadora": "secadora-samsung-carga-frontal",
      "torre-lavado": "torre-de-lavado-samsung", "microondas": "microondas-samsung-ceramic-inside", "portada-tecnico": "tecnico-samsung-a-domicilio-portada", "tecnico-neveras": "tecnico-reparando-nevera-samsung", "tecnico-lavadora": "tecnico-reparando-lavadora-samsung",
      "c-revision": "tecnico-samsung-revision-en-casa", "c-compresor": "tecnico-samsung-revisando-compresor", "sam-cin-o": "filtro-agua-samsung-haf-cin", "sam-qin-o": "filtro-agua-samsung-haf-qin", "sam-cu1-o": "filtro-agua-samsung-aqua-pure-plus", "sam-ex-o": "filtro-agua-externo-samsung"}
for _i in range(1, 8):
    RN[f"stp{_i}"] = f"tecnico-samsung-visita-a-domicilio-{_i}"
for _o, _n in sorted(RN.items(), key=lambda x: -len(x[0])):
    for _suf in ("", "-m", "-s", "-400"):
        _f = OUT / "img" / f"{_o}{_suf}.webp"
        if _f.exists():
            _f.rename(OUT / "img" / f"{_n}{_suf}.webp")
_pat = re.compile(r"img/(" + "|".join(re.escape(o) for o in sorted(RN, key=lambda x: -len(x))) + r")((?:-m|-s|-400)?)\.webp")
for _h in list(OUT.rglob("*.html")) + [OUT / "tema.css"]:
    _t = _h.read_text(encoding="utf-8")
    _t2 = _pat.sub(lambda m: f"img/{RN[m.group(1)]}{m.group(2)}.webp", _t)
    if _t2 != _t:
        _h.write_text(_t2, encoding="utf-8")
for _pk in list(PAISES) + ["inicio"]:
    _img = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    for _n, _pr, _t, _d, _tp in PAGINAS:
        if (_n.split("/")[0] if _n.split("/")[0] in PAISES else "inicio") != _pk:
            continue
        _imgs = []
        for _m in re.finditer(r'<img[^>]+src="img/([^"]+\.webp)"[^>]*alt="([^"]*)"', (OUT / _n).read_text(encoding="utf-8")):
            if _m.group(1) not in [x[0] for x in _imgs]:
                _imgs.append((_m.group(1), _m.group(2)))
        if _imgs:
            _img += f"  <url><loc>{U(_n)}</loc>" + "".join(f"<image:image><image:loc>{DOMINIO}/img/{a}</image:loc><image:caption>{esc(b)}</image:caption></image:image>" for a, b in _imgs[:8]) + "</url>\n"
    (OUT / f"sitemap-imagenes-{_pk}.xml").write_text(_img + "</urlset>\n", encoding="utf-8")
_sm = (OUT / "sitemap.xml").read_text(encoding="utf-8")
(OUT / "sitemap.xml").write_text(_sm.replace("</sitemapindex>", "".join(f"  <sitemap><loc>{DOMINIO}/sitemap-imagenes-{_pk}.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n" for _pk in list(PAISES) + ["inicio"]) + "</sitemapindex>"), encoding="utf-8")
_rb = (OUT / "robots.txt").read_text(encoding="utf-8")
(OUT / "robots.txt").write_text(_rb + "".join(f"Sitemap: {DOMINIO}/sitemap-imagenes-{_pk}.xml\n" for _pk in list(PAISES) + ["inicio"]), encoding="utf-8")
# IndexNow (Bing y buscadores que lo usan): archivo de clave + lista de URLs para enviar después de publicar
_key = hashlib.md5(("indexnow|" + DOMINIO).encode()).hexdigest()
(OUT / f"{_key}.txt").write_text(_key, encoding="utf-8")
(OUT.parent / (OUT.name + "-indexnow-urls.txt")).write_text("\n".join(U(n) for n, *_ in PAGINAS), encoding="utf-8")

# ---- pasada final: enlaces relativos según la profundidad de cada página (cada país es un directorio) y URLs limpias terminadas en «/»
_PREV = os.environ.get("ST_PREVIEW") == "1"
_attr = re.compile(r'(href|src)="(?!https?:|//|mailto:|tel:|data:|javascript:)([^"#]*)(#[^"]*)?"')


def _rel(nombre, t):
    pre = "../" * nombre.count("/")

    def f(m):
        ruta, frag = m.group(2), m.group(3) or ""
        if not _PREV and ruta.endswith("index.html"):
            ruta = ruta[:-10]
        if ruta == "" and not frag:
            return f'{m.group(1)}="{pre or "./"}"'
        if ruta == "" and frag and not pre:
            return f'{m.group(1)}="{frag}"'
        return f'{m.group(1)}="{pre}{ruta}{frag}"'
    t = _attr.sub(f, t)
    t = t.replace("url(img/", f"url({pre}img/").replace('window.ST_ROOT="__ROOT__"', f'window.ST_ROOT="{pre}"')
    return t


for _n in [n for n, *_ in PAGINAS]:
    _f = OUT / _n
    _f.write_text(_rel(_n, _f.read_text(encoding="utf-8")), encoding="utf-8")
print(f"listo: {OUT} · {len(PAGINAS)} páginas · {len(CIU)} ciudades · {len(PAISES)} países")
