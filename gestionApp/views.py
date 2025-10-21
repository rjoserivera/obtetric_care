from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .forms.Gestion_form import PersonaForm, PacienteForm, MedicoForm, MatronaForm, TensForm
from .models import Persona, Medico, Matrona, Tens
from matronaApp.models import Paciente



# ============================================
# VISTAS DE LISTA Y DETALLE
# ============================================

class PersonaListView(ListView):
    """Lista de todas las personas registradas"""
    model = Persona
    template_name = 'Gestion/Data/persona_list.html'
    context_object_name = 'personas'
    
    def get_queryset(self):
        return Persona.objects.filter(Activo=True).order_by('-id')


class PersonaDetailView(DetailView):
    """Detalle de una persona específica"""
    model = Persona
    template_name = 'Gestion/Data/persona_detail.html'
    context_object_name = 'persona'


# ============================================
# FORMULARIOS DE REGISTRO
# ============================================

def agregar_persona(request):
    """Registrar una nueva persona (datos básicos)"""
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Persona registrada correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PersonaForm()
    
    return render(request, 'Gestion/Formularios/registrar_persona.html', {'form': form})


def agregar_paciente(request):
    """Registrar un paciente (vinculado a una persona existente)"""
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente registrado correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PacienteForm()
    
    return render(request, 'Gestion/Formularios/paciente_form.html', {'form': form})


def agregar_medico(request):
    """Registrar un médico (vinculado a una persona existente)"""
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico registrado correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = MedicoForm()
    
    return render(request, 'Gestion/Formularios/registrar_medico.html', {'form': form})


def agregar_matrona(request):
    """Registrar una matrona (vinculada a una persona existente)"""
    if request.method == 'POST':
        form = MatronaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matrona registrada correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = MatronaForm()
    
    return render(request, 'Gestion/Formularios/registrar_matrona.html', {'form': form})


def agregar_tens(request):
    """Registrar un TENS (vinculado a una persona existente)"""
    if request.method == 'POST':
        form = TensForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "TENS registrado correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = TensForm()
    
    return render(request, 'Gestion/Formularios/registrar_tens.html', {'form': form})


# ============================================
# API REST (AJAX)
# ============================================

def buscar_persona_api(request):
    """Buscar persona por RUT vía AJAX (retorna JSON)"""
    rut = request.GET.get('rut', '').strip()
    
    if not rut:
        return JsonResponse({'encontrado': False, 'mensaje': 'RUT no proporcionado'})
    
    try:
        from utilidad.rut_validator import normalizar_rut
        rut_normalizado = normalizar_rut(rut)
        
        persona = Persona.objects.filter(Rut=rut_normalizado, Activo=True).first()
        
        if persona:
            return JsonResponse({
                'encontrado': True,
                'persona': {
                    'id': persona.id,
                    'rut': persona.Rut,
                    'nombre': persona.Nombre,
                    'apellido': persona.Apellido,
                    'nombre_completo': f"{persona.Nombre} {persona.Apellido}",
                    'sexo': persona.Sexo,
                    'fecha_nacimiento': persona.Fecha_nacimiento.strftime('%d/%m/%Y'),
                    'telefono': persona.Telefono or 'No registrado',
                    'email': persona.Email or 'No registrado',
                    'direccion': persona.Direccion or 'No registrada',
                }
            })
        else:
            return JsonResponse({
                'encontrado': False,
                'mensaje': 'No se encontró una persona con ese RUT'
            })
    
    except Exception as e:
        return JsonResponse({
            'encontrado': False,
            'mensaje': f'Error al buscar: {str(e)}'
        }, status=400)
    

    # AGREGAR ESTAS FUNCIONES AL FINAL DE gestionApp/views.py

# ============================================
# GESTIÓN DE ROLES
# ============================================

