#!/bin/bash

# Script de deployment para el proyecto de Clustering PYMEs
# =========================================================
#
# Este script automatiza el proceso de deployment del dashboard
# tanto en desarrollo como en producción.

set -e  # Salir si cualquier comando falla

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función de ayuda
show_help() {
    cat << EOF
🚀 Script de Deployment - Clustering PYMEs

Uso: ./deploy.sh [COMANDO] [OPCIONES]

COMANDOS:
    dev         Ejecutar en modo desarrollo
    prod        Ejecutar en modo producción
    build       Construir imagen Docker
    test        Ejecutar tests
    clean       Limpiar contenedores y volúmenes
    logs        Mostrar logs de la aplicación
    stop        Detener todos los servicios
    restart     Reiniciar servicios
    health      Verificar estado de salud

EJEMPLOS:
    ./deploy.sh dev                 # Desarrollo local
    ./deploy.sh prod                # Producción
    ./deploy.sh build              # Solo construir imagen
    ./deploy.sh test               # Ejecutar tests
    ./deploy.sh logs pymes-dashboard  # Ver logs específicos

EOF
}

# Verificar que Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Por favor, instala Docker primero."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado. Por favor, instala Docker Compose primero."
        exit 1
    fi
    
    print_success "Docker y Docker Compose están disponibles"
}

# Verificar archivos necesarios
check_files() {
    local required_files=("Dockerfile" "docker-compose.yml" "requirements.txt" "app.py")
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            print_error "Archivo requerido no encontrado: $file"
            exit 1
        fi
    done
    
    print_success "Todos los archivos requeridos están presentes"
}

# Función para desarrollo
run_development() {
    print_status "Iniciando entorno de desarrollo..."
    
    # Crear directorios necesarios
    mkdir -p data logs
    
    # Ejecutar en modo desarrollo
    docker-compose up --build -d pymes-dashboard postgres redis
    
    print_success "Entorno de desarrollo iniciado"
    print_status "Dashboard disponible en: http://localhost:8501"
    print_status "Base de datos disponible en: localhost:5432"
    
    # Mostrar logs en tiempo real
    print_status "Mostrando logs... (Ctrl+C para salir)"
    docker-compose logs -f pymes-dashboard
}

# Función para producción
run_production() {
    print_status "Iniciando entorno de producción..."
    
    # Verificar que existe configuración de SSL
    if [[ ! -d "nginx/ssl" ]]; then
        print_warning "Directorio SSL no encontrado. Creando certificado auto-firmado..."
        mkdir -p nginx/ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/ssl/private.key \
            -out nginx/ssl/certificate.crt \
            -subj "/C=PE/ST=Lima/L=Lima/O=PYMEs/CN=localhost"
    fi
    
    # Crear directorios necesarios
    mkdir -p data logs nginx
    
    # Crear configuración básica de nginx si no existe
    if [[ ! -f "nginx/nginx.conf" ]]; then
        cat > nginx/nginx.conf << 'EOL'
events {
    worker_connections 1024;
}

http {
    upstream app {
        server pymes-dashboard:8501;
    }

    server {
        listen 80;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        ssl_certificate /etc/nginx/ssl/certificate.crt;
        ssl_certificate_key /etc/nginx/ssl/private.key;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOL
    fi
    
    # Ejecutar en modo producción
    docker-compose --profile production up --build -d
    
    print_success "Entorno de producción iniciado"
    print_status "Dashboard disponible en: https://localhost"
    print_status "HTTP redirige automáticamente a HTTPS"
}

# Función para construir imagen
build_image() {
    print_status "Construyendo imagen Docker..."
    docker-compose build pymes-dashboard
    print_success "Imagen construida exitosamente"
}

# Función para ejecutar tests
run_tests() {
    print_status "Ejecutando tests..."
    
    # Ejecutar tests en contenedor temporal
    docker run --rm -v "$(pwd)":/app -w /app python:3.9-slim bash -c "
        pip install -r requirements.txt pytest &&
        python test_project.py
    "
    
    print_success "Tests completados"
}

# Función para limpiar
clean_environment() {
    print_status "Limpiando entorno..."
    
    docker-compose down -v --remove-orphans
    docker system prune -f
    
    print_success "Entorno limpiado"
}

# Función para mostrar logs
show_logs() {
    local service=${2:-"pymes-dashboard"}
    print_status "Mostrando logs de $service..."
    docker-compose logs -f "$service"
}

# Función para detener servicios
stop_services() {
    print_status "Deteniendo servicios..."
    docker-compose down
    print_success "Servicios detenidos"
}

# Función para reiniciar servicios
restart_services() {
    print_status "Reiniciando servicios..."
    docker-compose restart
    print_success "Servicios reiniciados"
}

# Función para verificar salud
check_health() {
    print_status "Verificando estado de salud..."
    
    # Verificar estado de contenedores
    echo -e "\n📊 Estado de contenedores:"
    docker-compose ps
    
    # Verificar conectividad
    echo -e "\n🔗 Verificando conectividad:"
    
    if curl -f http://localhost:8501/_stcore/health &>/dev/null; then
        print_success "Dashboard responde correctamente"
    else
        print_error "Dashboard no responde"
    fi
    
    # Verificar base de datos
    if docker-compose exec postgres pg_isready -U pymes_user &>/dev/null; then
        print_success "Base de datos responde correctamente"
    else
        print_warning "Base de datos no responde o no está configurada"
    fi
}

# Script principal
main() {
    case ${1:-help} in
        dev|development)
            check_docker
            check_files
            run_development
            ;;
        prod|production)
            check_docker
            check_files
            run_production
            ;;
        build)
            check_docker
            check_files
            build_image
            ;;
        test|tests)
            check_docker
            run_tests
            ;;
        clean)
            check_docker
            clean_environment
            ;;
        logs)
            check_docker
            show_logs "$@"
            ;;
        stop)
            check_docker
            stop_services
            ;;
        restart)
            check_docker
            restart_services
            ;;
        health)
            check_docker
            check_health
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Comando no reconocido: $1"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal con todos los argumentos
main "$@"
