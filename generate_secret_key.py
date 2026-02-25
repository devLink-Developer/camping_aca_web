#!/usr/bin/env python
"""
Script para generar una SECRET_KEY segura para Django
Ejecutar: python generate_secret_key.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\n" + "="*60)
    print("🔐 SECRET_KEY generada para Django")
    print("="*60)
    print(f"\nSECRET_KEY={secret_key}")
    print("\n⚠️  Copia esta clave en tu archivo .env")
    print("⚠️  NO compartas esta clave con nadie")
    print("⚠️  Guarda una copia segura como backup")
    print("="*60 + "\n")
