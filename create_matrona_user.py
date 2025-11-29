"""
Script para crear un usuario con rol de Matrona
Incluye: User de Django + Persona + Matrona + Grupo 'Matrona'
"""
import os
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.contrib.auth.models import User, Group
from gestionApp.models import Persona, Matrona
from utilidad.rut_validator import generar_rut_aleatorio, RutValidator

# ============================================
# DATOS DEL USUARIO MATRONA
# ============================================
# Datos de autenticacion
username = 'matrona1'
email = 'matrona1@hospital.cl'
password = 'matrona123'  # Cambiar despues del primer inicio de sesion

# Generar RUT valido aleatorio
rut_generado = generar_rut_aleatorio()
# Normalizar al formato de base de datos (sin puntos, con guion)
rut = RutValidator.normalizar(rut_generado)

# Datos personales
nombre = 'Maria'
apellido_paterno = 'Gonzalez'
apellido_materno = 'Lopez'
fecha_nacimiento = date(1985, 5, 15)
sexo = 'Femenino'
telefono = '+56912345678'
direccion = 'Av. Principal 123, Chillan'
email_personal = 'maria.gonzalez@email.com'

# Datos profesionales de matrona
especialidad = 'Atencion del Parto'  # Opciones: 'Atencion del Parto', 'Control Prenatal', 'Neonatologia'
registro_medico = 'MAT-2024-001'
anos_experiencia = 8
turno = 'Manana'  # Opciones: 'Manana', 'Tarde', 'Noche'

# ============================================
# CREAR USUARIO Y MATRONA
# ============================================

print("=" * 60)
print("CREACION DE USUARIO MATRONA")
print("=" * 60)

# 1. Verificar si el usuario ya existe
if User.objects.filter(username=username).exists():
    print(f"\n[!] El usuario '{username}' ya existe.")
    user = User.objects.get(username=username)
    print(f"    Email: {user.email}")
    print(f"    Activo: {user.is_active}")
else:
    # Crear usuario de Django
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=nombre,
        last_name=f"{apellido_paterno} {apellido_materno}"
    )
    print(f"\n[OK] Usuario Django creado: {username}")

# 2. Asignar al grupo 'Matrona'
grupo_matrona, created = Group.objects.get_or_create(name='Matrona')
if not user.groups.filter(name='Matrona').exists():
    user.groups.add(grupo_matrona)
    print(f"[OK] Usuario agregado al grupo 'Matrona'")
else:
    print(f"[!] Usuario ya pertenece al grupo 'Matrona'")

# 3. Verificar si la Persona ya existe
if Persona.objects.filter(Rut=rut).exists():
    print(f"\n[!] La persona con RUT {rut} ya existe.")
    persona = Persona.objects.get(Rut=rut)
else:
    # Crear Persona
    persona = Persona.objects.create(
        Rut=rut,
        Nombre=nombre,
        Apellido_Paterno=apellido_paterno,
        Apellido_Materno=apellido_materno,
        Fecha_nacimiento=fecha_nacimiento,
        Sexo=sexo,
        Telefono=telefono,
        Direccion=direccion,
        Email=email_personal,
        Activo=True
    )
    print(f"[OK] Persona creada: {persona}")

# 4. Verificar si la Matrona ya existe
if Matrona.objects.filter(persona=persona).exists():
    print(f"\n[!] Ya existe un registro de Matrona para esta persona.")
    matrona = Matrona.objects.get(persona=persona)
else:
    # Crear Matrona
    matrona = Matrona.objects.create(
        persona=persona,
        Especialidad=especialidad,
        Registro_medico=registro_medico,
        Años_experiencia=anos_experiencia,
        Turno=turno,
        Activo=True
    )
    print(f"[OK] Matrona creada: {matrona}")

# ============================================
# RESUMEN
# ============================================
print("\n" + "=" * 60)
print("RESUMEN - USUARIO MATRONA CREADO")
print("=" * 60)
print(f"\nCREDENCIALES DE ACCESO:")
print(f"  Usuario:     {username}")
print(f"  Contrasena:  {password}")
print(f"  Email:       {email}")
print(f"\nDATOS PERSONALES:")
print(f"  Nombre:      {persona.Nombre} {persona.Apellido_Paterno} {persona.Apellido_Materno}")
print(f"  RUT:         {persona.Rut}")
print(f"  Telefono:    {persona.Telefono}")
print(f"\nDATOS PROFESIONALES:")
print(f"  Especialidad:       {matrona.Especialidad}")
print(f"  Registro Medico:    {matrona.Registro_medico}")
print(f"  Anos Experiencia:   {matrona.Años_experiencia}")
print(f"  Turno:              {matrona.Turno}")
print(f"\nACCESO AL SISTEMA:")
print(f"  URL:         http://127.0.0.1:8000/login/")
print(f"  Dashboard:   http://127.0.0.1:8000/dashboard/matrona/")
print(f"\n[!] IMPORTANTE: Cambia la contrasena despues del primer inicio de sesion")
print("=" * 60)
