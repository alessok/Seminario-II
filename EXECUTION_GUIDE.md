# 🚀 Guía de Ejecución - Proyecto de Clustering PYMEs

## 📊 Estado Actual del Proyecto
- ✅ **Dashboard ejecutándose**: `http://localhost:8504` (desarrollo) | `https://localhost` (producción)
- ✅ **Datos sanitizados**: Información personal protegida
- ✅ **Funciones corregidas**: Error en `utils.py` resuelto
- ✅ **Tests verificados**: Todas las funciones principales funcionan
- ✅ **Docker desplegado**: Sistema en producción con HTTPS

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

### 3. Deployment con Docker (PRODUCCIÓN ACTIVA)
**Estado**: ✅ Sistema desplegado y funcionando

```bash
cd /Users/alessandroledesma/Seminario-II

# Verificar estado actual
docker ps

# Deployment en producción (YA EJECUTADO)
./deploy.sh prod

# Comandos adicionales de gestión:
./deploy.sh stop     # Detener servicios
./deploy.sh logs     # Ver logs del sistema
./deploy.sh restart  # Reiniciar servicios
```

**URLs de Acceso**:
- **HTTPS Seguro**: [https://localhost](https://localhost) (RECOMENDADO)
- **HTTP**: [http://localhost](http://localhost) (redirige automáticamente a HTTPS)

**Servicios Activos**:
- 🐘 PostgreSQL: `localhost:5432`
- 🔴 Redis: `localhost:6379`
- 🌐 Nginx (SSL): `localhost:443`
- 🐍 App Python: Interno (puerto 8501)

**Si Docker no está disponible**, usa las opciones 1 o 2 (ambas funcionan perfectamente).

### 4. Monitoreo del Sistema Docker
```bash
# Estado de contenedores
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f

# Recursos utilizados
docker stats

# Reiniciar servicio específico
docker-compose -f docker-compose.prod.yml restart pymes_clustering_app
```

### 5. Análisis Directo con Python
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
- `Dockerfile` & `docker-compose.yml` - Containerización desarrollo
- `docker-compose.prod.yml` - Configuración de producción
- `deploy.sh` - Script de deployment automatizado
- `nginx/nginx.conf` - Configuración del proxy reverso
- `nginx/ssl/` - Certificados SSL para HTTPS

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

### 🔧 Comandos Útiles

### Verificar Estado
```bash
# Estado del entorno virtual (desarrollo)
source .venv/bin/activate
python -c "import streamlit, pandas, plotly; print('✅ Todo funcionando')"

# Verificar datos
python -c "import pandas as pd; print(f'Registros: {len(pd.read_csv(\"pymes_con_clusters.csv\"))}')"

# Estado del sistema Docker (producción)
docker ps
docker-compose -f docker-compose.prod.yml ps
```

### Solución de Problemas
```bash
# Desarrollo - Si el puerto está ocupado
lsof -ti:8504 | xargs kill -9

# Desarrollo - Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Producción - Reiniciar sistema completo
./deploy.sh restart

# Producción - Ver logs de errores
docker-compose -f docker-compose.prod.yml logs pymes_clustering_app
```

## 📱 Acceso al Dashboard

### Modo Desarrollo
Una vez ejecutando con Streamlit, el dashboard estará disponible en:
- **Local**: [http://localhost:8504](http://localhost:8504)
- **Red**: Ver output del comando streamlit para IP externa

### Modo Producción (ACTIVO)
El sistema Docker está desplegado y disponible en:
- **HTTPS Seguro**: [https://localhost](https://localhost) ⭐ **RECOMENDADO**
- **HTTP**: [http://localhost](http://localhost) (redirige a HTTPS)

**Características del entorno de producción**:
- 🔒 SSL/TLS habilitado automáticamente
- 🚀 Nginx como proxy reverso para mejor rendimiento
- 💾 PostgreSQL para persistencia de datos
- ⚡ Redis para cache de alta velocidad
- 🛡️ Contenedores con usuarios no-root para seguridad

## 🎓 Contexto Académico
- **Proyecto**: Segmentación y Predicción de Comportamiento de Clientes en PYMEs
- **Metodología**: 8 fases de análisis
- **Dataset**: 3,944 registros de 155 empresas (2023-2025)
- **Técnicas**: K-Medoids + Prophet + PCA
- **Desarrolladores**: Alessandro Ledesma & Angelo Montes

---
**Última actualización**: 17 de junio de 2025
**Estado**: ✅ Completamente funcional (Desarrollo + Producción Docker)
**Producción**: ✅ Activa en https://localhost
