#!/usr/bin/env python
# Script para analizar campos del modelo ControlesPrevios

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from legacyApp.models import ControlesPrevios

# Buscar control para el RUT especificado
rut_buscar = '16293109-1'
print(f"\n{'='*60}")
print(f"ANÁLISIS DE CAMPOS PARA RUT: {rut_buscar}")
print(f"{'='*60}\n")

# Verificar si existe el control
controles = ControlesPrevios.objects.filter(paciente_rut=rut_buscar)
print(f"Total de controles encontrados: {controles.count()}\n")

if controles.exists():
    # Tomar el primer control
    control = controles.first()
    
    # Analizar campos
    campos_llenos = []
    campos_vacios = []
    
    for field in ControlesPrevios._meta.get_fields():
        if hasattr(control, field.name) and field.name != 'id':
            valor = getattr(control, field.name)
            if valor is None or valor == '':
                campos_vacios.append(field.name)
            else:
                campos_llenos.append((field.name, valor))
    
    total = len(campos_llenos) + len(campos_vacios)
    porcentaje = (len(campos_llenos) / total * 100) if total > 0 else 0
    
    print(f"RESUMEN:")
    print(f"   Total de campos: {total}")
    print(f"   Campos llenos: {len(campos_llenos)}")
    print(f"   Campos vacios: {len(campos_vacios)}")
    print(f"   Completitud: {porcentaje:.1f}%\n")
    
    print(f"\n{'='*60}")
    print(f"CAMPOS CON DATOS ({len(campos_llenos)}):")
    print(f"{'='*60}\n")
    for nombre, valor in campos_llenos:
        # Truncar valores muy largos
        valor_str = str(valor)
        if len(valor_str) > 60:
            valor_str = valor_str[:57] + "..."
        print(f"  • {nombre}: {valor_str}")
    
    print(f"\n{'='*60}")
    print(f"CAMPOS VACÍOS ({len(campos_vacios)}):")
    print(f"{'='*60}\n")
    for nombre in campos_vacios:
        print(f"  • {nombre}")
    
else:
    print(f"No se encontraron controles para el RUT: {rut_buscar}\n")
    print("RUTs disponibles en la base de datos:")
    ruts = ControlesPrevios.objects.values_list('paciente_rut', flat=True).distinct()
    for rut in ruts:
        count = ControlesPrevios.objects.filter(paciente_rut=rut).count()
        print(f"  • {rut}: {count} control(es)")

print(f"\n{'='*60}\n")
