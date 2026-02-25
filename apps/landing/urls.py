from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as django_auth_views
from django.urls import reverse_lazy
from . import views
from . import lead_views
from . import auth_views

app_name = 'landing'

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('acceso/', auth_views.acceso, name='acceso'),
    path('salir/', auth_views.salir, name='salir'),
    path('modo-cliente/', auth_views.toggle_client_mode, name='toggle_client_mode'),

    # Recuperación de contraseña (cuentas creadas desde el landing)
    path(
        'cuenta/recuperar/',
        django_auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset_form.html',
            email_template_name='auth/password_reset_email.txt',
            subject_template_name='auth/password_reset_subject.txt',
            success_url=reverse_lazy('landing:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'cuenta/recuperar/enviado/',
        django_auth_views.PasswordResetDoneView.as_view(
            template_name='auth/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'cuenta/restablecer/<uidb64>/<token>/',
        django_auth_views.PasswordResetConfirmView.as_view(
            template_name='auth/password_reset_confirm.html',
            success_url=reverse_lazy('landing:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'cuenta/restablecer/completo/',
        django_auth_views.PasswordResetCompleteView.as_view(
            template_name='auth/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),

    # URL canónica para QR/registro
    path('campaing/', lead_views.birthday_campaign, name='register_campaign'),
    path('campaing/gracias/', lead_views.birthday_success, name='register_success'),

    # Alias por nombre (compatibilidad de reverses antiguos)
    path('campaing/', lead_views.birthday_campaign, name='birthday_campaign'),
    path('campaing/gracias/', lead_views.birthday_success, name='birthday_success'),

    # Compatibilidad: URLs anteriores -> redirigen a la canónica
    path('cumpleanos/', RedirectView.as_view(pattern_name='landing:register_campaign', permanent=True)),
    path('cumpleanos/gracias/', RedirectView.as_view(pattern_name='landing:register_success', permanent=True)),
    path('registro/', RedirectView.as_view(pattern_name='landing:register_campaign', permanent=True)),
    path('registro/gracias/', RedirectView.as_view(pattern_name='landing:register_success', permanent=True)),

    # Extra: alias con ortografía correcta
    path('campaign/', RedirectView.as_view(pattern_name='landing:register_campaign', permanent=True)),
    path('campaign/gracias/', RedirectView.as_view(pattern_name='landing:register_success', permanent=True)),
]
