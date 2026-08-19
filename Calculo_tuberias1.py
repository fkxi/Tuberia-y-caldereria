import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Herramientas de Trazado Industrial", layout="wide")

# ==========================================
# BARRA LATERAL (SIDEBAR) - NAVEGACIÓN
# ==========================================
st.sidebar.title("Menú Principal")
st.sidebar.markdown("Seleccione el módulo de trabajo:")
modulo = st.sidebar.radio("Módulos:", ["Tuberías", "Calderería"])

st.sidebar.markdown("---")
st.sidebar.info("Desarrollado por Jesus Tasayco.\nAplicativo para cálculos de fabricación y trazado.")

# ==========================================
# MÓDULO 1: TUBERÍAS
# ==========================================
if modulo == "Tuberías":
    st.title("Aplicativo de Trazado y Generatrices para Tuberías")
    st.markdown("Unificación de cálculos fundamentales para el desarrollo de plantillas y cortes en tuberías cilíndricas.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Calcular Flecha", "Calcular Cuerda", "Calcular Radio", "Generatrices y Plantilla"])

    # --- PESTAÑA 1: CÁLCULO DE FLECHA ---
    with tab1:
        st.header("Cálculo de la Flecha")
        st.markdown("Calcula la altura máxima del arco (Flecha) a partir del radio y la longitud de la cuerda.")
        st.latex(r"f = R - \sqrt{R^2 - \left(\frac{C}{2}\right)^2}")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            radio_f = st.number_input("Radio de la circunferencia (R):", min_value=0.1, value=100.0, step=1.0, key="r_flecha")
            cuerda_f = st.number_input("Longitud de la cuerda (C):", min_value=0.1, value=150.0, step=1.0, key="c_flecha")
            calcular_btn_f = st.button("Calcular y Graficar Flecha", type="primary")

        with col2:
            if calcular_btn_f:
                if cuerda_f > 2 * radio_f:
                    st.error("Error geométrico: La cuerda no puede ser mayor que el diámetro (2R).")
                else:
                    mitad_cuerda = cuerda_f / 2
                    apotema_f = math.sqrt(radio_f**2 - mitad_cuerda**2)
                    flecha_f = radio_f - apotema_f
                    
                    fig1, ax1 = plt.subplots(figsize=(8, 8))
                    circ = plt.Circle((0, 0), radio_f, color='red', fill=False, linewidth=1.5)
                    ax1.add_artist(circ)
                    ax1.plot([0, mitad_cuerda], [0, apotema_f], color='red', linewidth=1)
                    ax1.plot([0, -mitad_cuerda], [0, apotema_f], color='red', linewidth=1)
                    ax1.plot([-mitad_cuerda, mitad_cuerda], [apotema_f, apotema_f], color='red', linewidth=1.5)
                    ax1.plot([0, 0], [0, apotema_f], color='red', linestyle='--', linewidth=1)
                    ax1.plot([0, 0], [apotema_f, radio_f], color='green', linewidth=3)
                    
                    ax1.text(mitad_cuerda/2, apotema_f/2, r'$R$', color='red', fontsize=12)
                    ax1.text(mitad_cuerda/2, apotema_f + (radio_f-apotema_f)/2, r'$C/2$', color='red', fontsize=12)
                    ax1.text(-radio_f*0.05, apotema_f/2, r'$a$', color='red', fontsize=12)
                    ax1.text(radio_f*0.05, apotema_f + flecha_f/2, r'$f$', color='green', fontsize=14, fontweight='bold')
                    
                    ax1.set_aspect('equal')
                    lim_max = radio_f * 1.2
                    ax1.set_xlim(-lim_max, lim_max)
                    ax1.set_ylim(-lim_max, lim_max)
                    ax1.axis('off')
                    st.pyplot(fig1)
                    st.success(f"**Resultado:** La flecha (f) es **{flecha_f:.2f}** unidades.")

    # --- PESTAÑA 2: CÁLCULO DE CUERDA ---
    with tab2:
        st.header("Cálculo de la Cuerda")
        st.markdown("Calcula la longitud de la cuerda conociendo el radio y el ángulo central en grados sexagesimales.")
        st.latex(r"C = 2R \sin\left(\frac{\theta}{2}\right)")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            radio_c = st.number_input("Radio de la circunferencia (R):", min_value=0.1, value=100.0, step=1.0, key="r_cuerda")
            angulo_c = st.number_input("Ángulo comprendido (θ en grados):", min_value=0.1, max_value=360.0, value=90.0, step=1.0, key="a_cuerda")
            calcular_btn_c = st.button("Calcular y Graficar Cuerda", type="primary")
            
        with col2:
            if calcular_btn_c:
                radianes = math.radians(angulo_c)
                cuerda_c = 2 * radio_c * math.sin(radianes / 2)
                
                fig2, ax2 = plt.subplots(figsize=(8, 8))
                if angulo_c > 180:
                    circ2 = plt.Circle((0, 0), radio_c, color='red', fill=False, linewidth=1.5)
                    ax2.add_artist(circ2)
                else:
                    x_arc_c = np.linspace(-radianes/2, radianes/2, 200)
                    ax2.plot(radio_c * np.sin(x_arc_c), radio_c * np.cos(x_arc_c), color='red', linewidth=1.5)
                
                x_r1, y_r1 = radio_c * np.sin(radianes/2), radio_c * np.cos(radianes/2)
                x_r2, y_r2 = radio_c * np.sin(-radianes/2), radio_c * np.cos(-radianes/2)
                ax2.plot([0, x_r1], [0, y_r1], color='red', linewidth=1)
                ax2.plot([0, x_r2], [0, y_r2], color='red', linewidth=1)
                ax2.plot([x_r1, x_r2], [y_r1, y_r2], color='green', linewidth=3)
                
                ax2.text(x_r1/2 + radio_c*0.05, y_r1/2, r'$R$', color='red', fontsize=12)
                ax2.text(0, -radio_c*0.15, r'$\theta$', color='black', fontsize=16, fontweight='bold')
                ax2.text(0, y_r1 + radio_c*0.05, r'$C$', color='green', fontsize=14, fontweight='bold')
                
                ax2.set_aspect('equal')
                lim_max_c = radio_c * 1.2
                ax2.set_xlim(-lim_max_c, lim_max_c)
                ax2.set_ylim(-lim_max_c, lim_max_c)
                ax2.axis('off')
                st.pyplot(fig2)
                st.success(f"**Resultado:** La longitud de la cuerda (C) es **{cuerda_c:.2f}** unidades.")

    # --- PESTAÑA 3: CÁLCULO DE RADIO ---
    with tab3:
        st.header("Cálculo del Radio")
        st.markdown("Obtén el radio de curvatura partiendo únicamente de la longitud de la cuerda y la altura de la flecha.")
        st.latex(r"R = \frac{f}{2} + \frac{C^2}{8f}")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            cuerda_r = st.number_input("Longitud de la cuerda (C):", min_value=0.1, value=150.0, step=1.0, key="c_radio")
            flecha_r = st.number_input("Altura de la flecha (f):", min_value=0.1, value=25.0, step=1.0, key="f_radio")
            calcular_btn_r = st.button("Calcular Radio", type="primary")

        with col2:
            if calcular_btn_r:
                radio_calc = (flecha_r / 2) + ((cuerda_r**2) / (8 * flecha_r))
                apotema_calc = radio_calc - flecha_r
                mitad_cuerda_r = cuerda_r / 2
                
                fig3, ax3 = plt.subplots(figsize=(8, 8))
                circ3 = plt.Circle((0, -apotema_calc), radio_calc, color='blue', fill=False, linestyle=':', linewidth=1)
                ax3.add_artist(circ3)
                ax3.plot([-mitad_cuerda_r, mitad_cuerda_r], [0, 0], color='black', linewidth=2, label='Cuerda (C)')
                ax3.plot([0, 0], [0, flecha_r], color='green', linewidth=3, label='Flecha (f)')
                ax3.plot([0, mitad_cuerda_r], [-apotema_calc, 0], color='red', linewidth=1.5, label='Radio (R)')
                ax3.plot([0, 0], [-apotema_calc, flecha_r], color='red', linestyle='--', linewidth=1)
                ax3.plot(0, -apotema_calc, marker='o', markersize=5, color='red')
                
                ax3.set_aspect('equal')
                ax3.set_xlim(-radio_calc * 1.2, radio_calc * 1.2)
                ax3.set_ylim(-radio_calc*1.2, flecha_r * 2)
                ax3.axis('off')
                ax3.legend(loc='lower right')
                st.pyplot(fig3)
                st.success(f"**Resultado:** El radio calculado (R) es **{radio_calc:.2f}** unidades.")

    # --- PESTAÑA 4: GENERATRICES Y PLANTILLA ---
    with tab4:
        st.header("Cálculo de Generatrices y Visualización de Plantilla")
        col_input1, col_input2, col_input3 = st.columns(3)
        with col_input1:
            diametro_g = st.number_input("Diámetro exterior (D):", min_value=1.0, value=26000.0, step=10.0)
        with col_input2:
            cuerda_g = st.number_input("Longitud de la cuerda (C):", min_value=1.0, value=500.0, step=10.0)
        with col_input3:
            separacion_g = st.number_input("Separación entre generatrices (s):", min_value=1.0, value=83.33, step=1.0)
            
        if st.button("Calcular y Graficar Plantilla", type="primary"):
            if cuerda_g > diametro_g:
                st.error("La cuerda no puede ser mayor al diámetro.")
            else:
                radio_g = diametro_g / 2.0
                mitad_cuerda_g = cuerda_g / 2.0
                apotema_g = math.sqrt(radio_g**2 - mitad_cuerda_g**2)
                flecha_g = radio_g - apotema_g
                
                posiciones_x_array = np.arange(0, mitad_cuerda_g + separacion_g, separacion_g)
                posiciones_x_array = posiciones_x_array[posiciones_x_array <= mitad_cuerda_g]
                if len(posiciones_x_array) == 0 or posiciones_x_array[-1] < mitad_cuerda_g - 1e-5:
                    posiciones_x_array = np.append(posiciones_x_array, mitad_cuerda_g)
                
                alturas_h_array = np.sqrt(radio_g**2 - posiciones_x_array**2) - apotema_g
                
                posiciones_x = posiciones_x_array.tolist()
                alturas_h = alturas_h_array.tolist()
                
                fig4, ax4 = plt.subplots(figsize=(16, 7))
                x_arc_g = np.linspace(-mitad_cuerda_g, mitad_cuerda_g, 500)
                y_arc_g = np.sqrt(radio_g**2 - x_arc_g**2) - apotema_g
                
                ax4.plot(x_arc_g, y_arc_g, color='blue', label='Arco de tubería', linewidth=2.5)
                ax4.plot([-mitad_cuerda_g, mitad_cuerda_g], [0, 0], color='black', linewidth=2, label='Cuerda base')
                ax4.plot([0, 0], [0, flecha_g], color='green', linewidth=3.5, label='Flecha central (f)')
                ax4.text(mitad_cuerda_g*0.05, flecha_g*0.6, f'f = {flecha_g:.2f}', color='green', fontsize=12, fontweight='bold')
                ax4.plot([0, 0], [-apotema_g, 0], color='red', linestyle=':', linewidth=2, label='Apotema central (a)')
                
                for i in range(len(posiciones_x)):
                    pos_x = posiciones_x[i]
                    alt = alturas_h[i]
                    ax4.plot([pos_x, pos_x], [0, alt], color='red', linestyle='--', linewidth=1.2)
                    if pos_x != 0:
                        ax4.plot([-pos_x, -pos_x], [0, alt], color='red', linestyle='--', linewidth=1.2)
                    
                    padding_y = flecha_g * 0.05
                    ax4.text(pos_x, alt + padding_y, f'{alt:.2f}', color='green', fontsize=10, fontweight='bold', rotation=90, va='bottom', ha='center')
                    if pos_x != 0:
                        ax4.text(-pos_x, alt + padding_y, f'{alt:.2f}', color='green', fontsize=10, fontweight='bold', rotation=90, va='bottom', ha='center')
                
                ax4.set_aspect('auto')
                ax4.set_xlim(-mitad_cuerda_g * 1.15, mitad_cuerda_g * 1.15)
                ax4.set_ylim(-flecha_g * 1.0, flecha_g * 1.5)
                ax4.grid(True, linestyle=':', alpha=0.6)
                st.pyplot(fig4, use_container_width=True)
                
                df_resultados_g = pd.DataFrame({
                    "Punto": [f"P_{i}" for i in range(len(posiciones_x))],
                    "Distancia desde centro (x)": [round(val, 2) for val in posiciones_x],
                    "Altura a cortar (h)": [round(val, 2) for val in alturas_h]
                })
                st.dataframe(df_resultados_g, use_container_width=True)

