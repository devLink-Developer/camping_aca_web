from django import forms
from django.utils import timezone
from datetime import date
from .models import Lead


class BirthdayLeadForm(forms.ModelForm):
    """Formulario público para captación de leads de cumpleaños"""
    
    class Meta:
        model = Lead
        fields = ['full_name', 'email', 'phone', 'dni', 'birth_date', 'accepts_marketing']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Juan Pérez'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'tu@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '11 2345-6789'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '12345678'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date',
                'max': date.today().isoformat()
            }),
            'accepts_marketing': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'full_name': 'Nombre Completo',
            'email': 'Email',
            'phone': 'Teléfono',
            'dni': 'DNI (opcional)',
            'birth_date': 'Fecha de Nacimiento',
            'accepts_marketing': 'Acepto recibir promociones y ofertas especiales',
        }
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            # Verificar que la fecha sea pasada
            if birth_date > date.today():
                raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
            
            # Verificar edad mínima (opcional, ej: 18 años)
            age = (date.today() - birth_date).days // 365
            if age < 1:
                raise forms.ValidationError('Debe tener al menos 1 año.')
        
        return birth_date
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verificar si el email ya existe (permitir actualización si existe)
        if email:
            existing = Lead.objects.filter(email=email).first()
            if existing and not self.instance.pk:
                # Si existe y no estamos editando, actualizar el existente
                self.instance = existing
        return email
