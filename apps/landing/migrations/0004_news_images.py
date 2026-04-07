from __future__ import annotations

import django.db.models.deletion
from django.db import migrations, models


def backfill_news_images(apps, schema_editor):
    News = apps.get_model("landing", "News")
    NewsImage = apps.get_model("landing", "NewsImage")

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
                "verbose_name_plural": "Im\u00e1genes de Novedad",
                "ordering": ["order", "created_at"],
            },
        ),
        migrations.RunPython(backfill_news_images, migrations.RunPython.noop),
    ]
