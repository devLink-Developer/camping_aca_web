#!/usr/bin/env python
"""Script para actualizar campos de vouchers"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("\n🔧 Actualizando tabla de vouchers...")

cursor = connection.cursor()

# 1. Actualizar valores existentes de voucher_type
try:
    cursor.execute("UPDATE vouchers_voucher SET voucher_type = 'amount' WHERE voucher_type = 'monetary';")
    print("✓ Vouchers 'monetary' convertidos a 'amount'")
except Exception as e:
    print(f"⚠ Actualizar monetary→amount: {e}")

try:
    cursor.execute("UPDATE vouchers_voucher SET voucher_type = 'free_text' WHERE voucher_type = 'benefit';")
    print("✓ Vouchers 'benefit' convertidos a 'free_text'")
except Exception as e:
    print(f"⚠ Actualizar benefit→free_text: {e}")

# 2. Agregar campo percentage
try:
    cursor.execute("ALTER TABLE vouchers_voucher ADD COLUMN percentage DECIMAL(5,2);")
    print("✓ Campo percentage agregado")
except Exception as e:
    print(f"⚠ percentage: {e}")

# 3. Agregar campos de envío
try:
    cursor.execute("ALTER TABLE vouchers_voucher ADD COLUMN sent BOOLEAN DEFAULT FALSE;")
    print("✓ Campo sent agregado")
except Exception as e:
    print(f"⚠ sent: {e}")

try:
    cursor.execute("ALTER TABLE vouchers_voucher ADD COLUMN sent_date TIMESTAMP;")
    print("✓ Campo sent_date agregado")
except Exception as e:
    print(f"⚠ sent_date: {e}")

# 4. Actualizar valores por defecto para vouchers existentes
try:
    cursor.execute("UPDATE vouchers_voucher SET sent = FALSE WHERE sent IS NULL;")
    print("✓ Campo sent inicializado en FALSE")
except Exception as e:
    print(f"⚠ Inicializar sent: {e}")

print("\n✅ Actualización de vouchers completada")
print("\n📊 Tipos de voucher disponibles:")
print("   • amount - Monto Fijo ($5000)")
print("   • percentage - Porcentaje de Descuento (50%)")
print("   • free_text - Texto Libre/Beneficio (2 horas de Paddle)")
