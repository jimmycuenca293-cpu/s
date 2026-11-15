# SEO técnico: sitemaps por tipo, feed de Google Merchant Center, caché, compresión y cabeceras de seguridad. Se ejecuta al final de ads_lg_paginas.py.
def _tipo(n):
    if n == "index.html" or n in {p["url"] for p in PS} or n.startswith(("filtro-nevecon-lg-", "referencia-filtro-lg-", "comparativa-", "filtro-lt1000p-", "lt1000p-")):
        return "filtros"
    if n.startswith(("filtro-agua-lg-", "precio-filtro-lg-")) and n != "filtro-agua-lg-por-ciudad-colombia.html":
        return "ciudades"
    if n.startswith(("filtros-lg-", "filtro-nevera-lg-")) or n in ("filtro-agua-lg-por-ciudad-colombia.html", "ciudades-con-filtros-lg-a-z.html"):
        return "cobertura"
    return "guias"


_grupos = {"filtros": [], "ciudades": [], "cobertura": [], "guias": []}
for n, pr, _t, _d in PAGINAS:
    _grupos[_tipo(n)].append((n, pr))
_hdr = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
for g, l in _grupos.items():
    (OUT / f"sitemap-{g}.xml").write_text(_hdr + "".join(
        f"  <url><loc>{DOMINIO}/{'' if n == 'index.html' else n}</loc><lastmod>{HOY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority>"
        + (f"<image:image><image:loc>{IMG_MAP[n]}</image:loc></image:image>" if n in IMG_MAP else "") + "</url>\n" for n, pr in l) + "</urlset>\n", encoding="utf-8")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <sitemap><loc>{DOMINIO}/sitemap-{g}.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n" for g in _grupos) + "</sitemapindex>\n", encoding="utf-8")

# Feed para Google Merchant Center (fichas gratuitas en Google Shopping)
_it = ""
for p in PS:
    _it += (f"<item><g:id>{p['id']}</g:id><g:title>{esc('Filtro de agua LG ' + p['nombre'] + ' (' + p['ref'] + ')')}</g:title>"
            f"<g:description>{esc('Filtro de agua ' + p['nombre'] + ', código ' + p['ref'] + ', equivalente a ' + (', '.join(p['refs'][1:4]) or p['ref']) + '. ' + ('Nevecones: ' + ', '.join(p['modelos']) + '. ' if p['modelos'] else '') + 'Se cambia cada 6 meses. Envío gratis a toda Colombia.')}</g:description>"
            f"<g:link>{DOMINIO}/{p['url']}</g:link><g:image_link>{DOMINIO}/{p['img']}</g:image_link><g:availability>in_stock</g:availability><g:price>{p['precio']}.00 COP</g:price><g:condition>new</g:condition>"
            f"<g:brand>LG</g:brand><g:mpn>{esc(p['ref'])}</g:mpn><g:identifier_exists>no</g:identifier_exists><g:product_type>Filtros de agua para nevecón LG</g:product_type>"
            f"<g:shipping><g:country>CO</g:country><g:service>Estándar</g:service><g:price>0.00 COP</g:price></g:shipping></item>\n")
(OUT / "feed-google-merchant.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0"><channel><title>Filtro de Agua LG Colombia</title>'
                                              f"<link>{DOMINIO}/</link><description>Filtros de agua para neveras LG</description>\n{_it}</channel></rss>\n", encoding="utf-8")
_r = (OUT / "robots.txt").read_text(encoding="utf-8")
(OUT / "robots.txt").write_text(_r.replace(f"Sitemap: {DOMINIO}/sitemap.xml\n", f"Sitemap: {DOMINIO}/sitemap.xml\n" + "".join(f"Sitemap: {DOMINIO}/sitemap-{g}.xml\n" for g in _grupos)), encoding="utf-8")

# Rendimiento y seguridad (Apache/Hostinger)
_h = (OUT / ".htaccess").read_text(encoding="utf-8")
_h += """
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json application/xml text/plain image/svg+xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
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
  <FilesMatch "\\.(webp|jpg|png|css|js)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
</IfModule>
"""
(OUT / ".htaccess").write_text(_h, encoding="utf-8")
print("técnico:", {g: len(l) for g, l in _grupos.items()})
