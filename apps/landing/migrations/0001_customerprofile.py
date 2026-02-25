from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(verbose_name='Fecha de nacimiento')),
                ('dni', models.CharField(blank=True, max_length=20, verbose_name='DNI')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='Teléfono')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='customer_profile',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Usuario',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Perfil de Cliente',
                'verbose_name_plural': 'Perfiles de Clientes',
                'ordering': ['-created_at'],
            },
        ),
    ]
