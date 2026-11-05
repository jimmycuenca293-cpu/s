# -*- coding: utf-8 -*-
# Marca: WhatsApp oficial (glifo) y logo de pesa con el nombre
WA_PATH="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"
WA_SVG=f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="{WA_PATH}"/></svg>'

GRAD='<defs><linearGradient id="gy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe27a"/><stop offset=".5" stop-color="#ffc400"/><stop offset="1" stop-color="#c98f00"/></linearGradient><linearGradient id="gm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1f4f8"/><stop offset=".45" stop-color="#9aa4b0"/><stop offset="1" stop-color="#d6dce3"/></linearGradient><linearGradient id="gb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a414b"/><stop offset=".5" stop-color="#1b1f25"/><stop offset="1" stop-color="#0f1215"/></linearGradient></defs>'
TEXTO='TÉCNICO GYM'
def _w(texto,s): return sum((16 if c==' ' else 30)*s for c in texto)-6*s
def _letters(x0,y0,s,sw,color):
    L={'O':'M12 4C6 4 5 9 5 17S6 30 12 30S19 25 19 17S18 4 12 4Z','Y':'M4 4L12 17L20 4M12 17V30','M':'M4 30V4L12 18L20 4V30','T':'M2 4H22M12 4V30','E':'M20 4H5V30H20M5 17H17','C':'M21 9C17 2 5 4 5 17S17 32 21 25','H':'M5 4V30M19 4V30M5 17H19','N':'M5 30V4L19 30V4','I':'M12 4V30','G':'M21 9C17 2 5 4 5 17S17 32 21 25V18H13'}
    out='';x=x0
    for ch in TEXTO:
        if ch==' ': x+=16*s; continue
        key='E' if ch=='\u00c9' else ch
        d=L[key]+('M10 -3L17 -8' if ch=='\u00c9' else '')
        out+=f'<path d="{d}" transform="translate({x:.1f},{y0}) scale({s})" fill="none" stroke="{color}" stroke-width="{sw/s:.2f}" stroke-linecap="round" stroke-linejoin="round"/>'
        x+=30*s
    return out
def dumbbell_icon():
    return GRAD.replace('id="gy"','id="gy"')+'<ellipse cx="80" cy="93" rx="64" ry="5" fill="#000" opacity=".22"/><rect x="34" y="43" width="92" height="14" rx="7" fill="url(#gm)"/>'+''.join(f'<path d="M{x} 45.5V54.5" stroke="#000" stroke-opacity=".2" stroke-width="1.4"/>' for x in range(56,106,4))+'<rect x="35" y="38" width="9" height="24" rx="3" fill="url(#gm)"/><rect x="116" y="38" width="9" height="24" rx="3" fill="url(#gm)"/><rect x="17" y="20" width="19" height="60" rx="7" fill="url(#gy)"/><rect x="124" y="20" width="19" height="60" rx="7" fill="url(#gy)"/><rect x="3" y="31" width="15" height="38" rx="6" fill="url(#gy)"/><rect x="142" y="31" width="15" height="38" rx="6" fill="url(#gy)"/><rect x="21" y="24" width="4" height="52" rx="2" fill="#fff" opacity=".38"/><rect x="135" y="24" width="4" height="52" rx="2" fill="#fff" opacity=".38"/><rect x="6" y="35" width="3" height="30" rx="1.5" fill="#fff" opacity=".38"/><rect x="151" y="35" width="3" height="30" rx="1.5" fill="#fff" opacity=".38"/>'
ICON_SVG='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 100" aria-hidden="true">'+dumbbell_icon()+'</svg>'
def logo_pesa(tag=True,uid=''):
    # pesa larga con el nombre grabado en la barra
    mir=lambda x,w:520-(x+w)
    parts=GRAD+'<ellipse cx="260" cy="148" rx="236" ry="6" fill="#000" opacity=".16"/>'
    for (x,y,w,h,r,f) in [(8,48,24,70,9,'gy'),(34,22,32,122,12,'gy'),(68,56,12,54,4,'gm')]:
        for xx in (x,mir(x,w)): parts+=f'<rect x="{xx}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{f})"/>'
    parts+='<rect x="80" y="60" width="360" height="46" rx="23" fill="url(#gb)"/><rect x="80" y="60" width="360" height="46" rx="23" fill="none" stroke="#ffc400" stroke-opacity=".35" stroke-width="1.5"/>'
    s=1.0; total=_w(TEXTO,s); x0=(520-total)/2
    parts+=_letters(x0,71,s,5.2,'#ffc400')
    for (x,w,y,h) in [(12,4,56,54),(38,5,28,110)]:
        for xx in (x,mir(x,w)+0): parts+=f'<rect x="{xx}" y="{y}" width="{w}" height="{h}" rx="2" fill="#fff" opacity=".35"/>'
    t=''
    if tag: t='<text x="260" y="167" text-anchor="middle" font-family="Barlow,Arial,sans-serif" font-weight="600" font-size="14" letter-spacing="5.5" fill="currentColor">EQUIPOS DE GIMNASIO · CALI</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 {178 if tag else 154}" role="img" aria-label="Técnico Gym, reparación de equipos de gimnasio en Cali">{parts}{t}</svg>'
if __name__=='__main__':
    open('assets/logo-pesa.svg','w').write(logo_pesa().replace('currentColor','#5b6470'))
    open('assets/logo-pesa-blanco.svg','w').write(logo_pesa().replace('currentColor','#c5ccd5'))
    open('assets/icono.svg','w').write(ICON_SVG)
    open('assets/favicon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14161a"/><g transform="translate(5,18) scale(.3375)">'+dumbbell_icon()+'</g></svg>')
    print('ok')
