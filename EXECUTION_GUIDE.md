# 🚀 Guía de Ejecución - Proyecto de Clustering PYMEs

## 📊 Estado Actual del Proyecto
- ✅ **Dashboard ejecutándose**: `http://localhost:8504`
- ✅ **Datos sanitizados**: Información personal protegida
- ✅ **Funciones corregidas**: Error en `utils.py` resuelto
- ✅ **Tests verificados**: Todas las funciones principales funcionan

## 🎯 Formas de Ejecutar el Proyecto

### 1. Dashboard Principal (RECOMENDADO)
```bash
cd /Users/alessandroledesma/Seminario-II
source .venv/bin/activate
streamlit run app.py --server.port 8504
```
**URL**: [http://localhost:8504](http://localhost:8504)

### 2. Jupyter Notebook Interactivo
```bash
cd /Users/alessandroledesma/Seminario-II
source .venv/bin/activate
jupyter notebook SemiCode.ipynb
```

### 3. Deployment con Docker
```bash
cd /Users/alessandroledesma/Seminario-II
chmod +x deploy.sh
./deploy.sh
```

### 4. Análisis Directo con Python
```python
import pandas as pd
import utils

# Cargar datos
df_clusters = pd.read_csv('pymes_con_clusters.csv')

# Calcular métricas avanzadas
metrics = utils.calculate_business_metrics(df_clusters)

# Generar insights automáticos
insights = utils.generate_cluster_insights(df_clusters, cluster_id=0)
```

## 📁 Archivos Principales

### 🔹 Aplicación Principal
- `app.py` - Dashboard interactivo de Streamlit
- `config.py` - Configuración centralizada
- `utils.py` - Funciones de análisis avanzado

### 🔹 Datos
- `pymes_con_clusters.csv` - Dataset principal con clusters
- `mapeo_pymes_demo.csv` - Datos de demostración (seguros)
- `ts_mensual_historico.csv` - Series temporales históricas
- `pronostico_prophet_cluster_*.csv` - Pronósticos por cluster

### 🔹 Configuración y Deployment
- `requirements.txt` - Dependencias Python
- `Dockerfile` & `docker-compose.yml` - Containerización
- `deploy.sh` - Script de deployment automatizado

### 🔹 Seguridad
- `.gitignore` - Archivos excluidos del repositorio
- `SECURITY_README.md` - Guía de seguridad
- `mapeo_pymes_demo.csv` - Datos ficticios para demo

## 🛠️ Funcionalidades Disponibles

### 📊 Dashboard Interactivo
1. **Análisis de Clusters**: Visualización de 3 clusters identificados
2. **Métricas de Negocio**: KPIs por cluster y comparativas
3. **Análisis PCA**: Reducción dimensional y visualización
4. **Series Temporales**: Datos históricos y pronósticos Prophet
5. **Recomendaciones**: Estrategias específicas por cluster

### 🔍 Análisis Avanzado
- Detección de outliers automática
- Validación de estabilidad de clustering
- Métricas de precisión de pronósticos
- Análisis de estacionalidad
- Generación de insights automáticos

### 📈 Reportes
- Exportación a HTML
- Métricas empresariales avanzadas
- Recomendaciones estratégicas cuantificadas

## 🎯 Clusters Identificados

### Cluster 0: Líderes Transaccionales (Azul)
- **Características**: Alto volumen de transacciones (30+ mensuales)
- **Ingresos promedio**: 35,000+ soles
- **Estrategia**: Programas VIP y expansión

### Cluster 1: Premium de Alto Valor (Verde)
- **Características**: Tickets altos (1,400+ soles promedio)
- **Ingresos promedio**: 20,000-35,000 soles
- **Estrategia**: Servicios premium y upselling

### Cluster 2: Emergentes Moderados (Naranja)
- **Características**: En crecimiento (600-900 soles ticket)
- **Ingresos promedio**: <20,000 soles
- **Estrategia**: Optimización y reactivación

## 🔧 Comandos Útiles

### Verificar Estado
```bash
# Estado del entorno virtual
source .venv/bin/activate
python -c "import streamlit, pandas, plotly; print('✅ Todo funcionando')"

# Verificar datos
python -c "import pandas as pd; print(f'Registros: {len(pd.read_csv(\"pymes_con_clusters.csv\"))}')"
```

### Solución de Problemas
```bash
# Si el puerto está ocupado
lsof -ti:8504 | xargs kill -9

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 📱 Acceso al Dashboard
Una vez ejecutando, el dashboard estará disponible en:
- **Local**: [http://localhost:8504](http://localhost:8504)
- **Red**: Ver output del comando streamlit para IP externa

## 🎓 Contexto Académico
- **Proyecto**: Segmentación y Predicción de Comportamiento de Clientes en PYMEs
- **Metodología**: 8 fases de análisis
- **Dataset**: 3,944 registros de 155 empresas (2023-2025)
- **Técnicas**: K-Medoids + Prophet + PCA
- **Desarrolladores**: Alessandro Ledesma & Angelo Montes

---
**Última actualización**: 17 de junio de 2025
**Estado**: ✅ Completamente funcional
