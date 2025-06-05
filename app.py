import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.decomposition import PCA # Para el gráfico PCA

# --- 1. Configuración de la Página ---
st.set_page_config(page_title="Dashboard PYMEs", layout="wide", initial_sidebar_state="expanded")
st.title("📊 Comprensión Dinámica del Cliente en PYMEs")
st.markdown("Análisis de Segmentación (K-Medoids) y Pronósticos de Ingresos (Prophet)")

# --- 2. Carga de Datos ---
@st.cache_data
def load_data():
    try:
        df_clusters_info = pd.read_csv('pymes_con_clusters.csv') 
        df_historico = pd.read_csv('ts_mensual_historico.csv', index_col='fecha', parse_dates=True)
        df_historico.columns = [str(int(float(col))) for col in df_historico.columns]

        pronosticos = {}
        for i in range(3):
            try:
                pronosticos[str(i)] = pd.read_csv(f'pronostico_prophet_cluster_{i}.csv', index_col='ds', parse_dates=True)
            except FileNotFoundError:
                 pronosticos[str(i)] = None

        df_summary = pd.read_csv('kmedoids_summary.csv', index_col='cluster_kmedoids')
        df_summary.index = df_summary.index.astype(str)
        
        df_mapeo = pd.read_csv('mapeo_pymes.csv')
        
        df_X_procesado = pd.read_csv('X_procesado_para_pca.csv')

        return df_clusters_info, df_historico, pronosticos, df_summary, df_mapeo, df_X_procesado
    except Exception as e:
        st.error(f"Error al cargar los datos. Error: {e}")
        return None, None, None, None, None, None

df_clusters_info, df_historico, pronosticos, df_summary, df_mapeo, df_X_procesado = load_data()

# --- Nombres, Descripciones COMPLETAS y Recomendaciones COMPLETAS ---
cluster_names = {"0": "Líderes Consolidados", "1": "Transaccionales Activos", "2": "Emergentes Moderados"}
cluster_colors = {"0": "blue", "1": "green", "2": "orange"}

cluster_descriptions = {
    "0": "Este clúster se destaca por sus altos ingresos totales (34,560.04) y el ticket promedio más alto (aproximadamente 1,515.64), lo que indica compras de gran valor con una frecuencia moderada de transacciones (22.89). Su largo periodo de actividad (766.08 días) y cantidad total significativa (4,048.82) reflejan una base de clientes estable y consolidada.",
    "1": "Este clúster lidera con los mayores ingresos totales (36,785.56), el mayor número de transacciones (33.51) y la mayor diversidad de productos únicos (16.63), además de un ticket promedio elevado (1,081.5). Su periodo de actividad más largo (801.9 días) sugiere una base de clientes leales y altamente activos.",
    "2": "Este clúster tiene los menores ingresos totales (16,082.32), número de transacciones (19.51) y productos únicos (12.23), junto con el ticket promedio más bajo (839.38) y el periodo de actividad más corto (725.88 días). Representa a clientes nuevos o de menor escala con una actividad menos intensa."
}

cluster_recommendations = {
    "0": """
    **Recomendación Principal:** Diversificar la base de clientes y modernizar sus operaciones.
    **Acciones Concretas:**
    * Explorar nuevos mercados: Identificar y contactar a clientes potenciales en segmentos no atendidos (e.g., clientes más pequeños pero recurrentes) mediante campañas de prospección en redes sociales o ferias comerciales.
    * Invertir en digitalización: Implementar una plataforma de comercio electrónico o un sistema CRM (gestión de relaciones con clientes) para llegar a más clientes y gestionar mejor las relaciones existentes.
    * Encuestas de satisfacción: Enviar un formulario breve a sus clientes actuales (por email o WhatsApp) para identificar por qué su desempeño podría estar decayendo y usar esos datos para ajustar productos o servicios.
    """,
    "1": """
    **Recomendación Principal:** Retener clientes activos y maximizar ganancias en temporadas altas mediante estrategias personalizadas.
    **Acciones Concretas:**
    * Programas de lealtad: Lanzar un sistema de puntos o descuentos acumulables para clientes frecuentes, incentivando compras repetidas (e.g., "10% de descuento en tu próxima compra tras 5 transacciones").
    * Marketing personalizado: Usar datos de ventas para enviar ofertas específicas por email o SMS antes de los picos estacionales (e.g., "Sabemos que compras X en Navidad, aquí tienes un 15% de descuento").
    * Optimización estacional: Aumentar inventario y personal temporal durante las temporadas altas, basándose en patrones de demanda históricos, para evitar cuellos de botella.
    """,
    "2": """
    **Recomendación Principal:** Enfocarse en un nicho específico y buscar apoyo externo para crecer de manera sostenible.
    **Acciones Concretas:**
    * Definir un nicho: Elegir un producto o servicio estrella (e.g., "somos los mejores en repostería vegana local") y concentrar recursos en promocionarlo, evitando dispersión.
    * Marketing de bajo costo: Crear una página en Instagram o TikTok y publicar contenido diario (fotos, videos cortos) para ganar visibilidad, complementado con colaboraciones con negocios locales.
    * Buscar mentoría: Inscribirse en un programa gratuito de apoyo a PYMEs (como los ofrecidos por cámaras de comercio o incubadoras) para recibir asesoramiento en gestión y finanzas.
    """
}

