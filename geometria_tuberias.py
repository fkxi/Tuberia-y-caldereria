import math
import numpy as np

def calcular_flecha(radio, cuerda):
    if cuerda > 2 * radio:
        return None, "Error: La cuerda no puede ser mayor que el diámetro."
    mitad_cuerda = cuerda / 2
    apotema = math.sqrt(radio**2 - mitad_cuerda**2)
    flecha = radio - apotema
    return flecha, apotema

def calcular_cuerda(radio, angulo_grados):
    radianes = math.radians(angulo_grados)
    cuerda = 2 * radio * math.sin(radianes / 2)
    return cuerda, radianes

def calcular_radio_por_flecha(cuerda, flecha):
    radio = (flecha / 2) + ((cuerda**2) / (8 * flecha))
    apotema = radio - flecha
    return radio, apotema

def calcular_generatrices_tuberia(diametro, cuerda, separacion):
    if cuerda > diametro:
        return None, None, None, None, "Error: La cuerda no puede ser mayor al diámetro."
    
    radio = diametro / 2.0
    mitad_cuerda = cuerda / 2.0
    apotema = math.sqrt(radio**2 - mitad_cuerda**2)
    flecha = radio - apotema
    
    posiciones_x = np.arange(0, mitad_cuerda + separacion, separacion)
    posiciones_x = posiciones_x[posiciones_x <= mitad_cuerda]
    if len(posiciones_x) == 0 or posiciones_x[-1] < mitad_cuerda - 1e-5:
        posiciones_x = np.append(posiciones_x, mitad_cuerda)
    
    alturas_h = np.sqrt(radio**2 - posiciones_x**2) - apotema
    return posiciones_x.tolist(), alturas_h.tolist(), flecha, apotema, None

def calcular_boca_pescado(
    d_cabezal: float,
    d_ramal: float,
    divisiones: int = 24,
    angulo_injerto: float = 90.0,
    espesor_ramal: float = 0.0,
    tipo_asiento: str = "interior"
):
    """
    Calcula la plantilla plana para corte de boca de pescado (injerto cilíndrico)
    considerando el espesor de pared del ramal para evitar filos de cuchillo (espesor cero).

    Parámetros:
    - d_cabezal: Diámetro exterior del tubo cabezal/colector (mm).
    - d_ramal: Diámetro exterior del tubo ramal (mm).
    - divisiones: Cantidad de generatrices (par, ej. 16, 24, 32).
    - angulo_injerto: Ángulo de intersección en grados (1° a 90°).
    - espesor_ramal: Espesor de pared del tubo ramal (mm). Si es 0.0, calcula el caso ideal.
    - tipo_asiento: 'interior' (asiento real de taller), 'exterior' o 'ambos'.
    """
    if d_ramal > d_cabezal:
        return None, "Error: El diámetro del ramal no puede ser mayor que el diámetro del cabezal principal."
    if espesor_ramal < 0:
        return None, "Error: El espesor del ramal no puede ser negativo."
    if angulo_injerto <= 0 or angulo_injerto > 90:
        return None, "Error: El ángulo de injerto debe estar entre 1° y 90°."
    if divisiones <= 0 or divisiones % 2 != 0:
        return None, "Error: La cantidad de divisiones debe ser un número par positivo."

    r_ext_cabezal = d_cabezal / 2.0
    r_ext_ramal = d_ramal / 2.0

    if espesor_ramal == 0.0:
        r_int_ramal = r_ext_ramal
    else:
        if espesor_ramal >= r_ext_ramal:
            return None, "Error: El espesor no puede ser mayor o igual al radio del ramal."
        r_int_ramal = r_ext_ramal - espesor_ramal

    phi_rad = math.radians(angulo_injerto)
    perimetro = math.pi * d_ramal
    paso = perimetro / divisiones

    angulos_deg = [round(i * (360.0 / divisiones), 2) for i in range(divisiones + 1)]
    distancias_x = [round(i * paso, 2) for i in range(divisiones + 1)]

    alturas_corte_int = []
    alturas_corte_ext = []

    for ang in angulos_deg:
        a_rad = math.radians(ang)

        # 1. Asiento Interior (Real de taller: pared interior del ramal sobre lomo exterior del cabezal)
        term_incl_int = (r_int_ramal * (1.0 - math.cos(a_rad))) / math.tan(phi_rad) if angulo_injerto != 90.0 else 0.0
        radicando_int = max(0.0, r_ext_cabezal**2 - (r_int_ramal * math.sin(a_rad))**2)
        h_int = term_incl_int + (r_ext_cabezal - math.sqrt(radicando_int)) / math.sin(phi_rad)
        alturas_corte_int.append(round(h_int, 2))

        # 2. Perfil Exterior (Referencia de penetración / bisel exterior)
        term_incl_ext = (r_ext_ramal * (1.0 - math.cos(a_rad))) / math.tan(phi_rad) if angulo_injerto != 90.0 else 0.0
        radicando_ext = max(0.0, r_ext_cabezal**2 - (r_ext_ramal * math.sin(a_rad))**2)
        h_ext = term_incl_ext + (r_ext_cabezal - math.sqrt(radicando_ext)) / math.sin(phi_rad)
        alturas_corte_ext.append(round(h_ext, 2))

    alturas_corte = alturas_corte_int if tipo_asiento == "interior" else alturas_corte_ext

    return {
        "r1": r_ext_cabezal,
        "r2": r_ext_ramal,
        "r_ext_cabezal": r_ext_cabezal,
        "r_ext_ramal": r_ext_ramal,
        "r_int_ramal": r_int_ramal,
        "espesor": espesor_ramal,
        "perimetro": perimetro,
        "paso": paso,
        "divisiones": divisiones,
        "angulos_deg": angulos_deg,
        "distancias_x": distancias_x,
        "alturas_corte": alturas_corte,
        "alturas_corte_int": alturas_corte_int,
        "alturas_corte_ext": alturas_corte_ext,
        "max_corte": max(alturas_corte),
        "min_corte": min(alturas_corte)
    }, None


