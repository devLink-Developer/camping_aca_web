from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import ContactMessage
from .models import CustomerProfile


class ContactForm(forms.ModelForm):
    """Formulario de contacto"""
    
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección de correo'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu mensaje',
                'rows': 5
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar', css_class='btn btn-primary w-100'))


class CustomerRegistrationForm(forms.Form):
    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Nombre'}),
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Apellido'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'tu@email.com'}),
    )
    birth_date = forms.DateField(
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
    )
    dni = forms.CharField(
        label='DNI (opcional)',
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'DNI (opcional)'}),
    )
    phone = forms.CharField(
        label='Teléfono (opcional)',
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Teléfono (opcional)'}),
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Repetí la contraseña'}),
    )

    def clean_email(self):
        User = get_user_model()
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            return email

        normalized_email = User.objects.normalize_email(email)
        exists = User.objects.filter(username__iexact=normalized_email).exists() or User.objects.filter(email__iexact=normalized_email).exists()
        if exists:
            raise ValidationError('Ya existe una cuenta con este email.')
        return normalized_email

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
            return cleaned

        if password1:
            try:
                validate_password(password1)
            except ValidationError as exc:
                self.add_error('password1', exc)

        return cleaned

    def save(self):
        User = get_user_model()

        email = self.cleaned_data['email']
        user = User.objects.create_user(
            username=email,
            email=email,
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )

        CustomerProfile.objects.create(
            user=user,
            birth_date=self.cleaned_data['birth_date'],
            dni=self.cleaned_data.get('dni', ''),
            phone=self.cleaned_data.get('phone', ''),
        )
        return user
