import streamlit as st
import pandas as pd
import random
import os

# =====================
# ESTADO GLOBAL
# =====================
if "fase" not in st.session_state:
    st.session_state.fase = "grupos"

# =====================
# FUNCIÓN DE AUXILIO PARA CARGAR DATOS
# =====================
def cargar_datos_locales():
    """Carga los datos desde archivos JSON o CSV en lugar de Google Sheets"""
    # Intentamos cargar la lista de grupos
    if os.path.exists("grupos.json"):
        df_grupos = pd.read_json("grupos.json")
    elif os.path.exists("grupos.csv"):
        df_grupos = pd.read_csv("grupos.csv")
    else:
        # Datos de simulación por defecto si no encuentra el archivo para que la app no explote
        st.warning("No se encontró el archivo 'grupos.json' o 'grupos.csv'. Usando datos de prueba.")
        df_grupos = pd.DataFrame([
            {"grupo": "a", "equipo": "Ecuador"}, {"grupo": "a", "equipo": "Qatar"}, 
            {"grupo": "a", "equipo": "Senegal"}, {"grupo": "a", "equipo": "Países Bajos"},
            {"grupo": "b", "equipo": "Inglaterra"}, {"grupo": "b", "equipo": "Irán"},
            {"grupo": "b", "equipo": "EEUU"}, {"grupo": "b", "equipo": "Gales"}
        ])

    df_grupos.columns = df_grupos.columns.str.strip().str.lower()
    
    # Organizar estructura de grupos
    dict_grupos = {
        g: df_grupos[df_grupos["grupo"] == g]["equipo"].tolist()
        for g in df_grupos["grupo"].unique()
    }

    # Intentamos cargar la estructura de los 16avos (cruces de llaves)
    if os.path.exists("emparejamiento16.json"):
        df_16 = pd.read_json("emparejamiento16.json")
    elif os.path.exists("emparejamiento16.csv"):
        df_16 = pd.read_csv("emparejamiento16.csv")
    else:
        # Estructura básica de simulación si no está el archivo
        df_16 = pd.DataFrame([
            {"llave": "L1", "equipo a": "1a", "equipo b": "t"},
            {"llave": "L2", "equipo a": "1b", "equipo b": "2a"}
        ])
        
    df_16.columns = df_16.columns.str.strip().str.lower()
    
    return dict_grupos, df_16

# Carga inicial veloz de datos
grupos, df16_estructura = cargar_datos_locales()

st.title("🏆 Polla Mundial - Bracket FIFA")

# =====================
# FASE GRUPOS
# =====================
if st.session_state.fase == "grupos":

    st.header("Fase de Grupos")

    clasificados = {}
    terceros_pool = []

    for g, equipos in grupos.items():

        st.subheader(f"Grupo {g.upper()}")

        primero = st.selectbox(f"1° {g}", equipos, key=f"p_{g}")
        segundo = st.selectbox(
            f"2° {g}",
            [e for e in equipos if e != primero],
            key=f"s_{g}"
        )

        clasificados[f"1{g}"] = primero
        clasificados[f"2{g}"] = segundo

        terceros_pool.extend([e for e in equipos if e not in [primero, segundo]])

    # guardar estado
    st.session_state.clasificados = clasificados
    st.session_state.terceros_pool = terceros_pool

    # =====================
    # SELECCIÓN 8 TERCEROS (SIN REPETIR GRUPO)
    # =====================
    st.header("Mejores terceros")

    mapa_grupo = {}
    for g, equipos in grupos.items():
        for e in equipos:
            if e in terceros_pool:
                mapa_grupo[e] = g

    seleccionados = []

    for i in range(min(8, len(terceros_pool))):

        usados_grupos = [mapa_grupo[e] for e in seleccionados]

        opciones = [
            e for e in terceros_pool
            if e not in seleccionados
            and mapa_grupo[e] not in usados_grupos
        ]

        if opciones:
            elegido = st.selectbox(f"Tercero {i+1}", opciones, key=f"t{i}")
            seleccionados.append(elegido)

    st.session_state.mejores_terceros = seleccionados

    # =====================
    # BOTÓN GENERAR 16AVOS
    # =====================
    if st.button("Generar 16avos"):

        terceros = st.session_state.mejores_terceros.copy()
        random.shuffle(terceros)

        clas = {k.lower(): v for k, v in st.session_state.clasificados.items()}

        contador = 0
        llaves = []

        for _, fila in df16_estructura.iterrows():

            a = str(fila["equipo a"]).lower()
            b = str(fila["equipo b"]).lower()

            if a == "t":
                if contador < len(terceros):
                    eq_a = terceros[contador]
                    contador += 1
                else:
                    eq_a = "Por definir"
            else:
                eq_a = clas.get(a, f"Ganador {a}")

            if b == "t":
                if contador < len(terceros):
                    eq_b = terceros[contador]
                    contador += 1
                else:
                    eq_b = "Por definir"
            else:
                eq_b = clas.get(b, f"Ganador {b}")

            llaves.append({"llave": fila["llave"], "a": eq_a, "b": eq_b})

        st.session_state.llaves_16 = llaves
        st.session_state.fase = "16avos"
        st.rerun()


