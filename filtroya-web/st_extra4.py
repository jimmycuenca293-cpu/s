# Contenido esencial adicional en cada página: qué incluye la visita, cómo prepararse, señales de alerta y seguridad (se inserta antes de las preguntas frecuentes).
VISITA_E = {
    "nevera": ["Revisión de la temperatura del refrigerador y del congelador.", "Inspección de los sellos de las puertas.", "Limpieza de la zona del condensador si hace falta.", "Revisión del ventilador y del sistema de deshielo.", "Prueba del compresor y del arranque.", "Explicación de la falla y del valor antes de reparar."],
    "lava": ["Prueba de llenado, lavado, desagüe y centrifugado.", "Revisión del filtro de la bomba y de las mangueras.", "Revisión del sello y del seguro de la puerta.", "Verificación de la nivelación y de los amortiguadores.", "Lectura del código de error en el panel.", "Explicación de la falla y del valor antes de reparar."],
    "seca": ["Revisión del filtro de pelusa y del ducto.", "Prueba de calentamiento y de giro del tambor.", "Revisión de sensores y termostatos.", "Verificación del circuito eléctrico y del enchufe.", "Prueba de un ciclo completo.", "Explicación de la falla y del valor antes de reparar."],
    "lavaplatos": ["Revisión del filtro y de los brazos rociadores.", "Prueba de llenado y de desagüe.", "Revisión del sello de la puerta.", "Verificación de la toma de agua y del desagüe.", "Prueba de un ciclo de lavado.", "Explicación de la falla y del valor antes de reparar."],
    "cocina": ["Revisión de los quemadores y del encendido.", "Prueba de las conexiones de gas con el equipo apagado.", "Revisión de la resistencia y del termostato del horno.", "Verificación del sello de la puerta del horno.", "Prueba de calentamiento.", "Explicación de la falla y del valor antes de reparar."],
    "micro": ["Prueba de calentamiento con un vaso de agua.", "Revisión del seguro y del cierre de la puerta.", "Inspección del plato giratorio y del motor.", "Revisión del panel y de la tarjeta.", "Prueba de fusibles y componentes de seguridad.", "Explicación de la falla y del valor antes de reparar."],
    "tv": ["Diagnóstico de imagen, sonido y encendido.", "Revisión de la fuente de poder y de las entradas.", "Prueba con otra toma y otro cable.", "Revisión de la retroiluminación.", "Verificación de la señal y de la conexión.", "Explicación de la falla y del valor antes de reparar."],
}
PREPARA = {
    "nevera": ["Ten a mano el modelo (etiqueta interior) y cuéntale al técnico desde cuándo falla.", "Si puedes, pasa los alimentos delicados a una nevera de apoyo.", "Deja libre el espacio alrededor del equipo.", "Evita desconectarla horas antes: así el técnico ve la falla real."],
    "lava": ["Vacía el tambor y revisa los bolsillos de la ropa.", "Ten a mano el modelo y el código que muestra el panel.", "Deja libre el acceso a las llaves de agua y al desagüe.", "Toma una foto del código de error."],
    "seca": ["Vacía el tambor y limpia el filtro de pelusa.", "Ten a mano el modelo y el tipo de conexión eléctrica.", "Deja libre el acceso al ducto y a la toma.", "Cuéntale al técnico si tarda más de lo normal en secar."],
    "lavaplatos": ["Vacía el equipo y retira los platos.", "Ten a mano el modelo y la marca del detergente que usas.", "Deja libre el acceso a la llave de agua y al desagüe.", "Cuéntale al técnico qué falla hace el equipo."],
    "cocina": ["Despeja la cocina y deja el equipo frío.", "Ten a mano el modelo y el tipo de gas o conexión.", "Si hay olor a gas, cierra la llave y ventila antes de la visita.", "Cuéntale al técnico qué quemador u horno falla."],
    "micro": ["Retira cualquier recipiente del interior.", "Ten a mano el modelo (etiqueta).", "Deja libre la toma de corriente.", "Cuéntale al técnico si hay chispas, olor o ruido."],
    "tv": ["Ten a mano el modelo y la señal que usas (cable, antena, internet).", "Cuéntale al técnico qué ves o no ves en pantalla.", "Deja libre el acceso al televisor y a las conexiones.", "Anota si hubo un corte de luz antes de la falla."],
}
SEGURIDAD = {
    "nevera": ["Desconéctala si huele a quemado o el compresor hace ruidos fuertes.", "No uses extensiones delgadas: calientan el cable.", "Si hay agua en el piso, desconecta antes de secar."],
    "lava": ["Cierra la llave de agua y desconecta si hay fuga.", "No metas la mano en el tambor mientras gira.", "Si salta el breaker al arrancar, no insistas."],
    "seca": ["Desconéctala si huele a quemado.", "Limpia la pelusa: acumulada es riesgo de incendio.", "No uses la secadora con el ducto obstruido."],
    "lavaplatos": ["Cierra la llave de agua si hay fuga.", "Desconecta antes de revisar el fondo.", "Si salta el breaker, no insistas."],
    "cocina": ["Si hay olor a gas, cierra la llave, ventila y no enciendas nada.", "No uses el horno si la puerta no sella.", "Deja enfriar antes de limpiar."],
    "micro": ["No lo abras: tiene alto voltaje aun desconectado.", "Si hay chispas, desconéctalo de inmediato.", "No lo uses vacío."],
    "tv": ["Desconéctalo si huele a quemado.", "No abras el televisor: tiene alto voltaje.", "Usa protector de voltaje en tormentas."],
}
ALERTA = ["El equipo hace un ruido nuevo que antes no hacía.", "Aparece un código de error que se repite.", "Consume más energía o el recibo de luz subió.", "Hay agua, olor a quemado o calor excesivo.", "El rendimiento bajó: tarda más, enfría menos o lava peor.", "Salta el breaker o el protector de voltaje."]


