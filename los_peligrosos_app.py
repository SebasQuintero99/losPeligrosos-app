import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Los Peligrosos Neiva", layout="wide")

# Función para redondear a la decena de mil más cercana

# Título vibrante animado
st.markdown("""
<h1 style='text-align: center; font-size: 50px; background: -webkit-linear-gradient(left, #ff4b1f, #1fddff); 
-webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
🏌️‍♂️ Torneo Golf – Liquidación <br> <strong>"Los Peligrosos Neiva"</strong> ⛳
</h1>
""", unsafe_allow_html=True)

# Función para redondear a la decena de mil más cercana
def redondear_decenas_mil(valor):
    resto = valor % 10000
    if resto < 5000:
        return valor - resto
    else:
        return valor + (10000 - resto)

# Datos de prueba 1
jugadores_de_prueba_1 = [
    {"Nombre": "Tarache", "Handicap": 13, "Gross1": 41, "Gross2": 41, "Putts": 34},
    {"Nombre": "amor", "Handicap": 18, "Gross1": 55, "Gross2": 44, "Putts": 29},
    {"Nombre": "leon", "Handicap": 29, "Gross1": 55, "Gross2": 50, "Putts": 35},
    {"Nombre": "apa", "Handicap": 23, "Gross1": 46, "Gross2": 55, "Putts": 31},
    {"Nombre": "zamora", "Handicap": 19, "Gross1": 50, "Gross2": 44, "Putts": 32},
    {"Nombre": "pinto", "Handicap": 27, "Gross1": 62, "Gross2": 54, "Putts": 34},
    {"Nombre": "lugo", "Handicap": 34, "Gross1": 56, "Gross2": 54, "Putts": 39},
    {"Nombre": "artunduaga", "Handicap": 22, "Gross1": 47, "Gross2": 41, "Putts": 32},
    {"Nombre": "D. Perdomo", "Handicap": 34, "Gross1": 55, "Gross2": 57, "Putts": 40},
    {"Nombre": "O. chavarro", "Handicap": 31, "Gross1": 55, "Gross2": 50, "Putts": 32},
    {"Nombre": "lba", "Handicap": 25, "Gross1": 58, "Gross2": 52, "Putts": 34},
    {"Nombre": "mompy", "Handicap": 4, "Gross1": 44, "Gross2": 39, "Putts": 32},
    {"Nombre": "mexican", "Handicap": 8, "Gross1": 50, "Gross2": 44, "Putts": 32},
    {"Nombre": "yoyi", "Handicap": 29, "Gross1": 56, "Gross2": 48, "Putts": 34},
    {"Nombre": "mauro", "Handicap": 36, "Gross1": 65, "Gross2": 60, "Putts": 38},
    {"Nombre": "Jorge perdomo", "Handicap": 17, "Gross1": 47, "Gross2": 46, "Putts": 26},
]

