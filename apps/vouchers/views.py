from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseRedirect
import json

from .models import Voucher, VoucherUsageLog
from .forms import VoucherCreateForm, VoucherScanForm


staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url=settings.LOGIN_URL)


@staff_required
def voucher_list(request):
    """Lista de todos los vouchers con filtros"""
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    search = request.GET.get('search', '')
    
    vouchers = Voucher.objects.all()
    
    if status_filter:
        vouchers = vouchers.filter(status=status_filter)
        
    if type_filter:
        vouchers = vouchers.filter(voucher_type=type_filter)
    
    if search:
        vouchers = vouchers.filter(
            Q(voucher_code__icontains=search) |
            Q(client_name__icontains=search) |
            Q(client_email__icontains=search) |
            Q(client_phone__icontains=search) |
            Q(client_id__icontains=search)
        )
    
    # Estadísticas
    stats = {
        'total': Voucher.objects.count(),
        'active': Voucher.objects.filter(status='active').count(),
        'used': Voucher.objects.filter(status='used').count(),
        'expired': Voucher.objects.filter(status='expired').count(),
    }
    
    context = {
        'vouchers': vouchers,
        'stats': stats,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search': search,
    }
    
    return render(request, 'vouchers/voucher_list.html', context)


@staff_required
def voucher_create(request):
    """Crear nuevo voucher"""
    if request.method == 'POST':
        form = VoucherCreateForm(request.POST)
        if form.is_valid():
            voucher = form.save(commit=False)
            voucher.created_by = request.user
            voucher.save()
            messages.success(request, f'Voucher {voucher.voucher_code} creado exitosamente.')
            return redirect('vouchers:detail', voucher_code=voucher.voucher_code)
    else:
        form = VoucherCreateForm()
    
    return render(request, 'vouchers/voucher_create.html', {'form': form})


@staff_required
def voucher_detail(request, voucher_code):
    """Detalle de un voucher"""
    voucher = get_object_or_404(Voucher, voucher_code=voucher_code)
    usage_logs = voucher.usage_logs.all()[:20]
    
    context = {
        'voucher': voucher,
        'usage_logs': usage_logs,
    }
    
    return render(request, 'vouchers/voucher_detail.html', context)


@staff_required
def voucher_scanner(request):
    """Compat: redirige a la lista (escaneo en modal)"""
    url = reverse('vouchers:list')
    return HttpResponseRedirect(f"{url}?scan=1")


@staff_required
@require_http_methods(["POST"])
def voucher_validate(request):
    """API endpoint para validar un voucher escaneado"""
    try:
        data = json.loads(request.body)
        voucher_code = data.get('voucher_code')
        
        if not voucher_code:
            return JsonResponse({'success': False, 'error': 'Código de voucher no proporcionado'})
        
        try:
            voucher = Voucher.objects.get(voucher_code=voucher_code)
        except Voucher.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Voucher no encontrado'})
        
        # Log intento de validación
        log_result = 'success' if voucher.is_valid() else voucher.status
        VoucherUsageLog.objects.create(
            voucher=voucher,
            action='validate',
            user=request.user,
            ip_address=get_client_ip(request),
            result=log_result
        )
        
        if voucher.is_valid():
            used_by = None
            if voucher.used_by_id:
                used_by = voucher.used_by.get_username() if hasattr(voucher.used_by, 'get_username') else str(voucher.used_by)

            return JsonResponse({
                'success': True,
                'voucher': {
                    # compatibilidad (frontend puede usar code o voucher_code)
                    'code': str(voucher.voucher_code),
                    'voucher_code': str(voucher.voucher_code),

                    'client_id': voucher.client_id,
                    'client_name': voucher.client_name,
                    'client_email': voucher.client_email,
                    'client_phone': voucher.client_phone,

                    'voucher_type': voucher.voucher_type,
                    'voucher_type_display': voucher.get_voucher_type_display(),
                    'value': str(voucher.value) if voucher.value is not None else None,
                    'percentage': str(voucher.percentage) if voucher.percentage is not None else None,
                    'benefit_description': voucher.benefit_description,

                    'description': voucher.description,
                    'service_type': voucher.service_type,
                    'issue_date': voucher.issue_date.strftime('%d/%m/%Y %H:%M') if voucher.issue_date else None,
                    'expiration_date': voucher.expiration_date.strftime('%d/%m/%Y'),
                    'days_left': voucher.days_until_expiration(),
                    'status': voucher.status,
                    'status_display': voucher.get_status_display(),

                    'sent': bool(voucher.sent),
                    'sent_date': voucher.sent_date.strftime('%d/%m/%Y %H:%M') if voucher.sent_date else None,
                    'sent_whatsapp': bool(getattr(voucher, 'sent_whatsapp', False)),
                    'sent_whatsapp_date': voucher.sent_whatsapp_date.strftime('%d/%m/%Y %H:%M') if getattr(voucher, 'sent_whatsapp_date', None) else None,
                    'used_date': voucher.used_date.strftime('%d/%m/%Y %H:%M') if voucher.used_date else None,
                    'used_by': used_by,
                }
            })
        else:
            error_msg = {
                'used': 'Este voucher ya fue utilizado',
                'expired': 'Este voucher está vencido',
                'cancelled': 'Este voucher fue cancelado',
            }.get(voucher.status, 'Voucher inválido')
            
            return JsonResponse({'success': False, 'error': error_msg})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error: {str(e)}'})


@staff_required
@require_http_methods(["POST"])
def voucher_use(request):
    """API endpoint para marcar un voucher como usado"""
    try:
        data = json.loads(request.body)
        voucher_code = data.get('voucher_code')
        
        if not voucher_code:
            return JsonResponse({'success': False, 'error': 'Código de voucher no proporcionado'})
        
        voucher = get_object_or_404(Voucher, voucher_code=voucher_code)
        
        if voucher.mark_as_used(request.user):
            # Log uso exitoso
            VoucherUsageLog.objects.create(
                voucher=voucher,
                action='use',
                user=request.user,
                ip_address=get_client_ip(request),
                result='success',
                notes='Voucher marcado como usado'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Voucher marcado como usado exitosamente',
                'used_date': voucher.used_date.strftime('%d/%m/%Y %H:%M'),
                'voucher': {
                    'code': str(voucher.voucher_code),
                    'voucher_code': str(voucher.voucher_code),
                    'status': voucher.status,
                    'status_display': voucher.get_status_display(),
                    'used_date': voucher.used_date.strftime('%d/%m/%Y %H:%M') if voucher.used_date else None,
                    'used_by': request.user.get_username() if hasattr(request.user, 'get_username') else str(request.user),
                }
            })
        else:
            # Log intento fallido
            VoucherUsageLog.objects.create(
                voucher=voucher,
                action='use',
                user=request.user,
                ip_address=get_client_ip(request),
                result='failed',
                notes=f'Estado actual: {voucher.status}'
            )
            
            return JsonResponse({
                'success': False,
                'error': f'No se puede usar el voucher. Estado: {voucher.get_status_display()}'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error: {str(e)}'})


def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
