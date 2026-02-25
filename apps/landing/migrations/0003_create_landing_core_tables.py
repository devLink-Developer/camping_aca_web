from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0002_create_lead_table"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            -- Core content tables for Landing app.
            -- These tables are required at runtime but weren't covered by earlier migrations.

            CREATE TABLE IF NOT EXISTS landing_siteconfiguration (
                id BIGSERIAL PRIMARY KEY,
                site_name VARCHAR(200) NOT NULL DEFAULT 'Camping ACA Luján',
                tagline VARCHAR(500) NOT NULL DEFAULT 'Un lugar para vos',
                hero_image VARCHAR(100) NULL,
                phone VARCHAR(50) NOT NULL DEFAULT '',
                email VARCHAR(254) NOT NULL DEFAULT '',
                address TEXT NOT NULL DEFAULT '',
                instagram_url VARCHAR(200) NOT NULL DEFAULT '',
                facebook_url VARCHAR(200) NOT NULL DEFAULT '',
                opening_hours TEXT NOT NULL DEFAULT 'Miércoles a Lunes de 10 a 18 hs',
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
    ]
