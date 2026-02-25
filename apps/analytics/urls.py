from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    path('api/visitors-chart/', views.analytics_visitors_chart, name='visitors_chart'),
    path('api/hourly-chart/', views.analytics_hourly_chart, name='hourly_chart'),
    path('api/sections/', views.analytics_sections, name='sections'),
    path('api/track-section/', views.analytics_track_section, name='track_section'),
    path('api/update-metrics/', views.analytics_update_page_metrics, name='update_metrics'),
]
