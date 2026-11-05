import sys; sys.argv=['x']
import content,content2,content3,content4,content5,content6,content7
from content import PAGES
import openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
S='https://tecnicogym.click'
rows=[('/','reparación de caminadoras Cali','técnico de caminadoras Cali · reparación de equipos de gimnasio Cali · servicio técnico gimnasio Cali','Comercial','Principal')]
for slug,p in PAGES.items():
    if slug in ('privacidad',) or p['kind']=='hub' and slug not in ('servicios','marcas','equipos-que-reparamos'): continue
    u='/'+slug+'/'
    if slug in content3.NUEVOS:
        n=[x for x in content3.M if x['slug']==slug][0]['n']; rows.append((u,f'reparación de {n} Cali',f'arreglo de {n} · técnico de {n} Cali · {n} no funciona · mantenimiento de {n}','Comercial','Equipo'))
    elif slug in content6.ZONAS_TODAS:
        z=p['h1'].split(' en ')[-1].replace(', Cali',''); rows.append((u,f'reparación de caminadoras {z}',f'técnico de caminadoras {z} Cali · reparación equipos de gimnasio {z} · técnico a domicilio {z}','Local','Zona'))
    elif slug in content5.NB:
        m=p['h1']; rows.append((u,m.lower().replace(' en cali',' Cali'),'servicio técnico '+m.split('de ')[-1].replace(' en Cali','').lower()+' Cali · reparación '+m.split(' ')[-3].lower()+' Cali','Marca','Marca'))
    elif slug in content5.NS:
        rows.append((u,p['h1'].lower().replace(' en cali',' Cali'),p['desc'][:110],'Comercial','Servicio'))
    elif p['kind']=='guia':
        rows.append((u,p['h1'].lower().rstrip('?').replace('¿',''),p['desc'][:110],'Informativa','Guía'))
    else:
        rows.append((u,p['h1'].lower(),p.get('desc',p['lead'])[:110],'Comercial / confianza','Servicio o índice'))
H=Font(bold=True,color='FFFFFF');F=PatternFill('solid',fgColor='14161A');wb=openpyxl.Workbook()
def sh(n,h,r,first=False):
    ws=wb.active if first else wb.create_sheet();ws.title=n;ws.append(h)
    for c in ws[1]:c.font=H;c.fill=F
    for x in r:ws.append(x)
    for col in ws.columns:ws.column_dimensions[col[0].column_letter].width=min(80,max(14,max(len(str(c.value or '')) for c in col)+2))
    for row in ws.iter_rows(min_row=2):
        for c in row:c.alignment=Alignment(wrap_text=True,vertical='top')
sh('Mapa de palabras clave',['Página','Palabra clave principal','Palabras secundarias','Intención','Tipo'],[[S+u,a,b,c,d] for u,a,b,c,d in rows],True)
sh('Contenido futuro',['Tema (palabra clave)','Formato'],[['reparación de caminadoras por modelo (cuando haya fotos y casos reales)','Página por modelo'],['cómo cambiar la banda: video paso a paso','Guía + video'],['casos reales: antes y después con fotos','Contenido de confianza'],['más zonas de Cali (Menga, Floralia, Vipasa y otras) con datos reales','Páginas de zona'],['más marcas: se agregan cuando el cliente las confirme','Páginas de marca'],['reseñas de clientes con su permiso','Testimonios']])
sh('Datos que faltan del cliente',['Dato','Para qué sirve'],[['Lista de las URL actuales del sitio y datos de Search Console','Para conservar el posicionamiento que ya tiene (redirecciones).'],['Código o archivo de verificación de Google Search Console','Para conectar el sitio nuevo.'],['Fotos reales de trabajos','Suben la confianza y el posicionamiento.'],['Años de experiencia','Hoy el sitio no afirma ninguna cifra.'],['Marcas que SÍ reparan','Permite más páginas por marca.'],['Garantía de la reparación','Diferenciador.'],['Horario de atención','Para el sitio y Google Business Profile.'],['Si la visita de diagnóstico tiene costo','Hoy el sitio dice que se informa antes de ir.']])
sh('Cómo validar volumen',['Paso','Detalle'],[['1','Google Ads > Herramientas > Planificador de palabras clave.'],['2','Pega las palabras principales y elige la ubicación Cali.'],['3','Prioriza volumen medio y competencia baja.'],['4','Este archivo no trae volúmenes: no tuve acceso a datos de Google.']])

