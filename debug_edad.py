import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from gestionApp.models import Paciente

rut = '16293109-1'
try:
    paciente = Paciente.objects.get(persona__Rut=rut)
    print(f"Paciente: {paciente}")
    print(f"Persona: {paciente.persona}")
    print(f"Fecha Nacimiento: {paciente.persona.Fecha_nacimiento} (Type: {type(paciente.persona.Fecha_nacimiento)})")
    print(f"Edad (property): {paciente.edad}")
    print(f"Calcular Edad (method): {paciente.persona.calcular_edad()}")
except Paciente.DoesNotExist:
    print(f"No se encontró paciente con RUT {rut}")
except Exception as e:
    print(f"Error: {e}")