# ==========================================
# MÓDULO 2: CALDERERÍA
# ==========================================
elif modulo == "Calderería":
    st.title("Trazado en Calderería Pesada")
    st.markdown("Generación de plantillas basadas en fibra neutra, triangulación exacta y desarrollo 2D.")
    
    tab_recta, tab_oblicua = st.tabs(["Transición Recta (Concéntrica)", "Transición Oblicua (Excéntrica/Inclinada)"])

    # --- PESTAÑA: TRANSICIÓN RECTA ---
    with tab_recta:
        st.header("Transición Recta")
        col1, col2, col3 = st.columns(3)
        with col1:
            lado_x = st.number_input("Lado Base X (L1):", min_value=1.0, value=600.0, step=10.0, key="cald_lx")
            lado_y = st.number_input("Lado Base Y (L2):", min_value=1.0, value=600.0, step=10.0, key="cald_ly")
        with col2:
            diametro_t = st.number_input("Diámetro Boca (D):", min_value=1.0, value=300.0, step=10.0, key="cald_d")
            altura_t = st.number_input("Altura Transición (H):", min_value=1.0, value=400.0, step=10.0, key="cald_h")
        with col3:
            espesor = st.number_input("Espesor de Chapa (t):", min_value=0.0, value=6.0, step=1.0, key="cald_espesor")
            tipo_trazo = st.selectbox("Posición de Medidas:", ["Interior", "Exterior", "Neutro"], key="cald_tipo")
            divisiones = st.selectbox("Cant. Divisiones Circunferencia:", [12, 16, 24, 32, 36, 48], index=2, key="cald_divs")
            
        btn_transicion = st.button("Calcular Plantilla Recta", type="primary", key="btn_cald_calc")
        
        if btn_transicion:
            # Fibra Neutra
            if tipo_trazo == "Interior":
                lx_n, ly_n, d_n = lado_x + espesor, lado_y + espesor, diametro_t + espesor
            elif tipo_trazo == "Exterior":
                lx_n, ly_n, d_n = lado_x - espesor, lado_y - espesor, diametro_t - espesor
            else:
                lx_n, ly_n, d_n = lado_x, lado_y, diametro_t
                
            r_n = d_n / 2
            ex, ey = lx_n / 2, ly_n / 2
            
            m_puntos = divisiones // 4
            angulos_rad = np.linspace(0, np.pi/2, m_puntos + 1)
            
            vms = []
            for ang in angulos_rad:
                cx, cy = r_n * np.cos(ang), r_n * np.sin(ang)
                vm = math.sqrt((ex - cx)**2 + (ey - cy)**2 + altura_t**2)
                vms.append(vm)
                
            h_x = math.sqrt((lx_n/2 - r_n)**2 + altura_t**2) 
            h_y = math.sqrt((ly_n/2 - r_n)**2 + altura_t**2) 
            
            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 2.5])
            with res_col1:
                st.info(f"**Fibra Neutra:**\nBase X = {lx_n}\nBase Y = {ly_n}\nDiámetro = {d_n}")
                df_vm = pd.DataFrame({
                    "Generatriz (VM)": [f"[{i+1}] a {round(math.degrees(a))}°" for i, a in enumerate(angulos_rad)],
                    "Longitud (mm)": [round(v, 2) for v in vms]
                })
                st.dataframe(df_vm, use_container_width=True)
                
            with res_col2:
                fig3d = plt.figure(figsize=(10, 6))
                ax3d = fig3d.add_subplot(111, projection='3d')
                ax3d.plot([-ex, ex, ex, -ex, -ex], [-ey, -ey, ey, ey, -ey], [0, 0, 0, 0, 0], 'k-', lw=2)
                theta_full = np.linspace(0, 2*np.pi, divisiones + 1)
                ax3d.plot(r_n * np.cos(theta_full), r_n * np.sin(theta_full), np.full_like(theta_full, altura_t), 'b-', lw=2)
                
                angulos_totales = np.linspace(0, 2*np.pi, divisiones, endpoint=False)
                for ang in angulos_totales:
                    cx, cy = r_n * np.cos(ang), r_n * np.sin(ang)
                    if 0 <= ang <= np.pi/2: eqx, eqy = ex, ey
                    elif np.pi/2 < ang <= np.pi: eqx, eqy = -ex, ey
                    elif np.pi < ang <= 3*np.pi/2: eqx, eqy = -ex, -ey
                    else: eqx, eqy = ex, -ey
                    ax3d.plot([eqx, cx], [eqy, cy], [0, altura_t], 'r--', alpha=0.5)
                
                ax3d.set_title('Modelo Estructural 3D')
                lim_ax = max(ex, ey, altura_t)
                ax3d.set_xlim(-lim_ax, lim_ax); ax3d.set_ylim(-lim_ax, lim_ax); ax3d.set_zlim(0, altura_t)
                st.pyplot(fig3d)

            # DESARROLLO 2D
            st.markdown("---")
            st.subheader("Desarrollo Plano de la Chapa (Media Plantilla Acotada)")
            
            def resolver_triangulo(a, b, c):
                val = (a**2 + b**2 - c**2) / (2 * a * b)
                return math.acos(max(-1.0, min(1.0, val)))
                
            Mx = np.array([0.0, 0.0])
            P0 = np.array([0.0, h_x])
            E = np.array([ly_n / 2, 0.0])
            
            P_pts = [P0]
            cuerda_arco = 2 * r_n * math.sin(math.pi / divisiones)
            
            for i in range(1, m_puntos + 1):
                beta = resolver_triangulo(vms[i-1], vms[i], cuerda_arco)
                vec_prev = P_pts[-1] - E
                theta_prev = math.atan2(vec_prev[1], vec_prev[0])
                theta_new = theta_prev - beta
                P_new = E + np.array([vms[i] * math.cos(theta_new), vms[i] * math.sin(theta_new)])
                P_pts.append(P_new)
                
            gamma = resolver_triangulo(vms[-1], lx_n / 2, h_y)
            vec_pm = P_pts[-1] - E
            theta_pm = math.atan2(vec_pm[1], vec_pm[0])
            theta_my = theta_pm - gamma
            My = E + np.array([(lx_n/2) * math.cos(theta_my), (lx_n/2) * math.sin(theta_my)])
            
            fig2d, ax2d = plt.subplots(figsize=(16, 9))
            
            def acotar_linea(A, B, texto, color='black', fsize=8):
                mid = (A + B) / 2
                dx, dy = B[0] - A[0], B[1] - A[1]
                angle = np.degrees(np.arctan2(dy, dx))
                if angle > 90: angle -= 180
                elif angle < -90: angle += 180
                ax2d.text(mid[0], mid[1], texto, rotation=angle, 
                          ha='center', va='center', fontsize=fsize, color=color, fontweight='bold',
                          bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85))

            # --- LADO DERECHO ---
            ax2d.plot([Mx[0], E[0]], [Mx[1], E[1]], 'k-', lw=2.5) 
            acotar_linea(Mx, E, f"L2/2 = {ly_n/2:.1f}")
            ax2d.plot([E[0], My[0]], [E[1], My[1]], 'k-', lw=2.5) 
            acotar_linea(E, My, f"L1/2 = {lx_n/2:.1f}")
            
            top_x, top_y = [p[0] for p in P_pts], [p[1] for p in P_pts]
            ax2d.plot(top_x, top_y, 'b-', lw=2.5) 
            
            # Acotar cada tramo del arco azul (Derecha)
            for i in range(len(P_pts) - 1):
                dist_arco = np.linalg.norm(P_pts[i] - P_pts[i+1])
                acotar_linea(P_pts[i], P_pts[i+1], f"{dist_arco:.1f}", color='blue')
            
            ax2d.plot([Mx[0], top_x[0]], [Mx[1], top_y[0]], 'g--', lw=2)
            acotar_linea(Mx, P_pts[0], f"h_x = {h_x:.1f}", color='green')
            ax2d.plot([My[0], top_x[-1]], [My[1], top_y[-1]], 'g--', lw=2)
            acotar_linea(My, P_pts[-1], f"h_y = {h_y:.1f}", color='green')
            
            # Acotar cada generatriz roja (Derecha)
            for i, p in enumerate(P_pts):
                ax2d.plot([E[0], p[0]], [E[1], p[1]], 'r:', lw=1.5, alpha=0.7)
                acotar_linea(E, p, f"[{i+1}] = {vms[i]:.1f}", color='red')
                
            # --- LADO IZQUIERDO (ESPEJO) ---
            E_izq = np.array([-E[0], E[1]])
            My_izq = np.array([-My[0], My[1]])
            P_pts_izq = [np.array([-p[0], p[1]]) for p in P_pts]
            
            ax2d.plot([Mx[0], E_izq[0]], [Mx[1], E_izq[1]], 'k-', lw=2.5)
            acotar_linea(Mx, E_izq, f"L2/2 = {ly_n/2:.1f}")
            ax2d.plot([E_izq[0], My_izq[0]], [E_izq[1], My_izq[1]], 'k-', lw=2.5)
            acotar_linea(E_izq, My_izq, f"L1/2 = {lx_n/2:.1f}")
            
            top_x_m, top_y_m = [p[0] for p in P_pts_izq], [p[1] for p in P_pts_izq]
            ax2d.plot(top_x_m, top_y_m, 'b-', lw=2.5, label='Boca Circular (Fibra Neutra)')
            
            # Acotar cada tramo del arco azul (Izquierda)
            for i in range(len(P_pts_izq) - 1):
                dist_arco = np.linalg.norm(P_pts_izq[i] - P_pts_izq[i+1])
                acotar_linea(P_pts_izq[i], P_pts_izq[i+1], f"{dist_arco:.1f}", color='blue')
            
            ax2d.plot([My_izq[0], top_x_m[-1]], [My_izq[1], top_y_m[-1]], 'g--', lw=2, label='Alturas Oblicuas (h)')
            acotar_linea(My_izq, P_pts_izq[-1], f"h_y = {h_y:.1f}", color='green')
            
            # Acotar cada generatriz roja (Izquierda)
            for i, p in enumerate(P_pts_izq):
                ax2d.plot([E_izq[0], p[0]], [E_izq[1], p[1]], 'r:', lw=1.5, alpha=0.7)
                acotar_linea(E_izq, p, f"[{i+1}] = {vms[i]:.1f}", color='red')
                
            ax2d.text(E[0], E[1]-20, 'ESQUINA', ha='center', color='black', fontsize=11)
            ax2d.text(E_izq[0], E_izq[1]-20, 'ESQUINA', ha='center', color='black', fontsize=11)
            
            ax2d.plot([], [], 'r:', lw=1.5, label='Líneas de Pliegue (VM)')
            ax2d.set_aspect('equal')
            ax2d.axis('off')
            ax2d.legend(loc='lower right')
            st.pyplot(fig2d)

    # --- PESTAÑA: TRANSICIÓN OBLICUA ---
    with tab_oblicua:
        st.header("Transición Oblicua (Tolva Excéntrica / Inclinada)")
        st.markdown("Permite desplazar la boca superior y/o inclinarla. Se asume simetría en el eje Y para generar media plantilla de trazado.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            obl_lx = st.number_input("Lado Base X (L1):", min_value=1.0, value=600.0, step=10.0, key="obl_lx")
            obl_ly = st.number_input("Lado Base Y (L2):", min_value=1.0, value=600.0, step=10.0, key="obl_ly")
            obl_d = st.number_input("Diámetro Boca (D):", min_value=1.0, value=300.0, step=10.0, key="obl_d")
        with col2:
            obl_h = st.number_input("Altura Transición (H):", min_value=1.0, value=400.0, step=10.0, key="obl_h")
            obl_dx = st.number_input("Desplazamiento Boca en X:", value=150.0, step=10.0, key="obl_dx")
            obl_ang = st.number_input("Ángulo de Inclinación Boca (°):", min_value=-80.0, max_value=80.0, value=15.0, step=1.0, key="obl_ang")
        with col3:
            obl_espesor = st.number_input("Espesor (t):", min_value=0.0, value=6.0, step=1.0, key="obl_espesor")
            obl_tipo = st.selectbox("Posición Medidas:", ["Interior", "Exterior", "Neutro"], key="obl_tipo")
            obl_divs = st.selectbox("Divisiones:", [12, 16, 24, 32, 36, 48], index=2, key="obl_divs")
            
        if st.button("Calcular Tolva Oblicua", type="primary", key="btn_obl_calc"):
            # Fibra Neutra
            if obl_tipo == "Interior":
                lx_n, ly_n, d_n = obl_lx + obl_espesor, obl_ly + obl_espesor, obl_d + obl_espesor
            elif obl_tipo == "Exterior":
                lx_n, ly_n, d_n = obl_lx - obl_espesor, obl_ly - obl_espesor, obl_d - obl_espesor
            else:
                lx_n, ly_n, d_n = obl_lx, obl_ly, obl_d
                
            r_n = d_n / 2
            ex, ey = lx_n / 2, ly_n / 2
            phi_rad = math.radians(obl_ang)
            
            # Generar puntos del semicírculo 3D inclinados y desplazados
            M_total = obl_divs // 2
            P_pts_3d = []
            for i in range(M_total + 1):
                ang = i * (math.pi / M_total)
                px = obl_dx + r_n * math.cos(ang) * math.cos(phi_rad)
                py = r_n * math.sin(ang)
                pz = obl_h + r_n * math.cos(ang) * math.sin(phi_rad)
                P_pts_3d.append(np.array([px, py, pz]))
                
            E1 = np.array([ex, ey, 0])
            E2 = np.array([-ex, ey, 0])
            
            M_quad = M_total // 2
            vms_E1 = [np.linalg.norm(P_pts_3d[i] - E1) for i in range(M_quad + 1)]
            vms_E2 = [np.linalg.norm(P_pts_3d[i] - E2) for i in range(M_quad, M_total + 1)]
            
            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 2.5])
            with res_col1:
                st.info(f"**Geometría Modificada:**\nOffset X: {obl_dx} mm\nInclinación: {obl_ang}°")
                st.markdown("**Generatrices desde Esquina Frontal (+X):**")
                df_vm1 = pd.DataFrame({"Línea": [f"[{i+1}]" for i in range(len(vms_E1))], "VM (mm)": [round(v, 1) for v in vms_E1]})
                st.dataframe(df_vm1, use_container_width=True)
                st.markdown("**Generatrices desde Esquina Trasera (-X):**")
                df_vm2 = pd.DataFrame({"Línea": [f"[{i+1}]" for i in range(len(vms_E2))], "VM (mm)": [round(v, 1) for v in vms_E2]})
                st.dataframe(df_vm2, use_container_width=True)
                
            with res_col2:
                fig3d_obl = plt.figure(figsize=(10, 6))
                ax3d = fig3d_obl.add_subplot(111, projection='3d')
                
                ax3d.plot([-ex, ex, ex, -ex, -ex], [-ey, -ey, ey, ey, -ey], [0, 0, 0, 0, 0], 'k-', lw=2)
                theta_full = np.linspace(0, 2*math.pi, obl_divs + 1)
                cx_f = obl_dx + r_n * np.cos(theta_full) * math.cos(phi_rad)
                cy_f = r_n * np.sin(theta_full)
                cz_f = obl_h + r_n * np.cos(theta_full) * math.sin(phi_rad)
                ax3d.plot(cx_f, cy_f, cz_f, 'b-', lw=2)
                
                for i in range(M_quad + 1):
                    ax3d.plot([ex, P_pts_3d[i][0]], [ey, P_pts_3d[i][1]], [0, P_pts_3d[i][2]], 'r--', alpha=0.6)
                for i in range(M_quad, M_total + 1):
                    ax3d.plot([-ex, P_pts_3d[i][0]], [ey, P_pts_3d[i][1]], [0, P_pts_3d[i][2]], 'r--', alpha=0.6)
                
                M1, M2 = np.array([ex, 0, 0]), np.array([-ex, 0, 0])
                ax3d.plot([ex, P_pts_3d[0][0]], [0, P_pts_3d[0][1]], [0, P_pts_3d[0][2]], 'g-', lw=1.5)
                ax3d.plot([-ex, P_pts_3d[-1][0]], [0, P_pts_3d[-1][1]], [0, P_pts_3d[-1][2]], 'g-', lw=1.5)
                
                ax3d.set_title('Modelo Estructural 3D (Tolva Oblicua)')
                ax3d.set_xlabel('Eje X'); ax3d.set_ylabel('Eje Y'); ax3d.set_zlabel('Altura Z')
                lim_ax = max(ex + abs(obl_dx), ey, obl_h)
                ax3d.set_xlim(-lim_ax, lim_ax); ax3d.set_ylim(-lim_ax, lim_ax); ax3d.set_zlim(0, lim_ax)
                st.pyplot(fig3d_obl)

            # DESARROLLO 2D (MESH UNROLLING)
            st.markdown("---")
            st.subheader("Desarrollo Plano de Tolva Oblicua (Media Plantilla)")
            
            seq = []
            seq.append((E1, 0))
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

            # Graficador 2D
            fig2d_obl, ax2d = plt.subplots(figsize=(16, 9))
            
            def acotar_linea_obl(A, B, texto, color='black', fsize=8):
                mid = (A + B) / 2
                dx, dy = B[0] - A[0], B[1] - A[1]
                angle = np.degrees(np.arctan2(dy, dx))
                if angle > 90: angle -= 180
                elif angle < -90: angle += 180
                ax2d.text(mid[0], mid[1], texto, rotation=angle, ha='center', va='center', 
                          fontsize=fsize, color=color, fontweight='bold',
                          bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.85))

            # Dibujar Costuras y acotarlas
            ax2d.plot([pts_2d_bottom[0][0], pts_2d_top[0][0]], [pts_2d_bottom[0][1], pts_2d_top[0][1]], 'g-', lw=2)
            acotar_linea_obl(pts_2d_bottom[0], pts_2d_top[0], f"Costura 1 = {L_init:.1f}", 'green')
            
            ax2d.plot([pts_2d_bottom[-1][0], pts_2d_top[-1][0]], [pts_2d_bottom[-1][1], pts_2d_top[-1][1]], 'g-', lw=2)
            L_end = np.linalg.norm(P_pts_3d[-1] - M2)
            acotar_linea_obl(pts_2d_bottom[-1], pts_2d_top[-1], f"Costura 2 = {L_end:.1f}", 'green')
            
            # Contornos
            bx, by = [p[0] for p in pts_2d_bottom], [p[1] for p in pts_2d_bottom]
            tx, ty = [p[0] for p in pts_2d_top], [p[1] for p in pts_2d_top]
            ax2d.plot(bx, by, 'k-', lw=2.5, label='Base de Tolva')
            ax2d.plot(tx, ty, 'b-', lw=2.5, label='Boca Inclinada/Excéntrica')
            
            # Generatrices (Líneas de pliegue rojas) acotadas
            for l in lines_to_draw:
                ax2d.plot([l[0][0], l[1][0]], [l[0][1], l[1][1]], 'r:', lw=1.5, alpha=0.6)
                dist_pliegue = np.linalg.norm(l[0] - l[1])
                acotar_linea_obl(l[0], l[1], f"{dist_pliegue:.1f}", color='red')
            
            # Acotar tramos del arco superior (azul) para el trazado de compás
            for i in range(len(pts_2d_top) - 1):
                dist_arco = np.linalg.norm(pts_2d_top[i] - pts_2d_top[i+1])
                acotar_linea_obl(pts_2d_top[i], pts_2d_top[i+1], f"{dist_arco:.1f}", color='blue')
            
            # Base Acotada
            acotar_linea_obl(pts_2d_bottom[0], pts_2d_bottom[1], f"Base Y/2 = {ly_n/2:.1f}")
            acotar_linea_obl(pts_2d_bottom[1], pts_2d_bottom[2], f"Base X = {lx_n:.1f}")
            acotar_linea_obl(pts_2d_bottom[2], pts_2d_bottom[3], f"Base Y/2 = {ly_n/2:.1f}")
            
            ax2d.set_title("Plantilla Asimétrica Desarrollada (Media Tolva Oblicua)", fontsize=16)
            ax2d.set_aspect('equal'); ax2d.axis('off')
            st.pyplot(fig2d_obl)
