# -*- coding: utf-8 -*-
import re,sys
sys.path.insert(0,'.')
import src_pa
from mq_base import *
def qfix(s):
    if isinstance(s,(list,tuple)): return type(s)(qfix(x) for x in s)
    if not isinstance(s,str): return s
    R=[("En clima húmedo como el de Panamá conviene dejar la puerta entreabierta y hacer una limpieza de tina.","Si la lavandería es cerrada o con poca ventilación, conviene dejar la puerta entreabierta y hacer una limpieza de tina."),
    ("Con el calor de Panamá puede hacer falta ajustar un grado según la carga y cuántas veces abres la puerta.","Puede hacer falta ajustar un grado según la carga y cuántas veces abres la puerta."),
    ("Cada vez que abres la puerta entra aire húmedo, y en un clima como el de Panamá esa humedad se convierte en escarcha.","Cada vez que abres la puerta entra aire húmedo y esa humedad se convierte en escarcha."),
    ("Moho y mal olor en la lavadora por la humedad de Panamá","Moho y mal olor en la lavadora: cómo evitarlo"),
    ("El clima húmedo favorece el moho en la tina y el empaque.","La humedad que queda dentro favorece el moho en la tina y el empaque."),
    ("importante en Panamá por la humedad","importante para evitar olores"),
    ("Ciudad de Panamá","El Salvador"),("en Panamá","en El Salvador"),("Panamá","El Salvador"),("-panama","-el-salvador"),
    ("Ajusta las patas","Ajusta las patas")]
    for a,b in R: s=s.replace(a,b)
    return s
def deep(x):
    if isinstance(x,dict): return {k:deep(v) for k,v in x.items()}
    if isinstance(x,list): return [deep(v) for v in x]
    if isinstance(x,tuple): return tuple(deep(v) for v in x)
    return qfix(x)
SRC=deep(src_pa.EQUIPOS); BLOG_SRC=deep(src_pa.BLOG)
GARANTIA_FAQ=("¿Dan garantía por la reparación?","Pregunta por la garantía al coordinar la visita: te confirmamos por WhatsApp las condiciones de la reparación antes de empezar.")
def fixfaq(f):
    out=[]
    for q,a in f:
        if 'garant' in q.lower(): out.append(GARANTIA_FAQ)
        else: out.append((q,a))
    return out
EQ={}
def add(k,**d): EQ[k]=d
# ---------- reutilizados (neveras, lavadoras, secadoras) ----------
s=SRC['neveras']
add('refrigeradoras',nombre='Refrigeradoras',corto='Refrigeradoras',sing='refrigeradora',art='la refrigeradora',h1='Reparación de refrigeradoras Samsung en El Salvador',slug='reparacion-de-refrigeradoras-samsung-el-salvador',icon='fridge',foto=['nevera-family-hub','nevera-superior-inox'],th='nevera-superior-inox',
 intro='Reparamos refrigeradoras (neveras) Samsung a domicilio en El Salvador: de congelador superior, Side by Side, French Door y modelos con dispensador de agua y hielo. No enfrían, hacen ruido, gotean, acumulan escarcha o se apagan solas.',
 modelos=s['modelos'],fallas=s['fallas'],mant=s['mant'],faq=fixfaq(s['faq']),
 slugs=['refrigeradora-samsung-no-enfria-el-salvador','refrigeradora-samsung-escarcha-en-el-congelador-el-salvador','refrigeradora-samsung-gotea-agua-por-dentro-el-salvador','refrigeradora-samsung-hace-ruido-el-salvador','dispensador-de-agua-de-refrigeradora-samsung-no-funciona-el-salvador','refrigeradora-samsung-no-hace-hielo-el-salvador','refrigeradora-samsung-alarma-o-luz-de-filtro-el-salvador','refrigeradora-samsung-se-apaga-sola-el-salvador','refrigeradora-samsung-huele-mal-el-salvador','refrigeradora-samsung-family-hub-pantalla-no-funciona-el-salvador','refrigeradora-samsung-digital-inverter-ruido-el-salvador'],
 seguridad='Desconecta la refrigeradora antes de mover, limpiar o intentar abrir cualquier panel trasero. Si huele a quemado, desenchúfala y no la vuelvas a conectar.',
 datos='marca y modelo (la etiqueta suele estar dentro, en el costado o en el techo del compartimento), cuánto tiempo lleva con la falla y si el congelador enfría o no',
 pais='El Salvador tiene cortes y bajones de voltaje ocasionales; un protector de voltaje con retardo ayuda a cuidar el compresor y la tarjeta electrónica.')