# Datos de prueba 2
jugadores_de_prueba_2 = [
    {"Nombre": "Saul Correa", "Handicap": 3, "Gross1": 44, "Gross2": 36, "Putts": 31},
    {"Nombre": "Juan E Ramirez", "Handicap": 12, "Gross1": 42, "Gross2": 44, "Putts": 34},
    {"Nombre": "Ricardo Leon", "Handicap": 13, "Gross1": 40, "Gross2": 43, "Putts": 30},
    {"Nombre": "Andres Zamora", "Handicap": 14, "Gross1": 43, "Gross2": 45, "Putts": 31},
    {"Nombre": "Mauricio Muñoz", "Handicap": 16, "Gross1": 50, "Gross2": 44, "Putts": 31},
    {"Nombre": "Rafael Gonzalez", "Handicap": 16, "Gross1": 45, "Gross2": 47, "Putts": 31},
    {"Nombre": "Francisco Jimenez", "Handicap": 16, "Gross1": 42, "Gross2": 52, "Putts": 31},
    {"Nombre": "Enrique Salas", "Handicap": 17, "Gross1": 57, "Gross2": 47, "Putts": 31},
    {"Nombre": "Juan Artunduaga", "Handicap": 17, "Gross1": 47, "Gross2": 52, "Putts": 32},
    {"Nombre": "Nicolas Rodriguez", "Handicap": 18, "Gross1": 53, "Gross2": 49, "Putts": 31},
    {"Nombre": "Felio Ardila", "Handicap": 19, "Gross1": 55, "Gross2": 42, "Putts": 30},
    {"Nombre": "Luis M Angel", "Handicap": 21, "Gross1": 50, "Gross2": 46, "Putts": 27},
    {"Nombre": "Andres Sanchez", "Handicap": 22, "Gross1": 54, "Gross2": 52, "Putts": 33},
    {"Nombre": "Carlos Chavarro", "Handicap": 22, "Gross1": 49, "Gross2": 45, "Putts": 34},
    {"Nombre": "Jorge Rodriguez", "Handicap": 23, "Gross1": 51, "Gross2": 62, "Putts": 34},
    {"Nombre": "Jorge Ramirez", "Handicap": 24, "Gross1": 46, "Gross2": 50, "Putts": 29},
    {"Nombre": "Andres Reina", "Handicap": 26, "Gross1": 48, "Gross2": 50, "Putts": 30},
    {"Nombre": "Ricardo Leon (sr)", "Handicap": 26, "Gross1": 52, "Gross2": 46, "Putts": 31},
    {"Nombre": "German Garzon", "Handicap": 26, "Gross1": 56, "Gross2": 48, "Putts": 32},
    {"Nombre": "Javier Barrero", "Handicap": 26, "Gross1": 57, "Gross2": 50, "Putts": 32},
    {"Nombre": "Bernardo Macias", "Handicap": 26, "Gross1": 44, "Gross2": 47, "Putts": 32},
    {"Nombre": "Marzin Ibaza", "Handicap": 28, "Gross1": 44, "Gross2": 47, "Putts": 29},
    {"Nombre": "Juan S Chavarro", "Handicap": 28, "Gross1": 53, "Gross2": 57, "Putts": 30},
    {"Nombre": "Juan C Leon", "Handicap": 28, "Gross1": 46, "Gross2": 55, "Putts": 26},
    {"Nombre": "Rodrigo Ortiz", "Handicap": 29, "Gross1": 65, "Gross2": 51, "Putts": 28},
    {"Nombre": "Jorge Reina", "Handicap": 29, "Gross1": 61, "Gross2": 51, "Putts": 31},
    {"Nombre": "Johan Pinto", "Handicap": 30, "Gross1": 44, "Gross2": 47, "Putts": 33},
    {"Nombre": "Felipe Cabrera", "Handicap": 30, "Gross1": 60, "Gross2": 58, "Putts": 29},
    {"Nombre": "Hector Suarez", "Handicap": 31, "Gross1": 54, "Gross2": 58, "Putts": 35},
    {"Nombre": "Libardo Vargas", "Handicap": 32, "Gross1": 49, "Gross2": 52, "Putts": 31},
    {"Nombre": "William Rubiano", "Handicap": 35, "Gross1": 64, "Gross2": 61, "Putts": 34},
    {"Nombre": "Jhon Jordan", "Handicap": 36, "Gross1": 63, "Gross2": 63, "Putts": 35},
    {"Nombre": "Diego Perdomo", "Handicap": 36, "Gross1": 50, "Gross2": 54, "Putts": 37},
    {"Nombre": "Carlos M Perez", "Handicap": 36, "Gross1": 57, "Gross2": 67, "Putts": 42},
    {"Nombre": "Jhon Bedoya", "Handicap": 36, "Gross1": 53, "Gross2": 59, "Putts": 32}
]

def cargar_datos_de_prueba_1():
    st.session_state.jugadores = []
    for jugador in jugadores_de_prueba_1:
        total_gross = jugador["Gross1"] + jugador["Gross2"]
        neto = total_gross - jugador["Handicap"]
        st.session_state.jugadores.append({
            **jugador,
            "Gross Total": total_gross,
            "Neto": neto
        })

