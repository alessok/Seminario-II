# Dockerfile para el proyecto de Clustering PYMEs
# ===============================================
# 
# Este Dockerfile permite ejecutar el dashboard en cualquier entorno
# de manera consistente y reproducible.

# Usar imagen oficial de Python 3.9 slim
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar archivos del proyecto
COPY . .

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 pyme_user && \
    chown -R pyme_user:pyme_user /app
USER pyme_user

# Exponer puerto 8501 (puerto por defecto de Streamlit)
EXPOSE 8501

# Configurar Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

# Verificar que los archivos necesarios existen
RUN python -c "import os; print('✅ Files check:'); [print(f'  {f}: {os.path.exists(f)}') for f in ['app.py', 'requirements.txt', 'README.md']]"

# Comando de salud para verificar que la app está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Metadatos del contenedor
LABEL maintainer="PYMEs Clustering Project"
LABEL version="1.0"
LABEL description="Dashboard interactivo para análisis de clustering de PYMEs"
