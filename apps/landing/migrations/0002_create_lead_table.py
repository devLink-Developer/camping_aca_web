from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('landing', '0001_customerprofile'),
        ('vouchers', '0001_initial'),
    ]

    operations = [
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
    ]
