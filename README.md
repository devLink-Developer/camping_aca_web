# Camping ACA Luján - Sistema de Gestión Web

Sistema web moderno para la gestión del Camping ACA Luján, desarrollado con Django, PostgreSQL y Docker. Incluye landing page responsive, dashboard de estadísticas, sistema de vouchers con QR, y panel de administración completo.

## 🚀 Características Principales

### Landing Page Moderna
- ✅ Diseño responsive adaptado a móviles, tablets y desktop
- ✅ Hero section con imagen de fondo personalizable
- ✅ Sección de servicios con iconos e información detallada
- ✅ Galería de imágenes con slider automático (Swiper.js)
- ✅ Preguntas frecuentes con acordeón interactivo
- ✅ Sistema de precios dinámico para socios y no socios
- ✅ Testimonios de clientes con calificaciones
- ✅ Formulario de contacto funcional con envío de emails
- ✅ Integración con redes sociales (Instagram, Facebook)
- ✅ Botón flotante para asociarse al ACA
- ✅ Animaciones suaves con AOS

### Dashboard de Estadísticas
- 📊 Visitantes por día con gráficos interactivos
- 📊 Tiempo promedio de permanencia en la página
- 📊 Tracking de scroll depth y tiempo por sección
- 📊 Análisis de origen geográfico (país, ciudad)
- 📊 Distribución por dispositivo (móvil, tablet, desktop)
- 📊 Navegadores más utilizados
- 📊 Páginas más visitadas
- 📊 Sesiones únicas de usuarios

### Sistema de Vouchers con QR
- 🎫 Generación automática de códigos QR únicos
- 🎫 Información completa del cliente (nombre, email, teléfono, ID)
- 🎫 Fechas de emisión, vencimiento y uso
- 🎫 Estados: activo, usado, vencido, cancelado
- 🎫 Interfaz de escaneo con cámara web
- 🎫 Validación en tiempo real
- 🎫 Panel de control con filtros y búsqueda
- 🎫 Registro de auditoría completo
- 🎫 Exportación de datos

### Panel de Administración
- ⚙️ Gestión de servicios y características
- ⚙️ Control de precios por categoría
- ⚙️ Administración de galería de imágenes
- ⚙️ Gestión de FAQs y testimonios
- ⚙️ Lectura de mensajes de contacto
- ⚙️ Configuración general del sitio
- ⚙️ Alertas especiales configurables

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.0.1, Python 3.11
- **Base de Datos**: PostgreSQL
- **Frontend**: Bootstrap 5, JavaScript, AOS, Swiper.js
- **QR Codes**: qrcode library con PIL
- **Analytics**: Middleware personalizado de Django
- **Containerización**: Docker, Docker Compose
- **Reverse Proxy**: Traefik (integración existente)
- **Web Server**: Gunicorn + Whitenoise

## 📋 Requisitos Previos

- Docker y Docker Compose instalados
- Acceso a la red `traefik_proxy` existente
- Base de datos PostgreSQL `devlink_db` corriendo en la red

## 🚀 Instalación y Despliegue

### 1. Clonar y Configurar

```bash
# Navegar al directorio del proyecto
cd d:\Camping_ACA_Lujan

# Copiar el archivo de environment
copy .env.example .env

# Editar .env con tus configuraciones
notepad .env
```

### 2. Configurar Variables de Entorno

Edita el archivo `.env` con tus valores:

```env
SECRET_KEY=tu-clave-secreta-aqui-muy-larga-y-segura
DEBUG=False
ALLOWED_HOSTS=campingacalujan.com,www.campingacalujan.com

DB_NAME=camping_aca_eb
DB_USER=devlink
DB_PASSWORD=@Inf124578..
DB_HOST=devlink_db
DB_PORT=5455

TRAEFIK_DOMAIN=campingacalujan.com

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-app

CSRF_TRUSTED_ORIGINS=https://campingacalujan.com,https://www.campingacalujan.com
```

### 3. Construir y Ejecutar

```bash
# Construir la imagen Docker
docker-compose build

# Iniciar el contenedor
docker-compose up -d

# Ver los logs
docker-compose logs -f web
```

### 4. Acceso al Sistema

- **Landing Page**: https://campingacalujan.com
- **Admin Panel**: https://campingacalujan.com/admin
  - Usuario: `admin`
  - Password: `admin123` (⚠️ **CAMBIAR INMEDIATAMENTE**)
- **Dashboard**: https://campingacalujan.com/dashboard/
- **Analytics**: https://campingacalujan.com/api/dashboard/
- **Vouchers**: https://campingacalujan.com/vouchers/

## 📁 Estructura del Proyecto

```
Camping_ACA_Lujan/
├── apps/
│   ├── landing/           # App del landing page
│   │   ├── models.py      # Servicios, Precios, Galería, FAQs, etc.
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── forms.py
│   ├── vouchers/          # Sistema de vouchers QR
│   │   ├── models.py      # Voucher, VoucherUsageLog
│   │   ├── views.py       # Scanner, validación, CRUD
│   │   └── admin.py
│   ├── analytics/         # Sistema de estadísticas
│   │   ├── models.py      # PageView, SectionView, UserSession
│   │   ├── middleware.py  # Tracking automático
│   │   └── views.py       # Charts y dashboards
│   └── dashboard/         # Dashboard de administración
│       ├── views.py
│       └── urls.py
├── config/                # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/             # Templates HTML
│   ├── base.html
│   ├── landing/
│   └── includes/
├── static/                # Archivos estáticos
│   └── css/
│       └── style.css
├── media/                 # Archivos subidos
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
└── manage.py
```

