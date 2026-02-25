from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .lead_forms import BirthdayLeadForm
from .models import Lead


def birthday_campaign(request):
    """Landing page pública para registro por QR (promos + cumple)."""
    if request.method == 'POST':
        form = BirthdayLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            # Capturar IP del visitante
            lead.ip_address = request.META.get('REMOTE_ADDR')
            lead.source = 'qr_register'
            lead.save()
            
            messages.success(
                request,
                f'¡Gracias {lead.full_name}! Te registraste correctamente. '
                'Te enviaremos ofertas especiales y un regalo cerca de tu cumpleaños.'
            )
            return redirect('landing:register_success')
    else:
        form = BirthdayLeadForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'landing/birthday_campaign.html', context)


def birthday_success(request):
    """Página de éxito después del registro"""
    return render(request, 'landing/birthday_success.html')