def calcular_corte_pluma(
    diametro_ext: float,
    angulo: float = 90.0,
    divisiones: int = 24,
    tipo_angulo: str = "union"
):
    """
    Calcula la plantilla plana y alturas de generatrices para Corte Pluma / Inglete (Miter cut).
    Permite unir dos tuberías a cualquier ángulo (ej. 90° para codo a escuadra de 2 piezas).

    Parámetros:
    - diametro_ext: Diámetro exterior de la tubería (mm).
    - angulo: Si tipo_angulo='union', es el ángulo total entre tuberías (ej. 90°).
              Si tipo_angulo='corte', es el ángulo de inglete/corte respecto a la perpendicular (ej. 45°).
    - divisiones: Cantidad de generatrices (par, ej. 12, 16, 24, 32).
    - tipo_angulo: 'union' (ángulo de desvío total β) o 'corte' (ángulo de corte θ).
    """
    if diametro_ext <= 0:
        return None, "Error: El diámetro exterior debe ser mayor a 0."
    if divisiones <= 0 or divisiones % 2 != 0:
        return None, "Error: La cantidad de divisiones debe ser un número par positivo."

    if tipo_angulo == "union":
        angulo_union = angulo
        theta_corte = angulo / 2.0
    else:
        theta_corte = angulo
        angulo_union = angulo * 2.0

    if theta_corte <= 0 or theta_corte >= 89.9:
        return None, "Error: El ángulo de corte de inglete debe estar entre 1° y 89°."

    r = diametro_ext / 2.0
    theta_rad = math.radians(theta_corte)
    perimetro = math.pi * diametro_ext
    paso = perimetro / divisiones

    angulos_deg = [round(i * (360.0 / divisiones), 2) for i in range(divisiones + 1)]
    distancias_x = [round(i * paso, 2) for i in range(divisiones + 1)]
    alturas_corte = []

    for ang in angulos_deg:
        a_rad = math.radians(ang)
        # Altura desde la línea base (talón = 0 en alfa=0°)
        h = r * math.tan(theta_rad) * (1.0 - math.cos(a_rad))
        alturas_corte.append(round(h, 2))

    eje_mayor = diametro_ext / math.cos(theta_rad)
    max_corte = max(alturas_corte)

    return {
        "diametro_ext": diametro_ext,
        "angulo_corte": round(theta_corte, 2),
        "angulo_union": round(angulo_union, 2),
        "perimetro": perimetro,
        "paso": paso,
        "divisiones": divisiones,
        "eje_mayor_elipse": round(eje_mayor, 2),
        "angulos_deg": angulos_deg,
        "distancias_x": distancias_x,
        "alturas_corte": alturas_corte,
        "max_corte": max_corte,
        "min_corte": min(alturas_corte)
    }, None


