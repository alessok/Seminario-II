# 📊 Segmentación y Predicción de Comportamiento de Clientes en PYMEs mediante Clustering y Series Temporales

## 🎓 **Proyecto de Investigación Académica**
**Enfoque:** Análisis de datos para optimización empresarial en PYMEs

### 👥 **Desarrolladores**
- **[Nombre ocultado por privacidad]**
- **[Nombre ocultado por privacidad]**

---

## 🔬 **Resumen del Proyecto**

Este proyecto implementa un **sistema integrado de clustering y series temporales** para optimizar la segmentación y predicción del comportamiento de clientes en pequeñas y medianas empresas (PYMEs) del sector minorista. La investigación aborda la **problemática de las PYMEs** que enfrentan dificultades para segmentar eficazmente a sus clientes debido a la falta de infraestructura tecnológica avanzada.

### 🎯 **Objetivo Principal**
Desarrollar una herramienta de análisis que permita a las PYMEs segmentar clientes y predecir comportamientos de compra mediante técnicas de machine learning.

---

## 🚀 **Características Técnicas del Proyecto**

### 📈 **Análisis de Clustering Comparativo**
- **Algoritmos implementados:** K-Means vs K-Medoids
- **Número óptimo de clusters:** 3 (determinado mediante análisis de silueta)
- **Muestra:** 155 PYMEs segmentadas exitosamente
- **Dataset:** 3,944 registros transaccionales
- **Métricas de validación:** Coeficiente de Silhouette, Davies-Bouldin, Calinski-Harabasz

### 🔮 **Pronósticos con Prophet**
- **Modelo:** Prophet para series temporales
- **Horizonte de pronóstico:** Hasta 2026
- **Variables predichas:** Ingresos mensuales por cluster
- **Métricas de evaluación:** RMSE, MAE, MAPE

### 📊 **Dashboard Interactivo**
- **Tecnología:** Streamlit con visualizaciones Plotly
- **Funcionalidades:** 
  - Visualización de clusters en tiempo real
  - Análisis PCA interactivo
  - Pronósticos temporales por cluster
  - Recomendaciones estratégicas basadas en evidencia
  - Validación con métricas técnicas

---

## 🎭 **Clusters Identificados (K-Medoids Seleccionado)**

### 🏆 **Cluster 0: "Líderes Transaccionales" (57 PYMEs)**
- **Ingresos promedio:** $38,119.24
- **Transacciones promedio:** 33.02
- **Productos únicos:** 16.58
- **Período actividad:** 804.16 días
- **Características:** Mayores ingresos, alta frecuencia transaccional, gran diversidad de productos

### 💎 **Cluster 1: "Premium de Alto Valor" (56 PYMEs)**
- **Ingresos promedio:** $32,567.36
- **Ticket promedio:** $1,473.63 (el más alto)
- **Transacciones promedio:** 22.23
- **Período actividad:** 759.18 días
- **Características:** Enfoque en productos/servicios de alto valor, clientes premium

### 🌱 **Cluster 2: "Emergentes Moderados" (42 PYMEs)**
- **Ingresos promedio:** $16,171.36
- **Ticket promedio:** $849.87
- **Transacciones promedio:** 19.45
- **Período actividad:** 725.95 días
- **Características:** Menor escala, gran potencial de crecimiento

---

## 🔬 **Metodología Implementada**

1. **Recolección de Dataset:** Colaboración con empresa del sector minorista
2. **Preprocesamiento y Selección:** Agregación de datos, normalización
3. **Implementación de Clustering:** Comparación K-Means vs K-Medoids
4. **Métricas de Validación:** Silhouette, Davies-Bouldin, Calinski-Harabasz
5. **Series Temporales Prophet:** Modelos predictivos por cluster
6. **Interpretación de Resultados:** Análisis de patrones financieros
7. **Dashboard Interactivo:** Visualización con Streamlit
8. **Validación:** Testing con usuarios reales

---

## 📁 **Estructura del Proyecto**

```
├── SemiCode.ipynb                      # Notebook principal con análisis completo
├── app.py                             # Dashboard interactivo
├── requirements.txt                   # Dependencias del proyecto
├── README.md                          # Documentación del proyecto
├── pymes_con_clusters.csv             # Dataset con asignaciones de clusters
├── kmedoids_summary.csv               # Resumen estadístico por cluster
├── ts_mensual_historico.csv           # Series temporales históricas
├── mapeo_pymes.csv                    # Mapeo de empresas
├── X_procesado_para_pca.csv           # Datos procesados para PCA
├── pronostico_prophet_cluster_0.csv   # Pronósticos Cluster 0
├── pronostico_prophet_cluster_1.csv   # Pronósticos Cluster 1
└── pronostico_prophet_cluster_2.csv   # Pronósticos Cluster 2
```

