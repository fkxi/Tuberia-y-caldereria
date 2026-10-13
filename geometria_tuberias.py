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