def calcular_esquina_3d(
    diametro_ext: float,
    divisiones: int = 24,
    tipo_nudo: str = "triple_inglete",
    d_codo: float = None,
    espesor: float = 0.0
):
    """
    Calcula el trazado y desarrollo plano para un nudo de 3 tuberias donde dos convergen
    en un plano a 90 grados (corte pluma) y el tercer tubo se proyecta perpendicularmente (producto vectorial).

    Modos:
    1. 'triple_inglete' (Esquina 3D simetrica / Triple Miter Corner):
       Los 3 tubos convergen simetricamente en el vertice a 90 grados. Cada tubo tiene dos cortes a 45 grados
       (uno en el plano horizontal y otro vertical). La misma plantilla sirve para los 3 tubos.
    2. 'injerto_sobre_codo' (Pilar vertical perpendicular montado sobre codo a 90 grados):
       Dos tubos forman el codo a 90 grados y el tercer tubo perpendicular (columna/montante) apoya
       a horcajadas sobre la costura del inglete.
    """
    if diametro_ext <= 0:
        return None, "Error: El diametro exterior debe ser mayor a 0."
    if divisiones <= 0 or divisiones % 2 != 0:
        return None, "Error: La cantidad de divisiones debe ser un numero par positivo."

    r = diametro_ext / 2.0
    perimetro = math.pi * diametro_ext
    paso = perimetro / divisiones

    angulos_deg = [round(i * (360.0 / divisiones), 2) for i in range(divisiones + 1)]
    distancias_x = [round(i * paso, 2) for i in range(divisiones + 1)]

    if tipo_nudo == "triple_inglete":
        # Esquina 3D simetrica (Triple Miter)
        z_vals = []
        for ang in angulos_deg:
            a_rad = math.radians(ang)
            if 45.0 <= ang <= 225.0:
                z = r * math.sin(a_rad)
            else:
                z = r * math.cos(a_rad)
            z_vals.append(z)

        z_min = min(z_vals)
        alturas_corte = [round(z - z_min, 2) for z in z_vals]
        max_corte = max(alturas_corte)
        h_arista = round(r * math.sqrt(2), 2)

        return {
            "diametro_ext": diametro_ext,
            "tipo_nudo": tipo_nudo,
            "perimetro": perimetro,
            "paso": paso,
            "divisiones": divisiones,
            "angulos_deg": angulos_deg,
            "distancias_x": distancias_x,
            "alturas_corte": alturas_corte,
            "max_corte": max_corte,
            "min_corte": min(alturas_corte),
            "h_arista_45": h_arista,
            "descripcion": "Triple Inglete Simetrico a 90 grados (Valido para los 3 tubos)"
        }, None

    else:
        # Injerto / Pilar perpendicular sobre codo soldado a 90 grados
        d_base = d_codo if d_codo and d_codo > 0 else diametro_ext
        r_codo = d_base / 2.0
        r_pilar_ext = r
        r_pilar_int = r_pilar_ext - espesor if espesor > 0 else r_pilar_ext

        alturas_corte = []
        for ang in angulos_deg:
            a_rad = math.radians(ang)
            if 45.0 <= ang <= 225.0:
                lat = r_pilar_int * math.cos(a_rad)
            else:
                lat = r_pilar_int * math.sin(a_rad)

            radicando = max(0.0, r_codo**2 - lat**2)
            h = r_codo - math.sqrt(radicando)
            alturas_corte.append(round(h, 2))

        max_corte = max(alturas_corte)
        return {
            "diametro_ext": diametro_ext,
            "d_codo": d_base,
            "espesor": espesor,
            "tipo_nudo": tipo_nudo,
            "perimetro": perimetro,
            "paso": paso,
            "divisiones": divisiones,
            "angulos_deg": angulos_deg,
            "distancias_x": distancias_x,
            "alturas_corte": alturas_corte,
            "max_corte": max_corte,
            "min_corte": min(alturas_corte),
            "descripcion": "Tubo Perpendicular montado a horcajadas sobre Codo a 90 grados"
        }, None


