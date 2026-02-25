from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Voucher, VoucherUsageLog


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['voucher_code', 'client_name', 'value', 'status', 'expiration_date', 
                    'qr_preview', 'days_left', 'created_at']
    list_filter = ['status', 'issue_date', 'expiration_date', 'created_at']
    search_fields = ['voucher_code', 'client_name', 'client_email', 'client_phone', 'client_id']
    readonly_fields = ['voucher_code', 'qr_code_preview', 'client_id', 'created_at',
                       'updated_at', 'used_date', 'used_by', 'sent_date', 'sent_whatsapp_date']
    
    fieldsets = (
        ('Información del Voucher', {
            'fields': ('voucher_code', 'qr_code_preview', 'status', 'value', 'description', 'service_type')
        }),
        ('Información del Cliente', {
            'fields': ('client_id', 'client_name', 'client_email', 'client_phone')
        }),
        ('Envío', {
            'fields': ('sent', 'sent_date', 'sent_whatsapp', 'sent_whatsapp_date')
        }),
        ('Validez', {
            'fields': ('issue_date', 'validity_days', 'expiration_date')
        }),
        ('Uso', {
            'fields': ('used_date', 'used_by')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'created_at', 'updated_at', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />', obj.qr_code.url)
        return '-'
    qr_preview.short_description = 'QR'
    
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="200" height="200" />', obj.qr_code.url)
        return 'QR no generado'
    qr_code_preview.short_description = 'Código QR'
    
    def days_left(self, obj):
        days = obj.days_until_expiration()
        if obj.status == 'used':
            return format_html('<span style="color: green;">✓ Usado</span>')
        elif obj.status == 'expired' or days == 0:
            return format_html('<span style="color: red;">Vencido</span>')
        elif days <= 30:
            return format_html('<span style="color: orange;">{} días</span>', days)
        else:
            return format_html('{} días', days)
    days_left.short_description = 'Estado/Días'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo voucher
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['mark_as_used', 'mark_as_cancelled', 'export_vouchers']
    
    def mark_as_used(self, request, queryset):
        count = 0
        for voucher in queryset:
            if voucher.mark_as_used(request.user):
                count += 1
        self.message_user(request, f'{count} voucher(s) marcado(s) como usado(s).')
    mark_as_used.short_description = 'Marcar como usado'
    
    def mark_as_cancelled(self, request, queryset):
        count = queryset.update(status='cancelled')
        self.message_user(request, f'{count} voucher(s) cancelado(s).')
    mark_as_cancelled.short_description = 'Cancelar vouchers'


@admin.register(VoucherUsageLog)
class VoucherUsageLogAdmin(admin.ModelAdmin):
    list_display = ['voucher', 'action', 'result', 'user', 'ip_address', 'timestamp']
    list_filter = ['action', 'result', 'timestamp']
    search_fields = ['voucher__voucher_code', 'voucher__client_name', 'ip_address']
    readonly_fields = ['voucher', 'action', 'user', 'ip_address', 'user_agent', 
                       'result', 'notes', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
