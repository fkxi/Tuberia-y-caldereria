import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import geometria_tuberias as gt
import geometria_caldereria as gc

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Herramientas de Trazado Industrial", layout="wide")

# ==========================================
# BARRA LATERAL (SIDEBAR) - NAVEGACIÓN
# ==========================================
st.sidebar.title("Menú Principal")
st.sidebar.markdown("Seleccione la rama de trabajo:")
modulo = st.sidebar.radio("Ramas:", ["Tuberías", "Calderería"], key="modulo_main")

st.sidebar.markdown("---")
st.sidebar.info("Desarrollado por Jesus Tasayco.\nAplicativo para cálculos de fabricación y trazado.")

# ==========================================
# MÓDULO 1: TUBERÍAS
# ==========================================
if modulo == "Tuberías":
    st.title("Aplicativo de Trazado y Tuberías")
    st.markdown("Seleccione una herramienta para generar el trazado, fórmulas y plantilla de corte.")

    # Navegación basada en iconos
    herramientas_tub = [
        "🏹 Flecha",
        "📏 Cuerda",
        "⭕ Radio",
        "📐 Generatrices",
        "🐟 Boca de Pescado"
    ]
    tool_tub = st.pills("Herramientas:", herramientas_tub, default=herramientas_tub[0], key="pills_tub", label_visibility="collapsed")
    if not tool_tub:
        tool_tub = herramientas_tub[0]

    st.markdown("---")

    # --- 1. CALCULAR FLECHA ---
    if tool_tub == "🏹 Flecha":
        st.header("Cálculo de la Flecha")
        col1, col2 = st.columns([1, 1])
        with col1:
            radio_f = st.number_input("Radio de la circunferencia (R):", min_value=0.1, value=100.0, step=1.0, key="tub_r_flecha")
            cuerda_f = st.number_input("Longitud de la cuerda (C):", min_value=0.1, value=150.0, step=1.0, key="tub_c_flecha")
            calcular_btn_f = st.button("Calcular y Graficar Flecha", type="primary", key="btn_tub_flecha")

            st.markdown("---")
            st.markdown("##### 📐 Fórmulas Matemáticas:")
            st.latex(r"a = \sqrt{R^2 - \left(\frac{C}{2}\right)^2}")
            st.latex(r"f = R - a")
            st.caption("Donde: **R** = Radio, **C** = Cuerda, **a** = Apotema, **f** = Flecha")

        with col2:
            if calcular_btn_f:
                flecha_f, apotema_f = gt.calcular_flecha(radio_f, cuerda_f)
                if isinstance(apotema_f, str):
                    st.error(apotema_f)
                else:
                    mitad_cuerda = cuerda_f / 2
                    fig1, ax1 = plt.subplots(figsize=(4.8, 4.8))
                    circ = plt.Circle((0, 0), radio_f, color='red', fill=False, linewidth=1.5)
                    ax1.add_artist(circ)
                    ax1.plot([0, mitad_cuerda], [0, apotema_f], color='red', linewidth=1)
                    ax1.plot([0, -mitad_cuerda], [0, apotema_f], color='red', linewidth=1)
                    ax1.plot([-mitad_cuerda, mitad_cuerda], [apotema_f, apotema_f], color='red', linewidth=1.5)
                    ax1.plot([0, 0], [0, apotema_f], color='red', linestyle='--', linewidth=1)
                    ax1.plot([0, 0], [apotema_f, radio_f], color='green', linewidth=3)
                    
                    # Cotas y textos
                    ax1.text(mitad_cuerda/2, apotema_f/2, r'$R$', color='red', fontsize=11)
                    ax1.text(mitad_cuerda/2, apotema_f + (radio_f-apotema_f)/2, r'$C/2$', color='red', fontsize=11)
                    ax1.text(-radio_f*0.06, apotema_f/2, r'$a$', color='red', fontsize=11)
                    ax1.text(radio_f*0.06, apotema_f + flecha_f/2, r'$f$', color='green', fontsize=12, fontweight='bold')
                    
                    ax1.set_aspect('equal')
                    lim_max = radio_f * 1.15
                    ax1.set_xlim(-lim_max, lim_max)
                    ax1.set_ylim(-lim_max, lim_max)
                    ax1.axis('off')
                    fig1.tight_layout()
                    st.pyplot(fig1, use_container_width=True)
                    st.success(f"**Resultados:**\n* **Flecha (f):** `{flecha_f:.2f}`\n* **Apotema (a):** `{apotema_f:.2f}`")

    # --- 2. CALCULAR CUERDA ---
    elif tool_tub == "📏 Cuerda":
        st.header("Cálculo de la Cuerda")
        col1, col2 = st.columns([1, 1])
        with col1:
            radio_c = st.number_input("Radio de la circunferencia (R):", min_value=0.1, value=100.0, step=1.0, key="tub_r_cuerda")
            angulo_c = st.number_input("Ángulo (θ en grados):", min_value=0.1, max_value=360.0, value=90.0, step=1.0, key="tub_a_cuerda")
            calcular_btn_c = st.button("Calcular Cuerda", type="primary", key="btn_tub_cuerda")
            
            st.markdown("---")
            st.markdown("##### 📐 Fórmulas Matemáticas:")
            st.latex(r"\theta_{\text{rad}} = \theta^\circ \cdot \frac{\pi}{180}")
            st.latex(r"C = 2 \cdot R \cdot \sin\left(\frac{\theta_{\text{rad}}}{2}\right)")
            st.latex(r"a = R \cdot \cos\left(\frac{\theta_{\text{rad}}}{2}\right), \quad f = R - a")
            st.caption("Donde: **R** = Radio, **θ** = Ángulo central, **C** = Cuerda, **a** = Apotema, **f** = Flecha")
            
        with col2:
            if calcular_btn_c:
                cuerda_c, radianes = gt.calcular_cuerda(radio_c, angulo_c)
                apotema_c = radio_c * math.cos(radianes / 2)
                flecha_c = radio_c - apotema_c
                
                fig2, ax2 = plt.subplots(figsize=(4.8, 4.8))
                x_arc_c = np.linspace(-radianes/2, radianes/2, 200)
                ax2.plot(radio_c * np.sin(x_arc_c), radio_c * np.cos(x_arc_c), color='red', linewidth=1.5)
                x_r1, y_r1 = radio_c * np.sin(radianes/2), radio_c * np.cos(radianes/2)
                x_r2, y_r2 = radio_c * np.sin(-radianes/2), radio_c * np.cos(-radianes/2)
                ax2.plot([0, x_r1], [0, y_r1], color='red', linewidth=1)
                ax2.plot([0, x_r2], [0, y_r2], color='red', linewidth=1)
                ax2.plot([x_r1, x_r2], [y_r1, y_r2], color='green', linewidth=3)
                
                # Cotas y textos
                ax2.text(x_r1/2, y_r1/2, r'$R$', color='red', fontsize=11)
                ax2.text(0, radio_c*0.2, rf'$\theta = {angulo_c}^\circ$', color='blue', fontsize=11, ha='center')
                ax2.text((x_r1+x_r2)/2, (y_r1+y_r2)/2 + radio_c*0.06, r'$C$', color='green', fontsize=12, fontweight='bold', ha='center')
                
                ax2.set_aspect('equal')
                ax2.axis('off')
                fig2.tight_layout()
                st.pyplot(fig2, use_container_width=True)
                st.success(f"**Resultados:**\n* **Cuerda (C):** `{cuerda_c:.2f}`\n* **Flecha (f):** `{flecha_c:.2f}`\n* **Apotema (a):** `{apotema_c:.2f}`")

    # --- 3. CALCULAR RADIO ---
    elif tool_tub == "⭕ Radio":
        st.header("Cálculo del Radio")
        col1, col2 = st.columns([1, 1])
        with col1:
            cuerda_r = st.number_input("Longitud cuerda (C):", min_value=0.1, value=150.0, step=1.0, key="tub_c_radio")
            flecha_r = st.number_input("Altura flecha (f):", min_value=0.1, value=25.0, step=1.0, key="tub_f_radio")
            calcular_btn_r = st.button("Calcular Radio", type="primary", key="btn_tub_radio")

            st.markdown("---")
            st.markdown("##### 📐 Fórmulas Matemáticas:")
            st.latex(r"R = \frac{f}{2} + \frac{C^2}{8f}")
            st.latex(r"a = R - f")
            st.caption("Donde: **C** = Cuerda, **f** = Flecha, **R** = Radio, **a** = Apotema")

        with col2:
            if calcular_btn_r:
                radio_calc, apotema_calc = gt.calcular_radio_por_flecha(cuerda_r, flecha_r)
                mitad_cuerda_r = cuerda_r / 2
                
                fig3, ax3 = plt.subplots(figsize=(4.8, 4.8))
                circ3 = plt.Circle((0, -apotema_calc), radio_calc, color='blue', fill=False, linestyle=':', linewidth=1)
                ax3.add_artist(circ3)
                ax3.plot([-mitad_cuerda_r, mitad_cuerda_r], [0, 0], color='black', linewidth=2)
                ax3.plot([0, 0], [0, flecha_r], color='green', linewidth=3)
                ax3.plot([0, mitad_cuerda_r], [-apotema_calc, 0], color='red', linewidth=1.5)
                ax3.plot([0, 0], [-apotema_calc, flecha_r], color='red', linestyle='--', linewidth=1)
                
                # Cotas y textos
                ax3.plot(0, -apotema_calc, marker='o', markersize=4, color='red')
                ax3.text(radio_calc*0.05, -apotema_calc*1.05, 'Centro', color='red', fontsize=9)
                ax3.text(mitad_cuerda_r/2, 0.05*radio_calc, r'$C/2$', color='black', fontsize=11)
                ax3.text(0.05*radio_calc, flecha_r/2, r'$f$', color='green', fontsize=12, fontweight='bold')
                ax3.text(mitad_cuerda_r/2, -apotema_calc/2, r'$R$', color='red', fontsize=11)
                ax3.text(-0.08*radio_calc, -apotema_calc/2, r'$a$', color='blue', fontsize=11)
                
                ax3.set_aspect('equal')
                ax3.axis('off')
                fig3.tight_layout()
                st.pyplot(fig3, use_container_width=True)
                st.success(f"**Resultados:**\n* **Radio (R):** `{radio_calc:.2f}`\n* **Apotema (a):** `{apotema_calc:.2f}`")

    # --- 4. GENERATRICES Y PLANTILLA ---
    elif tool_tub == "📐 Generatrices":
        st.header("Cálculo de Generatrices y Plantilla")
        col_in1, col_in2, col_in3 = st.columns(3)
        with col_in1: diametro_g = st.number_input("Diámetro exterior (D):", value=26000.0, step=10.0, key="tub_d_gen")
        with col_in2: cuerda_g = st.number_input("Longitud cuerda (C):", value=500.0, step=10.0, key="tub_c_gen")
        with col_in3: separacion_g = st.number_input("Separación generatrices:", value=83.33, step=1.0, key="tub_s_gen")

        with st.expander("📐 Ver Fórmulas de Generatrices y Plantilla", expanded=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.latex(r"R = \frac{D}{2}, \quad a = \sqrt{R^2 - \left(\frac{C}{2}\right)^2}")
            with f_col2:
                st.latex(r"h(x) = \sqrt{R^2 - x^2} - a, \quad f = R - a")
            st.caption("Donde: **D** = Diámetro exterior, **C** = Cuerda, **x** = Distancia desde el eje central, **h(x)** = Altura de generatriz, **f** = Flecha")
            
        if st.button("Calcular y Graficar Plantilla", type="primary", key="btn_tub_gen"):
            pos_x, alt_h, f_g, a_g, error = gt.calcular_generatrices_tuberia(diametro_g, cuerda_g, separacion_g)
            
            if error:
                st.error(error)
            else:
                mitad_cuerda_g = cuerda_g / 2.0
                fig4, ax4 = plt.subplots(figsize=(10, 4.2))
                x_arc_g = np.linspace(-mitad_cuerda_g, mitad_cuerda_g, 500)
                y_arc_g = np.sqrt((diametro_g/2)**2 - x_arc_g**2) - a_g
                ax4.plot(x_arc_g, y_arc_g, color='blue', linewidth=2.5, label='Arco de tubería')
                ax4.plot([-mitad_cuerda_g, mitad_cuerda_g], [0, 0], color='black', linewidth=2, label='Cuerda base')
                ax4.plot([0, 0], [0, f_g], color='green', linewidth=3, label=f'Flecha central (f={f_g:.2f})')
                
                for i in range(len(pos_x)):
                    px = pos_x[i]
                    ah = alt_h[i]
                    ax4.plot([px, px], [0, ah], color='red', linestyle='--', linewidth=1.2)
                    padding_y = f_g * 0.04
                    ax4.text(px, ah + padding_y, f'{ah:.1f}', color='green', fontsize=8, fontweight='bold', rotation=90, va='bottom', ha='center')
                    if px != 0:
                        ax4.plot([-px, -px], [0, ah], color='red', linestyle='--', linewidth=1.2)
                        ax4.text(-px, ah + padding_y, f'{ah:.1f}', color='green', fontsize=8, fontweight='bold', rotation=90, va='bottom', ha='center')
                
                ax4.set_title("Trazado de Plantilla Física", fontsize=13)
                ax4.set_xlabel("Distancia en la cuerda (x)", fontsize=10)
                ax4.set_ylabel("Altura de generatriz (h)", fontsize=10)
                ax4.grid(True, linestyle=':', alpha=0.6)
                ax4.legend(loc='upper right', fontsize=9)
                ax4.set_aspect('auto')
                fig4.tight_layout()
                st.pyplot(fig4, use_container_width=True)
                
                df_resultados = pd.DataFrame({
                    "Punto": [f"P_{i}" for i in range(len(pos_x))],
                    "Distancia desde centro (X)": [round(val, 2) for val in pos_x],
                    "Altura a cortar (h)": [round(val, 2) for val in alt_h]
                })
                st.dataframe(df_resultados, use_container_width=True)

    # --- 5. BOCA DE PESCADO (GEOMETRÍA PURA) ---
    elif tool_tub == "🐟 Boca de Pescado":
        st.header("Cálculo y Plantilla de Boca de Pescado (Injerto Cilíndrico)")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            d_cabezal = st.number_input(
                "D. EXTERIOR Cabezal (OD mm):", 
                min_value=10.0, value=150.0, step=5.0, key="bp_d1",
                help="Medida exterior del tubo principal/colector."
            )
        with col2:
            d_ramal = st.number_input(
                "D. EXTERIOR Ramal (OD mm):", 
                min_value=10.0, value=150.0, step=5.0, key="bp_d2",
                help="Medida exterior del tubo que se va a cortar/injertar."
            )
        with col3:
            espesor_bp = st.number_input(
                "Espesor Ramal (t mm):", 
                min_value=0.0, value=3.0, step=0.5, key="bp_t",
                help="Espesor de pared para calcular el asiento interior real."
            )
        with col4:
            ang_injerto = st.number_input(
                "Ángulo Injerto (θ°):", 
                min_value=15.0, max_value=90.0, value=90.0, step=5.0, key="bp_ang"
            )
        with col5:
            divs_bp = st.selectbox(
                "Cant. Generatrices:", 
                [12, 16, 24, 32, 36, 48], index=2, key="bp_divs"
            )

        with st.expander("📐 Ver Fórmulas de Boca de Pescado (Intersección Cilíndrica)", expanded=True):
            f1, f2 = st.columns(2)
            with f1:
                st.markdown("**1. Desarrollo del Perímetro:**")
                st.latex(r"P = \pi \cdot D_2, \quad \Delta x = \frac{P}{N}")
                st.caption("P = Perímetro exterior desarrollado, N = Cantidad de divisiones")
            with f2:
                st.markdown("**2. Altura de Corte en cada Generatriz (α) - Asiento Real de Taller:**")
                st.latex(r"y(\alpha) = \frac{R_{\text{int}}(1-\cos\alpha)}{\tan\phi} + \frac{R_1 - \sqrt{R_1^2 - (R_{\text{int}}\sin\alpha)^2}}{\sin\phi}")
                st.caption(r"Donde: $R_1 = D_1 / 2$  y  $R_{\text{int}} = (D_2 / 2) - t$ (espesor pared)")

        if st.button("Calcular y Graficar Boca de Pescado", type="primary", key="btn_bp_calc"):
            res, err = gt.calcular_boca_pescado(d_cabezal, d_ramal, divs_bp, ang_injerto, espesor_bp)
            if err:
                st.error(err)
            else:
                # Tarjetas métricas limpias e intuitivas
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Perímetro (P)", f"{res['perimetro']:.1f} mm")
                m2.metric("Paso (Δx)", f"{res['paso']:.1f} mm")
                m3.metric("Altura maxima", f"{res['max_corte']:.1f} mm")
                m4.metric("D. Interior Ramal (ID)", f"{d_ramal - 2*espesor_bp:.1f} mm")

                # Gráfico 2D de la Plantilla Desenrollada
                fig_bp, ax_bp = plt.subplots(figsize=(10, 4.2))
                x_pts = res['distancias_x']
                y_pts = res['alturas_corte']
                lim_y = max(res['max_corte'], 1.0)
                
                # Curva de corte
                ax_bp.plot(x_pts, y_pts, 'b-', lw=2.5, label='Línea de Corte (Asiento Real de Taller)')
                ax_bp.plot([0, res['perimetro']], [0, 0], 'k-', lw=2, label='Línea Base del Tubo')
                
                # Generatrices punteadas y cotas
                for i in range(len(x_pts)):
                    px = x_pts[i]
                    py = y_pts[i]
                    ax_bp.plot([px, px], [0, py], 'r--', lw=1.2, alpha=0.7)
                    if py > 0.5:
                        ax_bp.text(px, py + lim_y*0.04, f"{py:.1f}", 
                                   color='green', fontsize=8, fontweight='bold', rotation=90, va='bottom', ha='center')
                    # Etiqueta del punto
                    ax_bp.text(px, -lim_y*0.08, f"P{i}", 
                               color='black', fontsize=7, ha='center', va='top')

                ax_bp.set_title(f"Plantilla Plana Desarrollada - Boca de Pescado ({ang_injerto:.0f}°) [Asiento Real de Taller, t={espesor_bp} mm]", fontsize=13)
                ax_bp.set_xlabel("Distancia en el perímetro desenrollado (mm)", fontsize=10)
                ax_bp.set_ylabel("Profundidad de corte (mm) [Asiento de Taller]", fontsize=10)
                ax_bp.set_xlim(-res['paso']*0.5, res['perimetro'] + res['paso']*0.5)
                ax_bp.set_ylim(-lim_y*0.25, lim_y*1.35)
                ax_bp.grid(True, linestyle=':', alpha=0.6)
                ax_bp.legend(loc='upper right', fontsize=9)
                fig_bp.tight_layout()
                st.pyplot(fig_bp, use_container_width=True)

                # Tabla de datos
                df_bp = pd.DataFrame({
                    "Punto": [f"P_{i}" for i in range(len(x_pts))],
                    "Ángulo (°)": res['angulos_deg'],
                    "Distancia en Plantilla X (mm)": x_pts,
                    "Corte Y (mm)": y_pts
                })
                st.dataframe(df_bp, use_container_width=True)

# ==========================================
# MÓDULO 2: CALDERERÍA
# ==========================================
elif modulo == "Calderería":
    st.title("Trazado en Calderería Pesada")
    st.markdown("Generación de plantillas basadas en fibra neutra, triangulación exacta y desarrollo 2D.")

    herramientas_cald = [
        "📦 Transición Recta (Tolva Concéntrica)",
        "📐 Transición Oblicua (Tolva Excéntrica)"
    ]
    tool_cald = st.pills("Herramientas:", herramientas_cald, default=herramientas_cald[0], key="pills_cald", label_visibility="collapsed")
    if not tool_cald:
        tool_cald = herramientas_cald[0]

    st.markdown("---")

    # --- 1. TRANSICIÓN RECTA ---
    if tool_cald == "📦 Transición Recta (Tolva Concéntrica)":
        st.header("Transición Recta (Tolva Concéntrica)")
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

        with st.expander("📐 Ver Fórmulas de Transición Recta (Fibra Neutra y Triangulación)", expanded=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.markdown("**1. Ajuste por Fibra Neutra:**")
                st.latex(r"L_{x,n} = L_x \pm t, \quad L_{y,n} = L_y \pm t, \quad D_n = D \pm t")
                st.markdown("**2. Alturas de caras planas:**")
                st.latex(r"h_x = \sqrt{(L_{x,n}/2 - R_n)^2 + H^2}, \quad h_y = \sqrt{(L_{y,n}/2 - R_n)^2 + H^2}")
            with f_col2:
                st.markdown("**3. Generatrices en Verdadera Magnitud (VM):**")
                st.latex(r"VM(\theta) = \sqrt{\left(\frac{L_{x,n}}{2} - R_n\cos\theta\right)^2 + \left(\frac{L_{y,n}}{2} - R_n\sin\theta\right)^2 + H^2}")
                st.markdown("**4. Triangulación por Ley de Cosenos:**")
                st.latex(r"\cos(\beta) = \frac{VM_i^2 + VM_{i+1}^2 - C_{\text{arco}}^2}{2 \cdot VM_i \cdot VM_{i+1}}")

        btn_transicion = st.button("Calcular Plantilla Recta", type="primary", key="btn_cald_calc")
        
        if btn_transicion:
            res = gc.calcular_desarrollo_recta(lado_x, lado_y, diametro_t, altura_t, espesor, tipo_trazo, divisiones)
            
            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 1.2])
            with res_col1:
                st.info(f"**Fibra Neutra:** Base X = `{res['lx_n']:.1f}` | Base Y = `{res['ly_n']:.1f}` | Diámetro = `{res['d_n']:.1f}`")
                df_vm = pd.DataFrame({
                    "Generatriz (VM)": [f"[{i+1}] a {round(math.degrees(a))}°" for i, a in enumerate(res['angulos_rad'])],
                    "Longitud (mm)": [round(v, 2) for v in res['vms']]
                })
                st.dataframe(df_vm, use_container_width=True)
                
            with res_col2:
                fig3d = plt.figure(figsize=(5.5, 4.0))
                ax3d = fig3d.add_subplot(111, projection='3d')
                ex, ey, r_n = res['ex'], res['ey'], res['r_n']
                ax3d.plot([-ex, ex, ex, -ex, -ex], [-ey, -ey, ey, ey, -ey], [0, 0, 0, 0, 0], 'k-', lw=1.8)
                theta_full = np.linspace(0, 2*np.pi, divisiones + 1)
                ax3d.plot(r_n * np.cos(theta_full), r_n * np.sin(theta_full), np.full_like(theta_full, altura_t), 'b-', lw=1.8)
                
                angulos_totales = np.linspace(0, 2*np.pi, divisiones, endpoint=False)
                for ang in angulos_totales:
                    cx, cy = r_n * np.cos(ang), r_n * np.sin(ang)
                    if 0 <= ang <= np.pi/2: eqx, eqy = ex, ey
                    elif np.pi/2 < ang <= np.pi: eqx, eqy = -ex, ey
                    elif np.pi < ang <= 3*np.pi/2: eqx, eqy = -ex, -ey
                    else: eqx, eqy = ex, -ey
                    ax3d.plot([eqx, cx], [eqy, cy], [0, altura_t], 'r--', alpha=0.45, lw=1)
                
                ax3d.set_title('Modelo Estructural 3D', fontsize=11)
                lim_ax = max(ex, ey, altura_t)
                ax3d.set_xlim(-lim_ax, lim_ax); ax3d.set_ylim(-lim_ax, lim_ax); ax3d.set_zlim(0, altura_t)
                fig3d.tight_layout()
                st.pyplot(fig3d)

            # DESARROLLO 2D
            st.markdown("---")
            st.subheader("Desarrollo Plano de la Chapa (Media Plantilla Acotada)")
            
            def acotar_linea(ax, A, B, texto, color='black', fsize=9):
                mid = (A + B) / 2
                dx, dy = B[0] - A[0], B[1] - A[1]
                angle = np.degrees(np.arctan2(dy, dx))
                if angle > 90: angle -= 180
                elif angle < -90: angle += 180
                ax.text(mid[0], mid[1], texto, rotation=angle, 
                        ha='center', va='center', fontsize=fsize, color=color, fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85))

            fig2d, ax2d = plt.subplots(figsize=(9, 4.8))
            Mx, E, My = res['Mx'], res['E'], res['My']
            E_izq, My_izq = res['E_izq'], res['My_izq']
            P_pts, P_pts_izq = res['P_pts'], res['P_pts_izq']
            h_x, h_y = res['h_x'], res['h_y']
            lx_n, ly_n = res['lx_n'], res['ly_n']

            # Lado derecho
            ax2d.plot([Mx[0], E[0]], [Mx[1], E[1]], 'k-', lw=2.2) 
            acotar_linea(ax2d, Mx, E, f"L2/2 = {ly_n/2:.1f}")
            ax2d.plot([E[0], My[0]], [E[1], My[1]], 'k-', lw=2.2) 
            acotar_linea(ax2d, E, My, f"L1/2 = {lx_n/2:.1f}")
            
            top_x, top_y = [p[0] for p in P_pts], [p[1] for p in P_pts]
            ax2d.plot(top_x, top_y, 'b-', lw=2.2) 
            
            ax2d.plot([Mx[0], top_x[0]], [Mx[1], top_y[0]], 'g--', lw=1.8)
            acotar_linea(ax2d, Mx, P_pts[0], f"h_x = {h_x:.1f}", color='green')
            ax2d.plot([My[0], top_x[-1]], [My[1], top_y[-1]], 'g--', lw=1.8)
            acotar_linea(ax2d, My, P_pts[-1], f"h_y = {h_y:.1f}", color='green')
            
            for p in P_pts:
                ax2d.plot([E[0], p[0]], [E[1], p[1]], 'r:', lw=1.2, alpha=0.7)
                
            # Lado izquierdo (espejo)
            ax2d.plot([Mx[0], E_izq[0]], [Mx[1], E_izq[1]], 'k-', lw=2.2)
            acotar_linea(ax2d, Mx, E_izq, f"L2/2 = {ly_n/2:.1f}")
            ax2d.plot([E_izq[0], My_izq[0]], [E_izq[1], My_izq[1]], 'k-', lw=2.2)
            acotar_linea(ax2d, E_izq, My_izq, f"L1/2 = {lx_n/2:.1f}")
            
            top_x_m, top_y_m = [p[0] for p in P_pts_izq], [p[1] for p in P_pts_izq]
            ax2d.plot(top_x_m, top_y_m, 'b-', lw=2.2, label='Boca Circular (Fibra Neutra)')
            
            ax2d.plot([My_izq[0], top_x_m[-1]], [My_izq[1], top_y_m[-1]], 'g--', lw=1.8, label='Alturas Oblicuas (h)')
            acotar_linea(ax2d, My_izq, P_pts_izq[-1], f"h_y = {h_y:.1f}", color='green')
            
            for p in P_pts_izq:
                ax2d.plot([E_izq[0], p[0]], [E_izq[1], p[1]], 'r:', lw=1.2, alpha=0.7)
                
            ax2d.text(E[0], E[1]-15, 'ESQUINA', ha='center', color='black', fontsize=9, fontweight='bold')
            ax2d.text(E_izq[0], E_izq[1]-15, 'ESQUINA', ha='center', color='black', fontsize=9, fontweight='bold')
            
            ax2d.plot([], [], 'r:', lw=1.2, label='Líneas de Pliegue (VM)')
            ax2d.set_title("Plantilla Simétrica Desarrollada (Media Tolva)", fontsize=12)
            ax2d.set_aspect('equal')
            ax2d.axis('off')
            ax2d.legend(loc='lower right', fontsize=8)
            fig2d.tight_layout()
            st.pyplot(fig2d)

    # --- 2. TRANSICIÓN OBLICUA ---
    elif tool_cald == "📐 Transición Oblicua (Tolva Excéntrica)":
        st.header("Transición Oblicua (Tolva Excéntrica / Inclinada)")
        col1, col2, col3 = st.columns(3)
        with col1:
            obl_lx = st.number_input("Base X:", value=600.0, step=10.0, key="obl_lx")
            obl_ly = st.number_input("Base Y:", value=600.0, step=10.0, key="obl_ly")
            obl_d = st.number_input("Diámetro:", value=300.0, step=10.0, key="obl_d")
        with col2:
            obl_h = st.number_input("Altura (H):", value=400.0, step=10.0, key="obl_h")
            obl_dx = st.number_input("Offset X:", value=150.0, step=10.0, key="obl_dx")
            obl_ang = st.number_input("Ángulo (°):", value=15.0, step=1.0, key="obl_ang")
        with col3:
            obl_espesor = st.number_input("Espesor (t):", value=6.0, step=1.0, key="obl_espesor")
            obl_tipo = st.selectbox("Medidas:", ["Interior", "Exterior", "Neutro"], key="obl_tipo")
            obl_divs = st.selectbox("Divisiones:", [12, 16, 24, 32], index=2, key="obl_divs")

        with st.expander("📐 Ver Fórmulas de Calderería (Fibra Neutra y Triangulación)", expanded=False):
            st.latex(r"L_{n} = L \pm t \quad (\text{Fibra Neutra según posición de medidas})")
            st.latex(r"VM = \sqrt{\Delta x^2 + \Delta y^2 + \Delta z^2} \quad (\text{Verdadera Magnitud por triangulación})")
            
        if st.button("Calcular Tolva Oblicua", type="primary", key="btn_obl_calc"):
            lx_n, ly_n, d_n = gc.calcular_dimensiones_neutras(obl_lx, obl_ly, obl_d, obl_espesor, obl_tipo)
            
            # Cálculos 3D
            P_pts, E1, E2, vms1, vms2, M_quad, M_tot, ex, ey, rn, phi = gc.generar_nodos_3d_oblicua(
                lx_n, ly_n, d_n, obl_h, obl_dx, obl_ang, obl_divs)
            
            # Cálculos 2D
            pts_bot, pts_top, lineas, L_init, M2 = gc.desarrollar_plantilla_oblicua(
                P_pts, E1, E2, ex, M_quad, M_tot)
            
            # Gráfico 2D
            fig2d_obl, ax2d = plt.subplots(figsize=(8.5, 4.5))
            
            # Costuras
            ax2d.plot([pts_bot[0][0], pts_top[0][0]], [pts_bot[0][1], pts_top[0][1]], 'g-', lw=2)
            ax2d.plot([pts_bot[-1][0], pts_top[-1][0]], [pts_bot[-1][1], pts_top[-1][1]], 'g-', lw=2)
            
            # Contornos
            ax2d.plot([p[0] for p in pts_bot], [p[1] for p in pts_bot], 'k-', lw=2.5, label='Base')
            ax2d.plot([p[0] for p in pts_top], [p[1] for p in pts_top], 'b-', lw=2.5, label='Boca')
            
            # Generatrices rojas
            for l in lineas:
                ax2d.plot([l[0][0], l[1][0]], [l[0][1], l[1][1]], 'r:', lw=1.5, alpha=0.6)
            
            ax2d.set_title("Plantilla Asimétrica Desarrollada (Media Tolva Oblicua)")
            ax2d.set_aspect('equal')
            ax2d.axis('off')
            fig2d_obl.tight_layout()
            st.pyplot(fig2d_obl)