def cargar_datos_de_prueba_2():
    st.session_state.jugadores = []
    for jugador in jugadores_de_prueba_2:
        total_gross = jugador["Gross1"] + jugador["Gross2"]
        neto = total_gross - jugador["Handicap"]
        st.session_state.jugadores.append({
            **jugador,
            "Gross Total": total_gross,
            "Neto": neto
        })

# Sidebar: configuración
st.sidebar.header("Configuración del torneo")
# Botones de carga de datos de prueba
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Datos de prueba 1"):
        cargar_datos_de_prueba_1()
with col2:
    if st.button("Datos de prueba 2"):
        cargar_datos_de_prueba_2()
tipo_sabado = st.sidebar.selectbox("Tipo de sábado", ["Regular ($30.000 - x3.000)", "Peligroso ($60.000 - x2.000)"])
multiplicador = 3000 if "Regular" in tipo_sabado else 2000
case_individual = 30000 if "Regular" in tipo_sabado else 60000

# Ingreso de jugadores solo en la modal
st.subheader("Ingreso de jugadores")
if "jugadores" not in st.session_state:
    st.session_state.jugadores = []

if "show_modal" not in st.session_state:
    st.session_state.show_modal = False
    
if "jugador_a_editar" not in st.session_state:
    st.session_state.jugador_a_editar = None

if st.button("Agregar nuevo jugador"):
    st.session_state.jugador_a_editar = None
    st.session_state.show_modal = True