CL=[('Servicio general en Cali','técnico de equipos de gimnasio Cali · reparación de equipos de gimnasio Cali · servicio técnico de equipos fitness Cali · reparación de máquinas de gimnasio Cali · mantenimiento de equipos de gimnasio Cali','/tecnico-de-equipos-de-gimnasio-cali/ · /reparacion-de-maquinas-de-gimnasio-cali/ · /reparacion-de-equipos-fitness-cali/ · /mantenimiento-equipos-gimnasio-cali/'),
('Caminadoras','reparación de caminadoras Cali · arreglo de caminadoras Cali · técnico de caminadoras Cali · reparación de trotadoras Cali · cambio de banda de caminadora Cali · mantenimiento de caminadoras Cali','/reparacion-de-caminadoras-cali/ · /arreglo-de-caminadoras-cali/ · /reparacion-de-trotadoras-cali/ · /cambio-de-banda-de-caminadora-cali/'),
('Bicicletas y elípticas','reparación de bicicletas de spinning Cali · arreglo de bicicleta estática Cali · reparación de elípticas Cali','/reparacion-bicicletas-spinning-cali/ · /reparacion-bicicleta-estatica-cali/ · /reparacion-eliptica-cali/'),
('Escaladoras y cardio especial','reparación de escaladoras Cali · reparación de stairmaster Cali · reparación de máquina de remo Cali · reparación de air bike Cali','/reparacion-de-escaladoras-stairmaster-cali/ · /reparacion-escaladora-stepper-cali/ · /reparacion-maquina-de-remo-cali/'),
('Máquinas de fuerza','reparación de multifuncional Cali · reparación de multigimnasio Cali · cambio de cables de máquinas de gimnasio · retapizado de bancos de gimnasio Cali','/reparacion-maquinas-multifuncionales-cali/ · /reparacion-de-cables-y-poleas-de-maquinas-de-gimnasio-cali/ · /retapizado-de-bancos-y-asientos-de-gimnasio-cali/'),
('Empresas y gimnasios','mantenimiento de gimnasio Cali · mantenimiento equipos de gimnasio conjuntos residenciales Cali · mantenimiento equipos crossfit Cali · gimnasio comercial','/mantenimiento-de-gimnasios-en-conjuntos-residenciales-cali/ · /mantenimiento-equipos-gimnasio-hoteles-y-empresas-cali/ · /mantenimiento-de-equipos-crossfit-y-gimnasios-funcionales-cali/ · /reparacion-de-equipos-de-gimnasio-comercial-cali/'),
('Intención local','técnico de gimnasio cerca de mí Cali · reparación a domicilio Cali · técnico de caminadoras a domicilio Cali','/tecnico-de-equipos-de-gimnasio-cerca-de-mi-cali/ · /reparacion-equipos-gimnasio-a-domicilio-cali/'),
('Barrios de Cali','reparación de caminadoras + nombre del barrio (26 barrios)','/reparacion-de-caminadoras-[barrio]-cali/'),
('Marcas','reparación equipos Ultimate Fitness Cali · Centurfit · Evolution Fitness · Sportfitness','/reparacion-equipos-[marca]-cali/'),
('Problemas (informativas)','caminadora no enciende · banda de caminadora se corre · ruido en caminadora · caminadora se apaga sola · cuánto cuesta reparar una caminadora','/caminadora-no-enciende/ y las demás guías'),
('Local y de contexto','clima de Cali y equipos de gimnasio · protección eléctrica de equipos · mover una caminadora','/clima-de-cali-y-equipos-de-gimnasio/ · /voltaje-y-proteccion-electrica-equipos-de-gimnasio/ · /como-mover-o-trasladar-una-caminadora-o-multifuncional/')]
sh('Clusters para Cali',['Grupo de búsquedas','Palabras clave (todas con Cali cuando aplica)','Páginas del sitio'],[list(x) for x in CL])
PL=[('Semana 1','Publicar el sitio (con redirecciones de las URL que ya posicionan). Enviar el sitemap en Search Console.','Que Google descubra todas las páginas'),
('Semana 1','Revisar en Search Console que las páginas se indexen y que no haya errores.','Indexación completa'),
('Semana 2','Crear el perfil de Google Business Profile (Google Maps) con el mismo nombre y teléfono del sitio.','Posicionamiento local en el mapa'),
('Semana 2','Subir fotos reales de trabajos al sitio (con texto alternativo) y a Google Business Profile.','Confianza y relevancia'),
('Semana 3','Pedir reseñas a los primeros clientes (enlace de reseña de Google).','Reseñas reales'),
('Semana 3-4','Registrar el negocio en directorios y redes con el mismo nombre, dirección de servicio y teléfono (Facebook, Instagram, WhatsApp Business, directorios de Cali).','Consistencia del nombre y teléfono'),
('Mes 2','Publicar 2 guías nuevas al mes (ver hoja Contenido futuro).','Más búsquedas cubiertas'),
('Mes 2','Revisar en Search Console qué consultas traen clics y mejorar los títulos de esas páginas.','Más clics'),
('Mes 2','Conseguir enlaces locales: gimnasios, conjuntos residenciales y proveedores de equipos que enlacen al sitio.','Autoridad local'),
('Mes 3','Agregar casos reales (antes y después) con fotos y permiso del cliente.','Contenido de confianza'),
('Mes 3','Revisar posiciones para las palabras clave de la hoja Clusters y ajustar.','Medir y corregir')]
sh('Plan 90 días',['Cuándo','Tarea','Para qué'],[list(x) for x in PL])
FU=[('Google Business Profile (lo harás tú)','Nombre exacto, teléfono, área de servicio Cali, categorías de reparación de equipos, servicios, fotos reales, publicaciones y respuesta a reseñas.'),
('Reseñas','Pide a cada cliente satisfecho una reseña en Google. Responde todas.'),
('Directorios y redes','Facebook, Instagram, WhatsApp Business y directorios locales, con el mismo nombre y teléfono.'),
('Enlaces locales','Gimnasios, administradores de conjuntos, tiendas de equipos que quieran enlazar o recomendar.'),
('Contenido con fotos y videos','Videos cortos de reparaciones y consejos; súbelos a redes y enlázalos desde el sitio.'),
('Evitar','Comprar enlaces, reseñas falsas o páginas copiadas: Google las penaliza.')]
sh('SEO local fuera del sitio',['Acción','Detalle'],[list(x) for x in FU])
ME=[('Search Console > Rendimiento','Consultas y páginas con más impresiones y clics en Cali. Revisar cada semana.'),
('Search Console > Indexación','Páginas indexadas vs. enviadas. Corregir errores.'),
('Posiciones','Anota la posición de las 15 palabras clave principales cada mes.'),
('WhatsApp','Cuántos mensajes llegan del sitio y de Google Maps cada mes.'),
('Llamadas','Llamadas desde el sitio y desde el perfil de Google.')]
sh('Medición',['Qué mirar','Detalle'],[list(x) for x in ME])

wb.save('technigin-palabras-clave.xlsx');print(len(rows))
