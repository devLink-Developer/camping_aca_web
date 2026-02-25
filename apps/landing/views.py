from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import (
    Service, PriceCategory, GalleryImage, 
    FAQ, Testimonial, ContactMessage, SiteConfiguration, News
)
from .forms import ContactForm, CustomerRegistrationForm


def landing_page(request):
    """Vista principal del landing page"""
    # Obtener configuración del sitio
    config = SiteConfiguration.get_config()
    
    # Obtener datos para el landing
    services = Service.objects.filter(is_active=True)
    price_categories = PriceCategory.objects.filter(is_active=True).prefetch_related('prices')
    gallery_images = GalleryImage.objects.filter(is_active=True)[:12]  # Limitar a 12 imágenes
    faqs = FAQ.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:6]
    news = News.objects.filter(is_active=True).prefetch_related('images').order_by('order', '-created_at')
    
    contact_form = ContactForm()
    registration_form = CustomerRegistrationForm()

    if request.method == 'POST':
        form_name = request.POST.get('form_name')

        # Registro de cuenta desde el landing
        if form_name == 'register':
            registration_form = CustomerRegistrationForm(request.POST)
            if registration_form.is_valid():
                user = registration_form.save()
                login(request, user)
                messages.success(
                    request,
                    '¡Cuenta creada! Ya estás registrado para recibir regalos y ofertas especiales.'
                )
                return redirect(f"{reverse('landing:home')}#registro")

        # Contacto (por defecto)
        else:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_message = contact_form.save()

                try:
                    send_mail(
                        subject=f'Nuevo mensaje de {contact_message.full_name}',
                        message=f"""
                        Nombre: {contact_message.full_name}
                        Email: {contact_message.email}
                        Teléfono: {contact_message.phone}

                        Mensaje:
                        {contact_message.message}
                        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[config.email or settings.DEFAULT_FROM_EMAIL],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Error sending email: {e}")

                messages.success(request, '¡Gracias por contactarnos! Te responderemos pronto.')
                return redirect(f"{reverse('landing:home')}#contacto")
    
    context = {
        'config': config,
        'services': services,
        'price_categories': price_categories,
        'gallery_images': gallery_images,
        'faqs': faqs,
        'testimonials': testimonials,
        'contact_form': contact_form,
        'registration_form': registration_form,
        'news_list': news,
    }
    
    return render(request, 'landing/index.html', context)
