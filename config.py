# Configuración del Proyecto de Clustering PYMEs
# =================================================

# Parámetros de Clustering
CLUSTERING_CONFIG = {
    'n_clusters': 3,
    'random_state': 42,
    'max_iter': 300,
    'algorithm': 'k-medoids'
}

# Parámetros de Prophet
PROPHET_CONFIG = {
    'seasonality_mode': 'multiplicative',
    'yearly_seasonality': True,
    'weekly_seasonality': False,
    'daily_seasonality': False,
    'interval_width': 0.95
}

# Configuración del Dashboard
DASHBOARD_CONFIG = {
    'page_title': 'Dashboard PYMEs - Análisis Clustering',
    'layout': 'wide',
    'theme': 'streamlit',
    'show_sidebar': True
}

# Rutas de archivos
FILE_PATHS = {
    'clusters': 'pymes_con_clusters.csv',
    'historical': 'ts_mensual_historico.csv',
    'summary': 'kmedoids_summary.csv',
    'mapping': 'mapeo_pymes.csv',
    'pca_data': 'X_procesado_para_pca.csv',
    'forecasts': {
        0: 'pronostico_prophet_cluster_0.csv',
        1: 'pronostico_prophet_cluster_1.csv',
        2: 'pronostico_prophet_cluster_2.csv'
    }
}

# Colores para visualizaciones
CLUSTER_COLORS = {
    '0': '#1f77b4',  # Azul
    '1': '#2ca02c',  # Verde
    '2': '#ff7f0e'   # Naranja
}

# Nombres de clusters
CLUSTER_NAMES = {
    '0': 'Líderes Transaccionales',
    '1': 'Premium de Alto Valor',
    '2': 'Emergentes Moderados'
}

# Métricas objetivo por cluster
CLUSTER_TARGETS = {
    '0': {
        'transactions_growth': 0.10,  # 10% incremento
        'revenue_growth': 0.15,       # 15% incremento
        'retention_rate': 0.95        # 95% retención
    },
    '1': {
        'ticket_growth': 0.12,        # 12% incremento en ticket
        'revenue_growth': 0.18,       # 18% incremento
        'retention_rate': 0.98        # 98% retención
    },
    '2': {
        'transactions_growth': 0.28,  # 28% incremento
        'ticket_growth': 0.41,        # 41% incremento
        'retention_rate': 0.85        # 85% retención
    }
}
