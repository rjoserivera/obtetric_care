import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from legacyApp.models import ControlesPrevios

try:
    # Intentar consultar la base de datos legacy
    total = ControlesPrevios.objects.using("legacy").count()
    print(f"Total de controles en DB legacy: {total}")
    
    # Buscar controles del RUT específico
    rut = '16293109-1'
    controles = ControlesPrevios.objects.using("legacy").filter(paciente_rut=rut)
    print(f"\nControles para RUT {rut}: {controles.count()}")
    
    if controles.exists():
        ctrl = controles.first()
        print(f"\nPrimer control:")
        print(f"  - ID: {ctrl.id}")
        print(f"  - Fecha: {ctrl.fecha_control}")
        print(f"  - Semanas: {ctrl.semanas_gestacion}+{ctrl.dias_gestacion}")
        print(f"  - Profesional: {ctrl.profesional_nombre}")
        print("\n✅ Conexión a base de datos legacy funcionando correctamente")
    else:
        print(f"\n⚠️ No se encontraron controles para el RUT {rut}")
        
except Exception as e:
    print(f"\n❌ ERROR al conectar con la base de datos legacy:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
