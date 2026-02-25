# Makefile para Camping ACA Luján

.PHONY: help build up down restart logs shell migrate createsuperuser collectstatic backup test clean

help:
	@echo "Comandos disponibles para Camping ACA Luján:"
	@echo ""
	@echo "  make build          - Construir imagen Docker"
	@echo "  make up             - Iniciar contenedores"
	@echo "  make down           - Detener contenedores"
	@echo "  make restart        - Reiniciar servicio web"
	@echo "  make logs           - Ver logs en tiempo real"
	@echo "  make shell          - Acceder al shell de Django"
	@echo "  make migrate        - Ejecutar migraciones"
	@echo "  make createsuperuser - Crear superusuario"
	@echo "  make collectstatic  - Recolectar archivos estáticos"
	@echo "  make loaddata       - Cargar datos iniciales"
	@echo "  make backup         - Hacer backup de la base de datos"
	@echo "  make test           - Ejecutar tests"
	@echo "  make clean          - Limpiar archivos temporales"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Aplicación iniciada. Ver logs con: make logs"

down:
	docker-compose down

restart:
	docker-compose restart web

logs:
	docker-compose logs -f web

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

loaddata:
	docker-compose exec web python manage.py load_initial_data

backup:
	@echo "Creando backup de la base de datos..."
	docker exec devlink_db pg_dump -U devlink devlink > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup creado exitosamente"

test:
	docker-compose exec web python manage.py test

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "Archivos temporales eliminados"

deploy: build up
	@echo "Esperando a que la aplicación esté lista..."
	@sleep 10
	@echo "Deployment completado!"
	@echo "Accede a: https://campingacalujan.com/admin"

status:
	docker-compose ps
	@echo ""
	@docker-compose exec web python manage.py check --deploy