def calcular_injerto_y(
    d_cabezal: float,
    d_ramal: float,
    angulo_inclinacion: float = 45.0,
    espesor_ramal: float = 0.0,
    divisiones: int = 24
):
    """
    Calcula el desarrollo plano y plantilla de corte para un Injerto en 'Y' / Bifurcacion lateral
    (ramal oblicuo a 30 grados, 45 grados, 60 grados u otro angulo).
    Incluye la plantilla del Ramal (con compensacion de espesor de pared para asiento interior real)
    y las coordenadas de la plantilla del Orificio (desfonde) en el Cabezal.

    Parametros:
    - d_cabezal: Diametro EXTERIOR del tubo cabezal/colector (mm).
    - d_ramal: Diametro EXTERIOR del tubo ramal oblicuo (mm).
    - angulo_inclinacion: Angulo agudo de inclinacion del ramal respecto al eje del cabezal (grados, ej. 30, 45, 60).
    - espesor_ramal: Espesor de pared del tubo ramal (mm). Si es 0, calcula el caso ideal.
    - divisiones: Cantidad de generatrices (par, ej. 12, 16, 24, 32, 48).
    """
    if d_ramal > d_cabezal:
        return None, "Error: El diametro del ramal no puede ser mayor que el diametro del cabezal principal."
    if espesor_ramal < 0:
        return None, "Error: El espesor del ramal no puede ser negativo."
    if angulo_inclinacion <= 0 or angulo_inclinacion >= 90:
        return None, "Error: El angulo de inclinacion debe estar entre 1 grado y 89 grados (habitualmente 30, 45 o 60)."
    if divisiones <= 0 or divisiones % 2 != 0:
        return None, "Error: La cantidad de divisiones debe ser un numero par positivo."

    r_c = d_cabezal / 2.0
    r_r_ext = d_ramal / 2.0

    if espesor_ramal > 0:
        if espesor_ramal >= r_r_ext:
            return None, "Error: El espesor no puede ser mayor o igual al radio del ramal."
        r_r_int = r_r_ext - espesor_ramal
    else:
        r_r_int = r_r_ext

    if r_r_int > r_c:
        return None, "Error: El radio interior del ramal no puede superar el radio exterior del cabezal."

    phi_rad = math.radians(angulo_inclinacion)
    perimetro_ramal = math.pi * d_ramal
    paso_ramal = perimetro_ramal / divisiones

    angulos_deg = [round(i * (360.0 / divisiones), 2) for i in range(divisiones + 1)]
    distancias_x_ramal = [round(i * paso_ramal, 2) for i in range(divisiones + 1)]

    alturas_ramal_int = []
    alturas_ramal_ext = []

    for ang in angulos_deg:
        a_rad = math.radians(ang)

        # 1. Asiento interior (real de taller: radio interior de ramal sobre radio exterior cabezal)
        term_incl_int = (r_r_int * (1.0 - math.cos(a_rad))) / math.tan(phi_rad)
        rad_int = max(0.0, r_c**2 - (r_r_int * math.sin(a_rad))**2)
        term_pen_int = (r_c - math.sqrt(rad_int)) / math.sin(phi_rad)
        h_int = term_incl_int + term_pen_int
        alturas_ramal_int.append(round(h_int, 2))

        # 2. Perfil exterior (linea de referencia de bisel)
        term_incl_ext = (r_r_ext * (1.0 - math.cos(a_rad))) / math.tan(phi_rad)
        rad_ext = max(0.0, r_c**2 - (r_r_ext * math.sin(a_rad))**2)
        term_pen_ext = (r_c - math.sqrt(rad_ext)) / math.sin(phi_rad)
        h_ext = term_incl_ext + term_pen_ext
        alturas_ramal_ext.append(round(h_ext, 2))

    # Orificio en el Cabezal (Desfonde / Header Hole cutout)
    orificio_x = []
    orificio_y_arco = []
    for ang in angulos_deg:
        a_rad = math.radians(ang)
        seno_arg = max(-1.0, min(1.0, (r_r_int * math.sin(a_rad)) / r_c))
        y_arco = r_c * math.asin(seno_arg)
        z_pen = math.sqrt(max(0.0, r_c**2 - (r_r_int * math.sin(a_rad))**2))
        x_long = (r_r_int * math.cos(a_rad)) / math.sin(phi_rad) - ((r_c - z_pen) / math.tan(phi_rad))
        orificio_x.append(round(x_long, 2))
        orificio_y_arco.append(round(y_arco, 2))

    max_corte = max(alturas_ramal_int)
    min_corte = min(alturas_ramal_int)
    long_orificio = max(orificio_x) - min(orificio_x)
    ancho_orificio = max(orificio_y_arco) - min(orificio_y_arco)

    return {
        "d_cabezal": d_cabezal,
        "d_ramal": d_ramal,
        "angulo_inclinacion": angulo_inclinacion,
        "espesor_ramal": espesor_ramal,
        "perimetro_ramal": perimetro_ramal,
        "paso_ramal": paso_ramal,
        "divisiones": divisiones,
        "angulos_deg": angulos_deg,
        "distancias_x_ramal": distancias_x_ramal,
        "alturas_ramal": alturas_ramal_int,
        "alturas_ramal_int": alturas_ramal_int,
        "alturas_ramal_ext": alturas_ramal_ext,
        "max_corte": max_corte,
        "min_corte": min_corte,
        "orificio_x": orificio_x,
        "orificio_y_arco": orificio_y_arco,
        "long_orificio": round(long_orificio, 2),
        "ancho_orificio": round(ancho_orificio, 2)
    }, None


# ==========================================================
# CATÁLOGO NORMATIVO ASME B36.10 / B16.9 Y BAYONETAS (OFFSETS)
# ==========================================================
CATALOGO_TUBERIAS_ASME = {
    '1/2"': (0.5, 21.3),
    '3/4"': (0.75, 26.7),
    '1"': (1.0, 33.4),
    '1 1/4"': (1.25, 42.2),
    '1 1/2"': (1.5, 48.3),
    '2"': (2.0, 60.3),
    '2 1/2"': (2.5, 73.0),
    '3"': (3.0, 88.9),
    '4"': (4.0, 114.3),
    '6"': (6.0, 168.3),
    '8"': (8.0, 219.1),
    '10"': (10.0, 273.1),
    '12"': (12.0, 323.9),
    '14"': (14.0, 355.6),
    '16"': (16.0, 406.4),
    '18"': (18.0, 457.2),
    '20"': (20.0, 508.0),
    '24"': (24.0, 609.6),
}


