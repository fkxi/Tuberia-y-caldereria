import math
import numpy as np

def calcular_dimensiones_neutras(lx, ly, d, espesor, tipo):
    if tipo == "Interior":
        return lx + espesor, ly + espesor, d + espesor
    elif tipo == "Exterior":
        return lx - espesor, ly - espesor, d - espesor
    return lx, ly, d

def resolver_triangulo(a, b, c):
    val = (a**2 + b**2 - c**2) / (2 * a * b)
    return math.acos(max(-1.0, min(1.0, val)))

def generar_nodos_3d_oblicua(lx_n, ly_n, d_n, h, dx, ang_inclinacion, divisiones):
    r_n = d_n / 2
    ex, ey = lx_n / 2, ly_n / 2
    phi_rad = math.radians(ang_inclinacion)
    
    M_total = divisiones // 2
    P_pts_3d = []
    
    for i in range(M_total + 1):
        ang = i * (math.pi / M_total)
        px = dx + r_n * math.cos(ang) * math.cos(phi_rad)
        py = r_n * math.sin(ang)
        pz = h + r_n * math.cos(ang) * math.sin(phi_rad)
        P_pts_3d.append(np.array([px, py, pz]))
        
    E1 = np.array([ex, ey, 0])
    E2 = np.array([-ex, ey, 0])
    
    M_quad = M_total // 2
    vms_E1 = [np.linalg.norm(P_pts_3d[i] - E1) for i in range(M_quad + 1)]
    vms_E2 = [np.linalg.norm(P_pts_3d[i] - E2) for i in range(M_quad, M_total + 1)]
    
    return P_pts_3d, E1, E2, vms_E1, vms_E2, M_quad, M_total, ex, ey, r_n, phi_rad

def desarrollar_plantilla_oblicua(P_pts_3d, E1, E2, ex, M_quad, M_total):
    M1, M2 = np.array([ex, 0, 0]), np.array([-ex, 0, 0])
    seq = [(E1, 0)]
    for i in range(1, M_quad + 1): seq.append((P_pts_3d[i], 1))
    seq.append((E2, 0))
    for i in range(M_quad + 1, M_total + 1): seq.append((P_pts_3d[i], 1))
    seq.append((M2, 0))
    
    A2 = np.array([0.0, 0.0])
    L_init = np.linalg.norm(P_pts_3d[0] - M1)
    B2 = np.array([0.0, L_init])
    A3, B3 = M1, P_pts_3d[0]
    
    pts_2d_bottom = [A2]
    pts_2d_top = [B2]
    lines_to_draw = []
    
    for pt3, ptype in seq:
        L_AC = np.linalg.norm(pt3 - A3)
        L_BC = np.linalg.norm(pt3 - B3)
        d = np.linalg.norm(B2 - A2)
        
        x = (L_AC**2 - L_BC**2 + d**2) / (2*d)
        y = math.sqrt(max(0, L_AC**2 - x**2))
        
        u = (B2 - A2) / d
        v = np.array([-u[1], u[0]])
        C2 = A2 + x*u + y*v
        
        if ptype == 0: 
            pts_2d_bottom.append(C2)
            lines_to_draw.append((C2, B2))
            A2, A3 = C2, pt3
        else: 
            pts_2d_top.append(C2)
            lines_to_draw.append((A2, C2))
            B2, B3 = C2, pt3
            
    return pts_2d_bottom, pts_2d_top, lines_to_draw, L_init, M2

def calcular_desarrollo_recta(lado_x, lado_y, diametro_t, altura_t, espesor, tipo_trazo, divisiones):
    lx_n, ly_n, d_n = calcular_dimensiones_neutras(lado_x, lado_y, diametro_t, espesor, tipo_trazo)
    r_n = d_n / 2.0
    ex, ey = lx_n / 2.0, ly_n / 2.0
    
    m_puntos = divisiones // 4
    angulos_rad = np.linspace(0, np.pi/2, m_puntos + 1)
    
    vms = []
    for ang in angulos_rad:
        cx, cy = r_n * np.cos(ang), r_n * np.sin(ang)
        vm = math.sqrt((ex - cx)**2 + (ey - cy)**2 + altura_t**2)
        vms.append(vm)
        
    h_x = math.sqrt((lx_n/2.0 - r_n)**2 + altura_t**2)
    h_y = math.sqrt((ly_n/2.0 - r_n)**2 + altura_t**2)
    
    cuerda_arco = 2.0 * r_n * math.sin(math.pi / divisiones)
    
    Mx = np.array([0.0, 0.0])
    P0 = np.array([0.0, h_x])
    E = np.array([ly_n / 2.0, 0.0])
    
    P_pts = [P0]
    for i in range(1, m_puntos + 1):
        beta = resolver_triangulo(vms[i-1], vms[i], cuerda_arco)
        vec_prev = P_pts[-1] - E
        theta_prev = math.atan2(vec_prev[1], vec_prev[0])
        theta_new = theta_prev - beta
        P_new = E + np.array([vms[i] * math.cos(theta_new), vms[i] * math.sin(theta_new)])
        P_pts.append(P_new)
        
    gamma = resolver_triangulo(vms[-1], lx_n / 2.0, h_y)
    vec_pm = P_pts[-1] - E
    theta_pm = math.atan2(vec_pm[1], vec_pm[0])
    theta_my = theta_pm - gamma
    My = E + np.array([(lx_n/2.0) * math.cos(theta_my), (lx_n/2.0) * math.sin(theta_my)])
    
    E_izq = np.array([-E[0], E[1]])
    My_izq = np.array([-My[0], My[1]])
    P_pts_izq = [np.array([-p[0], p[1]]) for p in P_pts]
    
    return {
        "lx_n": lx_n,
        "ly_n": ly_n,
        "d_n": d_n,
        "r_n": r_n,
        "ex": ex,
        "ey": ey,
        "m_puntos": m_puntos,
        "angulos_rad": angulos_rad,
        "vms": vms,
        "h_x": h_x,
        "h_y": h_y,
        "cuerda_arco": cuerda_arco,
        "Mx": Mx,
        "E": E,
        "My": My,
        "P_pts": P_pts,
        "E_izq": E_izq,
        "My_izq": My_izq,
        "P_pts_izq": P_pts_izq
    }