st.markdown("""
<style>
div[data-modal-container='true'] {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 90% !important;
    max-width: 800px !important;
    margin: 0 auto !important;
    z-index: 1000 !important;
}

div[data-modal-container='true'] > div {
    background: #0e1117 !important;
    padding: 40px !important;
    border-radius: 15px !important;
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2) !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

div[data-modal-container='true'] input,
div[data-modal-container='true'] .stNumberInput {
    font-size: 1.1em !important;
    padding: 10px !important;
    margin-bottom: 15px !important;
}

div[data-modal-container='true'] .stButton button {
    font-size: 1.1em !important;
    padding: 0.5em 2em !important;
    margin-top: 10px !important;
}

@media (max-width: 600px) {
    div[data-modal-container='true'] {
        width: 95% !important;
        max-width: none !important;
    }
    
    div[data-modal-container='true'] > div {
        padding: 15px !important;
    }
}

.stButton button {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
if st.session_state.show_modal:
    st.markdown('<div class="modal-backdrop">', unsafe_allow_html=True)
    st.markdown('<div class="modal-content">', unsafe_allow_html=True)
    
    # Header del modal
    st.markdown('<div class="modal-header"><h2>Agregar jugador</h2></div>', unsafe_allow_html=True)
    
    form = st.form("formulario_jugador")
    with form:
        # Si estamos editando, prellenamos los campos con los datos del jugador
        jugador_actual = st.session_state.jugadores[st.session_state.jugador_a_editar] if st.session_state.jugador_a_editar is not None else None
        
        nombre = st.text_input("Nombre del jugador", value=jugador_actual["Nombre"] if jugador_actual else "").strip()
        handicap = st.number_input("Handicap", 0, 54, step=1, value=int(jugador_actual["Handicap"]) if jugador_actual else 0)
        gross1 = st.number_input("Gross vuelta 1 (Hoyos 1-9)", 0, 100, step=1, value=int(jugador_actual["Gross1"]) if jugador_actual else 0)
        gross2 = st.number_input("Gross vuelta 2 (Hoyos 10-18)", 0, 100, step=1, value=int(jugador_actual["Gross2"]) if jugador_actual else 0)
        putts = st.number_input("Putts totales", 0, 100, step=1, value=int(jugador_actual["Putts"]) if jugador_actual else 0)
        
        submitted = st.form_submit_button("Guardar cambios" if jugador_actual else "Agregar")
    
    if submitted:
        errores = []
        if not nombre or not all(c.isalpha() or c.isspace() for c in nombre):
            errores.append("Nombre inválido")
        if gross1 < 30 and gross1 != 0:
            errores.append("Score de ida muy bajo")
        if gross2 < 30 and gross2 != 0:
            errores.append("Score de vuelta muy bajo")
        if (gross1 + gross2) > 0:
            if putts < (gross1 + gross2) / 4 and putts != 0:
                errores.append("Número de putts muy bajo")
            elif putts > (gross1 + gross2) / 1.5:
                errores.append("Número de putts muy alto")
        
        if errores:
            st.error("Por favor corrija los siguientes errores:\n" + "\n".join("- " + e for e in errores))
        else:
            total_gross = gross1 + gross2
            neto = total_gross - handicap
            nuevo_jugador = {
                "Nombre": nombre,
                "Handicap": handicap,
                "Gross1": gross1,
                "Gross2": gross2,
                "Gross Total": total_gross,
                "Neto": neto,
                "Putts": putts
            }
            
            if st.session_state.jugador_a_editar is not None:
                st.session_state.jugadores[st.session_state.jugador_a_editar] = nuevo_jugador
                st.success(f"¡Jugador {nombre} actualizado exitosamente!")
            else:
                st.session_state.jugadores.append(nuevo_jugador)
                st.success(f"¡Jugador {nombre} agregado exitosamente!")
                
            st.session_state.jugador_a_editar = None
            st.session_state.show_modal = False
            st.rerun()
    
    # Botón de cerrar fuera del formulario
    if st.button("Cancelar"):
        st.session_state.show_modal = False
        st.rerun()

# Mostrar jugadores y opción para eliminar
if st.session_state.jugadores:
    df = pd.DataFrame(st.session_state.jugadores)
    st.subheader("Resumen de jugadores ingresados")

    for i, row in df.iterrows():
        col1, col2, col3 = st.columns([7, 1, 1])
        with col1:
            st.markdown(f"**{i+1}. {row['Nombre']}** – Handicap: {row['Handicap']}, Gross: {row['Gross Total']}, Neto: {row['Neto']}, Putts: {row['Putts']}")
        with col2:
            if st.button("✏️ Editar", key=f"editar_{i}"):
                st.session_state.jugador_a_editar = i
                st.session_state.show_modal = True
                st.rerun()
        with col3:
            if st.button("❌ Eliminar", key=f"eliminar_{i}"):
                st.session_state.jugadores.pop(i)
                st.rerun()

    st.subheader("Calcular y Liquidar Torneo")
    df = pd.DataFrame(st.session_state.jugadores)

    # Calcular Neto de la segunda vuelta para desempates
    df['Neto2'] = df['Gross2'] - (df['Handicap'] / 2)

    # Ordenar con criterios de desempate
    df_neto_sorted = df.sort_values(by=["Neto", "Neto2", "Putts"], ascending=[True, True, True])
    df_putts_sorted = df.sort_values(by=["Putts", "Neto"], ascending=[True, True])

    total_jugadores = len(df)
    num_to_pay = math.ceil(total_jugadores / 2)

    totales_neto = 0
    totales_putts = 0

    paga_neto_list = []
    paga_putts_list = []
    total_individual_list = []

    # Identificar los índices de los jugadores que pagan para Neto y Putts
    indices_pagan_neto = df_neto_sorted.tail(num_to_pay).index
    indices_pagan_putts = df_putts_sorted.tail(num_to_pay).index

    for i, row in df.iterrows():
        paga_n_raw = (row["Neto"] - df_neto_sorted.iloc[0]["Neto"]) * multiplicador if i in indices_pagan_neto else 0
        paga_p_raw = (row["Putts"] - df_putts_sorted.iloc[0]["Putts"]) * multiplicador if i in indices_pagan_putts else 0

        paga_n = paga_n_raw
        paga_p = paga_p_raw

        total_individual = redondear_decenas_mil(paga_n + paga_p)

        paga_neto_list.append(paga_n)
        paga_putts_list.append(paga_p)
        total_individual_list.append(total_individual)

        totales_neto += paga_n
        totales_putts += paga_p

    df["Paga Neto"] = paga_neto_list
    df["Paga Putts"] = paga_putts_list
    df["Total a Pagar"] = total_individual_list

    st.subheader("Liquidación por jugador")
    # Crear una copia del DataFrame y ajustar el índice para que comience en 1
    df_display = df[["Nombre", "Handicap", "Gross Total", "Neto", "Putts", "Paga Neto", "Paga Putts", "Total a Pagar"]].copy()
    df_display.index = df_display.index + 1  # Ajustar el índice para que comience en 1
    st.dataframe(df_display)

    total_case = total_jugadores * case_individual
    total_pagos = sum(total_individual_list)
    total_recaudo = total_case + total_pagos

    atencion = redondear_decenas_mil(total_recaudo * 0.3)
    premios = total_recaudo - atencion

    # Calcular menor neto y menor putts
    menor_neto = df_neto_sorted.iloc[0]["Neto"]
    menor_putts = df_putts_sorted.iloc[0]["Putts"]
    ganador_neto = df_neto_sorted.iloc[0]["Nombre"]
    ganador_putts = df_putts_sorted.iloc[0]["Nombre"]

    st.subheader("💰 Resumen económico del torneo")
    st.markdown(f"**Total jugadores**: {total_jugadores}")
    st.markdown(f"**Menor Neto**: {menor_neto} ({ganador_neto})")
    st.markdown(f"**Menor Putts**: {menor_putts} ({ganador_putts})")
    st.markdown(f"**Total case**: ${total_case:,.0f}")
    st.markdown(f"**Total a pagar**: ${total_pagos:,.0f}")
    st.markdown(f"**Recaudo total**: ${total_recaudo:,.0f}")
    st.markdown(f"**30% atención**: ${atencion:,.0f}")
    st.markdown(f"**70% premios a repartir**: ${premios:,.0f}")

    # Distribución de premios
    st.subheader("🏆 Premiación")

    if total_jugadores <= 12:
        # Regla para 12 o menos jugadores: premia a los 2 primeros
        st.markdown("**Regla aplicada**: 12 o menos jugadores. Se premian los 2 primeros puestos (65% y 35%).")
        df_top = df_neto_sorted.head(2)
        premios_porcentajes = [0.65, 0.35]
        premios_distribuidos = 0

        for i, (idx, jugador) in enumerate(df_top.iterrows()):
            if i == 1:  # Para el segundo lugar, asignar lo que queda del premio
                monto = premios - premios_distribuidos
            else:  # Primer lugar
                monto = redondear_decenas_mil(premios * premios_porcentajes[i])
            premios_distribuidos += monto
            st.markdown(f"**{i+1}° lugar – {jugador['Nombre']}**: ${monto:,.0f}")
    else:
        # Regla para más de 12 jugadores: premia a los 3 primeros, muestra top 5
        st.markdown("**Regla aplicada**: Más de 12 jugadores. Se premian los 3 primeros puestos (50%, 30%, 20%).")
        df_top5 = df_neto_sorted.head(5)
        premios_top3 = [0.50, 0.30, 0.20]
        premios_distribuidos = 0
        
        for i, (idx, jugador) in enumerate(df_top5.iterrows()):
            if i < 3:  # Para los primeros 3 lugares, mostrar premios
                if i == 2:  # Para el tercer lugar, asignar lo que queda del premio
                    monto = premios - premios_distribuidos
                else:
                    monto = redondear_decenas_mil(premios * premios_top3[i])
                premios_distribuidos += monto
                st.markdown(f"**{i+1}° lugar – {jugador['Nombre']}**: ${monto:,.0f}")
            else:  # Para 4° y 5° lugar, solo mostrar posición y nombre
                st.markdown(f"**{i+1}° lugar – {jugador['Nombre']}**")


