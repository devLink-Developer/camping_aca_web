from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0005_siteconfiguration_hero_focus"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
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
            ],
            state_operations=[
                migrations.AddField(
                    model_name="service",
                    name="icon_fa",
                    field=models.CharField(blank=True, default="", help_text="Ej: fa-campground, fa-swimming-pool", max_length=50, verbose_name="Icono FontAwesome"),
                ),
            ],
        ),
    ]
