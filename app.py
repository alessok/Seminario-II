import numpy as np
import streamlit as st
import pandas as pd # Importa pandas para manejar DataFrames
import plotly.express as px # Importa Plotly Express para crear gráficos de línea interactivos

# --- Configuración de la Página del Dashboard ---
st.set_page_config(layout='wide')
st.title('Dashboard de Pronóstico de Ingresos por Clúster de PYMEs')
# Texto Explicativo: Introducción (NUEVO)
st.write('Este dashboard presenta los resultados de la segmentación de PYMEs y el pronóstico de sus ingresos mensuales. Los pronósticos se basan en modelos de series temporales ajustados a datos históricos por cada segmento de clientes.')


# --- Cargar los Datos de Series de Tiempo ---
ts_data_filename = 'combined_time_series_data.csv'

@st.cache_data
def load_ts_data(filename):
    """Carga los datos de series de tiempo desde un archivo CSV."""
    data = pd.read_csv(filename)
    data['Fecha'] = pd.to_datetime(data['Fecha'])
    return data

combined_ts_data = load_ts_data(ts_data_filename)


# --- Cargar los Datos de Características de Clúster (Bloque Punto 1) ---
chars_filename = 'cluster_characteristics.csv'

@st.cache_data
def load_characteristics_data(filename):
    """Carga los datos de características de clúster desde un archivo CSV."""
    try:
        chars_data = pd.read_csv(filename, index_col=0) # Asumimos índice es el clúster
        return chars_data
    except FileNotFoundError:
        st.error(f"Error: Archivo de características de clúster no encontrado en '{filename}'. Asegúrate de que el archivo existe y está en la misma carpeta ('Seminario2') que app.py.")
        return None

cluster_characteristics_summary = load_characteristics_data(chars_filename)


# --- Definir Métricas de Evaluación (Bloque Punto 3) ---
sarima_metrics = {
    0: {'RMSE': 31103.02, 'MAE': 28321.19}, # Métricas para Clúster 0
    1: {'RMSE': 15242.39, 'MAE': 13051.92}, # Métricas para Clúster 1
    2: {'RMSE': 21687.07, 'MAE': 19497.38}  # Métricas para Clúster 2
}


# --- Opciones de Visualización (Sidebar) ---
st.sidebar.header('Opciones de Visualización')
cluster_list = ['Total', 'Clúster 0', 'Clúster 1', 'Clúster 2']
selected_cluster = st.sidebar.selectbox('Selecciona un Clúster', cluster_list)


# --- Preparar Datos para la Gráfica Principal ---
if selected_cluster == 'Total':
    plot_data = combined_ts_data[['Fecha', 'Ingresos_Total', 'Tipo_Dato']].copy()
    plot_data = plot_data.rename(columns={'Ingresos_Total': 'Ingresos'})
    y_label = 'Ingresos Mensuales Totales'
else:
    cluster_num_str = selected_cluster.split(' ')[1]
    ingresos_col = f'Ingresos_Cluster_{cluster_num_str}'
    plot_data = combined_ts_data[['Fecha', ingresos_col, 'Tipo_Dato']].copy()
    plot_data = plot_data.rename(columns={ingresos_col: 'Ingresos'})
    y_label = f'Ingresos Mensuales ({selected_cluster})'

# --- Crear y Mostrar la Gráfica de Series de Tiempo ---
fig = px.line(plot_data, x='Fecha', y='Ingresos', color='Tipo_Dato',
              title=f'Historial y Pronóstico de Ingresos - {selected_cluster}',
              labels={'Ingresos': y_label},
              line_dash='Tipo_Dato')

fig.update_layout(hovermode='x unified')
fig.update_xaxes(title_text='Fecha')
fig.update_yaxes(title_text=y_label)

st.plotly_chart(fig, use_container_width=True)

# Texto Explicativo: Gráfico (NUEVO)
st.markdown("""
**Cómo leer este gráfico:**
- La línea de color **azul (Histórico)** muestra los ingresos mensuales reales registrados hasta la fecha más reciente.
- La línea **punteada (Pronóstico)** muestra la proyección de ingresos para los próximos 6 meses según el modelo.
- Pasa el cursor sobre los puntos de la gráfica para ver la fecha y el valor exacto.
""")