---

## 🔧 **Instalación y Uso**

### 1. Clonar el repositorio
```bash
git clone https://github.com/alessok/Seminario-II.git
cd Seminario-II
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar análisis completo
```bash
jupyter notebook SemiCode.ipynb
```

### 4. Ejecutar dashboard
```bash
streamlit run app.py
```

### 5. Acceder al dashboard
Abrir en el navegador: `http://localhost:8501`

---

## 📊 **Resultados Obtenidos**

### **Métricas de Clustering (K-Medoids):**
- **Silhouette Score:** 0.234 (Separación aceptable)
- **Davies-Bouldin Index:** 1.324 (Buena cohesión)  
- **Calinski-Harabasz Index:** 54.65 (Clusters bien definidos)

### **Métricas de Pronósticos Prophet:**
- **Cluster Líderes:** MAPE=1.76% (Alta precisión)
- **Cluster Premium:** MAPE=1.72% (Muy alta precisión)
- **Cluster Emergentes:** MAPE=52.86% (Moderada precisión)

### **Validación del Sistema:**
- ✅ **Segmentación exitosa:** 3 clusters diferenciados
- ✅ **Alta precisión predictiva:** MAPE <2% para clusters principales
- ✅ **Metodología reproducible:** Proceso documentado
- ✅ **Dashboard funcional:** Herramienta práctica para PYMEs

---

## 🛠️ **Stack Tecnológico**

- **Python 3.8+** - Lenguaje principal
- **Pandas** - Manipulación de datos
- **Scikit-learn** - Algoritmos K-Means y PCA
- **Scikit-learn-extra** - Algoritmo K-Medoids
- **Prophet** - Pronósticos de series temporales
- **Streamlit** - Dashboard interactivo
- **Plotly** - Visualizaciones interactivas
- **NumPy** - Computación numérica
- **Jupyter** - Documentación y análisis

---

## 🎯 **Recomendaciones Estratégicas**

### **Para Líderes Transaccionales:**
- Programas de fidelización multinivel
- Cross-selling automatizado
- Expansión a nuevos canales

### **Para Premium de Alto Valor:**
- Servicios diferenciados premium
- Upselling estratégico
- Marketing de valor agregado

### **Para Emergentes Moderados:**
- Optimización de ticket promedio
- Incremento de frecuencia de compra
- Diversificación progresiva

---

## 📈 **Métricas de Validación**

### **Técnicas:**
- **Precisión de segmentación:** Silhouette > 0.2
- **Precisión predictiva:** MAPE < 2% para clusters principales
- **Estabilidad temporal:** Validación en datos históricos

### **De Negocio:**
- **Identificación de patrones:** Múltiples dimensiones
- **Personalización:** Estrategias específicas por cluster
- **Escalabilidad:** Metodología replicable

---

## 🔄 **Trabajo Futuro**

- [ ] **Extensión sectorial:** Aplicación a otros tipos de empresa
- [ ] **Algoritmos avanzados:** Clustering jerárquico y DBSCAN
- [ ] **Variables adicionales:** Datos demográficos y geográficos
- [ ] **Deep Learning:** LSTM para series temporales complejas
- [ ] **API de servicios:** Integración empresarial

---

## 📞 **Contacto**

**Para consultas sobre el proyecto:**
- **Angelo Montes:** [Contacto disponible bajo solicitud]
- **Alessandro Ledesma:** [Contacto disponible bajo solicitud]

---

**Proyecto desarrollado como parte de investigación en análisis de datos y optimización empresarial para PYMEs**

## 🚀 Características Principales

### 📈 Análisis de Clustering
- **Algoritmo utilizado:** K-Medoids (más robusto que K-Means para outliers)
- **Número óptimo de clusters:** 3 (determinado mediante análisis de silueta)
- **Muestra:** 155 PYMEs segmentadas exitosamente

### 🔮 Pronósticos con Prophet
- **Modelos entrenados:** Series temporales para cada cluster
- **Horizonte de pronóstico:** Hasta 2026
- **Variables predichas:** Ingresos mensuales por cluster

### 📊 Dashboard Interactivo
- **Tecnología:** Streamlit
- **Funcionalidades:** 
  - Visualización de clusters en tiempo real
  - Análisis PCA interactivo
  - Pronósticos temporales
  - Recomendaciones estratégicas personalizadas

## 🎭 Clusters Identificados

### 🏆 Cluster 0: "Líderes Transaccionales" (57 PYMEs)
- **Ingresos promedio:** $38,119.24
- **Transacciones promedio:** 33.02
- **Productos únicos:** 16.58
- **Características:** Mayores ingresos, alta frecuencia transaccional, gran diversidad de productos

