# -*- coding: utf-8 -*-
# slug, nombre, sector, tipo, referencias
Z=[
# --- Gran San Salvador
('san-salvador-centro','San Salvador Centro','Norte','mixto',['Centro Histórico de San Salvador','Plaza Libertad','Alameda Juan Pablo II','Alameda Roosevelt']),
('colonia-escalon','Colonia Escalón','Norte','edificios',['Colonia Escalón','Paseo General Escalón','Plaza Beethoven','Torres de Escalón']),
('san-benito','San Benito','Norte','edificios',['Colonia San Benito','Zona Rosa','Boulevard del Hipódromo']),
('colonia-flor-blanca','Colonia Flor Blanca','Norte','mixto',['Colonia Flor Blanca','Estadio Cuscatlán','Boulevard de los Héroes']),
('colonia-medica','Colonia Médica','Norte','mixto',['Colonia Médica','Alameda Dr. Manuel Enrique Araujo','Hospital de la Mujer']),
('colonia-miramonte','Colonia Miramonte','Norte','casas',['Colonia Miramonte','Boulevard Universitario']),
('colonia-layco','Colonia Layco','Norte','mixto',['Colonia Layco','Calle Arce','Avenida Bernal']),
('colonia-centroamerica','Colonia Centroamérica','Norte','mixto',['Colonia Centroamérica','Boulevard de los Héroes']),
('colonia-san-francisco','Colonia San Francisco','Norte','casas',['Colonia San Francisco','Boulevard Constitución']),
('colonia-zacamil','Colonia Zacamil','Norte','casas',['Colonia Zacamil','Mejicanos']),
('colonia-metropolis','Colonia Metrópolis','Norte','casas',['Colonia Metrópolis','Mejicanos']),
('mejicanos','Mejicanos','Norte','mixto',['Mejicanos','Avenida Dolores Bernal','Zacamil']),
('soyapango','Soyapango','Norte','mixto',['Soyapango','Boulevard del Ejército Nacional','Plaza Mundo']),
('ilopango','Ilopango','Norte','casas',['Ilopango','Boulevard del Ejército Nacional','Aeropuerto de Ilopango']),
('san-marcos','San Marcos','Norte','casas',['San Marcos','Carretera Panamericana']),
('ciudad-delgado','Ciudad Delgado','Norte','mixto',['Ciudad Delgado','Carretera Troncal del Norte']),
('cuscatancingo','Cuscatancingo','Norte','casas',['Cuscatancingo','Carretera Troncal del Norte']),
('ayutuxtepeque','Ayutuxtepeque','Norte','casas',['Ayutuxtepeque','Carretera Troncal del Norte']),
('apopa','Apopa','Norte','mixto',['Apopa','Carretera Troncal del Norte','Plaza Apopa']),
('tonacatepeque','Tonacatepeque','Norte','valle',['Tonacatepeque','Carretera a Tonacatepeque']),
('nejapa','Nejapa','Norte','valle',['Nejapa','Carretera a Quezaltepeque']),
('san-martin','San Martín','Norte','mixto',['San Martín','Carretera a San Martín']),
('colonia-atlacatl','Colonia Atlacatl','Norte','casas',['Colonia Atlacatl','Boulevard Venezuela']),
('colonia-costa-rica','Colonia Costa Rica','Norte','casas',['Colonia Costa Rica','Boulevard Venezuela']),
# --- La Libertad
('santa-tecla','Santa Tecla','Centro','mixto',['Santa Tecla','Parque Daniel Hernández','Boulevard Monseñor Romero']),
('antiguo-cuscatlan','Antiguo Cuscatlán','Centro','edificios',['Antiguo Cuscatlán','Multiplaza','La Gran Vía','Boulevard Orden de Malta']),
('ciudad-merliot','Ciudad Merliot','Centro','mixto',['Ciudad Merliot','Plaza Merliot','Boulevard Merliot']),
('nuevo-cuscatlan','Nuevo Cuscatlán','Centro','casas',['Nuevo Cuscatlán','Carretera Panamericana']),
('lourdes-colon','Lourdes Colón','Centro','mixto',['Lourdes Colón','Carretera a Santa Ana']),
('colon','Colón','Centro','mixto',['Colón','Carretera a Santa Ana']),
('ciudad-arce','Ciudad Arce','Centro','mixto',['Ciudad Arce','Carretera a Santa Ana']),
('san-juan-opico','San Juan Opico','Centro','mixto',['San Juan Opico','Carretera a Santa Ana']),
('quezaltepeque','Quezaltepeque','Centro','mixto',['Quezaltepeque','Carretera a Quezaltepeque']),
('zaragoza','Zaragoza','Centro','casas',['Zaragoza','Carretera al Puerto de La Libertad']),
('puerto-de-la-libertad','Puerto de La Libertad','Centro','casas',['Puerto de La Libertad','Carretera al Puerto de La Libertad','Playa El Tunco (cercana)']),
('huizucar','Huizúcar','Centro','valle',['Huizúcar','Carretera a Huizúcar']),
('comasagua','Comasagua','Centro','valle',['Comasagua','Carretera a Comasagua']),
('jayaque','Jayaque','Centro','valle',['Jayaque','Carretera a Sonsonate']),
('san-jose-villanueva','San José Villanueva','Centro','valle',['San José Villanueva']),
# --- Occidente
('santa-ana','Santa Ana','Sur','mixto',['Santa Ana','Parque Libertad','Metrocentro Santa Ana']),
('chalchuapa','Chalchuapa','Sur','mixto',['Chalchuapa','Carretera a Ahuachapán']),
('coatepeque','Coatepeque','Sur','valle',['Coatepeque','Lago de Coatepeque']),
('el-congo','El Congo','Sur','valle',['El Congo','Carretera a Santa Ana']),
('metapan','Metapán','Sur','mixto',['Metapán','Carretera a Metapán']),
('san-sebastian-salitrillo','San Sebastián Salitrillo','Sur','valle',['San Sebastián Salitrillo','Santa Ana']),
('sonsonate','Sonsonate','Sur','mixto',['Sonsonate','Parque Central de Sonsonate']),
('izalco','Izalco','Sur','mixto',['Izalco','Carretera a Sonsonate']),
('nahuizalco','Nahuizalco','Sur','valle',['Nahuizalco','Ruta de las Flores']),
('acajutla','Acajutla','Sur','casas',['Acajutla','Puerto de Acajutla']),
('armenia','Armenia','Sur','mixto',['Armenia','Carretera a Sonsonate']),
('juayua','Juayúa','Sur','valle',['Juayúa','Ruta de las Flores']),
('ahuachapan','Ahuachapán','Sur','mixto',['Ahuachapán','Parque Menéndez']),
('atiquizaya','Atiquizaya','Sur','mixto',['Atiquizaya','Carretera a Ahuachapán']),
# --- Oriente y paracentral
('san-miguel','San Miguel','Valles','mixto',['San Miguel','Parque Guzmán','Metrocentro San Miguel']),
('usulutan','Usulután','Valles','mixto',['Usulután','Parque Central de Usulután']),
('santiago-de-maria','Santiago de María','Valles','valle',['Santiago de María']),
('la-union','La Unión','Valles','mixto',['La Unión','Puerto de La Unión']),
('santa-rosa-de-lima','Santa Rosa de Lima','Valles','mixto',['Santa Rosa de Lima','Carretera Panamericana']),
('san-francisco-gotera','San Francisco Gotera','Valles','mixto',['San Francisco Gotera']),
('san-vicente','San Vicente','Valles','mixto',['San Vicente','Carretera Panamericana']),
('cojutepeque','Cojutepeque','Valles','mixto',['Cojutepeque','Carretera Panamericana']),
('ilobasco','Ilobasco','Valles','mixto',['Ilobasco','Carretera a Ilobasco']),
('zacatecoluca','Zacatecoluca','Valles','mixto',['Zacatecoluca','Carretera Litoral']),
('sensuntepeque','Sensuntepeque','Valles','mixto',['Sensuntepeque']),
('chalatenango','Chalatenango','Valles','mixto',['Chalatenango','Carretera Troncal del Norte']),
('jiquilisco','Jiquilisco','Valles','valle',['Jiquilisco','Carretera Litoral']),
('san-rafael-oriente','San Rafael Oriente','Valles','valle',['San Rafael Oriente','Carretera Panamericana']),
]
ZD={z[0]:dict(slug=z[0],nombre=z[1],sector=z[2],tipo=z[3],refs=z[4]) for z in Z}
ZSLUGS=[z[0] for z in Z]
# zonas con página por electrodoméstico
import os
ZXA=list(ZSLUGS) if os.environ.get('MQ_LITE')!='1' else ['colonia-escalon','santa-tecla','soyapango','santa-ana','san-miguel','sonsonate']
AXZ=['refrigeradoras','neveras','lavadoras','secadoras']
TIPO_TXT={
 'edificios':'En esta zona hay muchos edificios de apartamentos y oficinas. Coordinamos el acceso y el horario con la administración para que la visita no se complique.',
 'casas':'Predominan casas y conjuntos pequeños. Confirmamos la dirección exacta y la referencia por WhatsApp antes de ir.',
 'mixto':'Es una zona mixta, con casas, edificios y comercios. Te pedimos la dirección y alguna referencia para llegar sin demoras.',
 'valle':'Es una zona de urbanizaciones y conjuntos, algo más alejada del centro. Te confirmamos la disponibilidad de visita al coordinar por WhatsApp.'}
SECTOR_TXT={'Norte':'el Gran San Salvador','Centro':'La Libertad','Sur':'el occidente de El Salvador','Valles':'el oriente y la zona paracentral'}
