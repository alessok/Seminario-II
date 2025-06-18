import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import html
from sklearn.decomposition import PCA # Para el gráfico PCA

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard PYMEs - Análisis Clustering", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# CSS personalizado para un diseño más moderno
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: white;
        text-align: center;
        margin: 0.3rem 0;
        opacity: 0.9;
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .metric-card h3 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-card h2 {
        font-size: 2.2rem;
        font-weight: 700;
    }
    
    .cluster-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }
    
    .cluster-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .recommendation-box h4 {
        color: #ffd700;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    
    .recommendation-box ul {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    .recommendation-box li {
        margin: 0.3rem 0;
        line-height: 1.4;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Personalización de tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 12px 20px;
        border: 2px solid #e2e8f0;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #667eea;
        transform: translateY(-1px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Mejoras generales */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1, h2, h3, h4 {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .element-container {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header principal mejorado
st.markdown("""
<div class="main-header">
    <h1>🎓 Segmentación y Predicción de Comportamiento de Clientes en PYMEs</h1>
    <p><strong>Proyecto de Investigación en Análisis de Datos Empresariales</strong></p>
    <p><em>Sistema integrado de Clustering y Series Temporales para optimización de PYMEs</em></p>
    <p><strong>Desarrolladores:</strong> Alessandro Ledesma & Angelo Montes</p>
</div>
""", unsafe_allow_html=True)

# Información del proyecto en cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📊 Metodología</h3>
        <p><strong>8 fases de análisis</strong></p>
        <p>Clustering K-Medoids + Prophet</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>📈 Dataset</h3>
        <p><strong>3,944 registros</strong></p>
        <p>155 empresas analizadas</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>🕐 Período</h3>
        <p><strong>2023-2025</strong></p>
        <p>Pronósticos hasta 2026</p>
    </div>
    """, unsafe_allow_html=True)

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
cluster_names = {"0": "Líderes Transaccionales", "1": "Premium de Alto Valor", "2": "Emergentes Moderados"}
cluster_colors = {"0": "#667eea", "1": "#f093fb", "2": "#ffeaa7"}  # Colores más modernos y profesionales
cluster_icons = {"0": "🏆", "1": "💎", "2": "🌱"}  # Iconos representativos

cluster_descriptions = {
    "0": "Este clúster lidera con los mayores ingresos totales (38,119.24) y el mayor número de transacciones (33.02), además de la mayor diversidad de productos únicos (16.58). Su periodo de actividad más largo (804.16 días) sugiere una base de clientes leales y altamente activos. Representa a las PYMEs más consolidadas y exitosas.",
    "1": "Este clúster se destaca por tener el ticket promedio más alto (1,473.63), lo que indica compras de gran valor con una frecuencia moderada de transacciones (22.23). Sus ingresos totales significativos (32,567.36) y periodo de actividad considerable (759.18 días) reflejan una base de clientes estable y con alto poder adquisitivo.",
    "2": "Este clúster tiene los menores ingresos totales (16,171.36), número de transacciones (19.45) y productos únicos (12.07), junto con el ticket promedio más bajo (849.87) y el periodo de actividad más corto (725.95 días). Representa a PYMEs emergentes o de menor escala con una actividad menos intensa pero con potencial de crecimiento."
}

cluster_recommendations = {
    "0": """
    **Recomendación Principal (Basada en Marco Teórico):** Maximizar ventaja competitiva mediante modelo RFM extendido y clustering dinámico.
    
    **Fundamento Académico:** Según S. Wang et al. (2024), el modelo LRFMS supera al RFM tradicional en 18-21% para clusters de alta transaccionalidad.
    
    **Acciones Estratégicas Específicas:**
    
    🎯 **Programas de Fidelización Multinivel (Evidencia: Ebadi Jalal & Elmaghraby, 2024)**
    • Implementar sistema VIP con 3 niveles basado en frecuencia transaccional (33+ transacciones)
    • Beneficios escalonados: descuentos 5%-10%-15%, acceso temprano, servicios personalizados
    • ROI esperado: 15% aumento en ventas según modelo RFM mejorado (Kasem et al., 2024)
    
    🔄 **Cross-selling Predictivo (Base: Prophet + Clustering)**
    • Usar pronósticos Prophet para identificar ventanas óptimas de recomendación
    • Análisis de canasta de mercado en 16.58 productos únicos promedio
    • Automatización via email/WhatsApp en picos estacionales predichos
    
    📈 **Expansión Estratégica Basada en Datos**
    • Replicar modelo exitoso (804 días actividad promedio) en nuevos canales
    • Marketplace digital con algoritmos de recomendación similares
    • Franquicias usando metodología de clustering validada (Silhouette: 0.2337)
    """,
    "1": """
    **Recomendación Principal (Basada en Marco Teórico):** Optimizar experiencia premium mediante marketing de valor diferenciado.
    
    **Fundamento Académico:** Anitha & Neelakandan (2024) demuestran que la personalización premium aumenta retención en 20% y reduce inventario en sectores de alto valor.
    
    **Acciones Estratégicas Específicas:**
    
    💎 **Servicios Premium Científicamente Validados**
    • Justificación de ticket promedio ($1,473.63) mediante valor agregado cuantificable
    • Asesoramiento personalizado basado en análisis predictivo Prophet
    • Servicio postventa diferenciado para mantener período actividad (759 días promedio)
    • SLA premium: respuesta <2hrs, envío express, garantía extendida
    
    📊 **Upselling Estratégico con Inteligencia Temporal**
    • Identificar ventanas óptimas usando pronósticos MAPE 1.72% (mejor precisión)
    • Entrenar equipo con datos de 22.23 transacciones promedio por cliente
    • Productos complementarios de alto margen durante picos predichos
    • Seguimiento KPI: incremento ticket promedio 10-15%
    
    🎯 **Marketing de Valor Basado en Evidencia**
    • Contenido que destaque ROI cuantificable del ticket premium
    • Casos de éxito basados en datos reales del cluster
    • Testimonios de clientes con mayor período de actividad
    • Campañas dirigidas a prospectos similares (ingresos $30K-35K)
    """,
    "2": """
    **Recomendación Principal (Basada en Marco Teórico):** Acelerar crecimiento mediante estrategias de escalamiento validadas científicamente.
    
    **Fundamento Académico:** Bañales et al. (2025) demuestran que PYMEs emergentes pueden reducir distancia intra-cluster en 52% mediante clustering multifase.
    
    **Acciones Estratégicas Específicas:**
    
    📈 **Optimización de Ticket Promedio (Target: $849.87 → $1,200)**
    • Bundling inteligente basado en análisis de productos únicos (12.07 promedio)
    • Promociones "compra X, lleva Y" validadas estadísticamente
    • Descuentos por volumen escalados según capacidad financiera del cluster
    • Métricas: MAPE 52.86% indica alta variabilidad = oportunidad de mejora
    
    🔄 **Incremento de Frecuencia Transaccional (Target: 19.45 → 25)**
    • Campañas de reactivación cada 30 días (período actividad: 725 días)
    • WhatsApp automatizado con ofertas time-sensitive
    • Recordatorios predictivos basados en patrones Prophet identificados
    • Email marketing segmentado por comportamiento de compra histórico
    
    🚀 **Diversificación Estratégica Progresiva**
    • Incorporar gradualmente productos exitosos de clusters superiores
    • Análisis ABC de productos para maximizar rotación limitada
    • Alianzas estratégicas para ampliar catálogo sin inversión inicial
    • Plan escalonado: +2 productos únicos cada trimestre
    
    💡 **Mentoría Académica y Técnica**
    • Implementar metodología de 8 fases validada en esta investigación
    • Capacitación en análisis básico con herramientas gratuitas (Google Analytics)
    • Seguimiento mensual con métricas simplificadas del dashboard
    • Red de apoyo entre PYMEs del mismo cluster para mejores prácticas
    """
}

# --- 3. Verificar Carga y Crear Dashboard ---
if df_clusters_info is not None and df_historico is not None and pronosticos is not None and \
   df_summary is not None and df_mapeo is not None and df_X_procesado is not None:

    # Sidebar mejorado con diseño moderno
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
        <h2 style="margin-top: 0; text-align: center;">🎓 Investigación Académica</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
        <h4>🏛️ Universidad de Lima</h4>
        <p><strong>Facultad:</strong> Ingeniería</p>
        <p><strong>Carrera:</strong> Ingeniería de Sistemas</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
        <h4>📋 Trabajo de Investigación</h4>
        <p><em>Segmentación y Predicción de Comportamiento de Clientes en PYMEs mediante Clustering y Series Temporales</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
        <h4>👥 Autores</h4>
        <p>• Alessandro Paolo Ledesma Acuña <br><small>(20204562)</small></p>
        <p>• Angelo Montes Mamani <br><small>(20203252)</small></p>
        <p><strong>Asesora:</strong> Lourdes Ramírez Cerna</p>
        <p><strong>Fecha:</strong> Mayo 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
        <h4 style="margin-top: 0;">📊 Especificaciones Técnicas</h4>
        <p><strong>Metodología:</strong> 8 Fases</p>
        <p><strong>Dataset:</strong> 3,944 registros</p>
        <p><strong>Período:</strong> Enero 2023 - Mayo 2025</p>
        <p><strong>Algoritmo:</strong> K-Medoids (k=3)</p>
        <p><strong>Pronósticos:</strong> Prophet hasta 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Resumen General y Total", "🔍 Exploración por Clúster", "📊 Comparación y PCA"])

    with tab1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
            <h2 style="margin: 0; text-align: center;">📈 Resumen General de Ingresos</h2>
            <p style="text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;">
                Vista consolidada de los ingresos históricos y pronósticos de los 3 clústeres
            </p>
        </div>
        """, unsafe_allow_html=True)
        
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
        fig_total.update_layout(
            title='📊 Ingresos Totales: Histórico vs Pronóstico', 
            xaxis_title='Fecha', 
            yaxis_title='Ingresos Mensuales Totales',
            template='plotly_white',
            title_font_size=18,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_total, use_container_width=True)
        
        st.markdown("### 📋 Estadísticas Generales del Proyecto")
        
        # Métricas mejoradas con diseño de cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_pymes = df_clusters_info['numerodoi'].nunique()
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea; margin-top: 0;">🏢 Total PYMEs</h3>
                <h2 style="color: #2d3748; margin: 0;">{total_pymes}</h2>
                <p style="margin: 0; color: #718096;">Empresas analizadas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            num_clusters = df_summary.shape[0]
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea; margin-top: 0;">🎯 Clústeres</h3>
                <h2 style="color: #2d3748; margin: 0;">{num_clusters}</h2>
                <p style="margin: 0; color: #718096;">Segmentos identificados</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            total_registros = 3944
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea; margin-top: 0;">📊 Registros</h3>
                <h2 style="color: #2d3748; margin: 0;">{total_registros:,}</h2>
                <p style="margin: 0; color: #718096;">Datos procesados</p>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
            <h2 style="margin: 0; text-align: center;">🔍 Exploración Detallada por Clúster</h2>
            <p style="text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;">
                Análisis profundo de características, patrones y recomendaciones estratégicas
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        cluster_seleccionado = st.selectbox(
            "🎯 Selecciona un clúster para analizar:", 
            options=list(cluster_names.keys()),
            format_func=lambda x: f"{cluster_icons[x]} Clúster {x}: {cluster_names[x]}", 
            key='select_tab2_v6_completo'
        )

        # Header del clúster seleccionado
        st.markdown(f"""
        <div class="cluster-card">
            <h2 style="margin-top: 0; color: #2d3748;">
                {cluster_icons[cluster_seleccionado]} Clúster {cluster_seleccionado}: {cluster_names[cluster_seleccionado]}
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Layout en columnas para mejor organización
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 Características Promedio")
            # Crear una tabla más visual
            características_df = df_summary.loc[cluster_seleccionado].round(2)
            st.dataframe(
                características_df.to_frame().T, 
                use_container_width=True,
                hide_index=True
            )
            
            # Métrica de PYMEs con diseño mejorado
            num_pymes = df_clusters_info[df_clusters_info['cluster_kmedoids'] == int(cluster_seleccionado)].shape[0]
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: {cluster_colors[cluster_seleccionado]}; margin-top: 0;">
                    {cluster_icons[cluster_seleccionado]} PYMEs en este Clúster
                </h3>
                <h2 style="color: #2d3748; margin: 0;">{num_pymes}</h2>
                <p style="margin: 0; color: #718096;">Empresas clasificadas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📝 Descripción del Clúster")
            st.markdown(f"""
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; 
                        border-left: 4px solid {cluster_colors[cluster_seleccionado]};">
                {cluster_descriptions.get(cluster_seleccionado, "Descripción no disponible.")}
            </div>
            """, unsafe_allow_html=True)
        
        # Recomendaciones con diseño destacado
        st.markdown("#### 🎯 Recomendaciones Estratégicas")
        
        # Obtener el texto de recomendaciones
        recomendacion_texto = cluster_recommendations.get(cluster_seleccionado, "Recomendaciones no disponibles.")
        
        # Mostrar las recomendaciones usando st.info (SIN BACKGROUND MORADO)
        st.info(recomendacion_texto)

        # Sección de insights clave
        st.markdown("#### 💡 Insights Clave del Clúster")
        
        # Obtener datos específicos del cluster
        cluster_data = df_clusters_info[df_clusters_info['cluster_kmedoids'] == int(cluster_seleccionado)]
        
        if not cluster_data.empty:
            insights_col1, insights_col2, insights_col3 = st.columns(3)
            
            with insights_col1:
                avg_revenue = cluster_data['ingresos_totales'].mean()
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;
                            border-top: 3px solid {cluster_colors[cluster_seleccionado]};">
                    <h4 style="color: {cluster_colors[cluster_seleccionado]}; margin: 0;">💰 Ingreso Promedio</h4>
                    <h3 style="color: #2d3748; margin: 0.5rem 0;">S/{avg_revenue:,.0f}</h3>
                    <p style="color: #718096; margin: 0; font-size: 0.9rem;">por empresa</p>
                </div>
                """, unsafe_allow_html=True)
            
            with insights_col2:
                avg_transactions = cluster_data['numero_transacciones'].mean()
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;
                            border-top: 3px solid {cluster_colors[cluster_seleccionado]};">
                    <h4 style="color: {cluster_colors[cluster_seleccionado]}; margin: 0;">🔄 Transacciones</h4>
                    <h3 style="color: #2d3748; margin: 0.5rem 0;">{avg_transactions:.1f}</h3>
                    <p style="color: #718096; margin: 0; font-size: 0.9rem;">promedio por empresa</p>
                </div>
                """, unsafe_allow_html=True)
            
            with insights_col3:
                avg_ticket = cluster_data['ticket_promedio'].mean()
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;
                            border-top: 3px solid {cluster_colors[cluster_seleccionado]};">
                    <h4 style="color: {cluster_colors[cluster_seleccionado]}; margin: 0;">🎫 Ticket Promedio</h4>
                    <h3 style="color: #2d3748; margin: 0.5rem 0;">S/{avg_ticket:.2f}</h3>
                    <p style="color: #718096; margin: 0; font-size: 0.9rem;">por transacción</p>
                </div>
                """, unsafe_allow_html=True)

        # Sección del gráfico de pronóstico
        st.markdown("---") 
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="margin-top: 0; color: #2d3748;">📈 Ingresos Históricos y Pronóstico 2026</h4>
        </div>
        """, unsafe_allow_html=True)
        
        fig_cluster = go.Figure()
        fig_cluster.add_trace(go.Scatter(
            x=df_historico.index, 
            y=df_historico[cluster_seleccionado], 
            mode='lines', 
            name='📊 Histórico Real', 
            line=dict(color=cluster_colors[cluster_seleccionado], width=3)
        ))
        
        pronostico_actual = pronosticos.get(cluster_seleccionado)
        if pronostico_actual is not None:
             fig_cluster.add_trace(go.Scatter(
                 x=pronostico_actual.index, 
                 y=pronostico_actual['yhat'], 
                 mode='lines', 
                 name='🔮 Pronóstico Prophet', 
                 line=dict(color='#e74c3c', dash='dash', width=3)
             )) 
        
        fig_cluster.update_layout(
            title=f'{cluster_icons[cluster_seleccionado]} Evolución Temporal - Clúster {cluster_seleccionado}: {cluster_names[cluster_seleccionado]}', 
            xaxis_title='Fecha', 
            yaxis_title='Ingresos Mensuales',
            template='plotly_white',
            title_font_size=16,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='x unified'
        )
        st.plotly_chart(fig_cluster, use_container_width=True)

        # Tabla expandible mejorada
        with st.expander(f"🏢 Ver lista de PYMEs en Clúster {cluster_seleccionado} ({cluster_names[cluster_seleccionado]})"):
            pymes_en_cluster = df_clusters_info[df_clusters_info['cluster_kmedoids'] == int(cluster_seleccionado)]
            pymes_con_nombres = pd.merge(pymes_en_cluster, df_mapeo, on='numerodoi', how='left')
            st.markdown(f"""
            <div style="background: #f7fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <strong>Total de empresas en este clúster:</strong> {len(pymes_con_nombres)} PYMEs
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(
                pymes_con_nombres[['numerodoi', 'razonsocial', 'ingresos_totales']].round(0).set_index('numerodoi'),
                use_container_width=True
            )


    with tab3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;">
            <h2 style="margin: 0; text-align: center;">📊 Comparación Visual de Clústeres y Análisis PCA</h2>
            <p style="text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;">
                Análisis comparativo y visualización multidimensional de los segmentos
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sección de comparación rápida
        st.markdown("#### ⚡ Comparación Rápida de Clusters")
        
        # Crear métricas comparativas visuales
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        
        with comp_col1:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
                        border-left: 4px solid {cluster_colors['0']};">
                <h4 style="color: {cluster_colors['0']}; margin: 0;">{cluster_icons['0']} Clúster 0</h4>
                <h5 style="color: #2d3748; margin: 0.5rem 0;">Líderes Transaccionales</h5>
                <p style="color: #718096; margin: 0; font-size: 0.9rem;">Mayor frecuencia de transacciones</p>
                <div style="margin-top: 1rem;">
                    <span style="background: {cluster_colors['0']}; color: white; padding: 0.2rem 0.5rem; 
                                border-radius: 12px; font-size: 0.8rem;">57 PYMEs</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with comp_col2:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
                        border-left: 4px solid {cluster_colors['1']};">
                <h4 style="color: {cluster_colors['1']}; margin: 0;">{cluster_icons['1']} Clúster 1</h4>
                <h5 style="color: #2d3748; margin: 0.5rem 0;">Premium de Alto Valor</h5>
                <p style="color: #718096; margin: 0; font-size: 0.9rem;">Ticket promedio más alto</p>
                <div style="margin-top: 1rem;">
                    <span style="background: {cluster_colors['1']}; color: white; padding: 0.2rem 0.5rem; 
                                border-radius: 12px; font-size: 0.8rem;">56 PYMEs</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with comp_col3:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
                        border-left: 4px solid {cluster_colors['2']};">
                <h4 style="color: {cluster_colors['2']}; margin: 0;">{cluster_icons['2']} Clúster 2</h4>
                <h5 style="color: #2d3748; margin: 0.5rem 0;">Emergentes Moderados</h5>
                <p style="color: #718096; margin: 0; font-size: 0.9rem;">Mayor potencial de crecimiento</p>
                <div style="margin-top: 1rem;">
                    <span style="background: {cluster_colors['2']}; color: white; padding: 0.2rem 0.5rem; 
                                border-radius: 12px; font-size: 0.8rem;">42 PYMEs</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Sección de comparación mejorada
        st.markdown("### 📈 Análisis Comparativo de Características")
        
        col_comp1, col_comp2 = st.columns(2)

        with col_comp1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="margin-top: 0; color: #2d3748;">📊 Comparación de Medias</h4>
            </div>
            """, unsafe_allow_html=True)
            
            char_bar = st.selectbox(
                "Selecciona característica para comparar:", 
                options=df_summary.columns.tolist(), 
                key='bar_select_tab3_v6_completo'
            )
            
            fig_bar_comp = px.bar(
                df_summary, 
                x=df_summary.index, 
                y=char_bar, 
                title=f'📊 {char_bar} - Promedio por Clúster', 
                color=df_summary.index, 
                color_discrete_map=cluster_colors, 
                labels={'index': 'Clúster', char_bar: char_bar}
            )
            
            fig_bar_comp.update_layout(
                template='plotly_white',
                title_font_size=14,
                showlegend=False
            )
            
            # Agregar etiquetas de clúster con nombres
            for i, (idx, row) in enumerate(df_summary.iterrows()):
                fig_bar_comp.add_annotation(
                    x=idx,
                    y=row[char_bar],
                    text=f"{cluster_icons[idx]}",
                    showarrow=False,
                    font=dict(size=20),
                    yshift=10
                )
            
            st.plotly_chart(fig_bar_comp, use_container_width=True)
        
        with col_comp2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="margin-top: 0; color: #2d3748;">📦 Distribución de Características</h4>
            </div>
            """, unsafe_allow_html=True)
            
            char_box = st.selectbox(
                "Selecciona característica para distribución:", 
                options=df_summary.columns.tolist(), 
                key='box_select_tab3_v6_completo'
            )
            
            fig_box_comp = px.box(
                df_clusters_info, 
                x=df_clusters_info['cluster_kmedoids'].astype(str), 
                y=char_box, 
                title=f'📦 Distribución de {char_box}', 
                color=df_clusters_info['cluster_kmedoids'].astype(str), 
                color_discrete_map=cluster_colors, 
                labels={'cluster_kmedoids': 'Clúster'}
            )
            
            fig_box_comp.update_layout(
                template='plotly_white',
                title_font_size=14,
                showlegend=False
            )
            
            st.plotly_chart(fig_box_comp, use_container_width=True)

        # Sección PCA mejorada
        st.markdown("---")
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 2rem 0;">
            <h3 style="margin-top: 0; color: #2d3748;">🔬 Análisis de Componentes Principales (PCA)</h3>
            <p style="color: #718096; margin-bottom: 0;">
                Visualización de la separación natural de los clústeres en un espacio bidimensional
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if df_X_procesado is not None and df_clusters_info.shape[0] == df_X_procesado.shape[0]:
            pca = PCA(n_components=2, random_state=42)
            principal_components = pca.fit_transform(df_X_procesado)
            df_pca = pd.DataFrame(data=principal_components, columns=['PCA Componente 1', 'PCA Componente 2'])
            
            df_pca['Clúster Etiqueta'] = df_clusters_info['cluster_kmedoids'].astype(str).values 
            df_pca['Clúster Nombre'] = df_pca['Clúster Etiqueta'].map(
                lambda x: f"{cluster_icons[x]} {cluster_names.get(x, '')}"
            )

            fig_pca = px.scatter(
                df_pca, 
                x='PCA Componente 1', 
                y='PCA Componente 2', 
                color='Clúster Nombre',
                title='🔬 Separación de PYMEs por Clúster usando Análisis de Componentes Principales',
                color_discrete_map={f"{cluster_icons[k]} {v}": cluster_colors[k] for k, v in cluster_names.items()},
                hover_data={'Clúster Nombre': True, 'Clúster Etiqueta': True},
                size_max=10
            )
            
            fig_pca.update_layout(
                template='plotly_white',
                title_font_size=16,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02
                ),
                width=800,
                height=600
            )
            
            fig_pca.update_traces(marker=dict(size=8, opacity=0.7))
            st.plotly_chart(fig_pca, use_container_width=True)
            
            # Métricas de varianza explicada en cards
            explained_variance = pca.explained_variance_ratio_
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #667eea; margin-top: 0;">📊 Componente 1</h4>
                    <h3 style="color: #2d3748; margin: 0;">{explained_variance[0]:.1%}</h3>
                    <p style="margin: 0; color: #718096;">Varianza explicada</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #667eea; margin-top: 0;">📊 Componente 2</h4>
                    <h3 style="color: #2d3748; margin: 0;">{explained_variance[1]:.1%}</h3>
                    <p style="margin: 0; color: #718096;">Varianza explicada</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #667eea; margin-top: 0;">📊 Total</h4>
                    <h3 style="color: #2d3748; margin: 0;">{sum(explained_variance):.1%}</h3>
                    <p style="margin: 0; color: #718096;">Varianza total explicada</p>
                </div>
                """, unsafe_allow_html=True)
                
        else:
            st.markdown("""
            <div style="background: #fed7d7; border: 1px solid #fc8181; color: #c53030; 
                        padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                ⚠️ <strong>Datos no disponibles:</strong> No se puede generar el gráfico PCA. 
                Verifica que los datos de X_procesado estén disponibles y coincidan en tamaño.
            </div>
            """, unsafe_allow_html=True)

else:
    # Página de error mejorada
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fc8181 0%, #f56565 100%); 
                padding: 3rem; border-radius: 15px; color: white; text-align: center; margin: 2rem 0;">
        <h1 style="margin: 0; font-size: 3rem;">⚠️</h1>
        <h2 style="margin: 1rem 0;">Error en la Carga de Datos</h2>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            No se pudieron cargar todos los datos necesarios para el dashboard.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 10px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 2rem 0;">
        <h3 style="color: #2d3748; margin-top: 0;">🔧 Pasos para solucionar:</h3>
        <ol style="color: #4a5568; line-height: 1.6;">
            <li>Verifica que todos los archivos CSV estén en la carpeta del proyecto</li>
            <li>Asegúrate de que los archivos se hayan generado correctamente</li>
            <li>Ejecuta el proceso de análisis completo antes de usar el dashboard</li>
            <li>Revisa los logs para identificar errores específicos</li>
        </ol>
        
        <h4 style="color: #2d3748; margin-top: 2rem;">📋 Archivos requeridos:</h4>
        <ul style="color: #4a5568; line-height: 1.6;">
            <li><code>pymes_con_clusters.csv</code></li>
            <li><code>ts_mensual_historico.csv</code></li>
            <li><code>pronostico_prophet_cluster_0.csv</code></li>
            <li><code>pronostico_prophet_cluster_1.csv</code></li>
            <li><code>pronostico_prophet_cluster_2.csv</code></li>
            <li><code>kmedoids_summary.csv</code></li>
            <li><code>mapeo_pymes.csv</code></li>
            <li><code>X_procesado_para_pca.csv</code></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer del dashboard
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 10px; color: white; text-align: center; margin: 2rem 0;">
    <h3 style="margin: 0;">🎓 Dashboard de Investigación Académica</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Universidad de Lima | Facultad de Ingeniería | Ingeniería de Sistemas<br>
        <strong>Alessandro Ledesma & Angelo Montes</strong> | Mayo 2025
    </p>
</div>
""", unsafe_allow_html=True)