### 💎 Cluster 1: "Premium de Alto Valor" (56 PYMEs)
- **Ingresos promedio:** $32,567.36
- **Ticket promedio:** $1,473.63 (el más alto)
- **Transacciones promedio:** 22.23
- **Características:** Enfoque en productos/servicios de alto valor, clientes premium

### 🌱 Cluster 2: "Emergentes Moderados" (42 PYMEs)
- **Ingresos promedio:** $16,171.36
- **Ticket promedio:** $849.87
- **Transacciones promedio:** 19.45
- **Características:** Menor escala, gran potencial de crecimiento

## 📁 Estructura del Proyecto

```
├── SemiCode.ipynb                      # Notebook principal con análisis completo
├── app.py                             # Dashboard de Streamlit
├── requirements.txt                   # Dependencias del proyecto
├── README.md                          # Documentación del proyecto
├── pymes_con_clusters.csv             # Dataset con asignaciones de clusters
├── kmedoids_summary.csv               # Resumen estadístico por cluster
├── ts_mensual_historico.csv           # Series temporales históricas
├── mapeo_pymes.csv                    # Mapeo de PYMEs con razón social
├── X_procesado_para_pca.csv           # Datos procesados para PCA
├── pronostico_prophet_cluster_0.csv   # Pronósticos Cluster 0
├── pronostico_prophet_cluster_1.csv   # Pronósticos Cluster 1
└── pronostico_prophet_cluster_2.csv   # Pronósticos Cluster 2
```

## 🔧 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/usuario/Seminario-II.git
cd Seminario-II
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el dashboard
```bash
streamlit run app.py
```

### 4. Acceder al dashboard
Abrir en el navegador: `http://localhost:8501`

## 📊 Cómo Utilizar el Dashboard

### 📈 Tab 1: "Resumen General y Total"
- Visualización de ingresos totales consolidados
- Pronósticos agregados de todos los clusters
- Estadísticas generales del análisis

### 🔍 Tab 2: "Exploración por Clúster"
- Selección interactiva de clusters
- Características detalladas por cluster
- Pronósticos específicos
- Recomendaciones estratégicas personalizadas
- Lista completa de PYMEs por cluster

### 📊 Tab 3: "Comparación y PCA"
- Comparación visual entre clusters
- Análisis de componentes principales (PCA)
- Distribuciones de características
- Visualización de separación de clusters

## 🎯 Recomendaciones Estratégicas

### Para Líderes Transaccionales:
- Programas de fidelización avanzados
- Cross-selling inteligente
- Expansión estratégica

### Para Premium de Alto Valor:
- Servicios premium diferenciados
- Upselling estratégico
- Marketing de valor

### Para Emergentes Moderados:
- Mejora del ticket promedio
- Incremento de frecuencia de compra
- Diversificación de productos

## 🔬 Metodología

1. **Preprocesamiento de datos:** Limpieza y normalización
2. **Análisis exploratorio:** Identificación de patrones y outliers
3. **Clustering:** Implementación de K-Medoids con validación
4. **Series temporales:** Modelado con Prophet para pronósticos
5. **Visualización:** Dashboard interactivo con Streamlit
6. **Validación:** Análisis PCA y métricas de separación

## 📈 Resultados Clave

- ✅ **Segmentación exitosa:** 3 clusters bien diferenciados
- ✅ **Alta separación:** Clusters con características distintivas
- ✅ **Pronósticos precisos:** Modelos Prophet validados
- ✅ **Insights accionables:** Recomendaciones específicas por cluster
- ✅ **Visualización clara:** Dashboard intuitivo y funcional

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Pandas:** Manipulación de datos
- **Scikit-learn:** Clustering y PCA
- **Prophet:** Pronósticos de series temporales
- **Streamlit:** Dashboard interactivo
- **Plotly:** Visualizaciones interactivas
- **NumPy:** Computación numérica

## 📊 Métricas de Validación

- **Coeficiente de silueta:** Óptimo para k=3
- **Separación PCA:** Clara diferenciación visual
- **Estabilidad del clustering:** Resultados consistentes
- **Precisión de pronósticos:** Validación cruzada temporal

## 🔄 Trabajo Futuro

- [ ] Implementación de clustering jerárquico
- [ ] Integración de más variables de negocio
- [ ] Análisis de supervivencia de PYMEs
- [ ] Modelo de recomendaciones automatizado
- [ ] API REST para integración empresarial

## 📞 Contacto

Para consultas sobre el proyecto o colaboraciones:
- Angelo Montes: [email]
- Alessandro Ledesma: [email]

---

**Desarrollado como parte de la investigación en análisis de datos empresariales y segmentación de mercados para PYMEs.**