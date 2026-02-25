# 🚀 INICIO RÁPIDO - Camping ACA Luján

## ⚡ Despliegue en 5 Minutos

### 1️⃣ Configurar Variables de Entorno
```powershell
# Copiar archivo de configuración
Copy-Item .env.example .env

# Editar con tus valores
notepad .env
```

**Cambios críticos en .env:**
- `SECRET_KEY` → Generar clave única larga
- `TRAEFIK_DOMAIN` → Tu dominio real
- `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` → Para formulario de contacto

### 2️⃣ Desplegar
```powershell
# Construir e iniciar
docker-compose build
docker-compose up -d

# Ver progreso
docker-compose logs -f web
```

Espera hasta ver: **"Application is ready!"**

### 3️⃣ Primer Acceso

**Admin Panel:** https://tu-dominio.com/admin
- Usuario: `admin`
- Password: `admin123`

⚠️ **CAMBIAR PASSWORD INMEDIATAMENTE**

### 4️⃣ Configuración Inicial (5 min)

En el Admin Panel:

1. **Cambiar password** (Usuario > admin > Cambiar contraseña)

2. **Configuración del Sitio:**
   - Subir imagen hero principal
   - Completar teléfono, email, dirección
   - Agregar URLs de Instagram/Facebook

3. **Galería:**
   - Subir 8-12 imágenes del camping
   - Agregar descripciones y alt text para SEO

4. **Testimonios** (opcional):
   - Agregar opiniones de clientes
   - Calificación de estrellas

5. **Precios:**
   - Revisar y ajustar si es necesario
   - Ya vienen precargados desde el HTML actual

## ✅ URLs Principales

| Sección | URL |
|---------|-----|
| **Landing Page** | https://tu-dominio.com |
| **Admin Panel** | https://tu-dominio.com/admin |
| **Dashboard** | https://tu-dominio.com/dashboard |
| **Analytics** | https://tu-dominio.com/api/dashboard |
| **Vouchers** | https://tu-dominio.com/vouchers |
| **Scanner QR** | https://tu-dominio.com/vouchers/scanner |

## 📊 Features Incluidas

✅ Landing page moderno y responsive  
✅ Galería de imágenes con slider  
✅ Sistema de precios dinámico  
✅ Formulario de contacto funcional  
✅ Dashboard de estadísticas completo  
✅ Sistema de vouchers con QR  
✅ Scanner de QR con cámara  
✅ Panel de administración completo  
✅ Analytics de visitantes  
✅ Tracking de tiempo por sección  

## 🔧 Comandos Útiles

```powershell
# Ver logs
docker-compose logs -f web

# Reiniciar
docker-compose restart web

# Detener
docker-compose down

# Backup de base de datos
docker exec devlink_db pg_dump -U devlink devlink > backup.sql

# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Crear nuevo superusuario
docker-compose exec web python manage.py createsuperuser
```

## 🎨 Personalización Rápida

### Cambiar Colores
Edita `static/css/style.css`:
```css
:root {
    --primary-color: #df1d2e;      /* Rojo ACA */
    --secondary-color: #48ff00;     /* Verde */
}
```

### Agregar Servicios
Admin > Servicios > Agregar servicio
- Título, descripción, icono
- Características en formato: `["Item 1", "Item 2"]`

### Modificar Precios
Admin > Precios > Seleccionar precio > Editar monto

## 🎫 Uso de Vouchers

### Crear Voucher
1. Ir a Vouchers > Crear voucher
2. Completar datos del cliente
3. Definir valor y vigencia
4. El QR se genera automáticamente

### Escanear Voucher
1. Ir a `/vouchers/scanner/`
2. Permitir acceso a cámara
3. Escanear código QR
4. Validar y marcar como usado

## 📱 Integración Instagram (Opcional)

Para mostrar feed de Instagram:
1. Crear app en Facebook Developers
2. Obtener credenciales
3. Agregar a `.env`:
```env
INSTAGRAM_USERNAME=tu_usuario
INSTAGRAM_PASSWORD=tu_app_password
```

## 🐛 Solución de Problemas

### Error de conexión a DB
```powershell
# Verificar que devlink_db está corriendo
docker ps | Select-String "devlink_db"

# Verificar red
docker network ls | Select-String "traefik_proxy"
```

### Imágenes no se muestran
```powershell
# Recolectar static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Vouchers QR no se generan
```powershell
# Reinstalar dependencias
docker-compose exec web pip install qrcode[pil] Pillow
```

## 📞 Próximos Pasos

1. **Personalizar contenido** en el Admin Panel
2. **Subir imágenes reales** del camping
3. **Probar formulario de contacto** con email real
4. **Crear vouchers de prueba** y probar scanner
5. **Revisar analytics** después de algunos días
6. **Configurar backups automáticos**

## 📚 Documentación Completa

Ver `README.md` para documentación detallada completa.

---

**¿Necesitas ayuda?**  
Email: admin@campingacalujan.com  
Documentación Django: https://docs.djangoproject.com/

🎉 **¡Listo! Tu sitio está funcionando**
