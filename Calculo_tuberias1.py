import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Herramientas de Trazado para Calderería", layout="wide")

st.title("Aplicativo de Trazado y Generatrices para Tuberías")
st.markdown("""
Este aplicativo desarrollado por Jesus Tasayco unifica los cálculos fundamentales para el desarrollo de plantillas y cortes en tuberías. 
A continuacion seleccione la pestaña correspondiente a la operación que desea realizar:
""")

# Creación de pestañas para organizar la interfaz
tab1, tab2, tab3 = st.tabs(["Calcular Flecha", "Calcular Cuerda", "Generatrices y Plantilla"])

# ==========================================
# PESTAÑA 1: CÁLCULO DE FLECHA CON DIAGRAMA
# ==========================================
with tab1:
    st.header("Cálculo de la Flecha")
    st.markdown("Calcula la altura máxima del arco (Flecha) a partir del radio y la longitud de la cuerda.")
    
    st.latex(r"f = R - \sqrt{R^2 - \left(\frac{C}{2}\right)^2}")
    st.latex(r"a = \sqrt{R^2 - \left(\frac{C}{2}\right)^2}")
    
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
                ax1.text(-5, apotema_f/2, r'$a$', color='red', fontsize=12)
                ax1.text(5, apotema_f + flecha_f/2, r'$f$', color='green', fontsize=14, fontweight='bold')
                
                ax1.set_aspect('equal')
                lim_max = radio_f * 1.2
                ax1.set_xlim(-lim_max, lim_max)
                ax1.set_ylim(-lim_max, lim_max)
                ax1.axis('off')
                ax1.set_title("Diagrama Geométrico de la Flecha")
                
                red_patch = plt.plot([], [], color='red', linewidth=1.5, label='Geometría Base (R:Radio, C:Cuerda, a:Apotema)')[0]
                green_patch = plt.plot([], [], color='green', linewidth=3, label='Flecha Calculada (f)')[0]
                ax1.legend(handles=[red_patch, green_patch], loc='lower right', title="Leyenda")
                
                st.pyplot(fig1)
                st.success(f"**Resultado:** La flecha (f) es **{flecha_f:.2f}** unidades.")

# ==========================================
# PESTAÑA 2: CÁLCULO DE CUERDA CON DIAGRAMA
# ==========================================
with tab2:
    st.header("Cálculo de la Cuerda")
    st.markdown("Calcula la longitud de la cuerda conociendo el radio y el ángulo central en grados centígrados.")
    
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
                y_arc_c = radio_c * np.ones_like(x_arc_c)
                ax2.plot(radio_c * np.sin(x_arc_c), radio_c * np.cos(x_arc_c), color='red', linewidth=1.5)
            
            x_r1, y_r1 = radio_c * np.sin(radianes/2), radio_c * np.cos(radianes/2)
            x_r2, y_r2 = radio_c * np.sin(-radianes/2), radio_c * np.cos(-radianes/2)
            ax2.plot([0, x_r1], [0, y_r1], color='red', linewidth=1)
            ax2.plot([0, x_r2], [0, y_r2], color='red', linewidth=1)
            ax2.plot([x_r1, x_r2], [y_r1, y_r2], color='green', linewidth=3)
            
            ax2.text(x_r1/2 + 5, y_r1/2, r'$R$', color='red', fontsize=12)
            ax2.text(0, -radio_c/4, r'$\theta$', color='black', fontsize=16, fontweight='bold')
            ax2.text(0, y_r1 + cuerda_c/10, r'$C$', color='green', fontsize=14, fontweight='bold')
            
            ax2.set_aspect('equal')
            lim_max_c = radio_c * 1.2
            ax2.set_xlim(-lim_max_c, lim_max_c)
            ax2.set_ylim(-lim_max_c, lim_max_c)
            ax2.axis('off')
            ax2.set_title("Diagrama Geométrico de la Cuerda")
            
            red_patch_c = plt.plot([], [], color='red', linewidth=1.5, label='Geometría Base (R, arco)')[0]
            green_patch_c = plt.plot([], [], color='green', linewidth=3, label='Cuerda Calculada (C)')[0]
            ax2.legend(handles=[red_patch_c, green_patch_c], loc='lower right', title="Leyenda")
            
            st.pyplot(fig2)
            st.success(f"**Resultado:** La longitud de la cuerda (C) es **{cuerda_c:.2f}** unidades.")

