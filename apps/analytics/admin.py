from django.contrib import admin
from django.db.models import Count, Avg, Sum
from django.utils.html import format_html
from .models import PageView, SectionView, UserSession


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'device_type', 'browser', 'country', 'city', 
                    'time_on_page', 'scroll_depth', 'timestamp']
    list_filter = ['device_type', 'browser', 'country', 'timestamp']
    search_fields = ['path', 'ip_address', 'session_id', 'city']
    readonly_fields = ['session_id', 'ip_address', 'user_agent', 'device_type', 
                       'browser', 'os', 'country', 'city', 'region', 'path', 
                       'referrer', 'time_on_page', 'scroll_depth', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False


@admin.register(SectionView)
class SectionViewAdmin(admin.ModelAdmin):
    list_display = ['section_name', 'time_in_section', 'page_view', 'timestamp']
    list_filter = ['section_name', 'timestamp']
    search_fields = ['section_name', 'section_id']
    readonly_fields = ['page_view', 'section_id', 'section_name', 
                       'time_in_section', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'country', 'city', 'total_page_views', 
                    'duration_display', 'start_time', 'last_activity']
    list_filter = ['country', 'start_time']
    search_fields = ['session_id', 'ip_address', 'city']
    readonly_fields = ['session_id', 'ip_address', 'user_agent', 'start_time', 
                       'last_activity', 'total_page_views', 'total_time', 
                       'country', 'city']
    date_hierarchy = 'start_time'
    
    def duration_display(self, obj):
        minutes = obj.duration_minutes()
        if minutes < 1:
            return format_html('<span style="color: gray;">{} min</span>', minutes)
        elif minutes < 5:
            return format_html('<span style="color: green;">{} min</span>', minutes)
        else:
            return format_html('<span style="color: blue;">{} min</span>', minutes)
    duration_display.short_description = 'Duración'
    
    def has_add_permission(self, request):
        return False
