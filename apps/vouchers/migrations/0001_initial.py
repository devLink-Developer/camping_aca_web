import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Código de Voucher')),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='vouchers/qr/', verbose_name='Código QR')),
                ('client_id', models.CharField(blank=True, help_text='Identificador único del cliente', max_length=50, verbose_name='ID Cliente')),
                ('client_name', models.CharField(max_length=200, verbose_name='Nombre del Cliente')),
                ('client_email', models.EmailField(max_length=254, verbose_name='Email del Cliente')),
                ('client_phone', models.CharField(max_length=50, verbose_name='Teléfono del Cliente')),
                ('voucher_type', models.CharField(choices=[('amount', 'Monto Fijo'), ('percentage', 'Porcentaje de Descuento'), ('free_text', 'Texto Libre/Beneficio')], default='amount', max_length=20, verbose_name='Tipo de Voucher')),
                ('value', models.DecimalField(blank=True, decimal_places=2, help_text='Valor monetario fijo (ej: $5000)', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Valor')),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, help_text='Porcentaje de descuento (ej: 50 para 50%)', max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Porcentaje')),
                ('benefit_description', models.TextField(blank=True, help_text='Ej: "2 horas de Paddle", "Alquiler de kayak por 1 día"', verbose_name='Descripción del Beneficio')),
                ('description', models.TextField(blank=True, help_text='Descripción adicional del servicio', verbose_name='Descripción')),
                ('service_type', models.CharField(blank=True, max_length=200, verbose_name='Tipo de Servicio')),
                ('status', models.CharField(choices=[('active', 'Activo'), ('used', 'Usado'), ('expired', 'Vencido'), ('cancelled', 'Cancelado')], default='active', max_length=20, verbose_name='Estado')),
                ('issue_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Emisión')),
                ('expiration_date', models.DateTimeField(verbose_name='Fecha de Vencimiento')),
                ('validity_days', models.IntegerField(default=365, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Días de Validez')),
                ('used_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Uso')),
                ('sent', models.BooleanField(default=False, help_text='Indica si el voucher fue enviado por email', verbose_name='Enviado')),
                ('sent_date', models.DateTimeField(blank=True, help_text='Fecha y hora de envío del email', null=True, verbose_name='Fecha de Envío')),
                ('sent_whatsapp', models.BooleanField(default=False, help_text='Indica si el voucher fue enviado por WhatsApp', verbose_name='Enviado por WhatsApp')),
                ('sent_whatsapp_date', models.DateTimeField(blank=True, help_text='Fecha y hora de envío por WhatsApp', null=True, verbose_name='Fecha de Envío por WhatsApp')),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vouchers_created', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('used_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vouchers_used', to=settings.AUTH_USER_MODEL, verbose_name='Usado por')),
            ],
            options={
                'verbose_name': 'Voucher',
                'verbose_name_plural': 'Vouchers',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VoucherUsageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=50, verbose_name='Acción')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
                ('user_agent', models.TextField(blank=True, verbose_name='User Agent')),
                ('result', models.CharField(max_length=50, verbose_name='Resultado')),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha/Hora')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usage_logs', to='vouchers.voucher')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Registro de Uso',
                'verbose_name_plural': 'Registros de Uso',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='voucher',
            index=models.Index(fields=['voucher_code'], name='vouchers_vo_voucher_code_idx'),
        ),
        migrations.AddIndex(
            model_name='voucher',
            index=models.Index(fields=['status', 'expiration_date'], name='vouchers_vo_status_expiration_idx'),
        ),
        migrations.AddIndex(
            model_name='voucher',
            index=models.Index(fields=['client_email'], name='vouchers_vo_client_email_idx'),
        ),
    ]
