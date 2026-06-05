import streamlit as st
import pandas as pd
import random

# =====================
# DATOS DEL MUNDIAL INTEGRADOS
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

st.title("🏆 Polla Mundial - Bracket FIFA 2026")

# Pedir nombre de usuario
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if st.session_state.usuario == "":
    st.subheader("Configuración Inicial")
    nombre = st.text_input("Introduce tu nombre para empezar el pronóstico:")
    if st.button("Comenzar"):
        if nombre.strip() != "":
            st.session_state.usuario = nombre.strip()
            st.session_state.fase = "Grupos"
            st.rerun()
        else:
            st.error("Por favor, introduce un nombre válido.")
    st.stop()

# =====================
# CONTROL DE ESTADOS INICIALES EN BLANCO
# =====================
if "ganadores_16" not in st.session_state: st.session_state.ganadores_16 = {}
if "ganadores_8" not in st.session_state: st.session_state.ganadores_8 = {}
if "ganadores_4" not in st.session_state: st.session_state.ganadores_4 = {}
if "ganadores_2" not in st.session_state: st.session_state.ganadores_2 = {}
if "ganador_final" not in st.session_state: st.session_state.ganador_final = ""
if "orden_terceros" not in st.session_state: st.session_state.orden_terceros = []

# BARRA LATERAL: INFO Y SELECTOR DE FASES
st.sidebar.markdown(f"👤 **Usuario:** {st.session_state.usuario}")
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Navegar por el Torneo")

# Selector que le permite al usuario saltar a cualquier fase libremente
lista_fases = ["Grupos", "16avos de Final", "Octavos de Final", "Cuartos de Final", "Semifinales", "Gran Final"]
fase_seleccionada = st.sidebar.radio("Ir a la fase:", lista_fases, index=lista_fases.index(st.session_state.fase))
st.session_state.fase = fase_seleccionada

# =====================
# CÁLCULOS EN CADENA (EL CORAZÓN DE LA APLICACIÓN)
# =====================

# 1. Resolver Terceros (Solo se mezclan la primera vez para mantener estabilidad)
if "clasificados" in st.session_state and "mejores_terceros" in st.session_state:
    if not st.session_state.orden_terceros or len(st.session_state.orden_terceros) != len(st.session_state.mejores_terceros):
        st.session_state.orden_terceros = st.session_state.mejores_terceros.copy()
        random.shuffle(st.session_state.orden_terceros)

# 2. Armar llaves de 16avos de forma dinámica basado en las elecciones actuales de Grupos
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
# VISTA GENERAL DE LAS FASES
# =====================

# --- FASE GRUPOS ---
if st.session_state.fase == "Grupos":
    st.header("Fase de Grupos")
    clasificados = {}
    terceros_pool = []

    for g, equipos in grupos.items():
        st.subheader(f"Grupo {g.upper()}")
        primero = st.selectbox(f"1° {g.upper()}", equipos, key=f"p_{g}")
        segundo = st.selectbox(f"2° {g.upper()}", [e for e in equipos if e != primero], key=f"s_{g}")
        
        clasificados[f"1{g}"] = primero
        clasificados[f"2{g}"] = segundo
        terceros_pool.extend([e for e in equipos if e not in [primero, segundo]])

    st.session_state.clasificados = clasificados
    st.session_state.terceros_pool = terceros_pool

    st.header("Mejores Terceros")
    mapa_grupo = {e: g for g, eqs in grupos.items() for e in eqs if e in terceros_pool}
    seleccionados = []

    for i in range(8):
        usados_grupos = [mapa_grupo[e] for e in seleccionados]
        opciones = [e for e in terceros_pool if e not in seleccionados and mapa_grupo[e] not in usados_grupos]
        if opciones:
            elegido = st.selectbox(f"Mejor Tercero {i+1}", opciones, key=f"t{i}")
            seleccionados.append(elegido)

    st.session_state.mejores_terceros = seleccionados
    
    if st.button("Siguiente: 16avos de Final ➡️"):
        st.session_state.fase = "16avos de Final"
        st.rerun()

# --- FASE 16AVOS ---
elif st.session_state.fase == "16avos de Final":
    st.header("16avos de Final")
    if not llaves_16_calculadas:
        st.warning("⚠️ Primero debes completar la Fase de Grupos.")
    else:
        for p in llaves_16_calculadas:
            # Si el ganador guardado previamente ya no está en la llave por una corrección, se resetea la opción
            opciones = [p["a"], p["b"]]
            idx = 0
            if p['llave'] in st.session_state.ganadores_16 and st.session_state.ganadores_16[p['llave']] in opciones:
                idx = opciones.index(st.session_state.ganadores_16[p['llave']])
            
            ganador = st.radio(f"{p['a']} vs {p['b']}", opciones, index=idx, key=f"radio_16_{p['llave']}")
            st.session_state.ganadores_16[p["llave"]] = ganador

        if st.button("Siguiente: Octavos de Final ➡️"):
            st.session_state.fase = "Octavos de Final"
            st.rerun()

