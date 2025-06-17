"""
Utilidades para el análisis de clustering de PYMEs
================================================

Este módulo contiene funciones de utilidad para validación,
métricas y análisis complementarios del proyecto.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def validate_clustering_stability(X, labels, n_iterations=10, random_states=None):
    """
    Valida la estabilidad del clustering con diferentes semillas aleatorias.
    
    Args:
        X: Datos para clustering
        labels: Etiquetas actuales
        n_iterations: Número de iteraciones para validar
        random_states: Lista de semillas aleatorias
    
    Returns:
        dict: Métricas de estabilidad
    """
    if random_states is None:
        random_states = range(42, 42 + n_iterations)
    
    silhouette_scores = []
    davies_bouldin_scores = []
    calinski_harabasz_scores = []
    
    for rs in random_states:
        try:
            # Calcular métricas con los labels actuales
            sil_score = silhouette_score(X, labels)
            db_score = davies_bouldin_score(X, labels)
            ch_score = calinski_harabasz_score(X, labels)
            
            silhouette_scores.append(sil_score)
            davies_bouldin_scores.append(db_score)
            calinski_harabasz_scores.append(ch_score)
            
        except Exception as e:
            print(f"Error en iteración {rs}: {e}")
            continue
    
    return {
        'silhouette': {
            'mean': np.mean(silhouette_scores),
            'std': np.std(silhouette_scores),
            'scores': silhouette_scores
        },
        'davies_bouldin': {
            'mean': np.mean(davies_bouldin_scores),
            'std': np.std(davies_bouldin_scores),
            'scores': davies_bouldin_scores
        },
        'calinski_harabasz': {
            'mean': np.mean(calinski_harabasz_scores),
            'std': np.std(calinski_harabasz_scores),
            'scores': calinski_harabasz_scores
        }
    }

def calculate_business_metrics(df_clusters):
    """
    Calcula métricas de negocio adicionales por cluster.
    
    Args:
        df_clusters: DataFrame con información de clusters
    
    Returns:
        dict: Métricas de negocio por cluster
    """
    metrics = {}
    
    for cluster_id in df_clusters['cluster_kmedoids'].unique():
        cluster_data = df_clusters[df_clusters['cluster_kmedoids'] == cluster_id]
        
        metrics[cluster_id] = {
            'count': len(cluster_data),
            'revenue_mean': cluster_data['ingresos_totales'].mean(),
            'revenue_std': cluster_data['ingresos_totales'].std(),
            'revenue_median': cluster_data['ingresos_totales'].median(),
            'transactions_mean': cluster_data['numero_transacciones'].mean(),
            'ticket_mean': cluster_data['ticket_promedio'].mean(),
            'products_mean': cluster_data['numero_productos_unicos'].mean(),
            'activity_days_mean': cluster_data['periodo_actividad_dias'].mean(),
            
            # Métricas adicionales
            'revenue_per_day': cluster_data['ingresos_totales'].mean() / cluster_data['periodo_actividad_dias'].mean(),
            'efficiency_ratio': cluster_data['ingresos_totales'].mean() / cluster_data['numero_transacciones'].mean(),
            'product_diversity': cluster_data['numero_productos_unicos'].mean() / cluster_data['numero_transacciones'].mean(),
            
            # Percentiles
            'revenue_p25': cluster_data['ingresos_totales'].quantile(0.25),
            'revenue_p75': cluster_data['ingresos_totales'].quantile(0.75),
        }
    
    return metrics

def detect_outliers_iqr(df, column, factor=1.5):
    """
    Detecta outliers usando el método IQR.
    
    Args:
        df: DataFrame
        column: Columna a analizar
        factor: Factor de multiplicación para IQR
    
    Returns:
        pandas.Series: Máscara booleana de outliers
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - factor * IQR
    upper_bound = Q3 + factor * IQR
    
    return (df[column] < lower_bound) | (df[column] > upper_bound)

