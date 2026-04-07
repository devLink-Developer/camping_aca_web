from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0004_news_images"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
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
            ],
            state_operations=[
                migrations.AddField(
                    model_name="siteconfiguration",
                    name="hero_focus_x",
                    field=models.IntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Foco horizontal Hero (%)"),
                ),
                migrations.AddField(
                    model_name="siteconfiguration",
                    name="hero_focus_y",
                    field=models.IntegerField(default=28, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Foco vertical Hero (%)"),
                ),
            ],
        ),
    ]