def _ul2(l):
    return '<ul class="spec-list">' + "".join(f"<li>{esc(x)}</li>" for x in l) + "</ul>"


for _c in CIU:
    _pk = _c["pk"]; _P = PAISES[_pk]; _nom = _c["n"]
    for _sv in SERV_PAIS[_pk]:
        _s1, _s2 = pal(_pk, _sv); _key = f"e4|{_c['s']}|{_sv}"
        _bq = (seccion(f"Qué incluye la visita a domicilio para tu {esc(_s1)} Samsung en {esc(_nom)}", _ul2(mix(_key + "|v", VISITA_E[_sv], 5)) + f"<p>{esc(uno(_key + '|n', ['Si el equipo no tiene arreglo práctico, el técnico te lo dice con honestidad.', 'Tú decides si se repara después de conocer el valor.', 'La visita sirve para saber qué falla y cuánto costaría repararlo.']))}</p>")
                  + seccion(f"Prepara tu {esc(_s1)} antes de la visita", _ul2(mix(_key + "|p", PREPARA[_sv], 4)), alt=True)
                  + seccion(f"Seguridad con tu {esc(_s1)} mientras llega el técnico", _ul2(SEGURIDAD[_sv]))
                  + seccion(f"Señales de que tu {esc(_s1)} necesita revisión en {esc(_nom)}", _ul2(mix(_key + "|a", ALERTA, 4)), alt=True))
        _ins(R_CS(_c, _sv), _bq)
for _pk, _P in PAISES.items():
    for _sv in SERV_PAIS[_pk]:
        _s1, _s2 = pal(_pk, _sv); _key = f"e4h|{_pk}|{_sv}"
        _ins(R_SERV(_pk, _sv), seccion(f"Qué incluye la visita para tu {esc(_s1)} Samsung en {esc(_P['nombre'])}", _ul2(VISITA_E[_sv][:5])) + seccion(f"Seguridad con tu {esc(_s1)}", _ul2(SEGURIDAD[_sv]), alt=True))
for _c, _pr in PROB_P:
    _sv = _pr["sv"]; _s1 = pal(_c["pk"], _sv)[0]
    _ins(R_PROB(_c, _pr), seccion(f"Seguridad con tu {esc(_s1)} mientras la revisamos", _ul2(SEGURIDAD[_sv]), alt=True))