## 🔧 Comandos Útiles

### Gestión de Django

```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Shell de Django
docker-compose exec web python manage.py shell

# Ver logs
docker-compose logs -f web
```

### Gestión de Docker

```bash
# Reiniciar servicio
docker-compose restart web

# Detener todos los servicios
docker-compose down

# Reconstruir imagen
docker-compose build --no-cache

# Ver estado
docker-compose ps
```

### Backup de Base de Datos

```bash
# Desde el contenedor de PostgreSQL existente
docker exec devlink_db pg_dump -U devlink camping_aca_eb > backup.sql

# Restaurar backup
docker exec -i devlink_db psql -U devlink camping_aca_eb < backup.sql
```

## 📊 Modelos de Base de Datos

### Landing App
- **Service**: Servicios del camping
- **PriceCategory**: Categorías de precios (Socios/No Socios)
- **Price**: Precios individuales
- **GalleryImage**: Imágenes de la galería
- **FAQ**: Preguntas frecuentes
- **Testimonial**: Testimonios de clientes
- **ContactMessage**: Mensajes del formulario
- **SiteConfiguration**: Configuración general (singleton)

### Vouchers App
- **Voucher**: Vouchers con QR, cliente, fechas, estado
- **VoucherUsageLog**: Auditoría de intentos de uso

### Analytics App
- **PageView**: Registro de vistas de página
- **SectionView**: Tiempo en secciones específicas
- **UserSession**: Sesiones de usuario con métricas

## 🎨 Personalización

### Cambiar Colores del Tema

Edita `static/css/style.css`:

```css
:root {
    --primary-color: #df1d2e;      /* Rojo ACA */
    --secondary-color: #48ff00;     /* Verde */
    --dark-green: #273d27;
}
```

### Cambiar Imagen Hero

Desde el admin panel:
1. Ir a **Configuración del Sitio**
2. Subir nueva imagen en **Imagen principal**
3. Guardar cambios

### Agregar Servicios

1. Ir a **Admin** > **Servicios**
2. Click en **Agregar servicio**
3. Completar información y subir icono
4. Las características se agregan como lista JSON: `["Parrillas", "Luz", "Mesas"]`

## 🔒 Seguridad

### Configuraciones de Producción

- ✅ DEBUG=False en producción
- ✅ SECRET_KEY única y segura (50+ caracteres)
- ✅ ALLOWED_HOSTS configurado correctamente
- ✅ CSRF_TRUSTED_ORIGINS configurado
- ✅ HTTPS forzado (SECURE_SSL_REDIRECT)
- ✅ Cookies seguras (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- ✅ XSS y clickjacking protection activados
- ✅ Usuario no-root en Docker
- ✅ Cambiar password de admin inmediatamente

### Recomendaciones

1. **Cambiar password de admin**: Inmediatamente después del primer deploy
2. **Configurar emails**: Para recibir mensajes de contacto
3. **Backups regulares**: Programar backups automáticos de la DB
4. **Monitoreo**: Implementar monitoring (Sentry, New Relic, etc.)
5. **SSL**: Asegurar que Traefik esté configurado con Let's Encrypt

## 📱 Instagram Integration

Para integrar el feed de Instagram (opcional):

1. Crear una Instagram App en Facebook Developers
2. Obtener credenciales
3. Configurar en `.env`:
   ```env
   INSTAGRAM_USERNAME=tu_usuario
   INSTAGRAM_PASSWORD=tu_password
   ```
4. O usar Instagram Basic Display API para método más seguro

## 🐛 Troubleshooting

### Error de Conexión a Base de Datos

```bash
# Verificar que devlink_db esté corriendo
docker ps | grep devlink_db

# Verificar red
docker network inspect traefik_proxy

# Verificar credenciales en .env
```

### Errores de Permisos

```bash
# Ajustar permisos de directorios
chmod -R 755 staticfiles media logs
```

### Vouchers QR no se generan

```bash
# Instalar dependencias de imagen
docker-compose exec web pip install qrcode[pil] Pillow
```

## 📞 Soporte

Para soporte técnico o preguntas:
- **Email**: admin@campingacalujan.com
- **Documentación**: Este README
- **Django Docs**: https://docs.djangoproject.com/

## 📝 Próximas Características (Roadmap)

- [ ] Sistema de reservas online
- [ ] Integración con pasarela de pago para vouchers
- [ ] App móvil para escaneo de QR
- [ ] Sistema de notificaciones push
- [ ] Chat en vivo con visitantes
- [ ] Multi-idioma (inglés, portugués)
- [ ] Dashboard de reportes avanzado con PDF export
- [ ] Sistema de fidelización de clientes

## 📄 Licencia

© 2026 Camping ACA Luján. Todos los derechos reservados.

---

**Desarrollado con ❤️ para Camping ACA Luján**
