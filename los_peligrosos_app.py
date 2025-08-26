import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="Los Peligrosos Neiva",
    page_icon="🏌️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para redondear a la decena de mil más cercana

# CSS personalizado para diseño moderno
st.markdown("""
<style>
    /* Tema principal */
    .main {
        padding-top: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #f39c12, #e74c3c, #9b59b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        color: #ecf0f1;
        font-size: 1.2rem;
        font-weight: 300;
        margin-top: 0;
    }
    
    /* Cards modernas */
    .modern-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Botones modernos */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Sidebar mejorado */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* Inputs modernos */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>

<div class="main-header">
    <h1 class="main-title">🏌️‍♂️ TORNEO GOLF ⛳</h1>
    <p class="subtitle">Sistema de Liquidación - "Los Peligrosos Neiva"</p>
</div>
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

# Sidebar con diseño moderno
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; margin-bottom: 1rem;'>
    <h2 style='color: white; margin: 0; font-weight: 600;'>⚙️ Configuración</h2>
    <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Torneo de Golf</p>
</div>
""", unsafe_allow_html=True)
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

# Sección de jugadores con diseño moderno
st.markdown("""
<div class="modern-card">
    <h2 style='color: #2c3e50; margin-bottom: 1rem; font-weight: 600; display: flex; align-items: center;'>
        📝 Gestión de Jugadores
    </h2>
</div>
""", unsafe_allow_html=True)
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
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
    padding: 2.5rem !important;
    border-radius: 20px !important;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    backdrop-filter: blur(20px) !important;
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
    
    st.markdown("""
    <div class="modern-card">
        <h3 style='color: #2c3e50; margin-bottom: 1.5rem; font-weight: 600; display: flex; align-items: center;'>
            📊 Lista de Jugadores Registrados
        </h3>
    </div>
    """, unsafe_allow_html=True)

    for i, row in df.iterrows():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                    border-radius: 15px; padding: 1.5rem; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1); 
                    border-left: 5px solid #667eea;'>
            <h4 style='color: #2c3e50; margin: 0 0 0.5rem 0; font-weight: 600;'>
                🏌️‍♂️ {i+1}. {row['Nombre']}
            </h4>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; color: #666;'>
                <div><strong>Handicap:</strong> {row['Handicap']}</div>
                <div><strong>Gross Total:</strong> {row['Gross Total']}</div>
                <div><strong>Neto:</strong> {row['Neto']}</div>
                <div><strong>Putts:</strong> {row['Putts']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([6, 1, 1])
        with col2:
            if st.button("✏️", key=f"editar_{i}", help="Editar jugador"):
                st.session_state.jugador_a_editar = i
                st.session_state.show_modal = True
                st.rerun()
        with col3:
            if st.button("🗑️", key=f"eliminar_{i}", help="Eliminar jugador"):
                st.session_state.jugadores.pop(i)
                st.rerun()

    st.markdown("""
    <div class="modern-card">
        <h2 style='color: #2c3e50; margin-bottom: 1rem; font-weight: 600; display: flex; align-items: center;'>
            📊 Cálculo y Liquidación del Torneo
        </h2>
    </div>
    """, unsafe_allow_html=True)
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

    st.markdown("""
    <div class="modern-card">
        <h3 style='color: #2c3e50; margin-bottom: 1rem; font-weight: 600; display: flex; align-items: center;'>
            💰 Liquidación Individual
        </h3>
    </div>
    """, unsafe_allow_html=True)
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

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); 
                color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0; 
                box-shadow: 0 10px 30px rgba(39, 174, 96, 0.3);'>
        <h3 style='margin: 0 0 1.5rem 0; font-weight: 600; display: flex; align-items: center;'>
            💰 Resumen Económico del Torneo
        </h3>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem;'>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px;'>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Total Jugadores</div>
                <div style='font-size: 1.8rem; font-weight: 600;'>{total_jugadores}</div>
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px;'>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Menor Neto</div>
                <div style='font-size: 1.8rem; font-weight: 600;'>{menor_neto}</div>
                <div style='font-size: 0.8rem; opacity: 0.7;'>{ganador_neto}</div>
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px;'>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Menor Putts</div>
                <div style='font-size: 1.8rem; font-weight: 600;'>{menor_putts}</div>
                <div style='font-size: 0.8rem; opacity: 0.7;'>{ganador_putts}</div>
            </div>
        </div>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;'>
            <div style='text-align: center;'>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Total Case</div>
                <div style='font-size: 1.5rem; font-weight: 600;'>${total_case:,.0f}</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Total a Pagar</div>
                <div style='font-size: 1.5rem; font-weight: 600;'>${total_pagos:,.0f}</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Recaudo Total</div>
                <div style='font-size: 1.5rem; font-weight: 600;'>${total_recaudo:,.0f}</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 0.9rem; opacity: 0.8;'>30% Atención</div>
                <div style='font-size: 1.5rem; font-weight: 600;'>${atencion:,.0f}</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 0.9rem; opacity: 0.8;'>70% Premios</div>
                <div style='font-size: 1.5rem; font-weight: 600;'>${premios:,.0f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Distribución de premios
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%); 
                color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0; 
                box-shadow: 0 10px 30px rgba(243, 156, 18, 0.3);'>
        <h3 style='margin: 0 0 1.5rem 0; font-weight: 600; display: flex; align-items: center;'>
            🏆 Premiación del Torneo
        </h3>
    """, unsafe_allow_html=True)

    if total_jugadores <= 12:
        # Regla para 12 o menos jugadores: premia a los 2 primeros
        st.markdown("<div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'><strong>Regla aplicada:</strong> 12 o menos jugadores. Se premian los 2 primeros puestos (65% y 35%).</div>", unsafe_allow_html=True)
        df_top = df_neto_sorted.head(2)
        premios_porcentajes = [0.65, 0.35]
        premios_distribuidos = 0

        for i, (idx, jugador) in enumerate(df_top.iterrows()):
            if i == 1:  # Para el segundo lugar, asignar lo que queda del premio
                monto = premios - premios_distribuidos
            else:  # Primer lugar
                monto = redondear_decenas_mil(premios * premios_porcentajes[i])
            premios_distribuidos += monto
            trofeo = ['🥇', '🥈'][i]
            st.markdown(f"""<div style='background: rgba(255,255,255,0.3); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-weight: 600;'>{trofeo} {i+1}° lugar - {jugador['Nombre']}</span>
                <span style='font-size: 1.2rem; font-weight: bold;'>${monto:,.0f}</span>
            </div>""", unsafe_allow_html=True)
        
        # Cerrar la sección de premiación
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Regla para más de 12 jugadores: premia a los 3 primeros, muestra top 5
        st.markdown("<div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'><strong>Regla aplicada:</strong> Más de 12 jugadores. Se premian los 3 primeros puestos (50%, 30%, 20%).</div>", unsafe_allow_html=True)
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
                trofeo = ['🥇', '🥈', '🥉'][i]
                st.markdown(f"""<div style='background: rgba(255,255,255,0.3); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-weight: 600;'>{trofeo} {i+1}° lugar - {jugador['Nombre']}</span>
                    <span style='font-size: 1.2rem; font-weight: bold;'>${monto:,.0f}</span>
                </div>""", unsafe_allow_html=True)
            else:  # Para 4° y 5° lugar, solo mostrar posición y nombre
                st.markdown(f"""<div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-weight: 600;'>🏅 {i+1}° lugar - {jugador['Nombre']}</span>
                    <span style='font-style: italic; opacity: 0.7;'>Posición de Honor</span>
                </div>""", unsafe_allow_html=True)

    # Cerrar la sección de premiación
    st.markdown("</div>", unsafe_allow_html=True)


