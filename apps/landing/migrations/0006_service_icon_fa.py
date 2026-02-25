from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_siteconfiguration_hero_focus'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE IF EXISTS landing_service
                ADD COLUMN IF NOT EXISTS icon_fa VARCHAR(50) NOT NULL DEFAULT '';
            """,
            reverse_sql="""
            ALTER TABLE IF EXISTS landing_service
                DROP COLUMN IF EXISTS icon_fa;
            """,
        ),
    ]
