# matronaApp/views/ficha_views.py - VISTAS COMPLETAS

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.utils import timezone

from matronaApp.models import (
    FichaClinica,
    PatologiaFicha,
    MedicamentoFicha,
    EvolucionFicha,
    Paciente
)
from matronaApp.forms.ficha_forms import (
    FichaClinicaForm,
    PatologiaFichaForm,
    MedicamentoFichaForm,
    EvolucionFichaForm,
    BuscarFichaForm
)
from gestionApp.models import Persona


# ============================================
# LISTADO Y BÚSQUEDA DE FICHAS
# ============================================

class FichaClinicaListView(ListView):
    """Listado de todas las fichas clínicas"""
    model = FichaClinica
    template_name = 'Matrona/Ficha/ficha_list.html'
    context_object_name = 'fichas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = FichaClinica.objects.select_related(
            'paciente__persona',
            'matrona_responsable__persona',
            'medico_tratante__persona'
        ).prefetch_related(
            'patologias__patologia',
            'medicamentos'
        )
        
        # Aplicar filtros de búsqueda
        form = BuscarFichaForm(self.request.GET)
        
        if form.is_valid():
            busqueda = form.cleaned_data.get('busqueda', '').strip()
            estado = form.cleaned_data.get('estado', '')
            fecha_desde = form.cleaned_data.get('fecha_desde')
            fecha_hasta = form.cleaned_data.get('fecha_hasta')
            
            if busqueda:
                queryset = queryset.filter(
                    Q(numero_ficha__icontains=busqueda) |
                    Q(paciente__persona__Rut__icontains=busqueda) |
                    Q(paciente__persona__Nombre__icontains=busqueda) |
                    Q(paciente__persona__Apellido__icontains=busqueda)
                )
            
            if estado:
                queryset = queryset.filter(estado=estado)
            
            if fecha_desde:
                queryset = queryset.filter(fecha_apertura__date__gte=fecha_desde)
            
            if fecha_hasta:
                queryset = queryset.filter(fecha_apertura__date__lte=fecha_hasta)
        
        return queryset.order_by('-fecha_apertura')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_busqueda'] = BuscarFichaForm(self.request.GET)
        context['total_fichas'] = self.get_queryset().count()
        return context


def buscar_fichas(request):
    """Vista de búsqueda de fichas clínicas"""
    form = BuscarFichaForm(request.GET or None)
    fichas = []
    
    if form.is_valid():
        fichas = FichaClinica.objects.select_related(
            'paciente__persona',
            'matrona_responsable__persona'
        )
        
        busqueda = form.cleaned_data.get('busqueda', '').strip()
        estado = form.cleaned_data.get('estado', '')
        
        if busqueda:
            fichas = fichas.filter(
                Q(numero_ficha__icontains=busqueda) |
                Q(paciente__persona__Rut__icontains=busqueda) |
                Q(paciente__persona__Nombre__icontains=busqueda) |
                Q(paciente__persona__Apellido__icontains=busqueda)
            )
        
        if estado:
            fichas = fichas.filter(estado=estado)
        
        fichas = fichas.order_by('-fecha_apertura')[:50]
    
    return render(request, 'Matrona/Ficha/buscar_ficha.html', {
        'form': form,
        'fichas': fichas
    })


# ============================================
# DETALLE DE FICHA
# ============================================

