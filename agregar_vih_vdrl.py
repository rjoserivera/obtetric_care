import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from legacyApp.models import ControlesPrevios

# Actualizar el control #1 con datos de VIH y VDRL
try:
    control = ControlesPrevios.objects.using("legacy").get(id=1)

    # Agregar datos de VIH
    control.vih_resultado = "NEGATIVO"
    control.vih_fecha_toma = date(2023, 1, 10)
    control.vih_orden = 1  # Corregido: debe ser un entero

    # Agregar datos de VDRL
    control.vdrl_resultado = "NO REACTIVO"
    control.vdrl_fecha = date(2023, 1, 10)

    control.save(using="legacy")

    print(f"✅ Control #{control.id} actualizado exitosamente:")
    print(f"   VIH: {control.vih_resultado} ({control.vih_fecha_toma})")
    print(f"   VDRL: {control.vdrl_resultado} ({control.vdrl_fecha})")

except Exception as e:
    print(f"❌ Error al actualizar el control: {e}")
