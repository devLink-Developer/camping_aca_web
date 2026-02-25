#!/usr/bin/env python
"""Script para probar vouchers por monto y por beneficio"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.vouchers.models import Voucher
from django.utils import timezone
from datetime import timedelta

print("\n🎫 Creando vouchers de prueba...\n")

# 1. Voucher por MONTO
print("1️⃣ VOUCHER POR MONTO")
voucher_monto = Voucher.objects.create(
    client_name='Juan Pérez',
    client_email='juan.perez@example.com',
    client_phone='1122334455',
    client_id='DNI 35123456',
    voucher_type='monetary',
    value=5000,
    description='Vale por $5000 para usar en cualquier servicio',
    service_type='General',
    validity_days=365
)
print(f"   ✓ Código: {voucher_monto.voucher_code}")
print(f"   ✓ Tipo: {voucher_monto.get_voucher_type_display()}")
print(f"   ✓ Valor: ${voucher_monto.value}")
print(f"   ✓ QR generado: {'Sí' if voucher_monto.qr_code else 'No'}")

# 2. Voucher por BENEFICIO - Paddle
print("\n2️⃣ VOUCHER POR BENEFICIO (Paddle)")
voucher_paddle = Voucher.objects.create(
    client_name='María González',
    client_email='maria.gonzalez@example.com',
    client_phone='1133445566',
    client_id='DNI 28987654',
    voucher_type='benefit',
    benefit_description='2 horas de Paddle para 2 personas',
    description='Incluye equipo completo y chaleco salvavidas',
    service_type='Actividades Acuáticas',
    validity_days=180
)
print(f"   ✓ Código: {voucher_paddle.voucher_code}")
print(f"   ✓ Tipo: {voucher_paddle.get_voucher_type_display()}")
print(f"   ✓ Beneficio: {voucher_paddle.benefit_description}")
print(f"   ✓ QR generado: {'Sí' if voucher_paddle.qr_code else 'No'}")

# 3. Voucher por BENEFICIO - Descuento
print("\n3️⃣ VOUCHER POR BENEFICIO (Descuento)")
voucher_descuento = Voucher.objects.create(
    client_name='Carlos Rodríguez',
    client_email='carlos.rodriguez@example.com',
    client_phone='1144556677',
    voucher_type='benefit',
    benefit_description='50% de descuento en próximo ingreso al predio',
    description='Válido para una estadía de hasta 3 días',
    service_type='Descuento',
    validity_days=90
)
print(f"   ✓ Código: {voucher_descuento.voucher_code}")
print(f"   ✓ Tipo: {voucher_descuento.get_voucher_type_display()}")
print(f"   ✓ Beneficio: {voucher_descuento.benefit_description}")
print(f"   ✓ QR generado: {'Sí' if voucher_descuento.qr_code else 'No'}")

print(f"\n📊 Total de vouchers en sistema: {Voucher.objects.count()}")
print(f"   • Por monto: {Voucher.objects.filter(voucher_type='monetary').count()}")
print(f"   • Por beneficio: {Voucher.objects.filter(voucher_type='benefit').count()}")

print("\n✅ Pruebas completadas exitosamente!")