def gestionar_roles_persona(request, pk):
    """Vista para gestionar los roles de una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    # Verificar roles actuales
    roles_actuales = {
        'es_paciente': hasattr(persona, 'paciente'),
        'es_medico': hasattr(persona, 'medico'),
        'es_matrona': hasattr(persona, 'matrona'),
        'es_tens': hasattr(persona, 'tens'),
    }
    
    context = {
        'persona': persona,
        'roles': roles_actuales,
    }
    
    return render(request, 'Gestion/Formularios/gestionar_roles.html', context)


def asignar_rol_paciente(request, pk):
    """Asignar rol de Paciente a una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    # Verificar si ya es paciente
    if hasattr(persona, 'paciente'):
        messages.warning(request, "⚠️ Esta persona ya tiene el rol de Paciente.")
        return redirect('gestion:gestionar_roles', pk=pk)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        # Pre-llenar el RUT
        request.POST = request.POST.copy()
        request.POST['rut_persona'] = persona.Rut
        form = PacienteForm(request.POST)
        
        if form.is_valid():
            try:
                paciente = form.save()
                messages.success(request, f"✅ Rol de Paciente asignado exitosamente a {persona.Nombre} {persona.Apellido_Paterno}.")
                return redirect('gestion:gestionar_roles', pk=pk)
            except Exception as e:
                messages.error(request, f"❌ Error: {str(e)}")
    else:
        # Pre-cargar el formulario con el RUT de la persona
        form = PacienteForm(initial={'rut_persona': persona.Rut})
    
    return render(request, 'Gestion/Formularios/asignar_rol.html', {
        'form': form,
        'persona': persona,
        'rol_nombre': 'Paciente'
    })


def asignar_rol_medico(request, pk):
    """Asignar rol de Médico a una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if hasattr(persona, 'medico'):
        messages.warning(request, "⚠️ Esta persona ya tiene el rol de Médico.")
        return redirect('gestion:gestionar_roles', pk=pk)
    
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['rut_persona'] = persona.Rut
        form = MedicoForm(request.POST)
        
        if form.is_valid():
            try:
                medico = form.save()
                messages.success(request, f"✅ Rol de Médico asignado exitosamente.")
                return redirect('gestion:gestionar_roles', pk=pk)
            except Exception as e:
                messages.error(request, f"❌ Error: {str(e)}")
    else:
        form = MedicoForm(initial={'rut_persona': persona.Rut})
    
    return render(request, 'Gestion/Formularios/asignar_rol.html', {
        'form': form,
        'persona': persona,
        'rol_nombre': 'Médico'
    })


def asignar_rol_matrona(request, pk):
    """Asignar rol de Matrona a una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if hasattr(persona, 'matrona'):
        messages.warning(request, "⚠️ Esta persona ya tiene el rol de Matrona.")
        return redirect('gestion:gestionar_roles', pk=pk)
    
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['rut_persona'] = persona.Rut
        form = MatronaForm(request.POST)
        
        if form.is_valid():
            try:
                matrona = form.save()
                messages.success(request, f"✅ Rol de Matrona asignado exitosamente.")
                return redirect('gestion:gestionar_roles', pk=pk)
            except Exception as e:
                messages.error(request, f"❌ Error: {str(e)}")
    else:
        form = MatronaForm(initial={'rut_persona': persona.Rut})
    
    return render(request, 'Gestion/Formularios/asignar_rol.html', {
        'form': form,
        'persona': persona,
        'rol_nombre': 'Matrona'
    })


def asignar_rol_tens(request, pk):
    """Asignar rol de TENS a una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if hasattr(persona, 'tens'):
        messages.warning(request, "⚠️ Esta persona ya tiene el rol de TENS.")
        return redirect('gestion:gestionar_roles', pk=pk)
    
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['rut_persona'] = persona.Rut
        form = TensForm(request.POST)
        
        if form.is_valid():
            try:
                tens = form.save()
                messages.success(request, f"✅ Rol de TENS asignado exitosamente.")
                return redirect('gestion:gestionar_roles', pk=pk)
            except Exception as e:
                messages.error(request, f"❌ Error: {str(e)}")
    else:
        form = TensForm(initial={'rut_persona': persona.Rut})
    
    return render(request, 'Gestion/Formularios/asignar_rol.html', {
        'form': form,
        'persona': persona,
        'rol_nombre': 'TENS'
    })