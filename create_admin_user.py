"""
Script para crear un usuario con rol de Administrador
Incluye: User de Django + Grupo 'Administrador'
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.contrib.auth.models import User, Group

# ============================================
# DATOS DEL USUARIO ADMINISTRADOR
# ============================================
# Datos de autenticacion
username = 'administrador'
email = 'administrador@hospital.cl'
password = 'admin123'  # Cambiar despues del primer inicio de sesion
first_name = 'Carlos'
last_name = 'Rodriguez Martinez'

# ============================================
# CREAR USUARIO ADMINISTRADOR
# ============================================

print("=" * 60)
print("CREACION DE USUARIO ADMINISTRADOR")
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
        first_name=first_name,
        last_name=last_name
    )
    # Marcar como staff para que pueda acceder al admin de Django
    user.is_staff = True
    user.save()
    print(f"\n[OK] Usuario Django creado: {username}")

# 2. Asignar al grupo 'Administrador'
grupo_admin, created = Group.objects.get_or_create(name='Administrador')
if not user.groups.filter(name='Administrador').exists():
    user.groups.add(grupo_admin)
    print(f"[OK] Usuario agregado al grupo 'Administrador'")
else:
    print(f"[!] Usuario ya pertenece al grupo 'Administrador'")

# Asegurar que tiene permisos de staff
if not user.is_staff:
    user.is_staff = True
    user.save()
    print(f"[OK] Usuario marcado como staff")

# ============================================
# RESUMEN
# ============================================
print("\n" + "=" * 60)
print("RESUMEN - USUARIO ADMINISTRADOR CREADO")
print("=" * 60)
print(f"\nCREDENCIALES DE ACCESO:")
print(f"  Usuario:     {username}")
print(f"  Contrasena:  {password}")
print(f"  Email:       {email}")
print(f"\nDATOS PERSONALES:")
print(f"  Nombre:      {user.first_name} {user.last_name}")
print(f"\nPERMISOS:")
print(f"  Es staff:    {user.is_staff}")
print(f"  Grupos:      {', '.join([g.name for g in user.groups.all()])}")
print(f"\nACCESO AL SISTEMA:")
print(f"  URL Login:       http://127.0.0.1:8000/login/")
print(f"  Dashboard Admin: http://127.0.0.1:8000/dashboard/admin/")
print(f"  Panel Django:    http://127.0.0.1:8000/admin/")
print(f"\n[!] IMPORTANTE: Cambia la contrasena despues del primer inicio de sesion")
print("=" * 60)
