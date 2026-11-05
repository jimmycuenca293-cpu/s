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
    ("Ciudad de Panamá","Quito"),("en Panamá","en Quito"),("Panamá","Quito"),("-panama","-quito"),
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
add('refrigeradoras',nombre='Refrigeradoras',corto='Refrigeradoras',sing='refrigeradora',art='la refrigeradora',h1='Reparación de refrigeradoras Mabe en Quito',slug='reparacion-de-refrigeradoras-mabe-quito',icon='fridge',foto=['nevera-superior-inox','nevera-side-by-side','nevera-superior-negra'],th='nevera-superior-inox',
 intro='Reparamos refrigeradoras (neveras) Mabe a domicilio en Quito: de congelador superior, Side by Side, French Door y modelos con dispensador de agua y hielo. No enfrían, hacen ruido, gotean, acumulan escarcha o se apagan solas.',
 modelos=s['modelos'],fallas=s['fallas'],mant=s['mant'],faq=fixfaq(s['faq']),
 slugs=['refrigeradora-mabe-no-enfria-quito','refrigeradora-mabe-escarcha-en-el-congelador-quito','refrigeradora-mabe-gotea-agua-por-dentro-quito','refrigeradora-mabe-hace-ruido-quito','dispensador-de-agua-de-refrigeradora-mabe-no-funciona-quito','refrigeradora-mabe-no-hace-hielo-quito','refrigeradora-mabe-alarma-o-luz-de-filtro-quito','refrigeradora-mabe-se-apaga-sola-quito','refrigeradora-mabe-huele-mal-quito'],
 seguridad='Desconecta la refrigeradora antes de mover, limpiar o intentar abrir cualquier panel trasero. Si huele a quemado, desenchúfala y no la vuelvas a conectar.',
 datos='marca y modelo (la etiqueta suele estar dentro, en el costado o en el techo del compartimento), cuánto tiempo lleva con la falla y si el congelador enfría o no',
 quito='Quito tiene cortes y bajones de voltaje ocasionales; un protector de voltaje con retardo ayuda a cuidar el compresor y la tarjeta electrónica.')
s=SRC['lavadoras']
add('lavadoras',nombre='Lavadoras',corto='Lavadoras',sing='lavadora',art='la lavadora',h1='Reparación de lavadoras Mabe en Quito',slug='reparacion-de-lavadoras-mabe-quito',icon='washer',foto=['lavadora-superior','torre-lavado'],th='lavadora-superior',
 intro='Reparamos lavadoras Mabe de carga superior y de carga frontal a domicilio en Quito: no centrifugan, no desaguan, hacen ruido, gotean, no llenan o muestran códigos de error.',
 modelos=s['modelos'],fallas=s['fallas'],mant=s['mant'],faq=fixfaq(s['faq']),
 slugs=['lavadora-mabe-no-centrifuga-quito','lavadora-mabe-no-desagua-quito','lavadora-mabe-no-llena-de-agua-quito','lavadora-mabe-gotea-o-bota-agua-quito','lavadora-mabe-puerta-no-abre-o-no-cierra-quito','lavadora-mabe-vibra-mucho-quito','lavadora-mabe-huele-mal-o-tiene-moho-quito','lavadora-mabe-no-enciende-quito','lavadora-mabe-deja-pelusas-en-la-ropa-quito'],
 seguridad='Cierra la llave de agua y desconecta la lavadora antes de revisar mangueras o filtros. Ten toallas a mano: al abrir el filtro de desagüe sale agua.',
 datos='marca y modelo (la etiqueta suele estar en la parte trasera o en el borde de la tapa o la puerta), si es de carga superior o frontal y el código de error que muestra la pantalla',
 quito='En Quito muchas lavanderías están en terrazas o patios con lluvia; revisa que el tomacorriente esté protegido y que las mangueras no queden al sol ni a la intemperie.')
s=SRC['secadoras']
add('secadoras',nombre='Secadoras',corto='Secadoras',sing='secadora',art='la secadora',h1='Reparación de secadoras Mabe en Quito',slug='reparacion-de-secadoras-mabe-quito',icon='dryer',foto=['secadora','secadora-oscura'],th='secadora',
 intro='Reparamos secadoras Mabe eléctricas y a gas a domicilio en Quito: no secan, no calientan, hacen ruido, tardan mucho o se detienen a mitad del ciclo.',
 modelos=[m for m in s['modelos'] if 'bomba' not in m.lower()],fallas=s['fallas'],mant=s['mant'],faq=fixfaq(s['faq']),
 slugs=['secadora-mabe-no-seca-la-ropa-quito','secadora-mabe-no-calienta-quito','secadora-mabe-tarda-demasiado-en-secar-quito','secadora-mabe-hace-ruido-quito','secadora-mabe-se-detiene-a-mitad-del-ciclo-quito','secadora-mabe-no-enciende-quito','secadora-mabe-deja-olor-o-pelusa-quito','secadora-mabe-puerta-no-cierra-quito'],
 seguridad='La pelusa acumulada es combustible: limpia el filtro en cada ciclo. Si hay olor a quemado o la secadora se sobrecalienta, desconéctala y no la uses.',
 datos='si es eléctrica o a gas, marca y modelo (etiqueta dentro de la puerta o atrás), y si gira pero no calienta o no gira',
 quito='Muchas secadoras eléctricas usan 220 V y breaker propio; en edificios de Quito confirma que la toma y el breaker sean los indicados antes de culpar al equipo. Si es a gas, el suministro puede ser de cilindro o gas centralizado.')
