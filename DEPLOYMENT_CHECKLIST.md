# ✅ CHECKLIST DE DEPLOYMENT
# Camping ACA Luján

## PRE-DEPLOYMENT (Antes de desplegar)

### 1. Configuración del Entorno
- [ ] Archivo `.env` creado desde `.env.example`
- [ ] SECRET_KEY generada (ejecutar `python generate_secret_key.py`)
- [ ] DEBUG=False configurado
- [ ] ALLOWED_HOSTS actualizado con dominio real
- [ ] TRAEFIK_DOMAIN configurado con dominio real
- [ ] CSRF_TRUSTED_ORIGINS actualizado con URLs HTTPS reales
- [ ] Credenciales de email configuradas (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
- [ ] Variables de base de datos verificadas (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

### 2. Verificación de Infraestructura
- [ ] Red `traefik_proxy` existe y está activa
- [ ] Contenedor `devlink_db` está corriendo
- [ ] PostgreSQL accesible en puerto 5455
- [ ] Traefik configurado y funcionando
- [ ] Dominio apunta al servidor correcto
- [ ] Certificado SSL/Let's Encrypt configurado en Traefik

### 3. Archivos y Código
- [ ] Todos los archivos del proyecto están presentes
- [ ] Permisos de `entrypoint.sh` son ejecutables (chmod +x)
- [ ] `.gitignore` configurado correctamente
- [ ] `requirements.txt` completo

## DEPLOYMENT (Durante el despliegue)

### 4. Build y Construcción
- [ ] `docker-compose build` ejecutado sin errores
- [ ] Imagen Docker construida correctamente
- [ ] Dependencias Python instaladas (verificar logs)
- [ ] No hay errores de sintaxis en el código

### 5. Inicio del Servicio
- [ ] `docker-compose up -d` ejecutado
- [ ] Contenedor `camping_aca_lujan` está corriendo
- [ ] Healthcheck pasa correctamente
- [ ] Logs muestran "Application is ready!"
- [ ] Migraciones ejecutadas automáticamente
- [ ] Scripts de actualización de schema ejecutados (si aplica: `update_vouchers.py`, `add_voucher_whatsapp_fields.py`)
- [ ] Static files colectados
- [ ] Superuser creado automáticamente

### 6. Verificación de Conectividad
- [ ] Sitio accesible en https://dominio.com
- [ ] Admin accesible en https://dominio.com/admin
- [ ] HTTPS funciona correctamente (certificado válido)
- [ ] No hay errores 500 o 404
- [ ] Redirección HTTP → HTTPS funciona

## POST-DEPLOYMENT (Después de desplegar)

### 7. Configuración Inicial del Admin
- [ ] Login en admin panel (admin/admin123)
- [ ] **PASSWORD DE ADMIN CAMBIADO INMEDIATAMENTE** ⚠️
- [ ] Usuario administrador principal creado con email real
- [ ] Usuario 'admin' default deshabilitado o eliminado

### 8. Configuración del Sitio
- [ ] "Configuración del Sitio" completada:
  - [ ] Nombre del sitio
  - [ ] Eslogan/tagline
  - [ ] Imagen hero principal subida
  - [ ] Teléfono agregado
  - [ ] Email agregado
  - [ ] Dirección completa
  - [ ] Horarios actualizados
  - [ ] URL de Instagram
  - [ ] URL de Facebook
  - [ ] Alerta especial configurada (si aplica)

### 9. Contenido Inicial
- [ ] Servicios revisados y ajustados
- [ ] Precios verificados y actualizados
- [ ] Al menos 8-12 imágenes subidas a Galería
- [ ] Alt text y descripciones agregadas a imágenes
- [ ] FAQs revisadas y actualizadas
- [ ] Al menos 3-5 testimonios agregados (opcional)

### 10. Pruebas Funcionales
- [ ] Landing page carga correctamente
- [ ] Todas las secciones visibles (Hero, Servicios, Galería, FAQs, Precios, Contacto)
- [ ] Galería funciona (slider se mueve automáticamente)
- [ ] Acordeón de FAQs funciona
- [ ] Formulario de contacto envía emails
- [ ] Email de contacto recibido en bandeja
- [ ] Navegación smooth scroll funciona
- [ ] Links a redes sociales funcionan
- [ ] Botón flotante "Asociate" funciona
- [ ] Responsive design funciona en móvil
- [ ] Responsive design funciona en tablet

### 11. Pruebas de Dashboard
- [ ] Dashboard accesible en /dashboard/
- [ ] Estadísticas se muestran correctamente
- [ ] Mensajes de contacto aparecen
- [ ] Contador de visitantes funciona

### 12. Pruebas de Analytics
- [ ] Analytics dashboard accesible
- [ ] Tracking de visitantes funciona
- [ ] PageViews se registran en la base de datos
- [ ] Gráficos se cargan correctamente
- [ ] Datos geográficos se capturan

### 13. Pruebas de Vouchers
- [ ] Crear voucher de prueba
- [ ] QR se genera correctamente
- [ ] QR se puede descargar/visualizar
- [ ] Scanner de vouchers accesible en /vouchers/scanner/
- [ ] Validación de voucher funciona
- [ ] Marcar voucher como usado funciona
- [ ] Filtros de vouchers funcionan
- [ ] Búsqueda de vouchers funciona

### 14. Seguridad
- [ ] SSL/HTTPS activo y válido
- [ ] Certificado SSL no expira pronto
- [ ] HTTP redirige a HTTPS
- [ ] Admin panel solo accesible con login
- [ ] Dashboard requiere autenticación
- [ ] Vouchers requieren autenticación
- [ ] CSRF protection activo
- [ ] XSS protection activo
- [ ] Clickjacking protection activo
- [ ] No hay información sensible en logs públicos

### 15. Performance
- [ ] Página carga en menos de 3 segundos
- [ ] Imágenes optimizadas (no muy pesadas)
- [ ] Static files se sirven correctamente
- [ ] No hay errores 404 en consola del navegador
- [ ] No hay errores JavaScript en consola

### 16. SEO y Metadatos
- [ ] Meta description configurada
- [ ] Title tags apropiados
- [ ] Alt text en todas las imágenes
- [ ] URLs amigables
- [ ] Sitemap.xml (opcional, agregar después)
- [ ] robots.txt (opcional, agregar después)

### 17. Backups y Mantenimiento
- [ ] Primer backup de base de datos realizado
- [ ] Backup guardado en lugar seguro
- [ ] Script de backup programado (cron/tarea programada)
- [ ] Plan de backups definido (diario/semanal)
- [ ] Logs revisados para errores
- [ ] Sistema de monitoreo configurado (opcional)

### 18. Documentación
- [ ] Credenciales guardadas en gestor de passwords seguro
- [ ] Información de acceso documentada
- [ ] Contactos de soporte documentados
- [ ] Procedimientos de mantenimiento documentados

### 19. Entrenamiento/Handoff
- [ ] Cliente capacitado en uso del Admin Panel
- [ ] Cliente sabe cómo:
  - [ ] Modificar precios
  - [ ] Subir imágenes a galería
  - [ ] Editar servicios
  - [ ] Crear vouchers
  - [ ] Leer mensajes de contacto
  - [ ] Ver estadísticas
- [ ] Documentación entregada al cliente
- [ ] Contacto de soporte establecido

### 20. Go-Live Final
- [ ] Sitio antiguo/placeholder desactivado
- [ ] DNS actualizado (si aplica)
- [ ] Anuncio en redes sociales (opcional)
- [ ] Google Analytics/Search Console configurado (opcional)
- [ ] Monitoreo activo las primeras 24-48 horas
- [ ] Cliente notificado del go-live

## MONITOREO POST-LAUNCH (Primeras 48 horas)

### 21. Verificaciones Continuas
- [ ] Revisar logs cada 6 horas
- [ ] Verificar que no hay errores 500
- [ ] Verificar que emails se envían
- [ ] Verificar que analytics registra visitantes
- [ ] Verificar espacio en disco
- [ ] Verificar uso de memoria
- [ ] Verificar uso de CPU

### 22. Ajustes Rápidos
- [ ] Correcciones de contenido (si necesario)
- [ ] Ajustes de diseño menores (si necesario)
- [ ] Optimizaciones de performance (si necesario)

## NOTAS IMPORTANTES

⚠️ **CRÍTICO - NO OLVIDAR:**
1. Cambiar password de admin inmediatamente
2. Configurar backups automáticos
3. Guardar credenciales en lugar seguro
4. Monitorear logs las primeras 24 horas

✅ **RECOMENDACIONES:**
- Hacer backups antes de cualquier cambio grande
- Probar en staging antes de producción (si es posible)
- Mantener documentación actualizada
- Revisar logs regularmente
- Actualizar dependencias periódicamente

---

**Deployment completado cuando todos los checkboxes están marcados ✅**

**Fecha de deployment:** __________________

**Deployado por:** __________________

**Validado por:** __________________
