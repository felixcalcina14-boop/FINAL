import streamlit as st
import pandas as pd
import random

# =====================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# =====================
st.set_page_config(page_title="Polla Mundial 2026", page_icon="🏆", layout="centered")

url_imagen_web = "https://media.cnn.com/api/v1/images/stellar/prod/cnne-1279822-historia-de-la-copa-mundial-de-la-fifa.png?c=16x9&q=w_1280,c_fill/f_webp"


st.markdown(f"""
    <style>
    /* Forzar fondo transparente en capas nativas de Streamlit para que no tapen la imagen */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainBlockContainer"] {{
        background-color: transparent !important;
        background: transparent !important;
    }}
    
    /* Inyección directa de la URL de la imagen en el fondo absoluto de la página web */
    html, body, [data-testid="stApp"] {{
        background-color: #111827 !important;
        background-image: url("{url_imagen_web}") !important;
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    /* Contenedor central semi-oscuro para proteger la lectura de textos */
    [data-testid="stAppViewBlockContainer"] {{
        background-color: rgba(15, 23, 42, 0.75) !important;
        padding: 30px !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6) !important;
        margin-top: 20px !important;
    }}
    
    /* Títulos y textos con colores vivos y sombras forzadas */
    h1 {{ color: #FFD700 !important; text-align: center; font-weight: 800; text-shadow: 2px 2px 4px #000000 !important; }}
    h2 {{ color: #10B981 !important; border-bottom: 2px solid #10B981; padding-bottom: 5px; margin-top: 30px; font-weight: bold; text-shadow: 1px 1px 3px #000000 !important; }}
    h3 {{ color: #F59E0B !important; text-shadow: 1px 1px 3px #000000 !important; font-weight: bold; }}
    
    /* Estilo de los textos de los selectores para garantizar lectura total */
    label {{
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px #000000 !important;
    }}
    
    div.stButton > button:first-child {{
        background-color: #10B981; color: white; font-weight: bold;
        border-radius: 8px; border: none; padding: 10px 24px;
        transition: all 0.3s ease; width: 100%; margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    div.stButton > button:first-child:hover {{
        background-color: #059669; transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)

# =====================
# DATOS ESTRUCTURALES DEL TORNEO
# =====================
grupos = {
    "a": ["México", "Corea del Sur", "Sudáfrica", "República checa"],
    "b": ["Canadá", "Qatar", "Suiza", "Bosnia y Herzegovina"],
    "c": ["Brasil", "Marruecos", "Haití", "Escocia"],
    "d": ["Estados Unidos", "Paraguay", "Australia", "Turquía"],
    "e": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
    "f": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "g": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"],
    "h": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
    "i": ["Francia", "Senegal", "Irak", "Noruega"],
    "j": ["Argentina", "Argelia", "Austria", "Jordania"],
    "k": ["Portugal", "RD Congo", "Uzbekistán", "Colombia"],
    "l": ["Inglaterra", "Croacia", "Ghana", "Panamá"]
}

estructura_16 = [
    {"llave": "d1", "a": "1e", "b": "t"}, {"llave": "d2", "a": "1i", "b": "t"},
    {"llave": "d3", "a": "2a", "b": "2b"}, {"llave": "d4", "a": "1f", "b": "2c"},
    {"llave": "d5", "a": "2k", "b": "2l"}, {"llave": "d6", "a": "1h", "b": "2j"},
    {"llave": "d7", "a": "1d", "b": "t"}, {"llave": "d8", "a": "1g", "b": "t"},
    {"llave": "d9", "a": "1c", "b": "2f"}, {"llave": "d10", "a": "2e", "b": "2i"},
    {"llave": "d11", "a": "1a", "b": "t"}, {"llave": "d12", "a": "1l", "b": "t"},
    {"llave": "d13", "a": "1j", "b": "2h"}, {"llave": "d14", "a": "2d", "b": "2g"},
    {"llave": "d15", "a": "1b", "b": "t"}, {"llave": "d16", "a": "1k", "b": "t"}
]

estructura_8 = [
    {"llave": "d17", "a": "d1", "b": "d2"}, {"llave": "d18", "a": "d3", "b": "d4"},
    {"llave": "d19", "a": "d5", "b": "d6"}, {"llave": "d20", "a": "d7", "b": "d8"},
    {"llave": "d21", "a": "d9", "b": "d10"}, {"llave": "d22", "a": "d11", "b": "d12"},
    {"llave": "d23", "a": "d13", "b": "d14"}, {"llave": "d24", "a": "d15", "b": "d16"}
]

estructura_4 = [
    {"llave": "d25", "a": "d17", "b": "d18"}, {"llave": "d26", "a": "d19", "b": "d20"},
    {"llave": "d27", "a": "d21", "b": "d22"}, {"llave": "d28", "a": "d23", "b": "d24"}
]

estructura_2 = [
    {"llave": "d29", "a": "d25", "b": "d26"}, 
    {"llave": "d30", "a": "d27", "b": "d28"}
]

st.markdown("<h1>🏆 POLLA MUNDIAL FIFA 2026 🏆</h1>", unsafe_allow_html=True)

# Pedir nombre de usuario
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if st.session_state.usuario == "":
    st.markdown("<div class='partido-body'>", unsafe_allow_html=True)
    st.subheader("📝 Registro de Jugador")
    nombre = st.text_input("Introduce tu nombre o apodo para el fixture:")
    if st.button("🚀 Comenzar Desafío"):
        if nombre.strip() != "":
            st.session_state.usuario = nombre.strip()
            st.session_state.fase = "Grupos"
            st.rerun()
        else:
            st.error("Por favor, introduce un nombre válido.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Inicializaciones de estados de sesión
if "ganadores_16" not in st.session_state: st.session_state.ganadores_16 = {}
if "ganadores_8" not in st.session_state: st.session_state.ganadores_8 = {}
if "ganadores_4" not in st.session_state: st.session_state.ganadores_4 = {}
if "ganadores_2" not in st.session_state: st.session_state.ganadores_2 = {}
if "ganador_final" not in st.session_state: st.session_state.ganador_final = ""
if "orden_terceros" not in st.session_state: st.session_state.orden_terceros = []

# BARRA LATERAL
st.sidebar.markdown(f"### 👤 Jugador: `{st.session_state.usuario}`")
st.sidebar.markdown("---")
st.sidebar.subheader("🗺️ Menú del Torneo")

lista_fases = ["Grupos", "16avos de Final", "Octavos de Final", "Cuartos de Final", "Semifinales", "Gran Final"]
fase_seleccionada = st.sidebar.radio("Saltar directamente a:", lista_fases, index=lista_fases.index(st.session_state.fase))
st.session_state.fase = fase_seleccionada

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Tu Progreso")
st.sidebar.metric(label="Fase Actual", value=st.session_state.fase)

# Cálculos encadenados en caliente
if "clasificados" in st.session_state and "mejores_terceros" in st.session_state:
    if not st.session_state.orden_terceros or len(st.session_state.orden_terceros) != len(st.session_state.mejores_terceros):
        st.session_state.orden_terceros = st.session_state.mejores_terceros.copy()
        random.shuffle(st.session_state.orden_terceros)

llaves_16_calculadas = []
if "clasificados" in st.session_state and st.session_state.orden_terceros:
    clas = {k.lower(): v for k, v in st.session_state.clasificados.items()}
    contador = 0
    for item in estructura_16:
        a_key, b_key = item["a"], item["b"]
        eq_a = st.session_state.orden_terceros[contador] if a_key == "t" else clas.get(a_key, "Por definir")
        if a_key == "t": contador += 1
        eq_b = st.session_state.orden_terceros[contador] if b_key == "t" else clas.get(b_key, "Por definir")
        if b_key == "t": contador += 1
        llaves_16_calculadas.append({"llave": item["llave"], "a": eq_a, "b": eq_b})

# =====================
# INTERFAZ LÓGICA DE FASES
# =====================

# --- FASE GRUPOS ---
if st.session_state.fase == "Grupos":
    st.header("⚽ Clasificación de Fase de Grupos")
    clasificados = {}
    terceros_pool = []

    col1, col2 = st.columns(2)
    for idx, (g, equipos) in enumerate(grupos.items()):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.markdown(f"<div class='partido-header'>Grupo {g.upper()}</div><div class='partido-body'>", unsafe_allow_html=True)
            primero = st.selectbox(f"1° puesto", equipos, key=f"p_{g}")
            segundo = st.selectbox(f"2° puesto", [e for e in equipos if e != primero], key=f"s_{g}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            clasificados[f"1{g}"] = primero
            clasificados[f"2{g}"] = segundo
            terceros_pool.extend([e for e in equipos if e not in [primero, segundo]])

    st.session_state.clasificados = clasificados
    st.session_state.terceros_pool = terceros_pool

    st.header("🏅 Selección de los 8 Mejores Terceros")
    mapa_grupo = {e: g for g, eqs in grupos.items() for e in eqs if e in terceros_pool}
    seleccionados = []

    col_t1, col_t2 = st.columns(2)
    for i in range(8):
        t_col = col_t1 if i % 2 == 0 else col_t2
        with t_col:
            usados_grupos = [mapa_grupo[e] for e in seleccionados]
            opciones = [e for e in terceros_pool if e not in seleccionados and mapa_grupo[e] not in usados_grupos]
            if opciones:
                st.markdown(f"<div class='partido-header'>Cupo Tercero {i+1}</div><div class='partido-body'>", unsafe_allow_html=True)
                elegido = st.selectbox(f"Seleccionar", opciones, key=f"t{i}")
                seleccionados.append(elegido)
                st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.mejores_terceros = seleccionados
    if st.button("Siguiente: 16avos de Final ➡️"):
        st.session_state.fase = "16avos de Final"
        st.rerun()

# --- FASE 16AVOS ---
elif st.session_state.fase == "16avos de Final":
    st.header("🛡️ Cruces de 16avos de Final")
    if not llaves_16_calculadas:
        st.warning("⚠️ Primero debes completar la clasificación de la Fase de Grupos.")
    else:
        for p in llaves_16_calculadas:
            opciones = [p["a"], p["b"]]
            
            # Buscamos el ganador guardado. Si no existe, usamos una clave intermedia para evitar desfases
            key_radio = f"radio_16_{p['llave']}_{p['a']}_{p['b']}"
            if key_radio in st.session_state:
                ganador_actual = st.session_state[key_radio]
                st.session_state.ganadores_16[p["llave"]] = ganador_actual
            else:
                ganador_actual = st.session_state.ganadores_16.get(p['llave'], p["a"])
            
            idx = opciones.index(ganador_actual) if ganador_actual in opciones else 0
            
            # Cabecera ploma que ahora sí lee el estado en tiempo real
            st.markdown(f"""
                <div style='background-color: #1e293b; padding: 10px 15px; border-radius: 8px 8px 0px 0px; border-left: 5px solid #475569; margin-top: 20px;'>
                    <h4 style='margin: 0; padding: 0; font-size: 1rem; color: #FFD700;'>🏆 Avanza: {ganador_actual}</h4>
                </div>
            """, unsafe_allow_html=True)

            # El truco: Al cambiar el radio button, st.rerun() fuerza la actualización instantánea del texto de arriba
            st.radio("¿Quién avanza?", opciones, index=idx, key=key_radio, on_change=st.rerun)
            st.session_state.ganadores_16[p["llave"]] = st.session_state[key_radio]

        if st.button("Siguiente: Octavos de Final ➡️"):
            st.session_state.fase = "Octavos de Final"
            st.rerun()

# --- FASE OCTAVOS ---
elif st.session_state.fase == "Octavos de Final":
    st.header("⚡ Octavos de Final")
    if not st.session_state.ganadores_16:
        st.warning("⚠️ Primero debes definir los ganadores en los 16avos de Final.")
    else:
        for item in estructura_8:
            eq_a = st.session_state.ganadores_16.get(item["a"], "Por definir")
            eq_b = st.session_state.ganadores_16.get(item["b"], "Por definir")
            
            opciones = [eq_a, eq_b]
            key_radio = f"radio_8_{item['llave']}_{eq_a}_{eq_b}"
            
            if key_radio in st.session_state:
                ganador_actual = st.session_state[key_radio]
                st.session_state.ganadores_8[item["llave"]] = ganador_actual
            else:
                ganador_actual = st.session_state.ganadores_8.get(item['llave'], eq_a)
            
            idx = opciones.index(ganador_actual) if ganador_actual in opciones else 0
            
            st.markdown(f"""
                <div style='background-color: #1e293b; padding: 10px 15px; border-radius: 8px 8px 0px 0px; border-left: 5px solid #475569; margin-top: 20px;'>
                    <h4 style='margin: 0; padding: 0; font-size: 1rem; color: #FFD700;'>🏆 Avanza: {ganador_actual}</h4>
                </div>
            """, unsafe_allow_html=True)

            st.radio("¿Quién pasa a Cuartos?", opciones, index=idx, key=key_radio, on_change=st.rerun)
            st.session_state.ganadores_8[item["llave"]] = st.session_state[key_radio]

        if st.button("Siguiente: Cuartos de Final ➡️"):
            st.session_state.fase = "Cuartos de Final"
            st.rerun()

# --- FASE CUARTOS ---
elif st.session_state.fase == "Cuartos de Final":
    st.header("🔥 Cuartos de Final")
    if not st.session_state.ganadores_8:
        st.warning("⚠️ Primero debes definir los ganadores en los Octavos de Final.")
    else:
        for item in estructura_4:
            eq_a = st.session_state.ganadores_8.get(item["a"], "Por definir")
            eq_b = st.session_state.ganadores_8.get(item["b"], "Por definir")
            
            opciones = [eq_a, eq_b]
            key_radio = f"radio_4_{item['llave']}_{eq_a}_{eq_b}"
            
            if key_radio in st.session_state:
                ganador_actual = st.session_state[key_radio]
                st.session_state.ganadores_4[item["llave"]] = ganador_actual
            else:
                ganador_actual = st.session_state.ganadores_4.get(item['llave'], eq_a)
            
            idx = opciones.index(ganador_actual) if ganador_actual in opciones else 0
            
            st.markdown(f"""
                <div style='background-color: #1e293b; padding: 10px 15px; border-radius: 8px 8px 0px 0px; border-left: 5px solid #475569; margin-top: 20px;'>
                    <h4 style='margin: 0; padding: 0; font-size: 1rem; color: #FFD700;'>🏆 Avanza: {ganador_actual}</h4>
                </div>
            """, unsafe_allow_html=True)

            st.radio("¿Quién clasifica a la Semifinal?", opciones, index=idx, key=key_radio, on_change=st.rerun)
            st.session_state.ganadores_4[item["llave"]] = st.session_state[key_radio]

        if st.button("Siguiente: Semifinales ➡️"):
            st.session_state.fase = "Semifinales"
            st.rerun()

# --- FASE SEMIFINALES ---
elif st.session_state.fase == "Semifinales":
    st.header("🚀 Semifinales del Mundo")
    if not st.session_state.ganadores_4:
        st.warning("⚠️ Primero debes definir los ganadores en los Cuartos de Final.")
    else:
        for item in estructura_2:
            eq_a = st.session_state.ganadores_4.get(item["a"], "Por definir")
            eq_b = st.session_state.ganadores_4.get(item["b"], "Por definir")
            
            opciones = [eq_a, eq_b]
            key_radio = f"radio_2_{item['llave']}_{eq_a}_{eq_b}"
            
            if key_radio in st.session_state:
                ganador_actual = st.session_state[key_radio]
                st.session_state.ganadores_2[item["llave"]] = ganador_actual
            else:
                ganador_actual = st.session_state.ganadores_2.get(item['llave'], eq_a)
            
            idx = opciones.index(ganador_actual) if ganador_actual in opciones else 0
            
            st.markdown(f"""
                <div style='background-color: #1e293b; padding: 10px 15px; border-radius: 8px 8px 0px 0px; border-left: 5px solid #475569; margin-top: 20px;'>
                    <h4 style='margin: 0; padding: 0; font-size: 1rem; color: #FFD700;'>🏆 Avanza: {ganador_actual}</h4>
                </div>
            """, unsafe_allow_html=True)

            st.radio("¿Quién avanza a la Gran Final?", opciones, index=idx, key=key_radio, on_change=st.rerun)
            st.session_state.ganadores_2[item["llave"]] = st.session_state[key_radio]

        if st.button("Siguiente: Gran Final ➡️"):
            st.session_state.fase = "Gran Final"
            st.rerun()

# --- FASE GRAN FINAL Y RESUMEN ---
elif st.session_state.fase == "Gran Final":
    st.header("👑 El Partido Soñado: Gran Final")
    if not st.session_state.ganadores_2:
        st.warning("⚠️ Primero debes definir los ganadores en las Semifinales.")
    else:
        eq_a = st.session_state.ganadores_2.get("d29", "Por definir")
        eq_b = st.session_state.ganadores_2.get("d30", "Por definir")
        
        opciones = [eq_a, eq_b]
        key_radio = f"radio_final_{eq_a}_{eq_b}"
        
        if key_radio in st.session_state:
            ganador_actual = st.session_state[key_radio]
            st.session_state.ganador_final = ganador_actual
        else:
            ganador_actual = st.session_state.ganador_final if st.session_state.ganador_final else eq_a
            
        idx = opciones.index(ganador_actual) if ganador_actual in opciones else 0
        
        st.markdown(f"""
            <div style='background-color: #1e293b; padding: 10px 15px; border-radius: 8px 8px 0px 0px; border-left: 5px solid #FFD700; margin-top: 20px;'>
                <h4 style='margin: 0; padding: 0; font-size: 1rem; color: #FFD700;'>👑 Campeón Mundial: {ganador_actual}</h4>
            </div>
        """, unsafe_allow_html=True)

        st.radio("Elige al Campeón del Mundo 2026:", opciones, index=idx, key=key_radio, on_change=st.rerun)
        ganador_final = st.session_state[key_radio]
        st.session_state.ganador_final = ganador_final

        st.balloons()
        st.success(f"🏆 ¡EL CAMPEÓN DEL MUNDIAL ES: {ganador_final.upper()}! 🏆")

        # CONSTRUCCIÓN DE LA TABLA RESUMEN DE 7 COLUMNAS
        st.subheader("📊 Tabla Resumen de tu Pronóstico")
        
        lista_c32 = list(st.session_state.clasificados.values()) + st.session_state.orden_terceros
        c32_txt = ", ".join(lista_c32)
        
        g_16_txt = ", ".join(list(st.session_state.ganadores_16.values()))
        g_8_txt = ", ".join(list(st.session_state.ganadores_8.values()))
        g_4_txt = ", ".join(list(st.session_state.ganadores_4.values()))
        g_2_txt = ", ".join(list(st.session_state.ganadores_2.values()))

        datos_pronostico = {
            "usuario": [st.session_state.usuario],
            "clasficados32": [c32_txt],
            "ganadores_16avos": [g_16_txt],
            "ganadores_octavos": [g_8_txt],
            "ganadores_4tos": [g_4_txt],
            "Ganadores_semifinales": [g_2_txt],
            "final": [ganador_final]
        }
        
        df_pronostico = pd.DataFrame(datos_pronostico)
        st.dataframe(df_pronostico, use_container_width=True)

        csv = df_pronostico.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar mi Pronóstico en Formato CSV",
            data=csv,
            file_name=f"pronostico_{st.session_state.usuario}.csv",
            mime="text/csv"
        )

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🔄 Reiniciar y Borrar todo el Torneo"):
            st.session_state.clear()
            st.rerun()