def obtener_datos_codo_asme(
    nps_key: str,
    angulo_codo_deg: float,
    tipo_radio: str = "LR",
    luz_soldadura: float = 2.0
):
    """
    Calcula el radio de curvatura, el avance (take-out) del codo según ASME B16.9
    para cualquier ángulo (estándar o degradado), y los arcos de corte (intradós, eje, lomo).
    """
    nps_in, od_mm = CATALOGO_TUBERIAS_ASME.get(nps_key, (4.0, 114.3))
    if "LR" in tipo_radio:
        rc = 1.5 * nps_in * 25.4
    elif "SR" in tipo_radio:
        rc = 1.0 * nps_in * 25.4
    elif "3D" in tipo_radio:
        rc = 3.0 * nps_in * 25.4
    else:
        rc = 0.0

    theta_rad = math.radians(angulo_codo_deg)
    avance_codo = rc * math.tan(theta_rad / 2.0) if rc > 0 else 0.0

    r_tubo = od_mm / 2.0
    r_intrados = max(0.0, rc - r_tubo) if rc > 0 else 0.0
    r_extrados = (rc + r_tubo) if rc > 0 else 0.0

    arco_intrados = r_intrados * theta_rad
    arco_centro = rc * theta_rad
    arco_extrados = r_extrados * theta_rad

    descuento_par = 2.0 * avance_codo
    descuento_total = descuento_par + (2.0 * luz_soldadura if rc > 0 else 0.0)

    return {
        "nps_key": nps_key,
        "nps_in": nps_in,
        "od_mm": od_mm,
        "rc_mm": round(rc, 2),
        "avance_codo": round(avance_codo, 2),
        "descuento_par_codos": round(descuento_par, 2),
        "descuento_total_niple": round(descuento_total, 2),
        "arco_intrados": round(arco_intrados, 2),
        "arco_centro": round(arco_centro, 2),
        "arco_extrados": round(arco_extrados, 2),
        "luz_soldadura": luz_soldadura
    }


def calcular_bayoneta_2d(
    desplazamiento_o: float,
    valor_conocido: float,
    modo_calculo: str = "angulo",
    nps_key: str = '4"',
    tipo_radio: str = "LR (Radio Largo 1.5D)",
    luz_soldadura: float = 2.0
):
    """
    Calcula una Bayoneta Simple 2D en un solo plano.
    Modos:
    - 'angulo': Conocido el Desplazamiento (O) y el Ángulo del codo (θ).
    - 'avance': Conocido el Desplazamiento (O) y el Avance proyectado (A).
    """
    if desplazamiento_o <= 0:
        return None, "Error: El desplazamiento (O) debe ser mayor a 0."
    if valor_conocido <= 0:
        return None, "Error: El parámetro secundario debe ser mayor a 0."

    if modo_calculo == "angulo":
        theta_deg = valor_conocido
        if theta_deg <= 1.0 or theta_deg >= 89.5:
            return None, "Error: El ángulo del codo debe estar entre 1° y 89°."
        theta_rad = math.radians(theta_deg)
        recorrido_t = desplazamiento_o / math.sin(theta_rad)
        avance_a = desplazamiento_o / math.tan(theta_rad)
    else:
        avance_a = valor_conocido
        recorrido_t = math.sqrt(desplazamiento_o**2 + avance_a**2)
        theta_rad = math.atan2(desplazamiento_o, avance_a)
        theta_deg = math.degrees(theta_rad)

    datos_codo = obtener_datos_codo_asme(nps_key, theta_deg, tipo_radio, luz_soldadura)
    niple_neto = recorrido_t - datos_codo["descuento_total_niple"]

    return {
        "desplazamiento_o": round(desplazamiento_o, 2),
        "avance_a": round(avance_a, 2),
        "recorrido_t": round(recorrido_t, 2),
        "angulo_codo": round(theta_deg, 2),
        "niple_neto": round(niple_neto, 2),
        "codo_a_codo_alerta": niple_neto <= 0,
        "datos_codo": datos_codo
    }, None


def calcular_bayoneta_3d(
    desp_h: float,
    desp_v: float,
    valor_conocido: float,
    modo_calculo: str = "angulo",
    nps_key: str = '4"',
    tipo_radio: str = "LR (Radio Largo 1.5D)",
    luz_soldadura: float = 2.0
):
    """
    Calcula una Bayoneta Girada 3D (Rolling Offset).
    Combina un desplazamiento Horizontal (H / Roll) y uno Vertical (V / Set).
    """
    if desp_h < 0 or desp_v < 0 or (desp_h == 0 and desp_v == 0):
        return None, "Error: Los desplazamientos H y V deben ser positivos y no ambos cero."
    if valor_conocido <= 0:
        return None, "Error: El ángulo o avance debe ser mayor a 0."

    diagonal_d = math.sqrt(desp_h**2 + desp_v**2)

    if modo_calculo == "angulo":
        theta_deg = valor_conocido
        if theta_deg <= 1.0 or theta_deg >= 89.5:
            return None, "Error: El ángulo del codo debe estar entre 1° y 89°."
        theta_rad = math.radians(theta_deg)
        avance_a = diagonal_d / math.tan(theta_rad)
        recorrido_t = diagonal_d / math.sin(theta_rad)
    else:
        avance_a = valor_conocido
        recorrido_t = math.sqrt(diagonal_d**2 + avance_a**2)
        theta_rad = math.atan2(diagonal_d, avance_a)
        theta_deg = math.degrees(theta_rad)

    ang_giro_vert_rad = math.atan2(desp_h, desp_v)
    ang_giro_vert = math.degrees(ang_giro_vert_rad)
    ang_giro_horiz = 90.0 - ang_giro_vert

    datos_codo = obtener_datos_codo_asme(nps_key, theta_deg, tipo_radio, luz_soldadura)
    arco_giro_tubo = (datos_codo["od_mm"] / 2.0) * ang_giro_vert_rad
    niple_neto = recorrido_t - datos_codo["descuento_total_niple"]

    return {
        "desp_h": round(desp_h, 2),
        "desp_v": round(desp_v, 2),
        "diagonal_d": round(diagonal_d, 2),
        "avance_a": round(avance_a, 2),
        "recorrido_t": round(recorrido_t, 2),
        "angulo_codo": round(theta_deg, 2),
        "ang_giro_vert": round(ang_giro_vert, 2),
        "ang_giro_horiz": round(ang_giro_horiz, 2),
        "arco_giro_tubo": round(arco_giro_tubo, 2),
        "niple_neto": round(niple_neto, 2),
        "codo_a_codo_alerta": niple_neto <= 0,
        "datos_codo": datos_codo
    }, None


