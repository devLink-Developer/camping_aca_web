from django.db import models
from django.utils import timezone


class Lead(models.Model):
    """Leads capturados para campaña de cumpleaños"""
    
    # Datos personales
    full_name = models.CharField('Nombre Completo', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Teléfono', max_length=50)
    dni = models.CharField('DNI', max_length=20, blank=True)
    birth_date = models.DateField('Fecha de Cumpleaños')
    
    # Marketing
    accepts_marketing = models.BooleanField('Acepta Marketing', default=True, 
                                           help_text='Acepta recibir promociones y ofertas')
    
    # Control
    created_at = models.DateTimeField('Registrado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    ip_address = models.GenericIPAddressField('IP', blank=True, null=True)
    source = models.CharField('Fuente', max_length=50, default='qr_birthday', 
                             help_text='qr_birthday, web_form, etc')
    
    # Voucher generado
    birthday_voucher = models.ForeignKey('vouchers.Voucher', on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='lead',
                                        verbose_name='Voucher de Cumpleaños')
    voucher_sent = models.BooleanField('Voucher Enviado', default=False)
    voucher_sent_date = models.DateTimeField('Fecha Envío Voucher', blank=True, null=True)
    
    # Notas
    notes = models.TextField('Notas', blank=True)
    
    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['birth_date']),
            models.Index(fields=['voucher_sent']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.email}"
    
    def days_until_birthday(self):
        """Calcula días hasta el próximo cumpleaños"""
        today = timezone.now().date()
        next_birthday = self.birth_date.replace(year=today.year)
        
        # Si ya pasó este año, calcular para el próximo
        if next_birthday < today:
            next_birthday = self.birth_date.replace(year=today.year + 1)
        
        delta = next_birthday - today
        return delta.days
    
    def should_send_birthday_voucher(self):
        """Determina si debe enviarse el voucher (7 días antes del cumple)"""
        days = self.days_until_birthday()
        # Enviar 7 días antes si aún no se envió
        return 0 <= days <= 7 and not self.voucher_sent
