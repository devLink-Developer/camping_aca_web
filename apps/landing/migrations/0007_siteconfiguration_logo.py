from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_service_icon_fa'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='config/', verbose_name='Logo'),
        ),
    ]
