#!/usr/bin/env python
"""Script para probar la generación de QR en vouchers"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.vouchers.models import Voucher
from django.utils import timezone
from datetime import timedelta

# Crear voucher de prueba
print("\n🔧 Creando voucher de prueba...")
voucher = Voucher.objects.create(
    client_name='Test Cliente QR',
    client_email='test.qr@example.com',
    client_phone='1122334455',
    value=5000,
    description='Voucher de prueba para verificar generación de QR',
    service_type='Estadía de 2 noches',
    validity_days=365
)

print(f"\n✅ Voucher creado exitosamente:")
print(f"   Código: {voucher.voucher_code}")
print(f"   Cliente: {voucher.client_name}")
print(f"   Valor: ${voucher.value}")
print(f"   Estado: {voucher.get_status_display()}")
print(f"   Emisión: {voucher.issue_date.strftime('%d/%m/%Y %H:%M')}")
print(f"   Vencimiento: {voucher.expiration_date.strftime('%d/%m/%Y %H:%M')}")
print(f"   Días de validez: {voucher.validity_days}")

if voucher.qr_code:
    print(f"\n✅ Código QR generado:")
    print(f"   Archivo: {voucher.qr_code.name}")
    print(f"   Ruta completa: {voucher.qr_code.path}")
    print(f"   URL: {voucher.qr_code.url}")
    print(f"   Tamaño: {voucher.qr_code.size} bytes")
else:
    print("\n❌ ERROR: El código QR NO se generó")

print(f"\n📊 Total de vouchers en DB: {Voucher.objects.count()}")
