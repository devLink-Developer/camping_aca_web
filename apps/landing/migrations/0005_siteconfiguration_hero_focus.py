from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_news_images'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE IF EXISTS landing_siteconfiguration
                ADD COLUMN IF NOT EXISTS hero_focus_x INTEGER NOT NULL DEFAULT 50;

            ALTER TABLE IF EXISTS landing_siteconfiguration
                ADD COLUMN IF NOT EXISTS hero_focus_y INTEGER NOT NULL DEFAULT 28;
            """,
            reverse_sql="""
            ALTER TABLE IF EXISTS landing_siteconfiguration
                DROP COLUMN IF EXISTS hero_focus_y;

            ALTER TABLE IF EXISTS landing_siteconfiguration
                DROP COLUMN IF EXISTS hero_focus_x;
            """,
        ),
    ]