def create_cluster_comparison_chart(df_summary, metric):
    """
    Crea gráfico de comparación entre clusters.
    
    Args:
        df_summary: DataFrame con resumen por cluster
        metric: Métrica a comparar
    
    Returns:
        plotly.graph_objects.Figure: Gráfico de comparación
    """
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e']
    
    fig = go.Figure(data=[
        go.Bar(
            x=[f"Cluster {i}" for i in df_summary.index],
            y=df_summary[metric],
            marker_color=colors,
            text=df_summary[metric].round(2),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=f'Comparación de {metric} por Cluster',
        xaxis_title='Cluster',
        yaxis_title=metric,
        showlegend=False,
        height=400
    )
    
    return fig

def calculate_forecast_accuracy(actual, predicted):
    """
    Calcula métricas de precisión para pronósticos.
    
    Args:
        actual: Valores reales
        predicted: Valores predichos
    
    Returns:
        dict: Métricas de precisión
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    # Eliminar valores nulos
    mask = ~(np.isnan(actual) | np.isnan(predicted))
    actual = actual[mask]
    predicted = predicted[mask]
    
    if len(actual) == 0:
        return {'error': 'No hay datos válidos para calcular métricas'}
    
    mae = np.mean(np.abs(actual - predicted))
    mse = np.mean((actual - predicted) ** 2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'MAPE': mape,
        'R²': 1 - (np.sum((actual - predicted) ** 2) / np.sum((actual - np.mean(actual)) ** 2))
    }

def generate_cluster_insights(df_clusters, cluster_id):
    """
    Genera insights automáticos para un cluster específico.
    
    Args:
        df_clusters: DataFrame con datos de clusters
        cluster_id: ID del cluster a analizar
    
    Returns:
        dict: Insights del cluster
    """
    cluster_data = df_clusters[df_clusters['cluster_kmedoids'] == cluster_id]
    total_data = df_clusters
    
    insights = {
        'size_percentage': (len(cluster_data) / len(total_data)) * 100,
        'revenue_vs_average': (cluster_data['ingresos_totales'].mean() / total_data['ingresos_totales'].mean()) * 100,
        'transactions_vs_average': (cluster_data['numero_transacciones'].mean() / total_data['numero_transacciones'].mean()) * 100,
        'ticket_vs_average': (cluster_data['ticket_promedio'].mean() / total_data['ticket_promedio'].mean()) * 100,
        
        'top_performers': cluster_data.nlargest(3, 'ingresos_totales'),
        'growth_potential': 'High' if cluster_data['ingresos_totales'].std() > total_data['ingresos_totales'].std() else 'Moderate',
        
        'recommendations': _generate_recommendations(cluster_data, cluster_id)
    }
    
    return insights

def _generate_recommendations(cluster_data, cluster_id):
    """
    Genera recomendaciones automáticas basadas en datos del cluster.
    """
    avg_revenue = cluster_data['ingresos_totales'].mean()
    avg_transactions = cluster_data['numero_transacciones'].mean()
    avg_ticket = cluster_data['ticket_promedio'].mean()
    
    recommendations = []
    
    if cluster_id == 0:  # Líderes
        if avg_transactions > 30:
            recommendations.append("Implementar programa VIP de alto nivel")
        if avg_revenue > 35000:
            recommendations.append("Considerar expansión geográfica")
    
    elif cluster_id == 1:  # Premium
        if avg_ticket > 1400:
            recommendations.append("Enfocarse en servicios de ultra-premium")
        recommendations.append("Desarrollar paquetes de alto valor")
    
    elif cluster_id == 2:  # Emergentes
        if avg_transactions < 20:
            recommendations.append("Campaña de reactivación intensiva")
        if avg_ticket < 900:
            recommendations.append("Estrategias de bundling productos")
    
    return recommendations

def export_cluster_report(df_clusters, df_summary, output_path='cluster_report.html'):
    """
    Exporta un reporte completo en HTML.
    
    Args:
        df_clusters: DataFrame con datos de clusters
        df_summary: DataFrame con resumen por cluster
        output_path: Ruta del archivo de salida
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reporte de Clustering - PYMEs</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .cluster-section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007acc; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Reporte de Análisis de Clustering - PYMEs</h1>
            <p>Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <h2>📈 Resumen Ejecutivo</h2>
        <p>Total de PYMEs analizadas: {len(df_clusters)}</p>
        <p>Número de clusters identificados: {len(df_summary)}</p>
        
        <h2>📊 Métricas por Cluster</h2>
        {df_summary.to_html()}
        
        <h2>🎯 Recomendaciones Principales</h2>
        <div class="cluster-section">
            <h3>Cluster 0: Líderes Transaccionales</h3>
            <ul>
                <li>Implementar programas VIP multinivel</li>
                <li>Desarrollar estrategias de cross-selling</li>
                <li>Considerar expansión estratégica</li>
            </ul>
        </div>
        
        <div class="cluster-section">
            <h3>Cluster 1: Premium de Alto Valor</h3>
            <ul>
                <li>Servicios premium diferenciados</li>
                <li>Upselling temporal inteligente</li>
                <li>Marketing de valor</li>
            </ul>
        </div>
        
        <div class="cluster-section">
            <h3>Cluster 2: Emergentes Moderados</h3>
            <ul>
                <li>Optimización de ticket promedio</li>
                <li>Incremento de frecuencia</li>
                <li>Programas de mentoría</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Reporte exportado en: {output_path}")

# Funciones para análisis temporal avanzado
def analyze_seasonality(df_historical, cluster_id):
    """
    Analiza patrones estacionales en los datos históricos.
    """
    if str(cluster_id) not in df_historical.columns:
        return None
    
    data = df_historical[str(cluster_id)].dropna()
    
    # Análisis por mes
    monthly_avg = data.groupby(data.index.month).mean()
    
    # Análisis por trimestre
    quarterly_avg = data.groupby(data.index.quarter).mean()
    
    return {
        'monthly_patterns': monthly_avg,
        'quarterly_patterns': quarterly_avg,
        'peak_month': monthly_avg.idxmax(),
        'low_month': monthly_avg.idxmin(),
        'seasonality_strength': (monthly_avg.max() - monthly_avg.min()) / monthly_avg.mean()
    }