def calcular_bayoneta_doble(
    desplazamiento_o: float,
    angulo_codo_deg: float = 45.0,
    l_puente_centro: float = 400.0,
    nps_key: str = '4"',
    tipo_radio: str = "LR (Radio Largo 1.5D)",
    luz_soldadura: float = 2.0
):
    """
    Calcula una Bayoneta Doble Simétrica (Puente / Salto de obstáculo con 4 codos).
    """
    if desplazamiento_o <= 0:
        return None, "Error: La altura de salto (O) debe ser mayor a 0."
    if angulo_codo_deg <= 1.0 or angulo_codo_deg >= 89.5:
        return None, "Error: El ángulo del codo debe estar entre 1° y 89°."
    if l_puente_centro < 0:
        return None, "Error: La longitud del puente central no puede ser negativa."

    theta_rad = math.radians(angulo_codo_deg)
    recorrido_diag = desplazamiento_o / math.sin(theta_rad)
    avance_diag = desplazamiento_o / math.tan(theta_rad)
    abertura_total = 2.0 * avance_diag + l_puente_centro

    datos_codo = obtener_datos_codo_asme(nps_key, angulo_codo_deg, tipo_radio, luz_soldadura)
    niple_diag_neto = recorrido_diag - datos_codo["descuento_total_niple"]
    niple_puente_neto = l_puente_centro - datos_codo["descuento_total_niple"]
    sobre_metraje = (2.0 * recorrido_diag + l_puente_centro) - abertura_total

    return {
        "desplazamiento_o": round(desplazamiento_o, 2),
        "angulo_codo": round(angulo_codo_deg, 2),
        "recorrido_diag": round(recorrido_diag, 2),
        "avance_diag": round(avance_diag, 2),
        "l_puente_centro": round(l_puente_centro, 2),
        "abertura_total": round(abertura_total, 2),
        "niple_diag_neto": round(niple_diag_neto, 2),
        "niple_puente_neto": round(niple_puente_neto, 2),
        "sobre_metraje": round(sobre_metraje, 2),
        "datos_codo": datos_codo
    }, None


def calcular_bayoneta_paralela(
    separacion_s: float,
    angulo_codo_deg: float = 45.0,
    desplazamiento_o: float = 500.0,
    num_lineas: int = 4,
    l_base_arranque: float = 600.0
):
    """
    Calcula el desfase de arranque (Equal Spread Offset) para bancos de tuberías
    paralelas en Pipe Racks manteniendo la separación constante S.
    """
    if separacion_s <= 0:
        return None, "Error: La separación entre ejes (S) debe ser mayor a 0."
    if angulo_codo_deg <= 1.0 or angulo_codo_deg >= 89.5:
        return None, "Error: El ángulo del codo debe estar entre 1° y 89°."
    if desplazamiento_o <= 0:
        return None, "Error: El desplazamiento (O) debe ser mayor a 0."
    if num_lineas < 2 or num_lineas > 12:
        return None, "Error: La cantidad de líneas debe estar entre 2 y 12."

    theta_rad = math.radians(angulo_codo_deg)
    desfase_k = separacion_s * math.tan(theta_rad / 2.0)
    recorrido_t = desplazamiento_o / math.sin(theta_rad)
    avance_a = desplazamiento_o / math.tan(theta_rad)

    lineas_data = []
    for i in range(num_lineas):
        lineas_data.append({
            "linea": f"Línea {i + 1}",
            "indice": i,
            "pos_transversal": round(i * separacion_s, 2),
            "desfase_acumulado": round(i * desfase_k, 2),
            "cota_arranque_entrada": round(l_base_arranque + i * desfase_k, 2),
            "recorrido_diagonal_t": round(recorrido_t, 2)
        })

    return {
        "separacion_s": round(separacion_s, 2),
        "angulo_codo": round(angulo_codo_deg, 2),
        "desplazamiento_o": round(desplazamiento_o, 2),
        "desfase_k": round(desfase_k, 2),
        "recorrido_t": round(recorrido_t, 2),
        "avance_a": round(avance_a, 2),
        "num_lineas": num_lineas,
        "l_base_arranque": round(l_base_arranque, 2),
        "lineas": lineas_data
    }, None


