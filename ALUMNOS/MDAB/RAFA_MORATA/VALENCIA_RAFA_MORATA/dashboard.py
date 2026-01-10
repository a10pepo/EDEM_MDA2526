import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Valenbisi Dashboard", layout="wide")
st.title("🚲 Dashboard de Estado Valenbisi")

# --- CONEXIÓN A BASE DE DATOS ---
@st.cache_data
def cargar_datos():
    try:
        # Conectamos a localhost porque streamlit corre en tu PC, no en Docker
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password123",
            database="valenbisi_db",
            port="5432"
        )
        
        # Consultamos la tabla procesada por DBT
        query = """
        SELECT * FROM analytics.uso_horario
        ORDER BY hora DESC
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# Cargar datos
df = cargar_datos()

if not df.empty:
    # --- BARRA LATERAL ---
    st.sidebar.header("Filtros")
    # Si la columna se llama diferente en tu base de datos, ajusta esto.
    # Por defecto en DBT suele ser station_name.
    estacion = st.sidebar.selectbox("Elige una estación:", df['station_name'].unique())
    
    # Filtrar datos
    df_filtrado = df[df['station_name'] == estacion]
    
    # --- VISUALIZACIÓN ---
    col1, col2 = st.columns(2)
    
    # KPIs (Datos más recientes)
    if not df_filtrado.empty:
        ultimo_dato = df_filtrado.iloc[0]
        col1.metric("Bicis Disponibles (Avg)", f"{round(ultimo_dato['promedio_bicis_disponibles'], 1)}")
        col2.metric("Huecos Libres (Avg)", f"{round(ultimo_dato['promedio_espacios_libres'], 1)}")
        
        # Gráfico
        st.subheader(f"Evolución en: {estacion}")
        fig = px.line(df_filtrado, x='hora', y='promedio_bicis_disponibles', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos para esta estación.")

else:
    st.warning("No hay datos en la tabla analytics.uso_horario. Revisa si ejecutaste 'dbt run' y si Docker ha bajado datos.")