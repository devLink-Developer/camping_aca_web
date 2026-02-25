# GUÍA DE DESPLIEGUE RÁPIDO
# Camping ACA Luján

## Paso 1: Preparación Inicial

# 1.1 Crear archivo .env desde el ejemplo
Copy-Item .env.example .env

# 1.2 Editar .env con configuración real
notepad .env

# IMPORTANTE: Cambiar estos valores:
# - SECRET_KEY (generar una nueva clave de 50+ caracteres)
# - TRAEFIK_DOMAIN (tu dominio real)
# - EMAIL_HOST_USER y EMAIL_HOST_PASSWORD
# - CSRF_TRUSTED_ORIGINS (tu dominio con https)

## Paso 2: Verificar Conexión a Red y DB

# 2.1 Verificar que la red traefik_proxy existe
docker network ls | Select-String "traefik_proxy"

# 2.2 Verificar que devlink_db está corriendo
docker ps | Select-String "devlink_db"

# 2.3 Test de conexión a PostgreSQL (opcional)
docker exec devlink_db psql -U devlink -d devlink -c "SELECT version();"

## Paso 3: Construir y Desplegar

# 3.1 Construir la imagen Docker
docker-compose build

# 3.2 Iniciar el contenedor
docker-compose up -d

# 3.3 Ver los logs para verificar que todo está bien
docker-compose logs -f web

# Espera a ver: "Application is ready!"

## Paso 4: Verificación Post-Despliegue

# 4.1 Verificar que el contenedor está corriendo
docker-compose ps

# 4.2 Verificar migraciones
docker-compose exec web python manage.py showmigrations

# 4.3 Verificar superusuario creado
Write-Host "Login al admin con: admin / admin123" -ForegroundColor Yellow
Write-Host "CAMBIAR PASSWORD INMEDIATAMENTE!" -ForegroundColor Red

## Paso 5: Configuración Inicial en Admin

Write-Host "`nPasos siguientes en el Admin Panel:" -ForegroundColor Green
Write-Host "1. Ir a https://tu-dominio.com/admin" -ForegroundColor Cyan
Write-Host "2. Login con admin/admin123" -ForegroundColor Cyan
Write-Host "3. Cambiar password del admin INMEDIATAMENTE" -ForegroundColor Red
Write-Host "4. Ir a 'Configuración del Sitio' y completar:" -ForegroundColor Cyan
Write-Host "   - Subir imagen hero principal" -ForegroundColor White
Write-Host "   - Agregar teléfono, email, dirección" -ForegroundColor White
Write-Host "   - Configurar URLs de redes sociales" -ForegroundColor White
Write-Host "5. Subir imágenes a la Galería" -ForegroundColor Cyan
Write-Host "6. Revisar Precios y ajustar si es necesario" -ForegroundColor Cyan
Write-Host "7. Agregar Testimonios de clientes" -ForegroundColor Cyan

## Paso 6: Pruebas

Write-Host "`nPruebas a realizar:" -ForegroundColor Green
Write-Host "✓ Landing page carga correctamente" -ForegroundColor White
Write-Host "✓ Formulario de contacto funciona" -ForegroundColor White
Write-Host "✓ Galería muestra las imágenes" -ForegroundColor White
Write-Host "✓ Admin panel accesible" -ForegroundColor White
Write-Host "✓ Dashboard de analytics funciona" -ForegroundColor White
Write-Host "✓ Crear un voucher de prueba" -ForegroundColor White
Write-Host "✓ Escanear voucher de prueba" -ForegroundColor White

## Comandos Útiles de Mantenimiento

# Ver logs en tiempo real
# docker-compose logs -f web

# Reiniciar el servicio
# docker-compose restart web

# Ejecutar comando Django
# docker-compose exec web python manage.py [comando]

# Acceder al shell de Django
# docker-compose exec web python manage.py shell

# Crear backup de la base de datos
# docker exec devlink_db pg_dump -U devlink devlink > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql

# Detener el servicio
# docker-compose down

Write-Host "`n¡Despliegue completado!" -ForegroundColor Green
Write-Host "Accede a tu sitio en: https://tu-dominio.com" -ForegroundColor Cyan
