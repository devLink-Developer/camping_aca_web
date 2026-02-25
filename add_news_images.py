#!/usr/bin/env python
"""Script para agregar campos de imágenes de novedades"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("\n🔧 Agregando campos de imágenes de novedades...")

cursor = connection.cursor()

try:
    cursor.execute("ALTER TABLE landing_siteconfiguration ADD COLUMN news_sports_image VARCHAR(100);")
    print("✓ Campo news_sports_image agregado")
except Exception as e:
    print(f"⚠ news_sports_image: {e}")

try:
    cursor.execute("ALTER TABLE landing_siteconfiguration ADD COLUMN news_bikes_image VARCHAR(100);")
    print("✓ Campo news_bikes_image agregado")
except Exception as e:
    print(f"⚠ news_bikes_image: {e}")

print("\n✅ Actualización completada")
