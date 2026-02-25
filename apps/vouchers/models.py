import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont


class Voucher(models.Model):
    """Vouchers de regalo con QR"""
    
    VOUCHER_TYPE_CHOICES = [
        ('amount', 'Monto Fijo'),
        ('percentage', 'Porcentaje de Descuento'),
        ('free_text', 'Texto Libre/Beneficio'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('used', 'Usado'),
        ('expired', 'Vencido'),
        ('cancelled', 'Cancelado'),
    ]
    
    # Identificación
    voucher_code = models.UUIDField('Código de Voucher', default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField('Código QR', upload_to='vouchers/qr/', blank=True, null=True)
    
    # Información del cliente
    client_id = models.CharField('ID Cliente', max_length=50, blank=True, help_text='Identificador único del cliente')
    client_name = models.CharField('Nombre del Cliente', max_length=200)
    client_email = models.EmailField('Email del Cliente')
    client_phone = models.CharField('Teléfono del Cliente', max_length=50)
    
    # Tipo de voucher
    voucher_type = models.CharField('Tipo de Voucher', max_length=20, choices=VOUCHER_TYPE_CHOICES, default='amount')
    
    # Detalles del voucher - Monto (para tipo 'amount')
    value = models.DecimalField('Valor', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], 
                                 blank=True, null=True, help_text='Valor monetario fijo (ej: $5000)')
    
    # Detalles del voucher - Porcentaje (para tipo 'percentage')
    percentage = models.DecimalField('Porcentaje', max_digits=5, decimal_places=2, validators=[MinValueValidator(0)],
                                     blank=True, null=True, help_text='Porcentaje de descuento (ej: 50 para 50%)')
    
    # Detalles del voucher - Texto libre (para tipo 'free_text')
    benefit_description = models.TextField('Descripción del Beneficio', blank=True, 
                                           help_text='Ej: "2 horas de Paddle", "Alquiler de kayak por 1 día"')
    
    # Detalles generales
    description = models.TextField('Descripción', blank=True, help_text='Descripción adicional del servicio')
    service_type = models.CharField('Tipo de Servicio', max_length=200, blank=True)
    
    # Estado y validez
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='active')
    issue_date = models.DateTimeField('Fecha de Emisión', default=timezone.now)
    expiration_date = models.DateTimeField('Fecha de Vencimiento')
    validity_days = models.IntegerField('Días de Validez', default=365, validators=[MinValueValidator(1)])
    
    # Uso
    used_date = models.DateTimeField('Fecha de Uso', blank=True, null=True)
    used_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, 
                                 verbose_name='Usado por', related_name='vouchers_used')
    
    # Envío por email
    sent = models.BooleanField('Enviado', default=False, help_text='Indica si el voucher fue enviado por email')
    sent_date = models.DateTimeField('Fecha de Envío', blank=True, null=True, help_text='Fecha y hora de envío del email')

    # Envío por WhatsApp
    sent_whatsapp = models.BooleanField('Enviado por WhatsApp', default=False, help_text='Indica si el voucher fue enviado por WhatsApp')
    sent_whatsapp_date = models.DateTimeField('Fecha de Envío por WhatsApp', blank=True, null=True, help_text='Fecha y hora de envío por WhatsApp')
    
    # Auditoría
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Creado por', related_name='vouchers_created')
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    notes = models.TextField('Notas', blank=True)
    
    class Meta:
        verbose_name = 'Voucher'
        verbose_name_plural = 'Vouchers'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['voucher_code']),
            models.Index(fields=['status', 'expiration_date']),
            models.Index(fields=['client_email']),
        ]
    
    def __str__(self):
        return f"{self.client_name} - {self.voucher_code}"
    
    def save(self, *args, **kwargs):
        # Calcular fecha de vencimiento si no está definida
        if not self.expiration_date:
            self.expiration_date = self.issue_date + timedelta(days=self.validity_days)
        
        # Actualizar estado si está vencido
        if self.status == 'active' and timezone.now() > self.expiration_date:
            self.status = 'expired'
        
        # Generar ID de cliente si no existe
        if not self.client_id:
            self.client_id = f"CLI-{self.voucher_code.hex[:8].upper()}"
        
        super().save(*args, **kwargs)
        
        # Generar código QR si no existe
        if not self.qr_code:
            self.generate_qr_code()
    
    def generate_qr_code(self):
        """Genera el código QR para el voucher"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        
        # Datos del QR: código del voucher
        qr_data = str(self.voucher_code)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Crear imagen QR
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Agregar ID visible debajo del QR (para ingreso manual)
        voucher_id_text = f"ID: {self.voucher_code}"
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

        # Calcular área de texto (una o dos líneas si es largo)
        max_chars = 28
        lines = [voucher_id_text[i:i+max_chars] for i in range(0, len(voucher_id_text), max_chars)]
        lines = lines[:2]  # limitar a 2 líneas
        line_height = 14
        padding_y = 10
        text_area_height = padding_y * 2 + (len(lines) * line_height)

        canvas = Image.new('RGB', (qr_img.width, qr_img.height + text_area_height), 'white')
        canvas.paste(qr_img, (0, 0))

        draw = ImageDraw.Draw(canvas)
        y = qr_img.height + padding_y
        for line in lines:
            # centrar texto
            if font:
                text_w = draw.textlength(line, font=font)
            else:
                text_w = draw.textlength(line)
            x = max(0, (qr_img.width - int(text_w)) // 2)
            draw.text((x, y), line, fill='black', font=font)
            y += line_height

        img = canvas
        
        # Guardar en BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Guardar archivo
        filename = f'voucher_{self.voucher_code.hex}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        super().save(update_fields=['qr_code'])
    
    def mark_as_used(self, user=None):
        """Marca el voucher como usado"""
        if self.status == 'active':
            self.status = 'used'
            self.used_date = timezone.now()
            self.used_by = user
            self.save()
            return True
        return False
    
    def is_valid(self):
        """Verifica si el voucher es válido"""
        if self.status != 'active':
            return False
        if timezone.now() > self.expiration_date:
            self.status = 'expired'
            self.save()
            return False
        return True
    
    def days_until_expiration(self):
        """Días restantes hasta el vencimiento"""
        if self.expiration_date:
            delta = self.expiration_date - timezone.now()
            return max(0, delta.days)
        return 0


class VoucherUsageLog(models.Model):
    """Registro de intentos de uso de vouchers (auditoría)"""
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='usage_logs')
    action = models.CharField('Acción', max_length=50)  # 'scan', 'validate', 'use', 'reject'
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField('IP', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True)
    result = models.CharField('Resultado', max_length=50)  # 'success', 'failed', 'already_used', 'expired'
    notes = models.TextField('Notas', blank=True)
    timestamp = models.DateTimeField('Fecha/Hora', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Registro de Uso'
        verbose_name_plural = 'Registros de Uso'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.voucher.voucher_code} - {self.action} - {self.timestamp}"
