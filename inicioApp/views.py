"""
Vistas de la aplicación de inicio
"""
from django.shortcuts import render, redirect


def home(request):
    """
    Splash screen / Landing page pública
    Muestra la página de bienvenida para todos los usuarios
    """
    # Comentado: redirección automática desactivada para mostrar página de bienvenida
    # if request.user.is_authenticated:
    #     # Redirigir según el rol
    #     if request.user.is_superuser:
    #         return redirect('admin:index')
    #     elif request.user.groups.filter(name='Administrador').exists():
    #         return redirect('authentication:dashboard_admin')
    #     elif request.user.groups.filter(name='Médico').exists():
    #         return redirect('authentication:dashboard_medico')
    #     elif request.user.groups.filter(name='Matrona').exists():
    #         return redirect('authentication:dashboard_matrona')
    #     elif request.user.groups.filter(name='TENS').exists():
    #         return redirect('authentication:dashboard_tens')
    
    # Mostrar página de bienvenida
    return render(request, 'inicio/home.html')