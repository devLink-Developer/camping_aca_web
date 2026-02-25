from django import forms
from django.utils import timezone
from datetime import timedelta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Row, Column
from .models import Voucher


class VoucherCreateForm(forms.ModelForm):
    """Formulario para crear vouchers"""
    
    class Meta:
        model = Voucher
        fields = [
            'client_name', 'client_email', 'client_phone', 'client_id',
            'voucher_type', 'value', 'percentage', 'benefit_description',
            'description', 'service_type',
            'validity_days', 'notes'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'client_email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'client_phone': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'client_id': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'DNI o documento'}),
            'voucher_type': forms.Select(attrs={'class': 'form-select form-select-sm', 'id': 'voucher_type'}),
            'value': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'amount_value', 'placeholder': '5000'}),
            'percentage': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'percentage_value', 'placeholder': '50', 'step': '0.01'}),
            'benefit_description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'id': 'benefit_desc', 
                                                          'placeholder': 'Ej: 2 horas de Paddle, Alquiler de kayak por 1 día'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'service_type': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ej: Estadía, Actividades, Alquiler'}),
            'validity_days': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'value': 365}),
            'notes': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        voucher_type = cleaned_data.get('voucher_type')
        value = cleaned_data.get('value')
        percentage = cleaned_data.get('percentage')
        benefit_description = cleaned_data.get('benefit_description')
        
        # Validar que según el tipo, tenga el campo requerido
        if voucher_type == 'amount' and not value:
            self.add_error('value', 'El monto es requerido para vouchers de monto fijo.')
        
        if voucher_type == 'percentage' and not percentage:
            self.add_error('percentage', 'El porcentaje es requerido para vouchers de descuento.')
        
        if voucher_type == 'free_text' and not benefit_description:
            self.add_error('benefit_description', 'La descripción del beneficio es requerida para vouchers de texto libre.')
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Información del Cliente',
                Row(
                    Column('client_name', css_class='col-md-6'),
                    Column('client_email', css_class='col-md-6'),
                ),
                'client_phone',
            ),
            Fieldset(
                'Detalles del Voucher',
                Row(
                    Column('value', css_class='col-md-6'),
                    Column('service_type', css_class='col-md-6'),
                ),
                'description',
                'validity_days',
                'notes',
            ),
            Submit('submit', 'Crear Voucher', css_class='btn btn-primary')
        )


class VoucherScanForm(forms.Form):
    """Formulario para escaneo manual de voucher"""
    voucher_code = forms.UUIDField(
        label='Código de Voucher',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Ingrese el código del voucher'
        })
    )
