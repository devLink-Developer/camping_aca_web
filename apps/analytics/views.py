from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncDate, TruncHour
from django.utils import timezone
from datetime import timedelta
from .models import PageView, SectionView, UserSession


@login_required
def analytics_dashboard(request):
    """Dashboard principal de analytics"""
    # Obtener rango de fechas (últimos 30 días por defecto)
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Estadísticas generales
    total_views = PageView.objects.filter(timestamp__gte=start_date).count()
    total_sessions = UserSession.objects.filter(start_time__gte=start_date).count()
    avg_time_on_page = PageView.objects.filter(
        timestamp__gte=start_date
    ).aggregate(avg=Avg('time_on_page'))['avg'] or 0
    avg_session_duration = UserSession.objects.filter(
        start_time__gte=start_date
    ).aggregate(avg=Avg('total_time'))['avg'] or 0
    
    # Visitantes únicos (por sesión)
    unique_visitors = PageView.objects.filter(
        timestamp__gte=start_date
    ).values('session_id').distinct().count()
    
    # Páginas más visitadas
    top_pages = PageView.objects.filter(
        timestamp__gte=start_date
    ).values('path').annotate(
        views=Count('session_id', distinct=True)
    ).order_by('-views')[:10]
    
    # Distribución por dispositivo
    device_distribution = PageView.objects.filter(
        timestamp__gte=start_date
    ).values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Distribución por navegador
    browser_distribution = PageView.objects.filter(
        timestamp__gte=start_date
    ).values('browser').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Top países
    top_countries = PageView.objects.filter(
        timestamp__gte=start_date
    ).exclude(country='').values('country').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Top ciudades
    top_cities = PageView.objects.filter(
        timestamp__gte=start_date
    ).exclude(city='').values('city', 'country').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'total_views': total_views,
        'total_sessions': total_sessions,
        'unique_visitors': unique_visitors,
        'avg_time_on_page': round(avg_time_on_page, 2),
        'avg_session_duration': round(avg_session_duration / 60, 2) if avg_session_duration else 0,
        'top_pages': top_pages,
        'device_distribution': device_distribution,
        'browser_distribution': browser_distribution,
        'top_countries': top_countries,
        'top_cities': top_cities,
        'days': days,
    }
    
    return render(request, 'analytics/dashboard.html', context)


@login_required
def analytics_visitors_chart(request):
    """API endpoint para gráfico de visitantes por día"""
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Agrupar por día
    daily_stats = PageView.objects.filter(
        timestamp__gte=start_date
    ).annotate(
        date=TruncDate('timestamp')
    ).values('date').annotate(
        views=Count('id'),
        unique_visitors=Count('session_id', distinct=True)
    ).order_by('date')
    
    # Formatear datos para Chart.js
    labels = [stat['date'].strftime('%d/%m') for stat in daily_stats]
    views = [stat['views'] for stat in daily_stats]
    unique = [stat['unique_visitors'] for stat in daily_stats]
    
    return JsonResponse({
        'labels': labels,
        'datasets': [
            {
                'label': 'Vistas Totales',
                'data': views,
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            },
            {
                'label': 'Visitantes Únicos',
                'data': unique,
                'borderColor': 'rgb(255, 99, 132)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            }
        ]
    })


@login_required
def analytics_hourly_chart(request):
    """API endpoint para gráfico de visitantes por hora"""
    start_date = timezone.now() - timedelta(hours=24)
    
    # Agrupar por hora
    hourly_stats = PageView.objects.filter(
        timestamp__gte=start_date
    ).annotate(
        hour=TruncHour('timestamp')
    ).values('hour').annotate(
        views=Count('id')
    ).order_by('hour')
    
    # Formatear datos
    labels = [stat['hour'].strftime('%H:00') for stat in hourly_stats]
    data = [stat['views'] for stat in hourly_stats]
    
    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Visitas por Hora',
            'data': data,
            'borderColor': 'rgb(54, 162, 235)',
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
        }]
    })


@login_required
def analytics_sections(request):
    """Estadísticas de secciones más visitadas"""
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    section_stats = SectionView.objects.filter(
        timestamp__gte=start_date
    ).values('section_name').annotate(
        views=Count('id'),
        avg_time=Avg('time_in_section')
    ).order_by('-views')[:10]
    
    return JsonResponse({
        'sections': list(section_stats)
    })


@login_required
def analytics_track_section(request):
    """API endpoint para trackear tiempo en secciones (llamado desde JS)"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        session_id = request.session.get('analytics_session_id')
        if not session_id:
            return JsonResponse({'success': False})
        
        # Obtener la última PageView de esta sesión
        last_page_view = PageView.objects.filter(
            session_id=session_id
        ).order_by('-timestamp').first()
        
        if last_page_view:
            SectionView.objects.create(
                page_view=last_page_view,
                section_id=data.get('section_id'),
                section_name=data.get('section_name'),
                time_in_section=data.get('time_in_section', 0)
            )
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})


@login_required
def analytics_update_page_metrics(request):
    """API endpoint para actualizar métricas de la página (tiempo y scroll)"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        session_id = request.session.get('analytics_session_id')
        if not session_id:
            return JsonResponse({'success': False})
        
        # Actualizar la última PageView
        last_page_view = PageView.objects.filter(
            session_id=session_id
        ).order_by('-timestamp').first()
        
        if last_page_view:
            last_page_view.time_on_page = data.get('time_on_page') or 0
            last_page_view.scroll_depth = data.get('scroll_depth') or 0
            last_page_view.save()
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})
