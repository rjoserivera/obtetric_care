"""
Script para crear y configurar los grupos de Django del sistema obstétrico
Crea los grupos: Administrador, Médico, Matrona, TENS
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# ============================================
# DEFINICIÓN DE GRUPOS Y PERMISOS
# ============================================

GRUPOS_CONFIG = {
    'Administrador': {
        'descripcion': 'Acceso administrativo completo al sistema',
        'permisos': [
            # Permisos de gestión de usuarios
            'auth.add_user',
            'auth.change_user',
            'auth.view_user',
            # Permisos de gestión de grupos
            'auth.add_group',
            'auth.change_group',
            'auth.view_group',
            # Permisos de personas y pacientes
            'gestionApp.add_persona',
            'gestionApp.change_persona',
            'gestionApp.delete_persona',
            'gestionApp.view_persona',
            'gestionApp.add_paciente',
            'gestionApp.change_paciente',
            'gestionApp.view_paciente',
            # Permisos de médicos, matronas y TENS
            'gestionApp.add_medico',
            'gestionApp.change_medico',
            'gestionApp.view_medico',
            'gestionApp.add_matrona',
            'gestionApp.change_matrona',
            'gestionApp.view_matrona',
            'gestionApp.add_tens',
            'gestionApp.change_tens',
            'gestionApp.view_tens',
        ]
    },
    'Médico': {
        'descripcion': 'Acceso para médicos obstetras',
        'permisos': [
            # Permisos de pacientes (solo lectura y modificación)
            'gestionApp.view_persona',
            'gestionApp.view_paciente',
            'gestionApp.change_paciente',
            # Permisos de patologías
            'medicoApp.add_patologias',
            'medicoApp.change_patologias',
            'medicoApp.delete_patologias',
            'medicoApp.view_patologias',
            # Permisos de diagnósticos
            'medicoApp.add_diagnostico',
            'medicoApp.change_diagnostico',
            'medicoApp.view_diagnostico',
        ]
    },
    'Matrona': {
        'descripcion': 'Acceso para matronas',
        'permisos': [
            # Permisos de pacientes
            'gestionApp.view_persona',
            'gestionApp.view_paciente',
            'gestionApp.change_paciente',
            # Permisos de fichas obstétricas
            'matronaApp.add_fichaobstetrica',
            'matronaApp.change_fichaobstetrica',
            'matronaApp.view_fichaobstetrica',
            # Permisos de ingreso de pacientes
            'matronaApp.add_ingresopaciente',
            'matronaApp.change_ingresopaciente',
            'matronaApp.view_ingresopaciente',
            # Permisos de medicamentos
            'matronaApp.add_medicamentoficha',
            'matronaApp.change_medicamentoficha',
            'matronaApp.view_medicamentoficha',
            # Permisos de administración de medicamentos
            'matronaApp.add_administracionmedicamento',
            'matronaApp.change_administracionmedicamento',
            'matronaApp.view_administracionmedicamento',
        ]
    },
    'TENS': {
        'descripcion': 'Acceso para técnicos de enfermería',
        'permisos': [
            # Permisos de pacientes (solo lectura)
            'gestionApp.view_persona',
            'gestionApp.view_paciente',
            # Permisos de administración de medicamentos
            'matronaApp.add_administracionmedicamento',
            'matronaApp.change_administracionmedicamento',
            'matronaApp.view_administracionmedicamento',
            # Permisos de visualización de fichas
            'matronaApp.view_fichaobstetrica',
            'matronaApp.view_medicamentoficha',
        ]
    }
}

# ============================================
# CREAR GRUPOS
# ============================================

print("=" * 70)
print("CREACION Y CONFIGURACION DE GRUPOS DEL SISTEMA")
print("=" * 70)

grupos_creados = []
grupos_actualizados = []

for nombre_grupo, config in GRUPOS_CONFIG.items():
    # Crear o obtener el grupo
    grupo, created = Group.objects.get_or_create(name=nombre_grupo)
    
    if created:
        grupos_creados.append(nombre_grupo)
        print(f"\n[OK] Grupo creado: {nombre_grupo}")
    else:
        grupos_actualizados.append(nombre_grupo)
        print(f"\n[!] Grupo ya existe: {nombre_grupo}")
    
    print(f"    Descripcion: {config['descripcion']}")
    
    # Limpiar permisos existentes
    grupo.permissions.clear()
    
    # Asignar permisos
    permisos_asignados = 0
    permisos_no_encontrados = []
    
    for permiso_str in config['permisos']:
        try:
            app_label, codename = permiso_str.split('.')
            permiso = Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename
            )
            grupo.permissions.add(permiso)
            permisos_asignados += 1
        except Permission.DoesNotExist:
            permisos_no_encontrados.append(permiso_str)
        except Exception as e:
            print(f"    [ERROR] Error al asignar permiso {permiso_str}: {e}")
    
    print(f"    Permisos asignados: {permisos_asignados}")
    
    if permisos_no_encontrados:
        print(f"    [!] Permisos no encontrados: {len(permisos_no_encontrados)}")
        for p in permisos_no_encontrados[:5]:  # Mostrar solo los primeros 5
            print(f"        - {p}")
        if len(permisos_no_encontrados) > 5:
            print(f"        ... y {len(permisos_no_encontrados) - 5} mas")

# ============================================
# RESUMEN
# ============================================

print("\n" + "=" * 70)
print("RESUMEN DE GRUPOS")
print("=" * 70)

if grupos_creados:
    print(f"\n[OK] Grupos creados: {len(grupos_creados)}")
    for g in grupos_creados:
        print(f"    - {g}")

if grupos_actualizados:
    print(f"\n[!] Grupos actualizados: {len(grupos_actualizados)}")
    for g in grupos_actualizados:
        print(f"    - {g}")

print(f"\n[OK] Total de grupos en el sistema: {Group.objects.count()}")

# Mostrar todos los grupos con su cantidad de permisos
print("\n" + "-" * 70)
print("GRUPOS Y PERMISOS CONFIGURADOS:")
print("-" * 70)

for grupo in Group.objects.all().order_by('name'):
    permisos_count = grupo.permissions.count()
    usuarios_count = grupo.user_set.count()
    print(f"\n{grupo.name}")
    print(f"  Permisos: {permisos_count}")
    print(f"  Usuarios: {usuarios_count}")
    if usuarios_count > 0:
        usuarios = [u.username for u in grupo.user_set.all()]
        print(f"  Miembros: {', '.join(usuarios)}")

print("\n" + "=" * 70)
print("[OK] Configuracion de grupos completada")
print("=" * 70)