s=SRC['lavadoras']
add('lavadoras',nombre='Lavadoras',corto='Lavadoras',sing='lavadora',art='la lavadora',h1='Reparación de lavadoras Samsung en El Salvador',slug='reparacion-de-lavadoras-samsung-el-salvador',icon='washer',foto=['lavadora-superior','torre-lavado'],th='lavadora-superior',
 intro='Reparamos lavadoras Samsung de carga superior y de carga frontal a domicilio en El Salvador: no centrifugan, no desaguan, hacen ruido, gotean, no llenan o muestran códigos de error.',
 modelos=s['modelos'],fallas=s['fallas'],mant=s['mant'],faq=fixfaq(s['faq']),
 slugs=['lavadora-samsung-no-centrifuga-el-salvador','lavadora-samsung-no-desagua-el-salvador','lavadora-samsung-no-llena-de-agua-el-salvador','lavadora-samsung-gotea-o-bota-agua-el-salvador','lavadora-samsung-puerta-no-abre-o-no-cierra-el-salvador','lavadora-samsung-codigo-ue-vibra-mucho-el-salvador','lavadora-samsung-huele-mal-o-tiene-moho-el-salvador','lavadora-samsung-no-enciende-el-salvador','lavadora-samsung-deja-pelusas-en-la-ropa-el-salvador','lavadora-samsung-codigo-5e-o-se-no-desagua-el-salvador','lavadora-samsung-codigo-4e-no-entra-agua-el-salvador','lavadora-samsung-addwash-gotea-el-salvador','lavadora-samsung-no-conecta-a-smartthings-el-salvador'],
 seguridad='Cierra la llave de agua y desconecta la lavadora antes de revisar mangueras o filtros. Ten toallas a mano: al abrir el filtro de desagüe sale agua.',
 datos='marca y modelo (la etiqueta suele estar en la parte trasera o en el borde de la tapa o la puerta), si es de carga superior o frontal y el código de error que muestra la pantalla',
 pais='En El Salvador muchas lavanderías están en terrazas o patios con lluvia; revisa que el tomacorriente esté protegido y que las mangueras no queden al sol ni a la intemperie.')
s=SRC['secadoras']
add('secadoras',nombre='Secadoras',corto='Secadoras',sing='secadora',art='la secadora',h1='Reparación de secadoras Samsung en El Salvador',slug='reparacion-de-secadoras-samsung-el-salvador',icon='dryer',foto=['secadora','secadora-torre'],th='secadora',
 intro='Reparamos secadoras Samsung eléctricas a domicilio en El Salvador: no secan, no calientan, hacen ruido, tardan mucho o se detienen a mitad del ciclo.',
 modelos=[m for m in s['modelos'] if 'bomba' not in m.lower() and 'a gas' not in m.lower()],fallas=s['fallas'],mant=s['mant'],faq=fixfaq(s['faq']),
 slugs=['secadora-samsung-no-seca-la-ropa-el-salvador','secadora-samsung-no-calienta-el-salvador','secadora-samsung-tarda-demasiado-en-secar-el-salvador','secadora-samsung-hace-ruido-el-salvador','secadora-samsung-se-detiene-a-mitad-del-ciclo-el-salvador','secadora-samsung-no-enciende-el-salvador','secadora-samsung-deja-olor-o-pelusa-el-salvador','secadora-samsung-puerta-no-cierra-el-salvador','secadora-samsung-ciclo-largo-ducto-o-filtro-saturado-el-salvador'],
 seguridad='La pelusa acumulada es combustible: limpia el filtro en cada ciclo. Si hay olor a quemado o la secadora se sobrecalienta, desconéctala y no la uses.',
 datos='marca y modelo (etiqueta dentro de la puerta o atrás), y si gira pero no calienta o no gira',
 pais='Muchas secadoras eléctricas usan 240 V y breaker propio; en edificios de El Salvador confirma que la toma y el breaker sean los indicados antes de culpar al equipo.')

# ---------- fallas adicionales (más búsquedas de síntoma) ----------
def _more(k,items):
    if k not in EQ: return
    for (n,c,u,tip,slug) in items:
        EQ[k]['fallas'].append((n,c,u,tip)); EQ[k]['slugs'].append(slug)