# ==========================================
# PESTAÑA 3: GENERATRICES Y PLANTILLA MEJORADA
# ==========================================
with tab3:
    st.header("Cálculo de Generatrices y Visualización de Plantilla")
    st.markdown("Obtenga las ordenadas (alturas) para trazar la plantilla en funcion del radio y la cuerda.")
    
    st.latex(r"h(x) = \sqrt{R^2 - x^2} - \sqrt{R^2 - \left(\frac{C}{2}\right)^2}")
    
    # Entradas en la parte superior, alineadas horizontalmente
    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        diametro_g = st.number_input("Diámetro exterior (D):", min_value=1.0, value=26000.0, step=10.0)
    with col_input2:
        cuerda_g = st.number_input("Longitud de la cuerda (C):", min_value=1.0, value=500.0, step=10.0)
    with col_input3:
        separacion_g = st.number_input("Separación entre generatrices (s):", min_value=1.0, value=83.33, step=1.0)
        
    generar_btn = st.button("Calcular y Graficar Plantilla", type="primary")
    
    # Gráfico y Tabla debajo de los controles (Fuera de las columnas para ocupar ancho completo)
    if generar_btn:
        if cuerda_g > diametro_g:
            st.error("La cuerda no puede ser mayor al diámetro.")
        else:
            radio_g = diametro_g / 2.0
            mitad_cuerda_g = cuerda_g / 2.0
            apotema_g = math.sqrt(radio_g**2 - mitad_cuerda_g**2)
            flecha_g = radio_g - apotema_g
            
            posiciones_x = []
            alturas_h = []
            
            x = 0.0
            while x <= mitad_cuerda_g + 1e-6:
                y_arco_g = math.sqrt(radio_g**2 - x**2)
                altura_g = y_arco_g - apotema_g
                posiciones_x.append(x)
                alturas_h.append(altura_g)
                x += separacion_g
            
            # --- ZONA DE GRÁFICO MEJORADA ---
            fig3, ax3 = plt.subplots(figsize=(16, 7)) # Lienzo ancho
            
            # Dibujar arco de circunferencia
            x_arc_g = np.linspace(-mitad_cuerda_g, mitad_cuerda_g, 500)
            y_arc_g = np.sqrt(radio_g**2 - x_arc_g**2) - apotema_g
            ax3.plot(x_arc_g, y_arc_g, color='blue', label='Arco de tubería', linewidth=2.5)
            
            # Dibujar la cuerda base
            ax3.plot([-mitad_cuerda_g, mitad_cuerda_g], [0, 0], color='black', linewidth=2, label='Cuerda base')
            
            # Flecha central (Verde)
            ax3.plot([0, 0], [0, flecha_g], color='green', linewidth=3.5, label='Flecha central (f)')
            # Cota de flecha desplazada ligeramente a la derecha
            ax3.text(mitad_cuerda_g*0.05, flecha_g*0.6, f'f = {flecha_g:.2f}', color='green', fontsize=12, fontweight='bold')
            
            # Apotema (Rojo) dibujada hacia abajo pero cortada por los límites del gráfico
            ax3.plot([0, 0], [-apotema_g, 0], color='red', linestyle=':', linewidth=2, label='Apotema central (a)')
            # Texto de apotema visible dentro de los nuevos márgenes
            ax3.text(-mitad_cuerda_g*0.1, -flecha_g*0.5, f'a = {apotema_g:.1f}', color='red', fontsize=11)
            
            # Dibujar y cotar las generatrices
            num_generatrices = len(posiciones_x)
            etiquetar_h_paso = 1 # Etiquetamos todas por defecto, pero se ajustará si es muy denso
            
            for i in range(num_generatrices):
                pos_x = posiciones_x[i]
                alt = alturas_h[i]
                
                # Líneas de generatriz
                ax3.plot([pos_x, pos_x], [0, alt], color='red', linestyle='--', linewidth=1.2)
                if pos_x != 0:
                    ax3.plot([-pos_x, -pos_x], [0, alt], color='red', linestyle='--', linewidth=1.2)
                
                # Cotas de altura h(x)
                if i % etiquetar_h_paso == 0:
                    padding_y = flecha_g * 0.05 # Desplazamiento dinámico basado en la flecha
                    ax3.text(pos_x, alt + padding_y, f'{alt:.2f}', color='green', fontsize=10, fontweight='bold', rotation=90, va='bottom', ha='center')
                    if pos_x != 0:
                        ax3.text(-pos_x, alt + padding_y, f'{alt:.2f}', color='green', fontsize=10, fontweight='bold', rotation=90, va='bottom', ha='center')
                
                # Cotas de distancia x 
                padding_x = flecha_g * 0.1
                ax3.text(pos_x, -padding_x, f'{pos_x:.1f}', color='red', fontsize=9, rotation=90, va='top', ha='center')
                if pos_x != 0:
                    ax3.text(-pos_x, -padding_x, f'-{pos_x:.1f}', color='red', fontsize=9, rotation=90, va='top', ha='center')
            
            # Configuración dinámica para evitar el "aplastamiento"
            ax3.set_aspect('auto') # VITAL: Permite estirar curvas muy planas como la de D=26000 y C=500
            
            # Ajustar el "zoom" del eje Y solo a la zona de interés de la plantilla
            lim_x = mitad_cuerda_g * 1.15
            lim_y_up = flecha_g * 1.5   # Un poco de aire arriba para los textos
            lim_y_down = flecha_g * 1.0 # Suficiente espacio abajo para las cotas X
            
            ax3.set_xlim(-lim_x, lim_x)
            ax3.set_ylim(-lim_y_down, lim_y_up)
            
            ax3.set_title("Trazado de Plantilla Física (Auto-escalado para máxima legibilidad)", fontsize=16)
            ax3.set_xlabel("Distancia en la cuerda (x)", fontsize=14)
            ax3.set_ylabel("Altura de generatriz (h)", fontsize=14)
            ax3.grid(True, linestyle=':', alpha=0.6)
            ax3.legend(loc='upper right', fontsize=10)
            
            st.pyplot(fig3, use_container_width=True) # Gráfico a ancho completo
            
            # --- ZONA DE TABLA DE RESULTADOS ---
            st.subheader("Tabla de Ordenadas (Desde el centro hacia un extremo)")
            df_resultados_g = pd.DataFrame({
                "Punto": [f"P_{i}" for i in range(len(posiciones_x))],
                "Distancia desde el centro (x)": [round(val, 2) for val in posiciones_x],
                "Altura a cortar (h)": [round(val, 2) for val in alturas_h]
            })
            st.dataframe(df_resultados_g, use_container_width=True)