# --- FASE OCTAVOS ---
elif st.session_state.fase == "Octavos de Final":
    st.header("Octavos de Final")
    if not st.session_state.ganadores_16:
        st.warning("⚠️ Primero debes votar en los 16avos de Final.")
    else:
        for item in estructura_8:
            eq_a = st.session_state.ganadores_16.get(item["a"], "Por definir")
            eq_b = st.session_state.ganadores_16.get(item["b"], "Por definir")
            
            opciones = [eq_a, eq_b]
            idx = 0
            if item['llave'] in st.session_state.ganadores_8 and st.session_state.ganadores_8[item['llave']] in opciones:
                idx = opciones.index(st.session_state.ganadores_8[item['llave']])

            ganador = st.radio(f"{eq_a} vs {eq_b}", opciones, index=idx, key=f"radio_8_{item['llave']}")
            st.session_state.ganadores_8[item["llave"]] = ganador

        if st.button("Siguiente: Cuartos de Final ➡️"):
            st.session_state.fase = "Cuartos de Final"
            st.rerun()

# --- FASE CUARTOS ---
elif st.session_state.fase == "Cuartos de Final":
    st.header("Cuartos de Final")
    if not st.session_state.ganadores_8:
        st.warning("⚠️ Primero debes votar en los Octavos de Final.")
    else:
        for item in estructura_4:
            eq_a = st.session_state.ganadores_8.get(item["a"], "Por definir")
            eq_b = st.session_state.ganadores_8.get(item["b"], "Por definir")
            
            opciones = [eq_a, eq_b]
            idx = 0
            if item['llave'] in st.session_state.ganadores_4 and st.session_state.ganadores_4[item['llave']] in opciones:
                idx = opciones.index(st.session_state.ganadores_4[item['llave']])

            ganador = st.radio(f"{eq_a} vs {eq_b}", opciones, index=idx, key=f"radio_4_{item['llave']}")
            st.session_state.ganadores_4[item["llave"]] = ganador

        if st.button("Siguiente: Semifinales ➡️"):
            st.session_state.fase = "Semifinales"
            st.rerun()

elif st.session_state.fase == "Semifinales":
    st.header("Semifinales")
    if not st.session_state.ganadores_4:
        st.warning("⚠️ Primero debes votar en los Cuartos de Final.")
    else:
        for item in estructura_2:
            eq_a = st.session_state.ganadores_4.get(item["a"], "Por definir")
            eq_b = st.session_state.ganadores_4.get(item["b"], "Por definir")
            
            opciones = [eq_a, eq_b]
            idx = 0
            if item['llave'] in st.session_state.ganadores_2 and st.session_state.ganadores_2[item['llave']] in opciones:
                idx = opciones.index(st.session_state.ganadores_2[item['llave']])

            # Clave dinámica única para evitar bloqueos al cambiar de equipos
            llave_dinamica = f"radio_2_{item['llave']}_{eq_a}_{eq_b}"
            ganador = st.radio(f"{eq_a} vs {eq_b}", opciones, index=idx, key=llave_dinamica)
            st.session_state.ganadores_2[item["llave"]] = ganador

        if st.button("Siguiente: Gran Final ➡️"):
            st.session_state.fase = "Gran Final"
            st.rerun()

# --- FASE GRAN FINAL Y RESUMEN ---
elif st.session_state.fase == "Gran Final":
    st.header("Gran Final")
    if not st.session_state.ganadores_2:
        st.warning("⚠️ Primero debes votar en las Semifinales.")
    else:
        eq_a = st.session_state.ganadores_2.get("d29", "Por definir")
        eq_b = st.session_state.ganadores_2.get("d30", "Por definir")
        
        opciones = [eq_a, eq_b]
        idx = 0
        if st.session_state.ganador_final in opciones:
            idx = opciones.index(st.session_state.ganador_final)

        # Clave dinámica para la gran final
        llave_final_dinamica = f"radio_final_{eq_a}_{eq_b}"
        ganador_final = st.radio(f"{eq_a} vs {eq_b}", opciones, index=idx, key=llave_final_dinamica)
        st.session_state.ganador_final = ganador_final

        st.success(f"🏆 ¡EL CAMPEÓN DEL MUNDIAL ES: {ganador_final.upper()}! 🏆")

        # CONSTRUCCIÓN DE LA TABLA DE RECOLECCIÓN DE 7 COLUMNAS
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
        st.dataframe(df_pronostico)

        csv = df_pronostico.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar mi Pronóstico (CSV)",
            data=csv,
            file_name=f"pronostico_{st.session_state.usuario}.csv",
            mime="text/csv"
        )

        if st.button("🔄 Reiniciar todo el Torneo"):
            st.session_state.clear()
            st.rerun()