# =====================
# FUNCIÓN SIGUIENTE FASE
# =====================
def generar_siguiente(lista):
    return [
        {"a": lista[i], "b": lista[i+1], "llave": f"m{i//2}"}
        for i in range(0, len(lista), 2)
    ]


# =====================
# 16AVOS
# =====================
if st.session_state.fase == "16avos":

    st.header("16avos")

    ganadores = {}

    for p in st.session_state.llaves_16:

        ganador = st.radio(
            f"{p['a']} vs {p['b']}",
            [p["a"], p["b"]],
            key=f"16_{p['llave']}"
        )

        ganadores[p["llave"]] = ganador

    if st.button("Generar Octavos"):
        st.session_state.llaves_8 = generar_siguiente(list(ganadores.values()))
        st.session_state.fase = "octavos"
        st.rerun()


# =====================
# OCTAVOS
# =====================
if st.session_state.fase == "octavos":

    st.header("Octavos")

    ganadores = {}

    for p in st.session_state.llaves_8:

        ganador = st.radio(
            f"{p['a']} vs {p['b']}",
            [p["a"], p["b"]],
            key=f"8_{p['llave']}"
        )

        ganadores[p["llave"]] = ganador

    if st.button("Generar Cuartos"):
        st.session_state.llaves_4 = generar_siguiente(list(ganadores.values()))
        st.session_state.fase = "cuartos"
        st.rerun()


# =====================
# CUARTOS
# =====================
if st.session_state.fase == "cuartos":

    st.header("Cuartos")

    ganadores = {}

    for p in st.session_state.llaves_4:

        ganador = st.radio(
            f"{p['a']} vs {p['b']}",
            [p["a"], p["b"]],
            key=f"4_{p['llave']}"
        )

        ganadores[p["llave"]] = ganador

    if st.button("Generar Semis"):
        st.session_state.llaves_2 = generar_siguiente(list(ganadores.values()))
        st.session_state.fase = "semis"
        st.rerun()


# =====================
# SEMIS
# =====================
if st.session_state.fase == "semis":

    st.header("Semifinales")

    ganadores = {}

    for p in st.session_state.llaves_2:

        ganador = st.radio(
            f"{p['a']} vs {p['b']}",
            [p["a"], p["b"]],
            key=f"2_{p['llave']}"
        )

        ganadores[p["llave"]] = ganador

    if st.button("Generar Final"):
        lista = list(ganadores.values())
        st.session_state.llave_final = {"a": lista[0], "b": lista[1], "llave": "final"}
        st.session_state.fase = "final"
        st.rerun()


# =====================
# FINAL
# =====================
if st.session_state.fase == "final":

    st.header("Final")

    p = st.session_state.llave_final

    ganador = st.radio(
        f"{p['a']} vs {p['b']}",
        [p["a"], p["b"]],
        key="final"
    )

    st.success(f"🏆 CAMPEÓN: {ganador}")

