#!/usr/bin/env python
"""Script para agregar campos al modelo Voucher"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("\n🔧 Agregando nuevos campos a la tabla vouchers_voucher...")

cursor = connection.cursor()

try:
    # Agregar campo voucher_type
    cursor.execute("ALTER TABLE vouchers_voucher ADD COLUMN voucher_type VARCHAR(20) DEFAULT 'monetary';")
    print("✓ Campo voucher_type agregado")
except Exception as e:
    print(f"⚠ voucher_type: {e}")

try:
    # Agregar campo benefit_description
    cursor.execute("ALTER TABLE vouchers_voucher ADD COLUMN benefit_description TEXT;")
    print("✓ Campo benefit_description agregado")
except Exception as e:
    print(f"⚠ benefit_description: {e}")

try:
    # Hacer que value sea opcional
    cursor.execute("ALTER TABLE vouchers_voucher ALTER COLUMN value DROP NOT NULL;")
    print("✓ Campo value ahora es opcional")
except Exception as e:
    print(f"⚠ value: {e}")

print("\n✅ Actualización de base de datos completada")
