import uuid
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import PageView, UserSession


class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware para tracking de analytics"""

    DEDUPE_WINDOW_SECONDS = 30
    BOT_UA_SUBSTRINGS = (
        'curl/',
        'python-requests',
        'python-urllib',
        'wget/',
        'powershell',
        'postmanruntime',
        'insomnia',
        'healthcheck',
        'uptimerobot',
    )
    
    def process_request(self, request):
        # Generar o recuperar session_id
        if 'analytics_session_id' not in request.session:
            request.session['analytics_session_id'] = str(uuid.uuid4())
        
        request.analytics_session_id = request.session['analytics_session_id']
        request.analytics_start_time = timezone.now()
    
    def process_response(self, request, response):
        # Solo trackear páginas HTML exitosas
        if not hasattr(request, 'analytics_session_id'):
            return response

        # Evitar contar preflight/HEAD y otras solicitudes no-pageview
        if request.method != 'GET':
            return response
        
        if response.status_code != 200:
            return response
        
        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type:
            return response

        # Ignorar herramientas y bots comunes (incluye pruebas con curl/PowerShell)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ua_lower = (user_agent or '').lower()
        if any(token in ua_lower for token in self.BOT_UA_SUBSTRINGS):
            return response
        
        # No trackear páginas del admin, dashboard, vouchers ni estadísticas
        excluded_paths = ['/admin/', '/dashboard/', '/vouchers/', '/estadisticas/']
        if any(request.path.startswith(path) for path in excluded_paths):
            return response
        
        # Obtener información del user agent
        device_type = self._get_device_type(user_agent)
        browser = self._get_browser(user_agent)
        os = self._get_os(user_agent)
        
        # Obtener IP
        ip_address = self._get_client_ip(request)
        
        # Obtener referrer
        referrer = request.META.get('HTTP_REFERER', '')
        
        # Crear o actualizar sesión
        session, created = UserSession.objects.get_or_create(
            session_id=request.analytics_session_id,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent,
            }
        )
        
        if not created:
            session.last_activity = timezone.now()
            session.total_page_views += 1
            session.save()

        # Deduplicación: si el usuario refresca rápido o hay redirects, no inflar el contador
        dedupe_since = timezone.now() - timezone.timedelta(seconds=self.DEDUPE_WINDOW_SECONDS)
        if PageView.objects.filter(
            session_id=request.analytics_session_id,
            path=request.path,
            timestamp__gte=dedupe_since,
        ).exists():
            return response
        
        # Crear registro de vista de página
        PageView.objects.create(
            session_id=request.analytics_session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            device_type=device_type,
            browser=browser,
            os=os,
            path=request.path,
            referrer=referrer,
        )
        
        return response
    
    def _get_client_ip(self, request):
        """Obtiene la IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_device_type(self, user_agent):
        """Determina el tipo de dispositivo"""
        ua_lower = user_agent.lower()
        if 'mobile' in ua_lower or 'android' in ua_lower:
            return 'mobile'
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            return 'tablet'
        else:
            return 'desktop'
    
    def _get_browser(self, user_agent):
        """Determina el navegador"""
        ua_lower = user_agent.lower()
        if 'firefox' in ua_lower:
            return 'Firefox'
        elif 'chrome' in ua_lower and 'edg' not in ua_lower:
            return 'Chrome'
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            return 'Safari'
        elif 'edg' in ua_lower:
            return 'Edge'
        elif 'opera' in ua_lower or 'opr' in ua_lower:
            return 'Opera'
        else:
            return 'Other'
    
    def _get_os(self, user_agent):
        """Determina el sistema operativo"""
        ua_lower = user_agent.lower()
        if 'windows' in ua_lower:
            return 'Windows'
        elif 'mac' in ua_lower:
            return 'macOS'
        elif 'linux' in ua_lower:
            return 'Linux'
        elif 'android' in ua_lower:
            return 'Android'
        elif 'ios' in ua_lower or 'iphone' in ua_lower or 'ipad' in ua_lower:
            return 'iOS'
        else:
            return 'Other'
