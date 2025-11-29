import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from legacyApp.models import ControlesPrevios

rut = '16293109-1'
control = ControlesPrevios.objects.filter(paciente_rut=rut).first()

if control:
    llenos = []
    vacios = []
    
    for field in ControlesPrevios._meta.get_fields():
        if hasattr(control, field.name) and field.name != 'id':
            valor = getattr(control, field.name)
            if valor is None or valor == '':
                vacios.append(field.name)
            else:
                llenos.append(field.name)
    
    total = len(llenos) + len(vacios)
    resultado = {
        'rut': rut,
        'total_campos': total,
        'campos_llenos': len(llenos),
        'campos_vacios': len(vacios),
        'porcentaje_completitud': round((len(llenos) / total * 100), 1) if total > 0 else 0,
        'lista_campos_llenos': llenos,
        'lista_campos_vacios': vacios
    }
    
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
else:
    print(json.dumps({'error': f'No se encontro control para RUT {rut}'}, ensure_ascii=False))
