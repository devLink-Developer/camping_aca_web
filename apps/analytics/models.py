from django.db import models
from django.utils import timezone


class PageView(models.Model):
    """Registro de visualizaciones de página"""
    session_id = models.CharField('Session ID', max_length=100, db_index=True)
    ip_address = models.GenericIPAddressField('IP', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True)
    device_type = models.CharField('Tipo de Dispositivo', max_length=50, blank=True)  # mobile, tablet, desktop
    browser = models.CharField('Navegador', max_length=100, blank=True)
    os = models.CharField('Sistema Operativo', max_length=100, blank=True)
    
    # Información de geolocalización
    country = models.CharField('País', max_length=100, blank=True)
    city = models.CharField('Ciudad', max_length=100, blank=True)
    region = models.CharField('Región', max_length=100, blank=True)
    
    # Información de la visita
    path = models.CharField('Ruta', max_length=500, db_index=True)
    referrer = models.URLField('Referrer', blank=True, max_length=500)
    
    # Tiempo en la página
    time_on_page = models.IntegerField('Tiempo en Página (segundos)', default=0)
    scroll_depth = models.IntegerField('Profundidad de Scroll (%)', default=0)
    
    # Timestamp
    timestamp = models.DateTimeField('Fecha/Hora', default=timezone.now, db_index=True)
    
    class Meta:
        verbose_name = 'Vista de Página'
        verbose_name_plural = 'Vistas de Páginas'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['session_id', 'timestamp']),
            models.Index(fields=['path', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.path} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"


class SectionView(models.Model):
    """Registro de visualizaciones de secciones específicas"""
    page_view = models.ForeignKey(PageView, on_delete=models.CASCADE, related_name='section_views')
    section_id = models.CharField('ID de Sección', max_length=100)
    section_name = models.CharField('Nombre de Sección', max_length=200)
    time_in_section = models.IntegerField('Tiempo en Sección (segundos)', default=0)
    timestamp = models.DateTimeField('Fecha/Hora', default=timezone.now)
    
    class Meta:
        verbose_name = 'Vista de Sección'
        verbose_name_plural = 'Vistas de Secciones'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.section_name} - {self.time_in_section}s"


class UserSession(models.Model):
    """Sesiones de usuario"""
    session_id = models.CharField('Session ID', max_length=100, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField('IP', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True)
    
    # Información de la sesión
    start_time = models.DateTimeField('Inicio', default=timezone.now)
    last_activity = models.DateTimeField('Última Actividad', default=timezone.now)
    total_page_views = models.IntegerField('Páginas Vistas', default=0)
    total_time = models.IntegerField('Tiempo Total (segundos)', default=0)
    
    # Geolocalización
    country = models.CharField('País', max_length=100, blank=True)
    city = models.CharField('Ciudad', max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Sesión de Usuario'
        verbose_name_plural = 'Sesiones de Usuario'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Session {self.session_id} - {self.start_time.strftime('%d/%m/%Y')}"
    
    def duration_minutes(self):
        """Duración de la sesión en minutos"""
        delta = self.last_activity - self.start_time
        return round(delta.total_seconds() / 60, 2)
