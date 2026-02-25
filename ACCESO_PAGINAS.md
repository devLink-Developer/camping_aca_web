# 🎯 Acceso a las Páginas de Administración

## ⚠️ IMPORTANTE: Debes Iniciar Sesión Primero

Todas las páginas de administración requieren autenticación. Antes de acceder:

1. **Inicia sesión en el admin de Django:**
   - URL: http://127.0.0.1:8007/admin
   - Usuario: `admin`
   - Contraseña: `admin123`

2. **Después de iniciar sesión**, podrás acceder a las páginas de administración desde el menú superior o directamente.

---

## 📌 Páginas Disponibles

### 🏠 Página Principal (Pública)
**URL:** http://127.0.0.1:8007/

Esta es la landing page del camping con:
- Hero section con imagen destacada
- Servicios
- Galería de imágenes
- Preguntas frecuentes (FAQs)
- Precios
- Formulario de contacto

---

## 🔐 Páginas de Administración (Requieren Login)

### 1. 📊 Estadísticas
**URL:** http://127.0.0.1:8007/dashboard/statistics/

Muestra métricas y análisis del sitio:
- Visitas totales, diarias, semanales y mensuales
- Gráfico de visitas de los últimos 7 días
- Top 10 páginas más visitadas
- Estadísticas de vouchers
- Mensajes de contacto

**Características:**
- Diseño consistente con la landing page
- Gráficos interactivos con Chart.js
- Tarjetas con iconos para cada métrica
- Tabla responsiva con páginas más visitadas

---

### 2. ⚙️ Configuración
**URL:** http://127.0.0.1:8007/dashboard/settings/

Administra la configuración general del sitio:
- **Información General:**
  - Nombre del sitio
  - Lema/Tagline
  - Imagen Hero principal
  
- **Información de Contacto:**
  - Teléfono
  - Email
  - Dirección
  - Horario de atención
  
- **Redes Sociales:**
  - Instagram URL
  - Facebook URL
  
- **Alerta Especial:**
  - Activar/desactivar alerta en la página principal
  - Mensaje de alerta personalizado

**Accesos Rápidos:**
Links directos al admin de Django para:
- Servicios
- Galería de imágenes
- Precios
- FAQs

---

### 3. 🎟️ Vouchers
**URL:** http://127.0.0.1:8007/vouchers/

Sistema de vouchers de regalo con código QR:
- Crear nuevos vouchers
- Ver vouchers activos/usados/expirados
- Escanear códigos QR
- Historial de uso

---

## 🔑 Credenciales de Acceso

**Usuario:** admin
**Contraseña:** admin123

⚠️ **IMPORTANTE:** Cambia la contraseña inmediatamente después del primer login

---

## 📱 Navegación

Las páginas de administración están accesibles desde el **menú superior** cuando inicias sesión:

```
Inicio | Servicios | Galería | Precios | Contacto | 📊 Estadísticas | ⚙️ Configuración | 🎟️ Vouchers
```

Solo los usuarios autenticados pueden ver y acceder a:
- Estadísticas
- Configuración  
- Vouchers

---

## 🎨 Diseño

Todas las páginas mantienen el mismo estilo visual:
- **Colores ACA:** Primario (azul), Danger (rojo)
- **Typography:** Noto Sans & Montserrat
- **Framework:** Bootstrap 5
- **Animaciones:** AOS (Animate On Scroll)
- **Icons:** Font Awesome 6

---

## 🚀 Funcionalidades

### Estadísticas
- ✅ Métricas en tiempo real
- ✅ Gráficos interactivos
- ✅ Datos de los últimos 7, 30 días
- ✅ Top páginas visitadas

### Configuración
- ✅ Actualización en vivo
- ✅ Upload de imagen hero
- ✅ Gestión de redes sociales
- ✅ Sistema de alertas

### Vouchers
- ✅ Generación de QR automática
- ✅ Scanner web
- ✅ Validación en tiempo real
- ✅ Logs de uso

---

## 📞 Soporte

Si necesitas ayuda o tienes preguntas:
1. Revisa la documentación en el README.md principal
2. Consulta el QUICKSTART.md para configuración inicial
3. Accede al panel de admin de Django en /admin para gestión avanzada
