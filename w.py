import streamlit as st
import pandas as pd
import random

# =====================
# ESTADO GLOBAL
# =====================
if "fase" not in st.session_state:
    st.session_state.fase = "grupos"

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
            st.rerun()
        else:
            st.error("Por favor, introduce un nombre válido.")
    st.stop()

# BARRA LATERAL CON CONTROL DE NAVEGACIÓN
st.sidebar.markdown(f"👤 **Usuario:** {st.session_state.usuario}")

if st.session_state.fase != "grupos":
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Navegación")
    if st.sidebar.button("◀️ Volver a Fase de Grupos"):
        # Limpiamos todo el progreso posterior de las llaves para que no guarde lo anterior
        claves_a_borrar = [
            "ganadores_16", "ganadores_8", "ganadores_4", "ganadores_2", 
            "llaves_16", "llaves_8", "llaves_4", "llaves_2", "llave_final"
        ]
        for clave in claves_a_borrar:
            if clave in st.session_state:
                del st.session_state[clave]
        
        st.session_state.fase = "grupos"
        st.rerun()

# =====================
# FASE GRUPOS
# =====================
if st.session_state.fase == "grupos":
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

    if st.button("Generar 16avos de Final"):
        terceros = st.session_state.mejores_terceros.copy()
        random.shuffle(terceros)
        
        clas = {k.lower(): v for k, v in st.session_state.clasificados.items()}
        contador = 0
        llaves_16_listas = []

        for item in estructura_16:
            a_key = item["a"]
            b_key = item["b"]
            
            eq_a = terceros[contador] if a_key == "t" else clas[a_key]
            if a_key == "t": contador += 1
                
            eq_b = terceros[contador] if b_key == "t" else clas[b_key]
            if b_key == "t": contador += 1

            llaves_16_listas.append({"llave": item["llave"], "a": eq_a, "b": eq_b})

        st.session_state.llaves_16 = llaves_16_listas
        st.session_state.fase = "16avos"
        st.rerun()

# =====================
# FASE 16AVOS DE FINAL
# =====================
if st.session_state.fase == "16avos":
    st.header("16avos de Final")
    ganadores_16 = {}

    for p in st.session_state.llaves_16:
        ganador = st.radio(f"{p['a']} vs {p['b']}", [p["a"], p["b"]], key=f"r16_{p['llave']}")
        ganadores_16[p["llave"]] = ganador

    if st.button("Generar Octavos de Final"):
        llaves_8_listas = []
        for item in estructura_8:
            eq_a = ganadores_16[item["a"]]
            eq_b = ganadores_16[item["b"]]
            llaves_8_listas.append({"llave": item["llave"], "a": eq_a, "b": eq_b})
            
        st.session_state.ganadores_16 = ganadores_16
        st.session_state.llaves_8 = llaves_8_listas
        st.session_state.fase = "octavos"
        st.rerun()

# =====================
# FASE OCTAVOS DE FINAL
# =====================
if st.session_state.fase == "octavos":
    st.header("Octavos de Final")
    ganadores_8 = {}

    for p in st.session_state.llaves_8:
        ganador = st.radio(f"{p['a']} vs {p['b']}", [p["a"], p["b"]], key=f"r8_{p['llave']}")
        ganadores_8[p["llave"]] = ganador

    if st.button("Generar Cuartos de Final"):
        llaves_4_listas = []
        for item in estructura_4:
            eq_a = ganadores_8[item["a"]]
            eq_b = ganadores_8[item["b"]]
            llaves_4_listas.append({"llave": item["llave"], "a": eq_a, "b": eq_b})

        st.session_state.ganadores_8 = ganadores_8
        st.session_state.llaves_4 = llaves_4_listas
        st.session_state.fase = "cuartos"
        st.rerun()

# =====================
# FASE CUARTOS DE FINAL
# =====================
if st.session_state.fase == "cuartos":
    st.header("Cuartos de Final")
    ganadores_4 = {}

    for p in st.session_state.llaves_4:
        ganador = st.radio(f"{p['a']} vs {p['b']}", [p["a"], p["b"]], key=f"r4_{p['llave']}")
        ganadores_4[p["llave"]] = ganador

    if st.button("Generar Semifinales"):
        llaves_2_listas = []
        for item in estructura_2:
            eq_a = ganadores_4[item["a"]]
            eq_b = ganadores_4[item["b"]]
            llaves_2_listas.append({"llave": item["llave"], "a": eq_a, "b": eq_b})

        st.session_state.ganadores_4 = ganadores_4
        st.session_state.llaves_2 = llaves_2_listas
        st.session_state.fase = "semis"
        st.rerun()

# =====================
# FASE SEMIFINALES
# =====================
if st.session_state.fase == "semis":
    st.header("Semifinales")
    ganadores_2 = {}

    for p in st.session_state.llaves_2:
        ganador = st.radio(f"{p['a']} vs {p['b']}", [p["a"], p["b"]], key=f"r2_{p['llave']}")
        ganadores_2[p["llave"]] = ganador

    if st.button("Generar Gran Final"):
        st.session_state.ganadores_2 = ganadores_2
        st.session_state.llave_final = {
            "llave": "d31",
            "a": ganadores_2["d29"],
            "b": ganadores_2["d30"]
        }
        st.session_state.fase = "final"
        st.rerun()

# =====================
# GRAN FINAL Y RECOLECCIÓN
# =====================
if st.session_state.fase == "final":
    st.header("Gran Final")
    p = st.session_state.llave_final

    ganador_final = st.radio(f"{p['a']} vs {p['b']}", [p["a"], p["b"]], key="final_winner")

    st.success(f"🏆 ¡EL CAMPEÓN DEL MUNDIAL ES: {ganador_final.upper()}! 🏆")

    st.subheader("📊 Resumen de tu Pronóstico")
    
    lista_c32 = list(st.session_state.clasificados.values()) + st.session_state.mejores_terceros
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

