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
        "🐟 Boca de Pescado",
        "✒️ Corte Pluma (Inglete)",
        "🧊 Esquina 3D (3 Tubos a 90°)",
        "🔱 Injerto en Y (Bifurcación)",
        "🔀 Bayonetas (Offsets)",
        "🦐 Codos por Gajos (Virolas)"
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


    # --- 6. CORTE PLUMA (INGLETE / CODO 2 PIEZAS) ---
    elif tool_tub == "✒️ Corte Pluma (Inglete)":
        st.header("Cálculo y Plantilla de Corte Pluma (Inglete / Codo 2 Piezas)")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            d_ext_cp = st.number_input(
                "D. EXTERIOR Tubería (OD mm):", 
                min_value=10.0, value=150.0, step=5.0, key="cp_d",
                help="Diámetro exterior medido de la tubería a cortar."
            )
        with col2:
            tipo_ang_cp = st.selectbox(
                "Definición de Ángulo:", 
                ["Ángulo Unión entre Tubos (ej. 90°)", "Ángulo de Corte de Inglete (ej. 45°)"], 
                key="cp_tipo_ang"
            )
        with col3:
            if "Unión" in tipo_ang_cp:
                ang_val_cp = st.number_input(
                    "Ángulo Total de Desvío (β°):", 
                    min_value=1.0, max_value=170.0, value=90.0, step=5.0, key="cp_ang_val",
                    help="Ángulo total al que se desviará la línea (ej. 90° para codo a escuadra)."
                )
                modo_cp = "union"
            else:
                ang_val_cp = st.number_input(
                    "Ángulo de Corte (θ°):", 
                    min_value=1.0, max_value=85.0, value=45.0, step=2.5, key="cp_ang_val",
                    help="Ángulo de corte respecto a la perpendicular del tubo."
                )
                modo_cp = "corte"
        with col4:
            divs_cp = st.selectbox(
                "Cant. Generatrices:", 
                [12, 16, 24, 32, 36, 48], index=2, key="cp_divs"
            )

        with st.expander("📐 Ver Fórmulas de Corte Pluma (Desarrollo Cilíndrico)", expanded=True):
            f1, f2 = st.columns(2)
            with f1:
                st.markdown("**1. Desarrollo del Perímetro:**")
                st.latex(r"P = \pi \cdot D_{\text{ext}}, \quad \Delta x = \frac{P}{N}")
                st.markdown("**2. Ángulo de corte de inglete:**")
                st.latex(r"\theta = \frac{\beta}{2} \quad (\text{para unión a } 90^\circ, \theta = 45^\circ)")
            with f2:
                st.markdown("**3. Altura de corte en generatriz (α):**")
                st.latex(r"y(\alpha) = R \cdot \tan(\theta) \cdot (1 - \cos\alpha)")
                st.caption("Donde: R = D/2, α = ángulo generatriz (0° a 360°), y = altura desde línea base.")

        if st.button("Calcular y Graficar Corte Pluma", type="primary", key="btn_cp_calc"):
            res, err = gt.calcular_corte_pluma(d_ext_cp, ang_val_cp, divs_cp, modo_cp)
            if err:
                st.error(err)
            else:
                # Métricas limpias e intuitivas
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Perímetro a enrollar (P)", f"{res['perimetro']:.1f} mm")
                m2.metric("Paso generatrices (Δx)", f"{res['paso']:.1f} mm")
                m3.metric("Caída máx. corte (H)", f"{res['max_corte']:.1f} mm")
                m4.metric("Eje mayor corte (elipse)", f"{res['eje_mayor_elipse']:.1f} mm")

                # Gráfico 2D de la Plantilla
                fig_cp, ax_cp = plt.subplots(figsize=(10, 4.2))
                x_pts = res['distancias_x']
                y_pts = res['alturas_corte']
                lim_y = max(res['max_corte'], 1.0)

                ax_cp.plot(x_pts, y_pts, 'b-', lw=2.5, label=f"Línea de Corte Pluma (θ = {res['angulo_corte']:.1f}°)")
                ax_cp.plot([0, res['perimetro']], [0, 0], 'k-', lw=2, label='Línea Base del Tubo (Talón = 0)')

                for i in range(len(x_pts)):
                    px = x_pts[i]
                    py = y_pts[i]
                    ax_cp.plot([px, px], [0, py], 'r--', lw=1.2, alpha=0.7)
                    if py > 0.5:
                        ax_cp.text(px, py + lim_y * 0.04, f"{py:.1f}",
                                   color='green', fontsize=8, fontweight='bold', rotation=90, va='bottom', ha='center')
                    ax_cp.text(px, -lim_y * 0.08, f"P{i}",
                               color='black', fontsize=7, ha='center', va='top')

                ax_cp.set_title(f"Plantilla Plana Desarrollada - Corte Pluma / Inglete (Unión {res['angulo_union']:.0f}°, Corte {res['angulo_corte']:.1f}°)", fontsize=13)
                ax_cp.set_xlabel("Distancia en el perímetro desarrollado (mm)", fontsize=10)
                ax_cp.set_ylabel("Altura de corte (mm)", fontsize=10)
                ax_cp.set_xlim(-res['paso'] * 0.5, res['perimetro'] + res['paso'] * 0.5)
                ax_cp.set_ylim(-lim_y * 0.25, lim_y * 1.35)
                ax_cp.grid(True, linestyle=':', alpha=0.6)
                ax_cp.legend(loc='upper right', fontsize=9)
                fig_cp.tight_layout()
                st.pyplot(fig_cp, use_container_width=True)

                # Tabla de datos
                df_cp = pd.DataFrame({
                    "Punto": [f"P_{i}" for i in range(len(x_pts))],
                    "Ángulo Generatriz (°)": res['angulos_deg'],
                    "Distancia en Plantilla X (mm)": x_pts,
                    "Altura de Corte Y (mm)": y_pts
                })
                st.dataframe(df_cp, use_container_width=True)


    # --- 7. ESQUINA 3D (TRES TUBOS A 90° / PRODUCTO VECTORIAL) ---
    elif tool_tub == "🧊 Esquina 3D (3 Tubos a 90°)":
        st.header("Cálculo de Esquina 3D / Nudo de 3 Tuberías a 90°")
        st.markdown(
            "Cálculo del corte para estructuras tubulares donde convergen 3 tubos: dos en el plano horizontal "
            "a 90° (corte pluma) y un tercer tubo perpendicular vertical en la dirección normal."
        )

        col_conf1, col_conf2 = st.columns(2)
        with col_conf1:
            modo_nudo = st.selectbox(
                "Tipo de Nudo Estructural:",
                [
                    "Triple Inglete Simétrico (Los 3 tubos convergen en el vértice a 90°)",
                    "Pilar Perpendicular Montado sobre Codo a 90° (Asiento a horcajadas)"
                ],
                key="esq_modo"
            )
        with col_conf2:
            divs_esq = st.selectbox(
                "Cant. Generatrices:",
                [12, 16, 24, 32, 36, 48],
                index=2,
                key="esq_divs"
            )

        if "Triple Inglete" in modo_nudo:
            tipo_param = "triple_inglete"
            col1, col2 = st.columns(2)
            with col1:
                d_ext_esq = st.number_input(
                    "D. EXTERIOR Tuberías (OD mm):",
                    min_value=10.0, value=150.0, step=5.0, key="esq_d",
                    help="Diámetro exterior común para los 3 tubos del nudo."
                )
            with col2:
                st.info(
                    "💡 **Propiedad de Simetría 3D:** En un nudo tri-rectángulo a 90°, "
                    "los 3 tubos llevan **exactamente la misma plantilla de corte doble a 45°** "
                    "(corte pluma en el plano + corte vertical)."
                )
            d_codo_val = None
            esp_val = 0.0
        else:
            tipo_param = "injerto_sobre_codo"
            col1, col2, col3 = st.columns(3)
            with col1:
                d_ext_esq = st.number_input(
                    "D. EXTERIOR Tubo Perpendicular/Pilar (OD mm):",
                    min_value=10.0, value=150.0, step=5.0, key="esq_dp",
                    help="Diámetro del tubo que sale perpendicularmente."
                )
            with col2:
                d_codo_val = st.number_input(
                    "D. EXTERIOR Tubos del Codo Base (OD mm):",
                    min_value=10.0, value=150.0, step=5.0, key="esq_dc",
                    help="Diámetro de los dos tubos que forman el codo a 90°."
                )
            with col3:
                esp_val = st.number_input(
                    "Espesor Pilar (t mm):",
                    min_value=0.0, value=3.0, step=0.5, key="esq_t",
                    help="Espesor de pared para el asiento interior real de taller."
                )

        with st.expander("📐 Ver Fórmulas Matemáticas de Esquina 3D", expanded=True):
            f1, f2 = st.columns(2)
            with f1:
                st.markdown("**1. Desarrollo del Perímetro:**")
                st.latex(r"P = \pi \cdot D_{\text{ext}}, \quad \Delta x = \frac{P}{N}")
                st.markdown("**2. Planos de corte en el triedro 3D (X, Y, Z):**")
                st.latex(r"z_1 = x = R\cos\alpha \quad (45^\circ \text{ con eje } X)")
                st.latex(r"z_2 = y = R\sin\alpha \quad (45^\circ \text{ con eje } Y)")
            with f2:
                if tipo_param == "triple_inglete":
                    st.markdown("**3. Arista de encuentro y altura máxima:**")
                    st.latex(r"y(\alpha) = z(\alpha) - z_{\text{mín}} = z(\alpha) + R\frac{\sqrt{2}}{2}")
                    st.latex(r"H_{\text{máx}} = R\left(1 + \frac{\sqrt{2}}{2}\right) \approx 0.8536 \cdot D_{\text{ext}}")
                    st.caption("Crestas a 0° y 90°, arista de encuentro a 45° y talón interior a 225°.")
                else:
                    st.markdown("**3. Asiento a horcajadas sobre costura de codo a 90°:**")
                    st.latex(r"y(\alpha) = R_{\text{codo}} - \sqrt{R_{\text{codo}}^2 - (R_{\text{int}} \cdot \cos\alpha)^2}")
                    st.caption(r"Donde $R_{\text{int}} = R_{\text{pilar}} - t$ (asiento interior real sobre el codo).")

        if st.button("Calcular y Graficar Esquina 3D", type="primary", key="btn_esq_calc"):
            res, err = gt.calcular_esquina_3d(d_ext_esq, divs_esq, tipo_param, d_codo_val, esp_val)
            if err:
                st.error(err)
            else:
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Perímetro a enrollar (P)", f"{res['perimetro']:.1f} mm")
                m2.metric("Paso generatrices (Δx)", f"{res['paso']:.1f} mm")
                m3.metric("Caída máx. corte (H)", f"{res['max_corte']:.1f} mm")
                if tipo_param == "triple_inglete":
                    m4.metric("Altura arista a 45°", f"{res['h_arista_45']:.1f} mm")
                else:
                    m4.metric("D. Interior Pilar (ID)", f"{d_ext_esq - 2*esp_val:.1f} mm")

                # Gráfico 2D
                fig_esq, ax_esq = plt.subplots(figsize=(10, 4.4))
                x_pts = res['distancias_x']
                y_pts = res['alturas_corte']
                lim_y = max(res['max_corte'], 1.0)

                ax_esq.plot(x_pts, y_pts, 'b-', lw=2.5, label='Línea de Corte 3D')
                ax_esq.plot([0, res['perimetro']], [0, 0], 'k-', lw=2, label='Línea Base del Tubo')

                for i in range(len(x_pts)):
                    px = x_pts[i]
                    py = y_pts[i]
                    ax_esq.plot([px, px], [0, py], 'r--', lw=1.2, alpha=0.7)
                    if py > 0.5:
                        ax_esq.text(px, py + lim_y * 0.04, f"{py:.1f}",
                                    color='green', fontsize=8, fontweight='bold', rotation=90, va='bottom', ha='center')
                    ax_esq.text(px, -lim_y * 0.08, f"P{i}",
                                color='black', fontsize=7, ha='center', va='top')

                ax_esq.set_title(f"Plantilla Plana Desarrollada - {res['descripcion']}", fontsize=13)
                ax_esq.set_xlabel("Distancia en el perímetro desarrollado (mm)", fontsize=10)
                ax_esq.set_ylabel("Altura de corte (mm)", fontsize=10)
                ax_esq.set_xlim(-res['paso'] * 0.5, res['perimetro'] + res['paso'] * 0.5)
                ax_esq.set_ylim(-lim_y * 0.25, lim_y * 1.35)
                ax_esq.grid(True, linestyle=':', alpha=0.6)
                ax_esq.legend(loc='upper right', fontsize=9)
                fig_esq.tight_layout()
                st.pyplot(fig_esq, use_container_width=True)

                # Tabla de datos
                df_esq = pd.DataFrame({
                    "Punto": [f"P_{i}" for i in range(len(x_pts))],
                    "Ángulo Generatriz (°)": res['angulos_deg'],
                    "Distancia en Plantilla X (mm)": x_pts,
                    "Altura de Corte Y (mm)": y_pts
                })
                st.dataframe(df_esq, use_container_width=True)


    # --- 8. INJERTO EN Y / BIFURCACIÓN LATERAL ---
    elif tool_tub == "🔱 Injerto en Y (Bifurcación)":
        st.header("Cálculo y Plantilla de Injerto en 'Y' / Bifurcación Lateral")
        st.markdown(
            "Trazado analítico de ramal oblicuo a 30°, 45°, 60° o ángulo personalizado sobre cabezal principal. "
            "Incluye compensación por espesor para asiento interior real y plantilla del orificio en el colector."
        )

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            d_cab_y = st.number_input(
                "D. EXTERIOR Cabezal (OD mm):",
                min_value=10.0, value=150.0, step=5.0, key="y_dc",
                help="Diámetro exterior del tubo colector principal."
            )
        with col2:
            d_ram_y = st.number_input(
                "D. EXTERIOR Ramal (OD mm):",
                min_value=10.0, value=150.0, step=5.0, key="y_dr",
                help="Diámetro exterior del tubo ramal oblicuo."
            )
        with col3:
            ang_y = st.selectbox(
                "Ángulo de Inclinación (θ°):",
                [45.0, 30.0, 60.0, "Personalizado"],
                index=0,
                key="y_ang_sel"
            )
            if ang_y == "Personalizado":
                ang_y_val = st.number_input("Ángulo Custom (°):", min_value=15.0, max_value=85.0, value=45.0, step=1.0, key="y_ang_custom")
            else:
                ang_y_val = float(ang_y)
        with col4:
            esp_y = st.number_input(
                "Espesor Ramal (t mm):",
                min_value=0.0, value=4.5, step=0.5, key="y_esp",
                help="Espesor de pared del ramal para evitar filos de cuchillo."
            )
        with col5:
            divs_y = st.selectbox(
                "Cant. Generatrices:",
                [16, 24, 32, 48],
                index=1,
                key="y_divs"
            )

        with st.expander("📐 Ver Fórmulas de Injerto en Y / Ramal Oblicuo", expanded=True):
            f1, f2 = st.columns(2)
            with f1:
                st.markdown("**1. Desarrollo del Perímetro:**")
                st.latex(r"P = \pi \cdot D_{\text{ramal}}, \quad \Delta x = \frac{P}{N}")
                st.markdown("**2. Altura de corte en generatriz (α) - Asiento Real:**")
                st.latex(r"y(\alpha) = \frac{r_{\text{int}}(1-\cos\alpha)}{\tan\phi} + \frac{R_c - \sqrt{R_c^2 - (r_{\text{int}}\sin\alpha)^2}}{\sin\phi}")
                st.caption(r"Donde: $\phi$ = ángulo con eje del cabezal, $r_{\text{int}} = (D_{\text{ramal}}/2) - t$")
            with f2:
                st.markdown("**3. Orificio Desenrollado en Cabezal (Desfonde):**")
                st.latex(r"y_{\text{arco}}(\alpha) = R_c \cdot \arcsin\left(\frac{r_{\text{int}}\sin\alpha}{R_c}\right)")
                st.latex(r"x_{\text{long}}(\alpha) = \frac{r_{\text{int}}\cos\alpha}{\sin\phi} - \frac{R_c - \sqrt{R_c^2 - (r_{\text{int}}\sin\alpha)^2}}{\tan\phi}")
                st.caption("Cálculo exacto para marcar el recorte en el tubo cabezal sin holguras.")

        if st.button("Calcular y Graficar Injerto en Y", type="primary", key="btn_y_calc"):
            res, err = gt.calcular_injerto_y(d_cab_y, d_ram_y, ang_y_val, esp_y, divs_y)
            if err:
                st.error(err)
            else:
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Perímetro Ramal (P)", f"{res['perimetro_ramal']:.1f} mm")
                m2.metric("Paso generatrices (Δx)", f"{res['paso_ramal']:.1f} mm")
                m3.metric("Caída máx. Ramal (H)", f"{res['max_corte']:.1f} mm")
                m4.metric("Orificio Cabezal (L × A)", f"{res['long_orificio']:.1f} × {res['ancho_orificio']:.1f} mm")

                tab_ramal, tab_orificio = st.tabs([
                    "📐 Plantilla del Ramal Oblicuo (Tubo a Injertar)",
                    "⭕ Plantilla del Orificio en Cabezal (Desfonde del Colector)"
                ])

                with tab_ramal:
                    fig_y, ax_y = plt.subplots(figsize=(10, 4.4))
                    x_pts = res['distancias_x_ramal']
                    y_pts = res['alturas_ramal_int']
                    lim_y = max(res['max_corte'], 1.0)

                    ax_y.plot(x_pts, y_pts, 'b-', lw=2.5, label=f"Asiento Interior Real (θ = {ang_y_val:.0f}°)")
                    if esp_y > 0:
                        ax_y.plot(x_pts, res['alturas_ramal_ext'], 'g--', lw=1.5, label='Referencia Exterior (Bisel)')
                    ax_y.plot([0, res['perimetro_ramal']], [0, 0], 'k-', lw=2, label='Línea Base del Tubo (Talón = 0)')

                    for i in range(len(x_pts)):
                        px = x_pts[i]
                        py = y_pts[i]
                        ax_y.plot([px, px], [0, py], 'r--', lw=1.1, alpha=0.6)
                        if py > 0.5:
                            ax_y.text(px, py + lim_y * 0.04, f"{py:.1f}",
                                      color='green', fontsize=8, fontweight='bold', rotation=90, va='bottom', ha='center')
                        ax_y.text(px, -lim_y * 0.08, f"P{i}",
                                  color='black', fontsize=7, ha='center', va='top')

                    ax_y.set_title(f"Plantilla Plana Desarrollada - Ramal Oblicuo a {ang_y_val:.0f}° [t={esp_y} mm]", fontsize=13)
                    ax_y.set_xlabel("Distancia en el perímetro desarrollado del ramal (mm)", fontsize=10)
                    ax_y.set_ylabel("Profundidad de corte (mm)", fontsize=10)
                    ax_y.set_xlim(-res['paso_ramal'] * 0.5, res['perimetro_ramal'] + res['paso_ramal'] * 0.5)
                    ax_y.set_ylim(-lim_y * 0.25, lim_y * 1.35)
                    ax_y.grid(True, linestyle=':', alpha=0.6)
                    ax_y.legend(loc='upper right', fontsize=9)
                    fig_y.tight_layout()
                    st.pyplot(fig_y, use_container_width=True)

                    df_y = pd.DataFrame({
                        "Punto": [f"P_{i}" for i in range(len(x_pts))],
                        "Ángulo Generatriz (°)": res['angulos_deg'],
                        "Distancia en Plantilla X (mm)": x_pts,
                        "Corte Interior Real Y (mm)": y_pts,
                        "Corte Exterior Bisel Y (mm)": res['alturas_ramal_ext']
                    })
                    st.dataframe(df_y, use_container_width=True)

                with tab_orificio:
                    fig_orf, ax_orf = plt.subplots(figsize=(8.5, 4.4))
                    ox = res['orificio_x']
                    oy = res['orificio_y_arco']

                    ox_plot = ox + [ox[0]]
                    oy_plot = oy + [oy[0]]

                    ax_orf.plot(ox_plot, oy_plot, 'm-', lw=2.5, label='Contorno del Orificio')
                    ax_orf.scatter(ox[:-1], oy[:-1], color='red', s=25, zorder=5)

                    for i in range(len(ox) - 1):
                        ax_orf.text(ox[i], oy[i] + 3, f"P{i}", fontsize=7, ha='center', color='black')

                    ax_orf.axhline(0, color='gray', linestyle=':', lw=1)
                    ax_orf.axvline(0, color='gray', linestyle=':', lw=1)
                    ax_orf.set_title(f"Plantilla de Corte del Orificio en Cabezal (Desfonde para Ramal a {ang_y_val:.0f}°)", fontsize=13)
                    ax_orf.set_xlabel("Eje Longitudinal del Cabezal X (mm)", fontsize=10)
                    ax_orf.set_ylabel("Desarrollo en Circunferencia Y (mm)", fontsize=10)
                    ax_orf.set_aspect('equal')
                    ax_orf.grid(True, linestyle=':', alpha=0.6)
                    ax_orf.legend(loc='upper right', fontsize=9)
                    fig_orf.tight_layout()
                    st.pyplot(fig_orf, use_container_width=True)

                    df_orf = pd.DataFrame({
                        "Punto": [f"P_{i}" for i in range(len(ox))],
                        "Ángulo Generatriz (°)": res['angulos_deg'],
                        "Desplazamiento Long. X (mm)": ox,
                        "Arco en Cabezal Y (mm)": oy
                    })
                    st.dataframe(df_orf, use_container_width=True)


    # --- 9. BAYONETAS Y DESPLAZAMIENTOS (PIPE OFFSETS - TODAS LAS VERSIONES) ---
    elif tool_tub == "🔀 Bayonetas (Offsets)":
        st.header("Cálculo Integral de Bayonetas y Desplazamientos (Pipe Offsets)")
        st.markdown(
            "Cálculo trigonométrico y de montaje para desplazamientos en 2D, bayonetas giradas en 3D (*Rolling Offsets*), "
            "puentes de cruce y bancos de tuberías paralelas (*Pipe Racks*), con descuentos normativos de codos **ASME B16.9**."
        )

        sub_bayoneta = st.radio(
            "Seleccione la versión de Bayoneta:",
            [
                "📐 1. Bayoneta Simple 2D (Un Plano)",
                "🧊 2. Bayoneta Girada 3D (Rolling Offset)",
                "🚧 3. Puente / Salto de Obstáculo (4 Codos)",
                "📏 4. Bayonetas Paralelas en Pipe Rack (Equal Spread)"
            ],
            horizontal=True,
            key="sub_bay_radio"
        )
        st.markdown("---")

        lista_nps = list(gt.CATALOGO_TUBERIAS_ASME.keys())
        idx_nps_default = lista_nps.index('4"') if '4"' in lista_nps else 8

        # ==========================================================
        # SUB-APARTADO 1: BAYONETA SIMPLE 2D
        # ==========================================================
        if "1. Bayoneta Simple 2D" in sub_bayoneta:
            st.subheader("Bayoneta Simple 2D en un Plano")
            col1, col2, col3 = st.columns(3)
            with col1:
                modo_2d = st.selectbox(
                    "Variables Conocidas:",
                    ["Desplazamiento (O) y Ángulo de Codo (θ)", "Desplazamiento (O) y Avance Proyectado (A)"],
                    key="b2d_modo"
                )
                desp_2d = st.number_input("Desplazamiento / Altura (O mm):", min_value=10.0, value=500.0, step=10.0, key="b2d_o")
            with col2:
                if "Ángulo" in modo_2d:
                    ang_sel_2d = st.selectbox("Ángulo de Codos (θ°):", [45.0, 30.0, 60.0, 22.5, "Personalizado"], index=0, key="b2d_ang_sel")
                    if ang_sel_2d == "Personalizado":
                        val_sec_2d = st.number_input("Ángulo Custom (θ°):", min_value=5.0, max_value=85.0, value=37.5, step=0.5, key="b2d_ang_c")
                    else:
                        val_sec_2d = float(ang_sel_2d)
                    modo_param_2d = "angulo"
                else:
                    val_sec_2d = st.number_input("Avance Longitudinal Disponible (A mm):", min_value=10.0, value=500.0, step=10.0, key="b2d_a")
                    modo_param_2d = "avance"
                nps_2d = st.selectbox("Diámetro Nominal (NPS ASME):", lista_nps, index=idx_nps_default, key="b2d_nps")
            with col3:
                radio_2d = st.selectbox("Tipo de Codo ASME B16.9:", ["LR (Radio Largo 1.5D)", "SR (Radio Corto 1.0D)", "3D", "Sin descuento (Eje a Eje)"], key="b2d_rad")
                luz_2d = st.number_input("Luz de Raíz Soldadura (g mm):", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="b2d_luz")

            with st.expander("📐 Ver Fórmulas de Bayoneta 2D y Descuento ASME B16.9", expanded=True):
                f1, f2 = st.columns(2)
                with f1:
                    st.markdown("**1. Trigonometría de Ejes (Centro a Centro):**")
                    st.latex(r"T = \frac{O}{\sin\theta} = \sqrt{O^2 + A^2}, \quad A = \frac{O}{\tan\theta}")
                    st.caption("Para 45°: T = O × 1.4142  |  Para 30°: T = O × 2.0000  |  Para 60°: T = O × 1.1547")
                with f2:
                    st.markdown("**2. Descuento de Codos y Niple Neto de Corte:**")
                    st.latex(r"E = R_c \cdot \tan\left(\frac{\theta}{2}\right), \quad L_{\text{niple}} = T - 2E - 2g")
                    st.caption(r"Donde $R_c = 1.5 \times \text{NPS}$ (Radio Largo) y $g$ = abertura de raíz para soldadura.")

            if st.button("Calcular Bayoneta 2D", type="primary", key="btn_b2d"):
                res, err = gt.calcular_bayoneta_2d(desp_2d, val_sec_2d, modo_param_2d, nps_2d, radio_2d, luz_2d)
                if err:
                    st.error(err)
                else:
                    dc = res["datos_codo"]
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Recorrido Eje a Eje (T)", f"{res['recorrido_t']:.1f} mm")
                    m2.metric("Niple Neto a Cortar (L)", f"{res['niple_neto']:.1f} mm")
                    m3.metric("Avance Proyectado (A)", f"{res['avance_a']:.1f} mm")
                    m4.metric("Ángulo Codo / Avance E", f"{res['angulo_codo']:.1f}° / {dc['avance_codo']:.1f} mm")

                    if res["codo_a_codo_alerta"]:
                        st.warning("⚠️ **Alerta de Taller:** El descuento de los dos codos supera el recorrido centro a centro (T). Los codos se traslapan; reduzca el ángulo o use codos de Radio Corto (SR).")

                    # Gráfico 2D
                    fig_b2, ax_b2 = plt.subplots(figsize=(9.5, 4.2))
                    A_val = res["avance_a"]
                    O_val = res["desplazamiento_o"]
                    T_val = res["recorrido_t"]
                    tramo_recto = max(A_val * 0.45, 150.0)

                    # Coordenadas de la línea de tubería
                    x_pipe = [-tramo_recto, 0, A_val, A_val + tramo_recto]
                    y_pipe = [0, 0, O_val, O_val]

                    ax_b2.plot(x_pipe, y_pipe, 'b-', lw=5, alpha=0.85, label=f'Eje de Tubería ({nps_2d} - OD {dc["od_mm"]} mm)')
                    ax_b2.scatter([0, A_val], [0, O_val], color='red', s=70, zorder=5, label='Vértices Centro de Codo')

                    # Triángulo de referencia
                    ax_b2.plot([0, A_val], [0, 0], 'k--', lw=1.3)
                    ax_b2.plot([A_val, A_val], [0, O_val], 'g--', lw=1.5)

                    # Etiquetas
                    ax_b2.text(A_val / 2, -O_val * 0.09, f"Avance A = {A_val:.1f} mm", ha='center', va='top', fontsize=10, fontweight='bold')
                    ax_b2.text(A_val + tramo_recto * 0.08, O_val / 2, f"Desplazamiento\nO = {O_val:.1f} mm", ha='left', va='center', color='green', fontsize=10, fontweight='bold')
                    ang_rot = math.degrees(math.atan2(O_val, A_val))
                    ax_b2.text(A_val / 2, O_val / 2 + O_val * 0.07, f"T = {T_val:.1f} mm\n(Niple L = {res['niple_neto']:.1f} mm)",
                               ha='center', va='bottom', rotation=ang_rot, color='darkblue', fontsize=9, fontweight='bold',
                               bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="blue", alpha=0.85))
                    ax_b2.text(A_val * 0.16, O_val * 0.05, f"θ = {res['angulo_codo']:.1f}°", color='red', fontsize=10, fontweight='bold')

                    ax_b2.set_title(f"Esquema Técnico de Bayoneta Simple 2D - Tubería {nps_2d}", fontsize=12)
                    ax_b2.set_aspect('equal')
                    ax_b2.grid(True, linestyle=':', alpha=0.6)
                    ax_b2.legend(loc='upper left', fontsize=9)
                    fig_b2.tight_layout()
                    st.pyplot(fig_b2, use_container_width=True)

                    df_b2 = pd.DataFrame({
                        "Parámetro de Fabricación y Montaje": [
                            "Diámetro Nominal (NPS) / Diámetro Exterior (OD)",
                            "Ángulo de Trabajo de los Codos (θ)",
                            "Desplazamiento Perpendicular (O - Offset)",
                            "Avance Longitudinal Proyectado (A - Run)",
                            "Recorrido Diagonal Centro a Centro (T - Travel)",
                            "Radio Central del Codo (Rc ASME B16.9)",
                            "Avance / Descuento por 1 Codo (E)",
                            "Descuento Total (2 Codos + 2 Luces de Raíz)",
                            "LONGITUD NETA DE CORTE DEL NIPLE (L)",
                            "Degradado de Codo: Arco Interior (Intradós)",
                            "Degradado de Codo: Arco Neutro (Centro)",
                            "Degradado de Codo: Arco Exterior (Lomo / Extradós)"
                        ],
                        "Valor Calculado": [
                            f"{nps_2d} ({dc['od_mm']} mm)",
                            f"{res['angulo_codo']:.2f}°",
                            f"{res['desplazamiento_o']:.1f} mm",
                            f"{res['avance_a']:.1f} mm",
                            f"{res['recorrido_t']:.1f} mm",
                            f"{dc['rc_mm']:.1f} mm",
                            f"{dc['avance_codo']:.1f} mm",
                            f"{dc['descuento_total_niple']:.1f} mm",
                            f"{res['niple_neto']:.1f} mm",
                            f"{dc['arco_intrados']:.1f} mm",
                            f"{dc['arco_centro']:.1f} mm",
                            f"{dc['arco_extrados']:.1f} mm"
                        ]
                    })
                    st.dataframe(df_b2, use_container_width=True, hide_index=True)

        # ==========================================================
        # SUB-APARTADO 2: BAYONETA GIRADA 3D (ROLLING OFFSET)
        # ==========================================================
        elif "2. Bayoneta Girada 3D" in sub_bayoneta:
            st.subheader("Bayoneta Girada en 3D (Rolling Offset)")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                desp_h = st.number_input("Desplazamiento Horizontal (H / Roll mm):", min_value=0.0, value=300.0, step=10.0, key="b3d_h")
                desp_v = st.number_input("Desplazamiento Vertical (V / Set mm):", min_value=0.0, value=400.0, step=10.0, key="b3d_v")
            with col2:
                modo_3d = st.selectbox(
                    "Criterio Longitudinal:",
                    ["Por Ángulo de Codo Comercial (θ)", "Por Avance Longitudinal Fijo (A)"],
                    key="b3d_modo"
                )
                if "Ángulo" in modo_3d:
                    ang_sel_3d = st.selectbox("Ángulo Codos (θ°):", [45.0, 30.0, 60.0, "Personalizado"], index=0, key="b3d_ang_s")
                    if ang_sel_3d == "Personalizado":
                        val_sec_3d = st.number_input("Ángulo Custom (θ°):", min_value=5.0, max_value=85.0, value=45.0, step=0.5, key="b3d_ang_c")
                    else:
                        val_sec_3d = float(ang_sel_3d)
                    modo_param_3d = "angulo"
                else:
                    val_sec_3d = st.number_input("Avance Longitudinal Fijo (A mm):", min_value=10.0, value=500.0, step=10.0, key="b3d_a")
                    modo_param_3d = "avance"
            with col3:
                nps_3d = st.selectbox("Diámetro Nominal (NPS ASME):", lista_nps, index=idx_nps_default, key="b3d_nps")
                radio_3d = st.selectbox("Tipo de Codo ASME B16.9:", ["LR (Radio Largo 1.5D)", "SR (Radio Corto 1.0D)", "3D", "Sin descuento (Eje a Eje)"], key="b3d_rad")
            with col4:
                luz_3d = st.number_input("Luz de Raíz Soldadura (g mm):", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="b3d_luz")
                st.info("💡 **Tip de Montaje:** El **Arco de Giro (S)** te indica cuántos milímetros desplazar el centro del codo sobre el lomo del tubo usando la huincha.")

            with st.expander("📐 Ver Fórmulas de Bayoneta Girada 3D (Abatimiento Espacial)", expanded=True):
                f1, f2 = st.columns(2)
                with f1:
                    st.markdown("**1. Triángulo Frontal y Giro del Codo:**")
                    st.latex(r"D = \sqrt{H^2 + V^2}, \quad \alpha_{\text{vertical}} = \arctan\left(\frac{H}{V}\right)")
                    st.latex(r"S_{\text{giro}} = \frac{OD}{2} \cdot \alpha_{\text{rad}} \quad (\text{Arco en periferia del tubo})")
                with f2:
                    st.markdown("**2. Triángulo en Verdadera Magnitud (3D):**")
                    st.latex(r"T = \frac{D}{\sin\theta} = \sqrt{H^2 + V^2 + A^2}, \quad A = \frac{D}{\tan\theta}")
                    st.latex(r"L_{\text{niple}} = T - 2 R_c \tan\left(\frac{\theta}{2}\right) - 2g")

            if st.button("Calcular y Graficar Bayoneta 3D", type="primary", key="btn_b3d"):
                res, err = gt.calcular_bayoneta_3d(desp_h, desp_v, val_sec_3d, modo_param_3d, nps_3d, radio_3d, luz_3d)
                if err:
                    st.error(err)
                else:
                    dc = res["datos_codo"]
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Recorrido 3D (T)", f"{res['recorrido_t']:.1f} mm")
                    m2.metric("Niple Neto a Cortar (L)", f"{res['niple_neto']:.1f} mm")
                    m3.metric("Giro Codo (α vertical)", f"{res['ang_giro_vert']:.1f}°")
                    m4.metric("Arco Giro en Tubo (S)", f"{res['arco_giro_tubo']:.1f} mm")

                    if res["codo_a_codo_alerta"]:
                        st.warning("⚠️ **Alerta de Taller:** El descuento de los dos codos supera el recorrido 3D (T).")

                    gcol1, gcol2 = st.columns([1.15, 1])
                    with gcol1:
                        fig3d_b = plt.figure(figsize=(5.6, 4.4))
                        ax3d_b = fig3d_b.add_subplot(111, projection='3d')
                        A_v = res["avance_a"]
                        H_v = res["desp_h"]
                        V_v = res["desp_v"]
                        ext = max(A_v, H_v, V_v) * 0.35

                        # Caja envolvente (bounding box de la bayoneta)
                        box_x = [0, A_v, A_v, 0, 0, A_v, A_v, 0]
                        box_y = [0, 0, H_v, H_v, 0, 0, H_v, H_v]
                        box_z = [0, 0, 0, 0, V_v, V_v, V_v, V_v]
                        edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
                        for i, j in edges:
                            ax3d_b.plot([box_x[i], box_x[j]], [box_y[i], box_y[j]], [box_z[i], box_z[j]], 'k:', lw=0.9, alpha=0.5)

                        # Diagonal frontal D
                        ax3d_b.plot([A_v, A_v], [0, H_v], [0, V_v], 'g--', lw=2, label=f"Diagonal D = {res['diagonal_d']:.1f}")
                        # Tubería 3D
                        px = [-ext, 0, A_v, A_v + ext]
                        py = [0, 0, H_v, H_v]
                        pz = [0, 0, V_v, V_v]
                        ax3d_b.plot(px, py, pz, 'b-', lw=4, label=f"Recorrido T = {res['recorrido_t']:.1f}")
                        ax3d_b.scatter([0, A_v], [0, H_v], [0, V_v], color='red', s=50)

                        ax3d_b.set_title("Isométrico 3D de la Bayoneta Girada", fontsize=11)
                        ax3d_b.set_xlabel("Avance A (X)")
                        ax3d_b.set_ylabel("Desp. H (Y)")
                        ax3d_b.set_zlabel("Altura V (Z)")
                        ax3d_b.legend(loc='upper left', fontsize=8)
                        fig3d_b.tight_layout()
                        st.pyplot(fig3d_b, use_container_width=True)

                    with gcol2:
                        fig_ab, ax_ab = plt.subplots(figsize=(5.0, 4.4))
                        D_v = res["diagonal_d"]
                        ax_ab.plot([0, H_v, 0, 0], [0, 0, V_v, 0], 'g-', lw=2.2, label='Triángulo Frontal (H, V, D)')
                        ax_ab.fill([0, H_v, 0], [0, 0, V_v], color='green', alpha=0.08)
                        ax_ab.text(H_v / 2, -max(V_v, 10)*0.06, f"H = {H_v:.0f}", ha='center', va='top', color='green', fontweight='bold')
                        ax_ab.text(-max(H_v, 10)*0.05, V_v / 2, f"V = {V_v:.0f}", ha='right', va='center', color='green', fontweight='bold')
                        ax_ab.text(H_v / 2 + 10, V_v / 2, f"D = {D_v:.1f}\n(Giro α = {res['ang_giro_vert']:.1f}°)", color='darkgreen', fontsize=9, fontweight='bold')

                        ax_ab.set_title("Triángulo Frontal de Giro (H vs V)", fontsize=11)
                        ax_ab.set_aspect('equal')
                        ax_ab.grid(True, linestyle=':', alpha=0.6)
                        ax_ab.legend(loc='upper right', fontsize=8)
                        fig_ab.tight_layout()
                        st.pyplot(fig_ab, use_container_width=True)

                    df_b3 = pd.DataFrame({
                        "Parámetro de Fabricación 3D": [
                            "Desplazamiento Horizontal (H / Roll) y Vertical (V / Set)",
                            "Diagonal Verdadera en Plano Frontal (D)",
                            "Ángulo de Giro del Codo respecto a la Vertical (α)",
                            "Arco de Giro sobre Periferia del Tubo (S con huincha)",
                            "Ángulo Real de los Codos (θ)",
                            "Avance Longitudinal Proyectado (A - Run)",
                            "Recorrido Espacial 3D Centro a Centro (T - Travel)",
                            "Descuento Total (2 Codos ASME + 2 Luces de Raíz)",
                            "LONGITUD NETA DE CORTE DEL NIPLE DIAGONAL (L)",
                            "Arcos de Corte Codo (Intradós / Centro / Lomo)"
                        ],
                        "Valor Calculado": [
                            f"H = {res['desp_h']:.1f} mm  |  V = {res['desp_v']:.1f} mm",
                            f"{res['diagonal_d']:.1f} mm",
                            f"{res['ang_giro_vert']:.2f}° (o {res['ang_giro_horiz']:.2f}° respecto a horizontal)",
                            f"{res['arco_giro_tubo']:.1f} mm (para tubo OD {dc['od_mm']} mm)",
                            f"{res['angulo_codo']:.2f}°",
                            f"{res['avance_a']:.1f} mm",
                            f"{res['recorrido_t']:.1f} mm",
                            f"{dc['descuento_total_niple']:.1f} mm (E = {dc['avance_codo']:.1f} mm c/u)",
                            f"{res['niple_neto']:.1f} mm",
                            f"{dc['arco_intrados']:.1f} mm  /  {dc['arco_centro']:.1f} mm  /  {dc['arco_extrados']:.1f} mm"
                        ]
                    })
                    st.dataframe(df_b3, use_container_width=True, hide_index=True)

        # ==========================================================
        # SUB-APARTADO 3: PUENTE / SALTO DE OBSTÁCULO (BAYONETA DOBLE)
        # ==========================================================
        elif "3. Puente" in sub_bayoneta:
            st.subheader("Bayoneta Doble Simétrica / Puente de Cruce (4 Codos)")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                desp_dob = st.number_input("Altura de Salto / Desvío (O mm):", min_value=10.0, value=400.0, step=10.0, key="bdob_o")
                l_puente = st.number_input("Largo Puente Central Eje a Eje (mm):", min_value=50.0, value=500.0, step=10.0, key="bdob_lp")
            with col2:
                ang_dob = st.selectbox("Ángulo de los 4 Codos (θ°):", [45.0, 30.0, 60.0, 90.0], index=0, key="bdob_ang")
                nps_dob = st.selectbox("Diámetro Nominal (NPS ASME):", lista_nps, index=idx_nps_default, key="bdob_nps")
            with col3:
                rad_dob = st.selectbox("Tipo de Codo ASME B16.9:", ["LR (Radio Largo 1.5D)", "SR (Radio Corto 1.0D)", "3D", "Sin descuento (Eje a Eje)"], key="bdob_rad")
                luz_dob = st.number_input("Luz de Raíz Soldadura (g mm):", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="bdob_luz")
            with col4:
                st.info("💡 **Aplicación:** Se utiliza para saltar vigas, columnas u otras líneas cruzadas regresando al mismo eje de flujo original.")

            if st.button("Calcular Puente de 4 Codos", type="primary", key="btn_bdob"):
                ang_calc_dob = 89.0 if float(ang_dob) >= 90.0 else float(ang_dob)
                res, err = gt.calcular_bayoneta_doble(desp_dob, ang_calc_dob, l_puente, nps_dob, rad_dob, luz_dob)
                if err:
                    st.error(err)
                else:
                    dc = res["datos_codo"]
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Abertura Total en Línea", f"{res['abertura_total']:.1f} mm")
                    m2.metric("Niple Diagonal Neto (x2)", f"{res['niple_diag_neto']:.1f} mm")
                    m3.metric("Niple Puente Neto (x1)", f"{res['niple_puente_neto']:.1f} mm")
                    m4.metric("Sobre-metraje requerido", f"+{res['sobre_metraje']:.1f} mm")

                    fig_db, ax_db = plt.subplots(figsize=(9.5, 3.8))
                    A_d = res["avance_diag"]
                    O_d = res["desplazamiento_o"]
                    Lp = res["l_puente_centro"]
                    ext = max(A_d * 0.5, 150.0)

                    xp = [-ext, 0, A_d, A_d + Lp, 2*A_d + Lp, 2*A_d + Lp + ext]
                    yp = [0, 0, O_d, O_d, 0, 0]

                    ax_db.plot(xp, yp, 'b-', lw=4.5, label=f'Puente de Tubería ({nps_dob})')
                    ax_db.scatter([0, A_d, A_d + Lp, 2*A_d + Lp], [0, O_d, O_d, 0], color='red', s=65, zorder=5, label='4 Codos')
                    ax_db.plot([0, 2*A_d + Lp], [0, 0], 'k--', lw=1.2, label='Eje Original de Línea')

                    ax_db.text(A_d + Lp/2, O_d + O_d*0.08, f"Puente = {Lp:.0f} mm (Niple = {res['niple_puente_neto']:.1f} mm)", ha='center', fontweight='bold', color='darkblue')
                    ax_db.text(A_d + Lp/2, -O_d*0.15, f"Abertura Total = {res['abertura_total']:.1f} mm", ha='center', fontweight='bold', color='black')
                    ax_db.text(A_d + Lp/2, O_d/2, f"Altura O = {O_d:.0f} mm", ha='center', color='green', fontweight='bold')

                    ax_db.set_title("Esquema de Puente Simétrico / Salto de Obstáculo", fontsize=12)
                    ax_db.set_ylim(-O_d*0.35, O_d*1.35)
                    ax_db.set_aspect('equal')
                    ax_db.grid(True, linestyle=':', alpha=0.6)
                    ax_db.legend(loc='upper right', fontsize=8)
                    fig_db.tight_layout()
                    st.pyplot(fig_db, use_container_width=True)

                    df_db = pd.DataFrame({
                        "Elemento del Spool (Puente)": [
                            "2x Brazos Diagonales (Centro a Centro T)",
                            "2x Niples Diagonales Netos a Cortar",
                            "1x Puente Central (Centro a Centro)",
                            "1x Niple Puente Central Neto a Cortar",
                            "Tramo Total Afectado en la Línea Principal (2A + Lp)",
                            "Descuento Unitario por Codo (E)"
                        ],
                        "Medida de Taller": [
                            f"{res['recorrido_diag']:.1f} mm c/u",
                            f"{res['niple_diag_neto']:.1f} mm c/u",
                            f"{res['l_puente_centro']:.1f} mm",
                            f"{res['niple_puente_neto']:.1f} mm",
                            f"{res['abertura_total']:.1f} mm",
                            f"{dc['avance_codo']:.1f} mm"
                        ]
                    })
                    st.dataframe(df_db, use_container_width=True, hide_index=True)

        # ==========================================================
        # SUB-APARTADO 4: BAYONETAS PARALELAS EN PIPE RACK (EQUAL SPREAD)
        # ==========================================================
        elif "4. Bayonetas Paralelas" in sub_bayoneta:
            st.subheader("Bayonetas Paralelas Equidistantes en Pipe Rack (Equal Spread)")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                sep_s = st.number_input("Separación entre Ejes (S mm):", min_value=20.0, value=200.0, step=10.0, key="bpar_s")
                ang_par = st.selectbox("Ángulo de Desvío (θ°):", [45.0, 30.0, 60.0, 90.0], index=0, key="bpar_ang")
            with col2:
                desp_par = st.number_input("Desplazamiento Bayoneta (O mm):", min_value=50.0, value=500.0, step=20.0, key="bpar_o")
                num_lin = st.slider("Cantidad de Tuberías Paralelas:", 2, 8, 4, key="bpar_n")
            with col3:
                l_arr = st.number_input("Cota Base Arranque Línea 1 (mm):", min_value=100.0, value=600.0, step=50.0, key="bpar_l0")
            with col4:
                st.info(
                    r"💡 **Fórmula del Adelanto (K):** $K = S \cdot \tan(\theta / 2)$. "
                    "Al escalonar cada arranque con la constante K, todas las diagonales conservan exactamente la misma separación S."
                )

            if st.button("Calcular Banco de Tuberías Paralelas", type="primary", key="btn_bpar"):
                ang_calc_par = 89.0 if float(ang_par) >= 90.0 else float(ang_par)
                res, err = gt.calcular_bayoneta_paralela(sep_s, ang_calc_par, desp_par, num_lin, l_arr)
                if err:
                    st.error(err)
                else:
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Adelanto / Desfase (K)", f"{res['desfase_k']:.1f} mm")
                    m2.metric("Recorrido Diagonal Común (T)", f"{res['recorrido_t']:.1f} mm")
                    m3.metric("Avance Proyectado (A)", f"{res['avance_a']:.1f} mm")
                    m4.metric(f"Desfase Total (L1 a L{num_lin})", f"{(num_lin - 1) * res['desfase_k']:.1f} mm")

                    fig_pr, ax_pr = plt.subplots(figsize=(9.5, 4.4))
                    A_p = res["avance_a"]
                    O_p = res["desplazamiento_o"]
                    K_p = res["desfase_k"]
                    L0 = res["l_base_arranque"]

                    colores = plt.cm.tab10(np.linspace(0, 0.8, num_lin))
                    for item, col in zip(res["lineas"], colores):
                        idx = item["indice"]
                        y0 = item["pos_transversal"]
                        x_quiebre1 = item["cota_arranque_entrada"]
                        x_quiebre2 = x_quiebre1 + A_p
                        x_fin = L0 + A_p + (num_lin * K_p) + 300.0

                        ax_pr.plot([0, x_quiebre1, x_quiebre2, x_fin], [y0, y0, y0 + O_p, y0 + O_p],
                                   color=col, lw=3, label=f"{item['linea']} (Arranque = {x_quiebre1:.1f} mm)")
                        ax_pr.scatter([x_quiebre1, x_quiebre2], [y0, y0 + O_p], color='black', s=35, zorder=5)

                    ax_pr.set_title(f"Planta de Pipe Rack - {num_lin} Tuberías Paralelas (K = {K_p:.1f} mm)", fontsize=12)
                    ax_pr.set_xlabel("Longitud Axial del Rack (mm)")
                    ax_pr.set_ylabel("Posición Transversal (mm)")
                    ax_pr.set_aspect('equal')
                    ax_pr.grid(True, linestyle=':', alpha=0.6)
                    ax_pr.legend(loc='upper left', fontsize=8)
                    fig_pr.tight_layout()
                    st.pyplot(fig_pr, use_container_width=True)

                    df_pr = pd.DataFrame({
                        "Línea del Rack": [x["linea"] for x in res["lineas"]],
                        "Posición Transversal Y (mm)": [x["pos_transversal"] for x in res["lineas"]],
                        "Desfase Acumulado i×K (mm)": [x["desfase_acumulado"] for x in res["lineas"]],
                        "Cota de Arranque 1er Codo (mm)": [x["cota_arranque_entrada"] for x in res["lineas"]],
                        "Recorrido Diagonal Centro a Centro T (mm)": [x["recorrido_diagonal_t"] for x in res["lineas"]]
                    })
                    st.dataframe(df_pr, use_container_width=True, hide_index=True)


    # --- 10. CODOS POR GAJOS / VIROLAS (MITERED ELBOWS - TODAS LAS OPCIONES) ---
    elif tool_tub == "🦐 Codos por Gajos (Virolas)":
        st.header("Cálculo y Trazado de Codos por Gajos / Virolas (Mitered Elbows)")
        st.markdown(
            "Diseño analítico y generación de plantillas para codos segmentados a partir de **tubería comercial** "
            "o **chapa rolada (fibra neutra)**. Incluye plantillas de media virola, virola central, "
            "**trazado en tubo continuo sin desperdicio** y perfil geométrico de armado."
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metodo_cg = st.selectbox(
                "Método de Fabricación:",
                [
                    "Exterior (Tubo Comercial)",
                    "Neutro (Chapa Rolada - Diámetro Medio)",
                    "Interior (Chapa Rolada - Medida Interna)",
                    "Chapa Exterior (Medida Externa Rolada)"
                ],
                key="cg_metodo"
            )
            d_cg = st.number_input("Diámetro Tubería / Virola (D mm):", min_value=20.0, value=200.0, step=10.0, key="cg_d")
            esp_cg = st.number_input("Espesor de Pared / Chapa (t mm):", min_value=0.0, value=6.0, step=0.5, key="cg_t")

        with col2:
            ang_sel_cg = st.selectbox("Ángulo Total del Codo (β°):", [90.0, 60.0, 45.0, 30.0, "Personalizado"], index=0, key="cg_ang_s")
            if ang_sel_cg == "Personalizado":
                ang_cg = st.number_input("Ángulo Custom (β°):", min_value=10.0, max_value=180.0, value=75.0, step=5.0, key="cg_ang_c")
            else:
                ang_cg = float(ang_sel_cg)

            cortes_map = {
                "2 Cortes (1 Central + 2 Extremos = 3 Piezas)": 2,
                "3 Cortes (2 Centrales + 2 Extremos = 4 Piezas)": 3,
                "4 Cortes (3 Centrales + 2 Extremos = 5 Piezas)": 4,
                "5 Cortes (4 Centrales + 2 Extremos = 6 Piezas)": 5,
                "6 Cortes (5 Centrales + 2 Extremos = 7 Piezas)": 6,
                "1 Corte (2 Piezas / Inglete Simple)": 1
            }
            cortes_label = st.selectbox("Configuración de Gajos / Soldaduras:", list(cortes_map.keys()), index=1, key="cg_cortes")
            num_cortes_cg = cortes_map[cortes_label]

        with col3:
            radio_modo_cg = st.selectbox(
                "Criterio de Radio de Curvatura (Rc):",
                [
                    "Radio Largo Estándar (1.5 × D)",
                    "Radio Corto (1.0 × D)",
                    "Radio Amplio (2.0 × D)",
                    "Radio Especial (2.5 × D)",
                    "Radio Personalizado (mm)"
                ],
                index=0,
                key="cg_rmodo"
            )
            if "1.5" in radio_modo_cg:
                rc_cg = 1.5 * d_cg
            elif "1.0" in radio_modo_cg:
                rc_cg = 1.0 * d_cg
            elif "2.0" in radio_modo_cg:
                rc_cg = 2.0 * d_cg
            elif "2.5" in radio_modo_cg:
                rc_cg = 2.5 * d_cg
            else:
                rc_cg = st.number_input("Radio al Centro Rc (mm):", min_value=30.0, value=300.0, step=10.0, key="cg_rc_cust")
            st.caption(f"📏 **Radio al eje central aplicado:** `Rc = {rc_cg:.1f} mm`")

        with col4:
            divs_cg = st.selectbox("Cant. Generatrices (N):", [12, 16, 24, 32, 36, 48], index=2, key="cg_divs")
            kerf_cg = st.number_input("Sangría de Corte / Disco (Kerf mm):", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="cg_kerf")

        with st.expander("📐 Ver Fórmulas Analíticas de Codos por Gajos (Virolas)", expanded=True):
            f1, f2 = st.columns(2)
            with f1:
                st.markdown("**1. Ángulo de Corte y Cotas de Media Virola Extrema:**")
                st.latex(r"\alpha = \frac{\beta}{2 \cdot N_c}, \quad L_m = R_c \cdot \tan(\alpha)")
                st.latex(r"L_{\text{mín}} = (R_c - r)\tan(\alpha), \quad L_{\text{máx}} = (R_c + r)\tan(\alpha)")
                st.caption(r"La Virola Central tiene ángulo $2\alpha$ y sus medidas son exactamente el doble ($2L_m, 2L_{\text{mín}}, 2L_{\text{máx}}$).")
            with f2:
                st.markdown("**2. Ordenada de Corte por Generatriz ($\phi$) y Largo de Tubo:**")
                st.latex(r"y_{\text{extremo}}(\phi) = L_m - r \cdot \tan(\alpha) \cdot \cos(\phi)")
                st.latex(r"L_{\text{tubo total}} = 2 \cdot N_c \cdot L_m + N_c \cdot \text{kerf}")
                st.caption("Girando 180° cada virola sucesiva, los cortes encajan sin desperdicio de material.")

        vista_cg = st.radio(
            "Seleccione el plano de fabricación a visualizar:",
            [
                "📐 1. Plantillas de Gajos (Media Virola Extrema y Virola Central)",
                "✂️ 2. Trazado en Tubo Continuo Sin Desperdicio (Corte Alternado 180°)",
                "🔄 3. Perfil de Armado del Codo y Control Dimensional"
            ],
            horizontal=True,
            key="cg_vista_rad"
        )

        if st.button("Calcular y Generar Planos del Codo por Gajos", type="primary", key="btn_cg_calc"):
            res, err = gt.calcular_codo_gajos(d_cg, ang_cg, num_cortes_cg, rc_cg, divs_cg, esp_cg, metodo_cg, kerf_cg)
            if err:
                st.error(err)
            else:
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Ángulo de Corte (α)", f"{res['alfa_corte']:.2f}° (Virola: {res['alfa_virola_central']:.2f}°)")
                m2.metric("Media Virola (Mín / Máx)", f"{res['garganta_extremo']:.1f} / {res['lomo_extremo']:.1f} mm")
                m3.metric("Virola Central (Mín / Máx)", f"{res['garganta_central']:.1f} / {res['lomo_central']:.1f} mm")
                m4.metric("Tubo Recto Mínimo Total", f"{res['largo_tubo_sin_desperdicio']:.1f} mm")

                # ==========================================================
                # VISTA 1: PLANTILLAS DE MEDIA VIROLA Y VIROLA CENTRAL
                # ==========================================================
                if "1. Plantillas" in vista_cg:
                    x_pts = res["distancias_x"]
                    y_med = res["y_media_virola"]
                    y_inf = res["y_virola_central_inf"]
                    y_sup = res["y_virola_central_sup"]
                    h_cen = res["altura_total_central"]

                    pcol1, pcol2 = st.columns(2)
                    with pcol1:
                        fig_mv, ax_mv = plt.subplots(figsize=(6.5, 4.3))
                        lim_mv = max(res["lomo_extremo"], 1.0)
                        ax_mv.plot(x_pts, y_med, 'b-', lw=2.5, label=f"Curva de Corte (α = {res['alfa_corte']:.2f}°)")
                        ax_mv.plot([0, res["perimetro"]], [0, 0], 'k-', lw=2, label="Base Recta de Boca (0 mm)")
                        ax_mv.axhline(res["lm_extremo"], color='gray', linestyle='-.', lw=1, label=f"Eje Neutro Lm = {res['lm_extremo']:.1f} mm")

                        for i in range(len(x_pts)):
                            px, py = x_pts[i], y_med[i]
                            ax_mv.plot([px, px], [0, py], 'r--', lw=1.0, alpha=0.6)
                            if i % max(1, divs_cg // 12) == 0:
                                ax_mv.text(px, py + lim_mv*0.04, f"{py:.1f}", color='green', fontsize=7.5, fontweight='bold', rotation=90, ha='center', va='bottom')
                            ax_mv.text(px, -lim_mv*0.08, f"P{i}", fontsize=6.5, ha='center', va='top')

                        ax_mv.set_title("Plantilla: Media Virola Extrema (x2 uds)", fontsize=11)
                        ax_mv.set_xlabel("Perímetro Desarrollado X (mm)")
                        ax_mv.set_ylabel("Altura de Generatriz Y (mm)")
                        ax_mv.set_ylim(-lim_mv*0.22, lim_mv*1.32)
                        ax_mv.grid(True, linestyle=':', alpha=0.6)
                        ax_mv.legend(loc='upper right', fontsize=7.5)
                        fig_mv.tight_layout()
                        st.pyplot(fig_mv, use_container_width=True)

                    with pcol2:
                        fig_vc, ax_vc = plt.subplots(figsize=(6.5, 4.3))
                        lim_vc = max(y_sup)
                        eje_sim = res["desvio_onda"] + res["lm_extremo"]
                        ax_vc.plot(x_pts, y_sup, 'b-', lw=2.5, label="Corte Superior")
                        ax_vc.plot(x_pts, y_inf, 'b-', lw=2.5, label="Corte Inferior")
                        ax_vc.axhline(eje_sim, color='purple', linestyle='-.', lw=1.2, label="Eje Central Simetría Virola")

                        for i in range(len(x_pts)):
                            px, yi, ys, hc = x_pts[i], y_inf[i], y_sup[i], h_cen[i]
                            ax_vc.plot([px, px], [yi, ys], 'r--', lw=1.0, alpha=0.65)
                            if i % max(1, divs_cg // 12) == 0:
                                ax_vc.text(px, (yi + ys)/2, f"{hc:.1f}", color='darkgreen', fontsize=7.5, fontweight='bold', rotation=90, ha='center', va='center',
                                           bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.8))

                        ax_vc.set_title(f"Plantilla: Virola Central Completa (x{res['num_virolas_centrales']} uds)", fontsize=11)
                        ax_vc.set_xlabel("Perímetro Desarrollado X (mm)")
                        ax_vc.set_ylabel("Posición en Plancha (mm)")
                        ax_vc.set_ylim(-lim_vc*0.15, lim_vc*1.2)
                        ax_vc.grid(True, linestyle=':', alpha=0.6)
                        ax_vc.legend(loc='upper right', fontsize=7.5)
                        fig_vc.tight_layout()
                        st.pyplot(fig_vc, use_container_width=True)

                    df_cg = pd.DataFrame({
                        "Punto": [f"P_{i}" for i in range(len(x_pts))],
                        "Ángulo (°)": res["angulos_deg"],
                        "Distancia en Perímetro X (mm)": x_pts,
                        "Altura Media Virola Extrema (mm)": y_med,
                        "Variación sobre Eje Neutro ±Δy (mm)": res["delta_onda"],
                        "Ancho Total Virola Central (mm)": h_cen
                    })
                    st.dataframe(df_cg, use_container_width=True, hide_index=True)

                # ==========================================================
                # VISTA 2: TRAZADO EN TUBO CONTINUO SIN DESPERDICIO
                # ==========================================================
                elif "2. Trazado en Tubo" in vista_cg:
                    st.info(
                        "💡 **Técnica de Taller (Corte Alternado):** Marque dos líneas longitudinales opuestas a **0°** y **180°** "
                        "a lo largo del tubo. Al alternar la orientación de la plantilla en cada corte, la garganta de una pieza "
                        "coincide exactamente con el lomo de la pieza contigua, logrando **cero desperdicio de material**."
                    )
                    fig_tc, ax_tc = plt.subplots(figsize=(10.5, 4.5))
                    x_pts = res["distancias_x"]
                    L_tot = res["largo_tubo_sin_desperdicio"]

                    # Contorno del tubo desenrollado
                    ax_tc.plot([0, 0, res["perimetro"], res["perimetro"], 0], [0, L_tot, L_tot, 0, 0], 'k-', lw=2.2, label="Tubo Recto Desarrollado")

                    colores_c = plt.cm.Set1(np.linspace(0, 0.8, res["num_cortes"]))
                    for item, col in zip(res["curvas_tubo_alternado"], colores_c):
                        k = item["corte_num"]
                        zc = item["z_curva"]
                        ax_tc.plot(x_pts, zc, color=col, lw=2.2, label=f"Corte #{k} (Eje = {item['z_centro']:.1f} mm)")
                        ax_tc.axhline(item["z_centro"], color=col, linestyle=':', lw=0.9, alpha=0.6)

                    ax_tc.set_title(f"Mapa de Cortes Alternados en Tubo Continuo (Largo Total = {L_tot:.1f} mm)", fontsize=12)
                    ax_tc.set_xlabel("Perímetro Desarrollado X (mm)  [0° = Garganta | 180° = Mitad Perímetro]")
                    ax_tc.set_ylabel("Longitud Axial del Tubo Z (mm)")
                    ax_tc.grid(True, linestyle=':', alpha=0.5)
                    ax_tc.legend(loc='upper right', fontsize=8.5)
                    fig_tc.tight_layout()
                    st.pyplot(fig_tc, use_container_width=True)

                    df_alt = pd.DataFrame(res["cotas_generatrices_0_180"])
                    df_alt.columns = [
                        "Número de Corte",
                        "Posición al Eje Neutro (mm)",
                        "Marca en Generatriz 0° (mm)",
                        "Marca en Generatriz 180° (mm)"
                    ]
                    st.dataframe(df_alt, use_container_width=True, hide_index=True)

                # ==========================================================
                # VISTA 3: PERFIL DE ARMADO DEL CODO Y CONTROL DIMENSIONAL
                # ==========================================================
                elif "3. Perfil de Armado" in vista_cg:
                    gcol1, gcol2 = st.columns([1.15, 1])
                    with gcol1:
                        fig_arm, ax_arm = plt.subplots(figsize=(5.8, 5.2))
                        Rc = res["radio_curvatura"]
                        r_t = res["r"]
                        beta_r = math.radians(res["angulo_total"])

                        # Arcos teóricos de referencia (intradós, eje neutro, extradós)
                        t_arc = np.linspace(0, beta_r, 120)
                        ax_arm.plot(Rc * np.cos(t_arc), Rc * np.sin(t_arc), 'r-.', lw=1.2, label=f"Eje Radio Rc = {Rc:.0f} mm")
                        ax_arm.plot((Rc - r_t) * np.cos(t_arc), (Rc - r_t) * np.sin(t_arc), 'k:', lw=1.0, alpha=0.6)
                        ax_arm.plot((Rc + r_t) * np.cos(t_arc), (Rc + r_t) * np.sin(t_arc), 'k:', lw=1.0, alpha=0.6)

                        # Dibujar las costuras radiales de cada corte
                        nc = res["num_cortes"]
                        alfa_r = math.radians(res["alfa_corte"])
                        angulos_costura = [0.0] + [(2*k - 1)*alfa_r for k in range(1, nc + 1)] + [beta_r]

                        for idx_s in range(len(angulos_costura) - 1):
                            a1 = angulos_costura[idx_s]
                            a2 = angulos_costura[idx_s + 1]
                            a_mid = (a1 + a2) / 2.0
                            # Costura
                            if idx_s > 0:
                                r_sec = r_t / math.cos(alfa_r)
                                x_in = (Rc - r_t) / math.cos(alfa_r) * math.cos(a1)
                                y_in = (Rc - r_t) / math.cos(alfa_r) * math.sin(a1)
                                x_out = (Rc + r_t) / math.cos(alfa_r) * math.cos(a1)
                                y_out = (Rc + r_t) / math.cos(alfa_r) * math.sin(a1)
                                ax_arm.plot([x_in, x_out], [y_in, y_out], 'r-', lw=2.0)

                        # Contorno poligonal exterior e interior de los gajos
                        pts_in_x, pts_in_y = [], []
                        pts_out_x, pts_out_y = [], []
                        for idx_c, ang_c in enumerate(angulos_costura):
                            factor_sec = 1.0 if (idx_c == 0 or idx_c == len(angulos_costura) - 1) else (1.0 / math.cos(alfa_r))
                            r_in_c = (Rc - r_t) * factor_sec
                            r_out_c = (Rc + r_t) * factor_sec
                            pts_in_x.append(r_in_c * math.cos(ang_c))
                            pts_in_y.append(r_in_c * math.sin(ang_c))
                            pts_out_x.append(r_out_c * math.cos(ang_c))
                            pts_out_y.append(r_out_c * math.sin(ang_c))

                        ax_arm.plot(pts_in_x, pts_in_y, 'b-', lw=2.5, label="Contorno de Gajos")
                        ax_arm.plot(pts_out_x, pts_out_y, 'b-', lw=2.5)
                        ax_arm.plot([pts_in_x[0], pts_out_x[0]], [pts_in_y[0], pts_out_y[0]], 'k-', lw=2.5)
                        ax_arm.plot([pts_in_x[-1], pts_out_x[-1]], [pts_in_y[-1], pts_out_y[-1]], 'k-', lw=2.5)

                        ax_arm.set_title(f"Perfil Geométrico de Armado ({nc} Cortes / {res['num_piezas_totales']} Gajos)", fontsize=11)
                        ax_arm.set_aspect('equal')
                        ax_arm.grid(True, linestyle=':', alpha=0.6)
                        ax_arm.legend(loc='lower left', fontsize=8)
                        fig_arm.tight_layout()
                        st.pyplot(fig_arm, use_container_width=True)

                    with gcol2:
                        df_res_cg = pd.DataFrame({
                            "Parámetro Técnico del Codo": [
                                "Diámetro de Cálculo / Perímetro Desarrollado (P)",
                                "Ángulo Total del Codo (β)",
                                "Cantidad de Soldaduras (Cortes) / Total Piezas",
                                "Ángulo de Corte de Inglete (α)",
                                "Ángulo de cada Virola Central (2α)",
                                "Radio de Curvatura al Centro (Rc)",
                                "Avance del Codo Centro a Cara (A)",
                                "Media Virola Extrema (Garganta / Eje / Lomo)",
                                "Virola Central Completa (Garganta / Eje / Lomo)",
                                "Longitud Total de Tubo Recto Necesario",
                                "Metros Lineales Totales de Soldadura"
                            ],
                            "Valor de Taller": [
                                f"{res['d_calculo']:.1f} mm  /  P = {res['perimetro']:.1f} mm",
                                f"{res['angulo_total']:.1f}°",
                                f"{res['num_cortes']} cortes  ({res['num_virolas_centrales']} centrales + 2 extremos)",
                                f"{res['alfa_corte']:.2f}°",
                                f"{res['alfa_virola_central']:.2f}°",
                                f"{res['radio_curvatura']:.1f} mm",
                                f"{res['avance_codo']:.1f} mm",
                                f"{res['garganta_extremo']:.1f}  /  {res['lm_extremo']:.1f}  /  {res['lomo_extremo']:.1f} mm",
                                f"{res['garganta_central']:.1f}  /  {res['lm_central']:.1f}  /  {res['lomo_central']:.1f} mm",
                                f"{res['largo_tubo_sin_desperdicio']:.1f} mm (incluye kerf)",
                                f"{res['longitud_total_soldadura'] / 1000.0:.2f} m ({res['longitud_total_soldadura']:.0f} mm)"
                            ]
                        })
                        st.dataframe(df_res_cg, use_container_width=True, hide_index=True)

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
