import django.db.models.deletion
from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0002_create_lead_table"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                    -- Core content tables for Landing app.
                    -- These tables are required at runtime but weren't covered by earlier migrations.

                    CREATE TABLE IF NOT EXISTS landing_siteconfiguration (
                        id BIGSERIAL PRIMARY KEY,
                        site_name VARCHAR(200) NOT NULL DEFAULT 'Camping ACA Luj\u00e1n',
                        tagline VARCHAR(500) NOT NULL DEFAULT 'Un lugar para vos',
                        hero_image VARCHAR(100) NULL,
                        phone VARCHAR(50) NOT NULL DEFAULT '',
                        email VARCHAR(254) NOT NULL DEFAULT '',
                        address TEXT NOT NULL DEFAULT '',
                        instagram_url VARCHAR(200) NOT NULL DEFAULT '',
                        facebook_url VARCHAR(200) NOT NULL DEFAULT '',
                        opening_hours TEXT NOT NULL DEFAULT 'Mi\u00e9rcoles a Lunes de 10 a 18 hs',
                        special_alert TEXT NOT NULL DEFAULT '',
                        is_alert_active BOOLEAN NOT NULL DEFAULT FALSE
                    );

                    CREATE TABLE IF NOT EXISTS landing_service (
                        id BIGSERIAL PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        icon VARCHAR(100) NULL,
                        description TEXT NOT NULL,
                        features JSONB NOT NULL DEFAULT '[]'::jsonb,
                        "order" INTEGER NOT NULL DEFAULT 0,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );

                    CREATE TABLE IF NOT EXISTS landing_pricecategory (
                        id BIGSERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        description TEXT NOT NULL DEFAULT '',
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        "order" INTEGER NOT NULL DEFAULT 0
                    );

                    CREATE TABLE IF NOT EXISTS landing_price (
                        id BIGSERIAL PRIMARY KEY,
                        category_id BIGINT NOT NULL,
                        item_name VARCHAR(200) NOT NULL,
                        description TEXT NOT NULL DEFAULT '',
                        amount NUMERIC(10, 2) NOT NULL,
                        is_free BOOLEAN NOT NULL DEFAULT FALSE,
                        "order" INTEGER NOT NULL DEFAULT 0,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        CONSTRAINT landing_price_category_fk
                            FOREIGN KEY (category_id)
                            REFERENCES landing_pricecategory (id)
                            ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS landing_galleryimage (
                        id BIGSERIAL PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        image VARCHAR(100) NOT NULL,
                        description TEXT NOT NULL DEFAULT '',
                        alt_text VARCHAR(200) NOT NULL,
                        "order" INTEGER NOT NULL DEFAULT 0,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );

                    CREATE TABLE IF NOT EXISTS landing_faq (
                        id BIGSERIAL PRIMARY KEY,
                        question VARCHAR(500) NOT NULL,
                        answer TEXT NOT NULL,
                        "order" INTEGER NOT NULL DEFAULT 0,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );

                    CREATE TABLE IF NOT EXISTS landing_testimonial (
                        id BIGSERIAL PRIMARY KEY,
                        name VARCHAR(200) NOT NULL,
                        text TEXT NOT NULL,
                        rating INTEGER NOT NULL DEFAULT 5,
                        photo VARCHAR(100) NULL,
                        is_featured BOOLEAN NOT NULL DEFAULT FALSE,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );

                    CREATE TABLE IF NOT EXISTS landing_contactmessage (
                        id BIGSERIAL PRIMARY KEY,
                        full_name VARCHAR(200) NOT NULL,
                        email VARCHAR(254) NOT NULL,
                        phone VARCHAR(50) NOT NULL,
                        message TEXT NOT NULL,
                        is_read BOOLEAN NOT NULL DEFAULT FALSE,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );

                    CREATE TABLE IF NOT EXISTS landing_news (
                        id BIGSERIAL PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        description TEXT NOT NULL,
                        image VARCHAR(100) NOT NULL,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        "order" INTEGER NOT NULL DEFAULT 0,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );

                    CREATE INDEX IF NOT EXISTS landing_service_order_idx ON landing_service ("order");
                    CREATE INDEX IF NOT EXISTS landing_price_category_id_idx ON landing_price (category_id);
                    CREATE INDEX IF NOT EXISTS landing_galleryimage_order_idx ON landing_galleryimage ("order");
                    CREATE INDEX IF NOT EXISTS landing_faq_order_idx ON landing_faq ("order");
                    CREATE INDEX IF NOT EXISTS landing_testimonial_created_at_idx ON landing_testimonial (created_at);
                    CREATE INDEX IF NOT EXISTS landing_contactmessage_created_at_idx ON landing_contactmessage (created_at);
                    CREATE INDEX IF NOT EXISTS landing_news_order_idx ON landing_news ("order");
                    """,
                    reverse_sql="""
                    DROP TABLE IF EXISTS landing_news CASCADE;
                    DROP TABLE IF EXISTS landing_contactmessage CASCADE;
                    DROP TABLE IF EXISTS landing_testimonial CASCADE;
                    DROP TABLE IF EXISTS landing_faq CASCADE;
                    DROP TABLE IF EXISTS landing_galleryimage CASCADE;
                    DROP TABLE IF EXISTS landing_price CASCADE;
                    DROP TABLE IF EXISTS landing_pricecategory CASCADE;
                    DROP TABLE IF EXISTS landing_service CASCADE;
                    DROP TABLE IF EXISTS landing_siteconfiguration CASCADE;
                    """,
                ),
            ],
            state_operations=[
                migrations.CreateModel(
                    name="SiteConfiguration",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("site_name", models.CharField(default="Camping ACA Luj\u00e1n", max_length=200, verbose_name="Nombre del sitio")),
                        ("tagline", models.CharField(default="Un lugar para vos", max_length=500, verbose_name="Eslogan")),
                        ("hero_image", models.ImageField(blank=True, null=True, upload_to="config/", verbose_name="Imagen principal")),
                        ("phone", models.CharField(blank=True, max_length=50, verbose_name="Tel\u00e9fono")),
                        ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                        ("address", models.TextField(blank=True, verbose_name="Direcci\u00f3n")),
                        ("instagram_url", models.URLField(blank=True, verbose_name="Instagram URL")),
                        ("facebook_url", models.URLField(blank=True, verbose_name="Facebook URL")),
                        ("opening_hours", models.TextField(default="Mi\u00e9rcoles a Lunes de 10 a 18 hs", verbose_name="Horarios")),
                        ("special_alert", models.TextField(blank=True, help_text="Ej: PILETA CERRADA", verbose_name="Alerta especial")),
                        ("is_alert_active", models.BooleanField(default=False, verbose_name="Mostrar alerta")),
                    ],
                    options={
                        "verbose_name": "Configuraci\u00f3n del Sitio",
                        "verbose_name_plural": "Configuraci\u00f3n del Sitio",
                    },
                ),
                migrations.CreateModel(
                    name="Service",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("title", models.CharField(max_length=200, verbose_name="T\u00edtulo")),
                        ("icon", models.ImageField(blank=True, null=True, upload_to="services/icons/", verbose_name="Icono (imagen)")),
                        ("description", models.TextField(verbose_name="Descripci\u00f3n")),
                        ("features", models.JSONField(default=list, help_text="Lista de caracter\u00edsticas del servicio", verbose_name="Caracter\u00edsticas")),
                        ("order", models.IntegerField(default=0, verbose_name="Orden")),
                        ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                        ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Creado")),
                        ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Actualizado")),
                    ],
                    options={
                        "verbose_name": "Servicio",
                        "verbose_name_plural": "Servicios",
                        "ordering": ["order", "title"],
                    },
                ),
                migrations.CreateModel(
                    name="PriceCategory",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("name", models.CharField(max_length=100, verbose_name="Nombre")),
                        ("description", models.TextField(blank=True, verbose_name="Descripci\u00f3n")),
                        ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                        ("order", models.IntegerField(default=0, verbose_name="Orden")),
                    ],
                    options={
                        "verbose_name": "Categor\u00eda de Precio",
                        "verbose_name_plural": "Categor\u00edas de Precios",
                        "ordering": ["order", "name"],
                    },
                ),
                migrations.CreateModel(
                    name="GalleryImage",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("title", models.CharField(max_length=200, verbose_name="T\u00edtulo")),
                        ("image", models.ImageField(upload_to="gallery/", verbose_name="Imagen")),
                        ("description", models.TextField(blank=True, verbose_name="Descripci\u00f3n")),
                        ("alt_text", models.CharField(help_text="Para SEO", max_length=200, verbose_name="Texto alternativo")),
                        ("order", models.IntegerField(default=0, verbose_name="Orden")),
                        ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                        ("uploaded_at", models.DateTimeField(auto_now_add=True, verbose_name="Subida")),
                    ],
                    options={
                        "verbose_name": "Imagen de Galer\u00eda",
                        "verbose_name_plural": "Im\u00e1genes de Galer\u00eda",
                        "ordering": ["order", "-uploaded_at"],
                    },
                ),
                migrations.CreateModel(
                    name="FAQ",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("question", models.CharField(max_length=500, verbose_name="Pregunta")),
                        ("answer", models.TextField(verbose_name="Respuesta")),
                        ("order", models.IntegerField(default=0, verbose_name="Orden")),
                        ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                        ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Creado")),
                        ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Actualizado")),
                    ],
                    options={
                        "verbose_name": "Pregunta Frecuente",
                        "verbose_name_plural": "Preguntas Frecuentes",
                        "ordering": ["order", "question"],
                    },
                ),
                migrations.CreateModel(
                    name="Testimonial",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("name", models.CharField(max_length=200, verbose_name="Nombre")),
                        ("text", models.TextField(verbose_name="Testimonio")),
                        ("rating", models.IntegerField(default=5, validators=[MinValueValidator(1)], verbose_name="Calificaci\u00f3n")),
                        ("photo", models.ImageField(blank=True, null=True, upload_to="testimonials/", verbose_name="Foto")),
                        ("is_featured", models.BooleanField(default=False, verbose_name="Destacado")),
                        ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                        ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Creado")),
                    ],
                    options={
                        "verbose_name": "Testimonio",
                        "verbose_name_plural": "Testimonios",
                        "ordering": ["-is_featured", "-created_at"],
                    },
                ),
                migrations.CreateModel(
                    name="ContactMessage",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("full_name", models.CharField(max_length=200, verbose_name="Nombre completo")),
                        ("email", models.EmailField(max_length=254, verbose_name="Email")),
                        ("phone", models.CharField(max_length=50, verbose_name="Tel\u00e9fono")),
                        ("message", models.TextField(verbose_name="Mensaje")),
                        ("is_read", models.BooleanField(default=False, verbose_name="Le\u00eddo")),
                        ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Recibido")),
                    ],
                    options={
                        "verbose_name": "Mensaje de Contacto",
                        "verbose_name_plural": "Mensajes de Contacto",
                        "ordering": ["-created_at"],
                    },
                ),
                migrations.CreateModel(
                    name="News",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("title", models.CharField(max_length=200, verbose_name="T\u00edtulo")),
                        ("description", models.TextField(verbose_name="Descripci\u00f3n")),
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
                migrations.CreateModel(
                    name="Price",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("item_name", models.CharField(max_length=200, verbose_name="Servicio")),
                        ("description", models.TextField(blank=True, verbose_name="Descripci\u00f3n")),
                        ("amount", models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)], verbose_name="Precio")),
                        ("is_free", models.BooleanField(default=False, verbose_name="Gratis")),
                        ("order", models.IntegerField(default=0, verbose_name="Orden")),
                        ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                        ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Actualizado")),
                        ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="prices", to="landing.pricecategory", verbose_name="Categor\u00eda")),
                    ],
                    options={
                        "verbose_name": "Precio",
                        "verbose_name_plural": "Precios",
                        "ordering": ["category", "order", "item_name"],
                    },
                ),
            ],
        ),
    ]