# ==========================================================
# CODOS MITRADOS POR GAJOS / VIROLAS (MITERED ELBOWS)
# ==========================================================
def calcular_codo_gajos(
    diametro: float,
    angulo_total_deg: float = 90.0,
    num_cortes: int = 3,
    radio_curvatura: float = 225.0,
    divisiones: int = 24,
    espesor: float = 0.0,
    tipo_medida: str = "Exterior (Tubo Comercial)",
    kerf_corte: float = 2.0
):
    """
    Calcula el desarrollo analítico completo de un Codo por Gajos / Virolas (Mitered Bend):
    1. Plantilla de Media Virola Extrema (2 unidades).
    2. Plantilla de Virola Central Completa (num_cortes - 1 unidades).
    3. Trazado en Tubo Completo Sin Desperdicio (corte alternado a 180°).
    4. Geometría poligonal 2D de armado y control dimensional.
    """
    if diametro <= 0:
        return None, "Error: El diámetro debe ser mayor a 0."
    if angulo_total_deg <= 5.0 or angulo_total_deg > 180.0:
        return None, "Error: El ángulo total del codo debe estar entre 5° y 180°."
    if num_cortes < 1 or num_cortes > 12:
        return None, "Error: El número de cortes debe estar entre 1 y 12."
    if divisiones <= 0 or divisiones % 2 != 0:
        return None, "Error: La cantidad de generatrices debe ser un número par positivo."
    if espesor < 0:
        return None, "Error: El espesor no puede ser negativo."

    # Ajuste por fibra neutra cuando se fabrica desde chapa rolada
    if "Interior" in tipo_medida:
        d_calculo = diametro + espesor
        d_ext = diametro + 2.0 * espesor
    elif "Neutro" in tipo_medida:
        d_calculo = diametro
        d_ext = diametro + espesor
    elif "Chapa Exterior" in tipo_medida:
        d_calculo = diametro - espesor
        d_ext = diametro
    else:
        # Tubo comercial: la plantilla envuelve el exterior (OD)
        d_calculo = diametro
        d_ext = diametro

    if d_calculo <= 0:
        return None, "Error: El espesor ingresado supera el diámetro."

    r = d_calculo / 2.0

    # Validación crítica de taller: el radio de curvatura Rc debe ser mayor al radio del tubo
    if radio_curvatura <= r * 1.05:
        return None, (
            f"Error Geométrico de Taller: El radio de curvatura al centro (Rc = {radio_curvatura:.1f} mm) "
            f"debe ser mayor al radio del tubo (r = {r:.1f} mm) para evitar que los cortes se crucen en la garganta interior."
        )

    # Ángulo de corte sesgado (alfa) y ángulo de cada virola central (2*alfa)
    # Con num_cortes soldaduras: hay 2 medias virolas extremas (alfa) y (num_cortes - 1) virolas centrales (2*alfa)
    alfa_deg = angulo_total_deg / (2.0 * num_cortes)
    alfa_rad = math.radians(alfa_deg)
    beta_rad = math.radians(angulo_total_deg)

    # Dimensiones fundamentales de la Media Virola Extrema (1x alfa)
    lm_extremo = radio_curvatura * math.tan(alfa_rad)
    desvio_onda = r * math.tan(alfa_rad)
    garganta_extremo = (radio_curvatura - r) * math.tan(alfa_rad)  # L_min en phi = 0°
    lomo_extremo = (radio_curvatura + r) * math.tan(alfa_rad)      # L_max en phi = 180°

    # Dimensiones de la Virola Central Completa (2x alfa)
    lm_central = 2.0 * lm_extremo
    garganta_central = 2.0 * garganta_extremo
    lomo_central = 2.0 * lomo_extremo

    # Desarrollo perimetral
    perimetro = math.pi * d_calculo
    paso = perimetro / divisiones
    angulos_deg = [round(i * (360.0 / divisiones), 2) for i in range(divisiones + 1)]
    distancias_x = [round(i * paso, 2) for i in range(divisiones + 1)]

    y_media_virola = []
    delta_onda = []
    y_virola_central_inf = []
    y_virola_central_sup = []
    altura_total_central = []

    for ang in angulos_deg:
        phi_rad = math.radians(ang)
        # Variación senoidal respecto al eje neutro: -r * tan(alfa) * cos(phi)
        # En phi = 0° (garganta): -r*tan(alfa) -> altura mínima
        # En phi = 180° (lomo): +r*tan(alfa) -> altura máxima
        dy = -r * math.tan(alfa_rad) * math.cos(phi_rad)
        h_ext = lm_extremo + dy

        # Para graficar la virola central completa sobre una chapa base recta:
        # El punto más bajo de la curva inferior ocurre en phi=180° -> desplazamos r*tan(alfa) para que toque y=0
        y_inf = r * math.tan(alfa_rad) * (1.0 + math.cos(phi_rad))
        h_cen = 2.0 * h_ext
        y_sup = y_inf + h_cen

        y_media_virola.append(round(h_ext, 2))
        delta_onda.append(round(dy, 2))
        y_virola_central_inf.append(round(y_inf, 2))
        y_virola_central_sup.append(round(y_sup, 2))
        altura_total_central.append(round(h_cen, 2))

    # Cálculo de aprovechamiento de tubo recto sin desperdicio (Corte Alternado a 180°)
    # Suma de todos los ejes neutros = 2 * num_cortes * lm_extremo
    suma_ejes_neutros = 2.0 * num_cortes * lm_extremo
    largo_tubo_sin_desperdicio = suma_ejes_neutros + (num_cortes * kerf_corte)

    # Posiciones axiales de las curvas de corte sobre un tubo recto para corte alternado
    # Corte k (k = 1 .. num_cortes) tiene su centro en x_corte = (2*k - 1)*lm_extremo + (k-1)*kerf
    # y alterna el signo de cos(phi) con (-1)**(k-1)
    curvas_tubo_alternado = []
    cotas_generatrices_0_180 = []
    for k in range(1, num_cortes + 1):
        z_centro = (2 * k - 1) * lm_extremo + (k - 1) * kerf_corte
        signo = 1.0 if (k % 2 == 1) else -1.0
        z_curva = []
        for ang in angulos_deg:
            phi_rad = math.radians(ang)
            z_pt = z_centro - signo * r * math.tan(alfa_rad) * math.cos(phi_rad)
            z_curva.append(round(z_pt, 2))
        curvas_tubo_alternado.append({
            "corte_num": k,
            "z_centro": round(z_centro, 2),
            "z_curva": z_curva
        })
        # Posición en generatriz 0° y 180°
        z_gen_0 = z_centro - signo * r * math.tan(alfa_rad)
        z_gen_180 = z_centro + signo * r * math.tan(alfa_rad)
        cotas_generatrices_0_180.append({
            "corte": f"Corte #{k}",
            "eje_centro_mm": round(z_centro, 2),
            "marca_linea_0_deg_mm": round(z_gen_0, 2),
            "marca_linea_180_deg_mm": round(z_gen_180, 2)
        })

    # Avance del codo armado (Centro a cara) y cuerda total
    avance_codo = radio_curvatura * math.tan(beta_rad / 2.0)
    cuerda_media = 2.0 * radio_curvatura * math.sin(beta_rad / 2.0)
    perimetro_elipse_soldadura = math.pi * (d_calculo / math.cos(alfa_rad))
    longitud_total_soldadura = num_cortes * perimetro_elipse_soldadura

    return {
        "diametro_input": diametro,
        "d_calculo": round(d_calculo, 2),
        "d_ext": round(d_ext, 2),
        "r": round(r, 2),
        "espesor": espesor,
        "tipo_medida": tipo_medida,
        "angulo_total": round(angulo_total_deg, 2),
        "num_cortes": num_cortes,
        "num_virolas_centrales": num_cortes - 1,
        "num_piezas_totales": num_cortes + 1,
        "alfa_corte": round(alfa_deg, 2),
        "alfa_virola_central": round(2.0 * alfa_deg, 2),
        "radio_curvatura": round(radio_curvatura, 2),
        "lm_extremo": round(lm_extremo, 2),
        "garganta_extremo": round(garganta_extremo, 2),
        "lomo_extremo": round(lomo_extremo, 2),
        "lm_central": round(lm_central, 2),
        "garganta_central": round(garganta_central, 2),
        "lomo_central": round(lomo_central, 2),
        "desvio_onda": round(desvio_onda, 2),
        "perimetro": round(perimetro, 2),
        "paso": round(paso, 2),
        "divisiones": divisiones,
        "angulos_deg": angulos_deg,
        "distancias_x": distancias_x,
        "y_media_virola": y_media_virola,
        "delta_onda": delta_onda,
        "y_virola_central_inf": y_virola_central_inf,
        "y_virola_central_sup": y_virola_central_sup,
        "altura_total_central": altura_total_central,
        "largo_tubo_sin_desperdicio": round(largo_tubo_sin_desperdicio, 2),
        "curvas_tubo_alternado": curvas_tubo_alternado,
        "cotas_generatrices_0_180": cotas_generatrices_0_180,
        "avance_codo": round(avance_codo, 2),
        "cuerda_media": round(cuerda_media, 2),
        "longitud_total_soldadura": round(longitud_total_soldadura, 2),
        "kerf_corte": kerf_corte
    }, None

