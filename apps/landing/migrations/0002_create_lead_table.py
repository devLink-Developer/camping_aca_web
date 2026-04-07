import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0001_customerprofile"),
        ("vouchers", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                    CREATE TABLE IF NOT EXISTS landing_lead (
                        id BIGSERIAL PRIMARY KEY,
                        full_name VARCHAR(200) NOT NULL,
                        email VARCHAR(254) NOT NULL UNIQUE,
                        phone VARCHAR(50) NOT NULL,
                        dni VARCHAR(20) NOT NULL DEFAULT '',
                        birth_date DATE NOT NULL,
                        accepts_marketing BOOLEAN NOT NULL DEFAULT TRUE,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        ip_address INET NULL,
                        source VARCHAR(50) NOT NULL DEFAULT 'qr_birthday',
                        birthday_voucher_id BIGINT NULL,
                        voucher_sent BOOLEAN NOT NULL DEFAULT FALSE,
                        voucher_sent_date TIMESTAMPTZ NULL,
                        notes TEXT NOT NULL DEFAULT '',
                        CONSTRAINT landing_lead_birthday_voucher_id_fk
                            FOREIGN KEY (birthday_voucher_id)
                            REFERENCES vouchers_voucher (id)
                            ON DELETE SET NULL
                    );

                    CREATE INDEX IF NOT EXISTS landing_lead_birth_date_idx
                        ON landing_lead (birth_date);

                    CREATE INDEX IF NOT EXISTS landing_lead_voucher_sent_idx
                        ON landing_lead (voucher_sent);
                    """,
                    reverse_sql="""
                    DROP TABLE IF EXISTS landing_lead CASCADE;
                    """,
                ),
            ],
            state_operations=[
                migrations.CreateModel(
                    name="Lead",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("full_name", models.CharField(max_length=200, verbose_name="Nombre Completo")),
                        ("email", models.EmailField(max_length=254, unique=True, verbose_name="Email")),
                        ("phone", models.CharField(max_length=50, verbose_name="Tel\u00e9fono")),
                        ("dni", models.CharField(blank=True, max_length=20, verbose_name="DNI")),
                        ("birth_date", models.DateField(verbose_name="Fecha de Cumplea\u00f1os")),
                        ("accepts_marketing", models.BooleanField(default=True, help_text="Acepta recibir promociones y ofertas", verbose_name="Acepta Marketing")),
                        ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Registrado")),
                        ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Actualizado")),
                        ("ip_address", models.GenericIPAddressField(blank=True, null=True, verbose_name="IP")),
                        ("source", models.CharField(default="qr_birthday", help_text="qr_birthday, web_form, etc", max_length=50, verbose_name="Fuente")),
                        ("voucher_sent", models.BooleanField(default=False, verbose_name="Voucher Enviado")),
                        ("voucher_sent_date", models.DateTimeField(blank=True, null=True, verbose_name="Fecha Env\u00edo Voucher")),
                        ("notes", models.TextField(blank=True, verbose_name="Notas")),
                        ("birthday_voucher", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="lead", to="vouchers.voucher", verbose_name="Voucher de Cumplea\u00f1os")),
                    ],
                    options={
                        "verbose_name": "Lead",
                        "verbose_name_plural": "Leads",
                        "ordering": ["-created_at"],
                    },
                ),
            ],
        ),
    ]