# --- Organizar Métricas y Características en Columnas (Layout Mejorado) ---
if selected_cluster != 'Total':
    # Texto Explicativo: Perfil de Clúster (NUEVO - Condicional)
    st.markdown(f"---") # Línea separadora
    st.markdown(f"### Perfil del {selected_cluster}")
    # Añadir descripción según el clúster seleccionado
    if selected_cluster == 'Clúster 0':
        st.write("Este clúster representa a las PYMEs de **Alto Valor y Alta Actividad**, consistentemente importantes en términos de ingresos y frecuencia.")
    elif selected_cluster == 'Clúster 1':
        st.write("Este clúster agrupa a las PYMEs que han estado **Activas Recientemente** y tienen una **Larga Duración** como clientes, aunque sus patrones de ingresos pueden ser más intermitentes.")
    elif selected_cluster == 'Clúster 2':
         st.write("Este clúster corresponde a las PYMEs de **Menor Valor y Menos Actividad**, con ingresos y transacciones generalmente bajos o intermitentes.")
    else: # Esto no debería ocurrir con el selectbox, pero es seguro.
        st.write("Información de perfil no disponible para este clúster.")

    # Creamos 2 columnas para Métricas y Características.
    col_metrics, col_chars = st.columns(2)

    # Colocamos las Métricas en la primera columna
    with col_metrics:
        st.subheader(f'Métricas de Evaluación del Modelo ({selected_cluster})')
        try:
            cluster_num_int = int(selected_cluster.split(' ')[1])
            if cluster_num_int in sarima_metrics:
                metrics = sarima_metrics[cluster_num_int]
                st.metric(label="RMSE", value=f"{metrics['RMSE']:,.2f}")
                st.metric(label="MAE", value=f"{metrics['MAE']:,.2f}")
            else:
                st.write(f'No se encontraron métricas de evaluación para el {selected_cluster}.')
        except ValueError:
            st.write("Error interno al procesar la selección del clúster para mostrar métricas.")
        except Exception as e:
             st.write(f"Ocurrió un error inesperado al mostrar las métricas: {e}")

    # Colocamos las Características en la segunda columna
    with col_chars:
        st.subheader(f'Características Clave ({selected_cluster})')
        if cluster_characteristics_summary is not None:
            try:
                cluster_num_int = int(selected_cluster.split(' ')[1])
                if cluster_num_int in cluster_characteristics_summary.index:
                    st.dataframe(cluster_characteristics_summary.loc[[cluster_num_int]])
                else:
                    st.write(f'No se encontraron características detalladas para el {selected_cluster} en el archivo de características.')
            except ValueError:
                st.write("Error interno al procesar la selección del clúster para mostrar características.")
            except Exception as e:
                 st.write(f"Ocurrió un error inesperado al mostrar las características: {e}")
        # Si cluster_characteristics_summary es None, el error de archivo ya se mostró.


# --- Sección para Mostrar el Pronóstico Numérico en Tabla (Punto 2) ---
st.subheader('Pronóstico Numérico (Próximos 6 Meses)')
# Texto Explicativo: Tabla de Pronóstico (NUEVO)
st.write("Esta tabla muestra los valores numéricos exactos del pronóstico de ingresos mensuales para los próximos 6 meses (Enero a Junio de 2026) para cada clúster y el total agregado.")


# Filtra el DataFrame combinado para obtener solo las filas de 'Pronóstico'.
forecast_table_data = combined_ts_data[combined_ts_data['Tipo_Dato'] == 'Pronóstico'].copy()

# Selecciona las columnas para la tabla.
columns_for_forecast_table = [
    'Fecha',
    'Ingresos_Cluster_0',
    'Ingresos_Cluster_1',
    'Ingresos_Cluster_2',
    'Ingresos_Total'
]
forecast_table_data = forecast_table_data[columns_for_forecast_table]

# Formatear los números para la tabla.
for col in ['Ingresos_Cluster_0', 'Ingresos_Cluster_1', 'Ingresos_Cluster_2', 'Ingresos_Total']:
     if col in forecast_table_data.columns:
          forecast_table_data[col] = forecast_table_data[col].apply(lambda x: f'{x:,.2f}' if pd.notna(x) else '')

# Muestra la tabla.
st.dataframe(forecast_table_data)