b_="samsung"
_more('refrigeradoras',[
 ('El congelador no congela','Ventilador o evaporador con escarcha, sensor de temperatura, tarjeta de control o compresor.','Urgente','Revisa que la temperatura esté bien configurada y que las puertas cierren; si los alimentos se descongelan, escríbenos de inmediato.',f'refrigeradora-{b_}-congelador-no-congela-el-salvador'),
 ('La puerta no cierra bien o el empaque no sella','Empaque (goma) deformado o sucio, bisagras flojas, refrigeradora mal nivelada o cajones mal puestos.','Vigilar','Limpia el empaque con agua tibia y prueba con una hoja de papel: si sale sin resistencia, no está sellando.',f'refrigeradora-{b_}-puerta-no-cierra-el-salvador'),
 ('La luz interior no enciende','Foco o LED quemado, interruptor de la puerta o conexión suelta.','Vigilar','Si el resto funciona con normalidad, no es urgente; pide que lo revisen en la próxima visita.',f'refrigeradora-{b_}-luz-interior-no-enciende-el-salvador'),
 ('El agua o el hielo salen con mal sabor u olor','Filtro de agua vencido, agua estancada en la manguera o depósito de hielo sucio.','Vigilar','Cambia el filtro cada 6 meses y desecha los primeros litros y el hielo después del cambio.',f'refrigeradora-{b_}-agua-con-mal-sabor-el-salvador'),
 ('El compresor no arranca o se calienta mucho','Relé de arranque, protector térmico, tarjeta de control, voltaje bajo o compresor con falla.','Urgente','Desconéctala unos 10 minutos y no la prendas repetidamente: puedes dañar el compresor.',f'refrigeradora-{b_}-compresor-no-arranca-el-salvador')])
_more('lavadoras',[
 ('El tambor no gira','Correa suelta o rota (carga superior), motor, acople, tarjeta de control o carga excesiva.','Revisar pronto','Reduce la carga y prueba otro ciclo; si el motor zumba pero el tambor no gira, no insistas.',f'lavadora-{b_}-tambor-no-gira-el-salvador'),
 ('No agita la ropa','Acople del agitador, transmisión, motor o seguro de la tapa.','Revisar pronto','Verifica que la tapa cierre bien y que el agitador no esté suelto antes de escribirnos.',f'lavadora-{b_}-no-agita-el-salvador'),
 ('Se detiene a mitad del ciclo','Carga desbalanceada, nivel de agua que no se detecta, seguro de puerta, tarjeta de control o variaciones de voltaje.','Revisar pronto','Redistribuye la ropa, revisa que las llaves de agua estén abiertas y anota el código de error si aparece.',f'lavadora-{b_}-se-detiene-a-mitad-del-ciclo-el-salvador'),
 ('Hace ruido fuerte al centrifugar','Amortiguadores o rodamientos desgastados, objetos atrapados, patas sin nivelar o carga desbalanceada.','Revisar pronto','Un golpeteo o chillido constante merece revisión antes de que dañe la tina.',f'lavadora-{b_}-ruido-al-centrifugar-el-salvador'),
 ('No dispensa el suavizante o el detergente','Dispensador tapado por residuos, válvula de entrada de agua o baja presión de agua.','Vigilar','Retira y lava el cajón del dispensador con agua tibia; revisa la presión de agua de la llave.',f'lavadora-{b_}-no-dispensa-suavizante-el-salvador')])
_more('secadoras',[
 ('El tambor no gira','Correa rota, polea tensora, motor o rodillos desgastados.','Revisar pronto','Si escuchas el motor pero el tambor no gira, desconéctala y no la fuerces.',f'secadora-{b_}-tambor-no-gira-el-salvador'),
 ('Se sobrecalienta o huele a quemado','Ducto o filtro obstruido, termostato o resistencia con falla, exceso de pelusa acumulada.','Urgente','Desconéctala, no la uses y revisa filtro y ducto; si el olor continúa, escríbenos.',f'secadora-{b_}-se-sobrecalienta-el-salvador'),
 ('Salta el breaker al encender','Resistencia a tierra, breaker inadecuado para 240 V, cable o tomacorriente dañado, o motor con falla.','Urgente','No subas el breaker por tu cuenta: puede ser un riesgo eléctrico. Desconéctala y pide revisión.',f'secadora-{b_}-salta-el-breaker-el-salvador')])
