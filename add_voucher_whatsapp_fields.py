#!/usr/bin/env python
"""Script para agregar campos de envío por WhatsApp al modelo Voucher.

Este proyecto viene manejando algunos cambios de schema vía scripts SQL/Django (ver update_vouchers.py).
Este script agrega:
- sent_whatsapp (BOOLEAN, default FALSE)
- sent_whatsapp_date (TIMESTAMP, nullable)

Es idempotente: si la columna ya existe, lo informa y sigue.
"""

import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection


def main() -> None:
    print("\n🔧 Agregando campos WhatsApp a la tabla vouchers_voucher...")
    cursor = connection.cursor()

    try:
        cursor.execute("ALTER TABLE vouchers_voucher ADD COLUMN sent_whatsapp BOOLEAN DEFAULT FALSE;")
        print("✓ Campo sent_whatsapp agregado")
    except Exception as e:
        print(f"⚠ sent_whatsapp: {e}")

    try:
        cursor.execute("ALTER TABLE vouchers_voucher ADD COLUMN sent_whatsapp_date TIMESTAMP;")
        print("✓ Campo sent_whatsapp_date agregado")
    except Exception as e:
        print(f"⚠ sent_whatsapp_date: {e}")

    try:
        cursor.execute("UPDATE vouchers_voucher SET sent_whatsapp = FALSE WHERE sent_whatsapp IS NULL;")
        print("✓ Campo sent_whatsapp inicializado en FALSE")
    except Exception as e:
        print(f"⚠ Inicializar sent_whatsapp: {e}")

    print("\n✅ Actualización WhatsApp completada")


if __name__ == '__main__':
    main()
