from __future__ import annotations

import django.db.models.deletion
from django.db import migrations, models


def backfill_news_images(apps, schema_editor):
    News = apps.get_model("landing", "News")
    NewsImage = apps.get_model("landing", "NewsImage")

    # Crear una imagen inicial por cada News existente (si tiene cover).
    for news in News.objects.all().iterator():
        try:
            has_cover = bool(getattr(news, "image", None))
        except Exception:
            has_cover = False

        if not has_cover:
            continue

        exists = NewsImage.objects.filter(news_id=news.id, order=0).exists()
        if exists:
            continue

        NewsImage.objects.create(news_id=news.id, image=news.image, order=0)


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0003_create_landing_core_tables"),
    ]

    operations = [
        # Nota: las tablas del landing se crearon por SQL en 0003, pero ese
        # migration no registró los modelos en el estado de Django.
        # Para poder crear el FK, declaramos el modelo News en el estado,
        # sin tocar la base (SeparateDatabaseAndState).
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="News",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("title", models.CharField(max_length=200, verbose_name="Título")),
                        ("description", models.TextField(verbose_name="Descripción")),
                        ("image", models.ImageField(upload_to="config/news/", verbose_name="Imagen")),
                        ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                        ("order", models.IntegerField(default=0, verbose_name="Orden")),
                        ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Creado")),
                        ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Actualizado")),
                    ],
                    options={
                        "verbose_name": "Novedad",
                        "verbose_name_plural": "Novedades",
                        "ordering": ["order", "-created_at"],
                    },
                ),
            ],
        ),
        migrations.CreateModel(
            name="NewsImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="config/news/", verbose_name="Imagen")),
                ("order", models.IntegerField(default=0, verbose_name="Orden")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Creado")),
                (
                    "news",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="landing.news"),
                ),
            ],
            options={
                "verbose_name": "Imagen de Novedad",
                "verbose_name_plural": "Imágenes de Novedad",
                "ordering": ["order", "created_at"],
            },
        ),
        migrations.RunPython(backfill_news_images, migrations.RunPython.noop),
    ]