class FichaClinicaDetailView(DetailView):
    """Vista detallada de una ficha clínica"""
    model = FichaClinica
    template_name = 'Matrona/Ficha/ficha_detail.html'
    context_object_name = 'ficha'
    
    def get_queryset(self):
        return FichaClinica.objects.select_related(
            'paciente__persona',
            'matrona_responsable__persona',
            'medico_tratante__persona',
            'ingreso'
        ).prefetch_related(
            Prefetch(
                'patologias',
                queryset=PatologiaFicha.objects.select_related('patologia').filter(activo=True)
            ),
            Prefetch(
                'medicamentos',
                queryset=MedicamentoFicha.objects.filter(activo=True)
            ),
            Prefetch(
                'evoluciones',
                queryset=EvolucionFicha.objects.select_related('profesional').order_by('-fecha_evolucion')
            )
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ficha = self.object
        
        # Contar elementos
        context['total_patologias'] = ficha.patologias.filter(activo=True).count()
        context['total_medicamentos'] = ficha.medicamentos.filter(activo=True).count()
        context['total_evoluciones'] = ficha.evoluciones.count()
        
        # Última evolución
        context['ultima_evolucion'] = ficha.evoluciones.first()
        
        return context


# ============================================
# APERTURA DE FICHA CLÍNICA
# ============================================

def abrir_ficha_clinica(request, paciente_pk=None):
    """
    Abrir una nueva ficha clínica para un paciente.
    Puede recibir el ID del paciente como parámetro o en GET.
    """
    # Obtener el ID del paciente
    paciente_id = paciente_pk or request.GET.get('paciente_id')
    
    if not paciente_id:
        messages.error(request, "Debe seleccionar un paciente.")
        return redirect('matrona:lista_pacientes')
    
    # Validar que el paciente existe
    paciente = get_object_or_404(Paciente, pk=paciente_id, activo=True)
    
    # Verificar si ya tiene una ficha abierta
    ficha_abierta = FichaClinica.objects.filter(
        paciente=paciente,
        estado__in=['ABIERTA', 'EN_TRATAMIENTO']
    ).first()
    
    if ficha_abierta:
        messages.warning(
            request, 
            f"El paciente ya tiene una ficha clínica abierta: {ficha_abierta.numero_ficha}"
        )
        return redirect('matrona:detalle_ficha', pk=ficha_abierta.pk)
    
    if request.method == 'POST':
        form = FichaClinicaForm(request.POST)
        if form.is_valid():
            ficha = form.save()
            messages.success(
                request,
                f"Ficha clínica {ficha.numero_ficha} creada exitosamente."
            )
            return redirect('matrona:detalle_ficha', pk=ficha.pk)
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = FichaClinicaForm(initial={'paciente_id': paciente_id})
    
    return render(request, 'Matrona/Ficha/abrir_ficha.html', {
        'form': form,
        'paciente': paciente
    })


# ============================================
# GESTIÓN DE PATOLOGÍAS EN FICHA
# ============================================

def agregar_patologia_ficha(request, ficha_pk):
    """Agregar una patología a una ficha clínica"""
    ficha = get_object_or_404(FichaClinica, pk=ficha_pk)
    
    # Verificar que la ficha no esté cerrada
    if ficha.estado == 'CERRADA':
        messages.error(request, "No se pueden agregar patologías a una ficha cerrada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    if request.method == 'POST':
        form = PatologiaFichaForm(request.POST, ficha=ficha)
        if form.is_valid():
            patologia_ficha = form.save(commit=False)
            patologia_ficha.ficha = ficha
            patologia_ficha.save()
            messages.success(request, "Patología agregada exitosamente.")
            return redirect('matrona:detalle_ficha', pk=ficha.pk)
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = PatologiaFichaForm(ficha=ficha)
    
    return render(request, 'Matrona/Ficha/agregar_patologia.html', {
        'form': form,
        'ficha': ficha
    })


def eliminar_patologia_ficha(request, ficha_pk, patologia_pk):
    """Eliminar/Desactivar una patología de una ficha"""
    ficha = get_object_or_404(FichaClinica, pk=ficha_pk)
    patologia_ficha = get_object_or_404(PatologiaFicha, pk=patologia_pk, ficha=ficha)
    
    # Verificar que la ficha no esté cerrada
    if ficha.estado == 'CERRADA':
        messages.error(request, "No se pueden modificar patologías de una ficha cerrada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    if request.method == 'POST':
        patologia_ficha.activo = False
        patologia_ficha.save()
        messages.success(request, "Patología desactivada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    return render(request, 'Matrona/Ficha/confirmar_eliminar_patologia.html', {
        'ficha': ficha,
        'patologia_ficha': patologia_ficha
    })


# ============================================
# GESTIÓN DE MEDICAMENTOS EN FICHA
# ============================================

def agregar_medicamento_ficha(request, ficha_pk):
    """Agregar un medicamento a una ficha clínica"""
    ficha = get_object_or_404(FichaClinica, pk=ficha_pk)
    
    # Verificar que la ficha no esté cerrada
    if ficha.estado == 'CERRADA':
        messages.error(request, "No se pueden agregar medicamentos a una ficha cerrada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    if request.method == 'POST':
        form = MedicamentoFichaForm(request.POST)
        if form.is_valid():
            medicamento_ficha = form.save(commit=False)
            medicamento_ficha.ficha = ficha
            medicamento_ficha.save()
            messages.success(request, "Medicamento agregado exitosamente.")
            return redirect('matrona:detalle_ficha', pk=ficha.pk)
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = MedicamentoFichaForm()
    
    return render(request, 'Matrona/Ficha/agregar_medicamento.html', {
        'form': form,
        'ficha': ficha
    })


def eliminar_medicamento_ficha(request, ficha_pk, medicamento_pk):
    """Eliminar/Desactivar un medicamento de una ficha"""
    ficha = get_object_or_404(FichaClinica, pk=ficha_pk)
    medicamento_ficha = get_object_or_404(MedicamentoFicha, pk=medicamento_pk, ficha=ficha)
    
    # Verificar que la ficha no esté cerrada
    if ficha.estado == 'CERRADA':
        messages.error(request, "No se pueden modificar medicamentos de una ficha cerrada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    if request.method == 'POST':
        medicamento_ficha.activo = False
        medicamento_ficha.save()
        messages.success(request, "Medicamento desactivado.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    return render(request, 'Matrona/Ficha/confirmar_eliminar_medicamento.html', {
        'ficha': ficha,
        'medicamento_ficha': medicamento_ficha
    })


# ============================================
# GESTIÓN DE EVOLUCIONES
# ============================================

def agregar_evolucion_ficha(request, ficha_pk):
    """Agregar una evolución/seguimiento a una ficha"""
    ficha = get_object_or_404(FichaClinica, pk=ficha_pk)
    
    # Verificar que la ficha no esté cerrada
    if ficha.estado == 'CERRADA':
        messages.error(request, "No se pueden agregar evoluciones a una ficha cerrada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    if request.method == 'POST':
        form = EvolucionFichaForm(request.POST)
        if form.is_valid():
            evolucion = form.save(commit=False)
            evolucion.ficha = ficha
            
            # TODO: Obtener el profesional del usuario logueado
            # Por ahora usamos el primer profesional disponible
            profesional = Persona.objects.first()
            if not profesional:
                messages.error(request, "No hay profesionales registrados en el sistema.")
                return redirect('matrona:detalle_ficha', pk=ficha.pk)
            
            evolucion.profesional = profesional
            evolucion.save()
            
            messages.success(request, "Evolución registrada exitosamente.")
            return redirect('matrona:detalle_ficha', pk=ficha.pk)
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = EvolucionFichaForm()
    
    return render(request, 'Matrona/Ficha/agregar_evolucion.html', {
        'form': form,
        'ficha': ficha
    })


# ============================================
# CERRAR FICHA
# ============================================

def cerrar_ficha(request, pk):
    """Cerrar una ficha clínica"""
    ficha = get_object_or_404(FichaClinica, pk=pk)
    
    # Verificar que no esté ya cerrada
    if ficha.estado == 'CERRADA':
        messages.warning(request, "Esta ficha ya está cerrada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    if request.method == 'POST':
        ficha.cerrar_ficha()
        messages.success(request, f"Ficha {ficha.numero_ficha} cerrada exitosamente.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    return render(request, 'Matrona/Ficha/confirmar_cerrar_ficha.html', {
        'ficha': ficha
    })