# --- 3. Verificar Carga y Crear Dashboard ---
if df_clusters_info is not None and df_historico is not None and pronosticos is not None and \
   df_summary is not None and df_mapeo is not None and df_X_procesado is not None:

    st.sidebar.header("Información del Proyecto")
    st.sidebar.markdown("---")
    st.sidebar.markdown("Desarrollado como parte de la investigación:")
    st.sidebar.markdown("*Comprensión Dinámica del Cliente en PYMEs*")
    st.sidebar.markdown("**Autores:** Angelo Montes & Alessandro Ledesma")
    
    tab1, tab2, tab3 = st.tabs(["📈 Resumen General y Total", "🔍 Exploración por Clúster", "📊 Comparación y PCA"])

    with tab1:
        st.header("Ingresos Totales y Pronóstico")
        st.markdown("Esta vista muestra la suma de los ingresos históricos y el pronóstico consolidado de los 3 clústeres.")
        if 'Total' not in df_historico.columns: df_historico['Total'] = df_historico[["0", "1", "2"]].sum(axis=1)
        
        df_pronostico_total_calc = None
        for cl_id, forecast_df in pronosticos.items():
            if forecast_df is not None:
                temp_df = forecast_df[['yhat']].rename(columns={'yhat': cl_id})
                if df_pronostico_total_calc is None: df_pronostico_total_calc = temp_df
                else: df_pronostico_total_calc = df_pronostico_total_calc.join(temp_df, how='outer')
        
        df_pronostico_total_futuro = None
        if df_pronostico_total_calc is not None:
            df_pronostico_total_calc = df_pronostico_total_calc.fillna(0)
            if 'Total' not in df_pronostico_total_calc.columns: df_pronostico_total_calc['Total'] = df_pronostico_total_calc.sum(axis=1)
            
            ultima_fecha_hist = df_historico.index[-1]
            df_pronostico_total_futuro = df_pronostico_total_calc[df_pronostico_total_calc.index > ultima_fecha_hist]

        fig_total = go.Figure()
        fig_total.add_trace(go.Scatter(x=df_historico.index, y=df_historico['Total'], mode='lines', name='Histórico Total', line=dict(color='green', width=2))) 
        if df_pronostico_total_futuro is not None and not df_pronostico_total_futuro.empty:
            fig_total.add_trace(go.Scatter(x=df_pronostico_total_futuro.index, y=df_pronostico_total_futuro['Total'], mode='lines', name='Pronóstico Total', line=dict(color='purple', dash='dash', width=2)))
        fig_total.update_layout(title='Ingresos Totales (Histórico + Pronóstico)', xaxis_title='Fecha', yaxis_title='Ingresos Mensuales Totales')
        st.plotly_chart(fig_total, use_container_width=True)
        
        st.subheader("Estadísticas Generales")
        st.metric("Total PYMEs Analizadas", df_clusters_info['numerodoi'].nunique())
        st.metric("Número de Clústeres", df_summary.shape[0])

    with tab2:
        st.header("Exploración Detallada por Clúster")
        cluster_seleccionado = st.selectbox(
            "Selecciona un clúster:", options=list(cluster_names.keys()),
            format_func=lambda x: f"Clúster {x}: {cluster_names[x]}", key='select_tab2_v6_completo'
        )

        st.subheader(f"Perfil del Clúster {cluster_seleccionado}: {cluster_names[cluster_seleccionado]}")
        
        # Columna Izquierda para Características, Descripción y Recomendaciones
        st.markdown("#### Características Promedio")
        st.dataframe(df_summary.loc[cluster_seleccionado].round(2))
        st.metric(f"PYMEs en Clúster {cluster_seleccionado}", df_clusters_info[df_clusters_info['cluster_kmedoids'] == int(cluster_seleccionado)].shape[0])
        
        st.markdown("#### Descripción del Clúster")
        st.write(cluster_descriptions.get(cluster_seleccionado, "Descripción no disponible."))
        
        st.markdown("#### Recomendaciones Estratégicas")
        st.info(cluster_recommendations.get(cluster_seleccionado, "Recomendaciones no disponibles."))

        # Columna (o sección) para Gráfico de Pronóstico y Tabla Drill-Down debajo
        st.markdown("---") 
        st.markdown("#### Ingresos Históricos y Pronóstico 2026")
        fig_cluster = go.Figure()
        fig_cluster.add_trace(go.Scatter(x=df_historico.index, y=df_historico[cluster_seleccionado], mode='lines', name='Histórico Real', line=dict(color='green', width=2)))
        pronostico_actual = pronosticos.get(cluster_seleccionado)
        if pronostico_actual is not None:
             fig_cluster.add_trace(go.Scatter(x=pronostico_actual.index, y=pronostico_actual['yhat'], mode='lines', name='Pronóstico Prophet', line=dict(color='red', dash='dash', width=2))) 
        fig_cluster.update_layout(title=f'Ingresos - Clúster {cluster_seleccionado}', xaxis_title='Fecha', yaxis_title='Ingresos Mensuales', showlegend=True)
        st.plotly_chart(fig_cluster, use_container_width=True)

        with st.expander(f"Ver lista de PYMEs (numerodoi y Razón Social) en Clúster {cluster_seleccionado}"):
            pymes_en_cluster = df_clusters_info[df_clusters_info['cluster_kmedoids'] == int(cluster_seleccionado)]
            pymes_con_nombres = pd.merge(pymes_en_cluster, df_mapeo, on='numerodoi', how='left')
            st.dataframe(pymes_con_nombres[['numerodoi', 'razonsocial', 'ingresos_totales']].round(0).set_index('numerodoi'))


    with tab3:
        st.header("Comparación Visual de Clústeres y Análisis PCA")
        st.markdown("Utiliza estos gráficos para comparar características y ver la separación de clústeres.")
        
        col_comp1, col_comp2 = st.columns(2)

        with col_comp1:
            st.subheader("Comparación de Medias")
            char_bar = st.selectbox("Característica (Barras):", options=df_summary.columns.tolist(), key='bar_select_tab3_v6_completo')
            fig_bar_comp = px.bar(df_summary, x=df_summary.index, y=char_bar, 
                                 title=f'{char_bar} Promedio', color=df_summary.index, 
                                 color_discrete_map=cluster_colors, labels={'index': 'Clúster'})
            st.plotly_chart(fig_bar_comp, use_container_width=True)
        
        with col_comp2:
            st.subheader("Distribución de Características")
            char_box = st.selectbox("Característica (Cajas):", options=df_summary.columns.tolist(), key='box_select_tab3_v6_completo')
            fig_box_comp = px.box(df_clusters_info, x=df_clusters_info['cluster_kmedoids'].astype(str), y=char_box, 
                                 title=f'Distribución de {char_box}', color=df_clusters_info['cluster_kmedoids'].astype(str), 
                                 color_discrete_map=cluster_colors, labels={'cluster_kmedoids': 'Clúster'})
            st.plotly_chart(fig_box_comp, use_container_width=True)

        st.markdown("---")
        st.subheader("Visualización de Clústeres con PCA (2 Componentes)")
        if df_X_procesado is not None and df_clusters_info.shape[0] == df_X_procesado.shape[0]:
            pca = PCA(n_components=2, random_state=42)
            principal_components = pca.fit_transform(df_X_procesado)
            df_pca = pd.DataFrame(data=principal_components, columns=['PCA Componente 1', 'PCA Componente 2'])
            
            df_pca['Clúster Etiqueta'] = df_clusters_info['cluster_kmedoids'].astype(str).values 
            df_pca['Clúster Nombre'] = df_pca['Clúster Etiqueta'].map(lambda x: f"Clúster {x}: {cluster_names.get(x, '')}")

            fig_pca = px.scatter(df_pca, x='PCA Componente 1', y='PCA Componente 2', color='Clúster Nombre',
                                 title='Separación de PYMEs por Clúster (PCA)',
                                 color_discrete_map={f"Clúster {k}: {v}": cluster_colors[k] for k, v in cluster_names.items()},
                                 hover_data={'Clúster Nombre': True, 'Clúster Etiqueta': True}
                                )
            st.plotly_chart(fig_pca, use_container_width=True)
            
            explained_variance = pca.explained_variance_ratio_
            st.caption(f"Varianza explicada por PCA1: {explained_variance[0]:.2%}")
            st.caption(f"Varianza explicada por PCA2: {explained_variance[1]:.2%}")
            st.caption(f"Varianza total explicada por los 2 componentes: {sum(explained_variance):.2%}")
        else:
            st.warning("No se puede generar el gráfico PCA: datos de X_procesado no disponibles o no coinciden en tamaño.")

else:
    st.error("No se pudieron cargar todos los datos necesarios. Por favor, verifica que los archivos CSV estén en la misma carpeta y se hayan generado correctamente.")