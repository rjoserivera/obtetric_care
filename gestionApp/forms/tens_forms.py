"""
Formularios para la gestión de TENS
"""
from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Tens
from utilidad.rut_validator import normalizar_rut, validar_rut, validar_rut_chileno
from tensApp.models import RegistroTens

from django.utils import timezone
from tensApp.models import Tratamiento_aplicado
from matronaApp.models import MedicamentoFicha


class TensForm(forms.ModelForm):
    """Formulario para vincular TENS a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_tens'
        }),
        help_text="Ingrese el RUT de la persona a vincular como TENS"
    )
    
    class Meta:
        model = Tens
        fields = ['Nivel', 'Años_experiencia', 'Turno', 'Certificaciones']
        widgets = {
            'Nivel': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '50',
                'required': True
            }),
            'Turno': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Certificaciones': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            })
        }
        labels = {
            'Nivel': 'Nivel TENS',
            'Años_experiencia': 'Años de Experiencia',
            'Turno': 'Turno de Trabajo',
            'Certificaciones': 'Certificaciones'
        }
    
    def clean_rut_persona(self):
        """Validar que la persona exista y no sea ya TENS"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if hasattr(persona, 'tens'):
                    raise ValidationError(
                        f'Esta persona ya está registrada como TENS.'
                    )
                
                return persona
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT. '
                    'Por favor, registre primero los datos básicos de la persona.'
                )
        return rut

class BuscarPacienteForm(forms.Form):
    """Formulario para buscar paciente por RUT"""
    rut = forms.CharField(
        max_length=12,
        label='RUT del Paciente',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'autofocus': True
        })
    )


class RegistroTensForm(forms.ModelForm):
    """Formulario para registrar signos vitales"""
    
    tens_responsable = forms.ModelChoiceField(
        queryset=Tens.objects.select_related('persona').filter(Activo=True),
        label='TENS Responsable',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        empty_label='--- Seleccione TENS ---'
    )
    
    class Meta:
        model = RegistroTens
        fields = [
            'ficha',
            'tens_responsable',
            'fecha',
            'turno',
            'temperatura',
            'frecuencia_cardiaca',
            'presion_arterial',
            'frecuencia_respiratoria',
            'saturacion_oxigeno',
            'observaciones'
        ]
        widgets = {
            'ficha': forms.HiddenInput(),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'turno': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'temperatura': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '36.5',
                'step': '0.1',
                'min': '35',
                'max': '45',
                'required': True
            }),
            'frecuencia_cardiaca': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '70',
                'min': '40',
                'max': '220',
                'required': True
            }),
            'presion_arterial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '120/80',
                'required': True
            }),
            'frecuencia_respiratoria': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '16',
                'min': '10',
                'max': '40',
                'required': True
            }),
            'saturacion_oxigeno': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '98',
                'min': '70',
                'max': '100',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones adicionales...'
            })
        }
        labels = {
            'fecha': 'Fecha de Registro',
            'turno': 'Turno',
            'tens_responsable': 'TENS Responsable',
            'temperatura': 'Temperatura (°C)',
            'frecuencia_cardiaca': 'Frecuencia Cardíaca (lpm)',
            'presion_arterial': 'Presión Arterial (mmHg)',
            'frecuencia_respiratoria': 'Frecuencia Respiratoria (rpm)',
            'saturacion_oxigeno': 'Saturación de Oxígeno (%)',
            'observaciones': 'Observaciones'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el display de los TENS
        self.fields['tens_responsable'].label_from_instance = lambda obj: f"{obj.persona.Nombre} {obj.persona.Apellido_Paterno} - {obj.persona.Rut}"





# ============================================================
# FORMULARIO TRATAMIENTO APLICADO - VINCULADO A FICHA
# ============================================================
class FormularioTratamientoAplicado(forms.ModelForm):
    """
    Formulario para registrar tratamientos aplicados por TENS
    vinculados a una FichaObstetrica específica
    """

    class Meta:
        model = Tratamiento_aplicado
        fields = [
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'fecha_aplicacion',
            'hora_aplicacion',
            'observaciones',
            'medicamento_ficha',  # Opcional: vincular con medicamento específico
        ]

        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Paracetamol 500mg',
                'required': True
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1 tableta / 5ml / 10 UI'
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_aplicacion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'value': timezone.now().strftime('%Y-%m-%dT%H:%M')
            }),
            'hora_aplicacion': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'value': timezone.now().strftime('%H:%M')
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ej: Paciente presentó náuseas leves tras administración. Se mantuvo en observación por 30 minutos.',
            }),
            'medicamento_ficha': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        
        labels = {
            'nombre_medicamento': 'Nombre del Medicamento',
            'dosis': 'Dosis o Cantidad',
            'via_administracion': 'Vía de Administración',
            'fecha_aplicacion': 'Fecha y Hora de Aplicación',
            'hora_aplicacion': 'Hora de Aplicación',
            'observaciones': 'Observaciones Clínicas',
            'medicamento_ficha': 'Medicamento Prescrito en Ficha (Opcional)',
        }
        
        help_texts = {
            'medicamento_ficha': 'Seleccione si este tratamiento corresponde a un medicamento ya prescrito en la ficha',
            'observaciones': 'Registre cualquier reacción, efecto adverso o situación relevante durante la administración',
        }

    def __init__(self, *args, ficha=None, **kwargs):
        """
        Inicializa el formulario y filtra medicamentos por ficha
        
        Args:
            ficha: Instancia de FichaObstetrica para filtrar medicamentos
        """
        super().__init__(*args, **kwargs)
        
        # Si se proporciona una ficha, filtrar solo sus medicamentos activos
        if ficha:
            self.fields['medicamento_ficha'].queryset = MedicamentoFicha.objects.filter(
                ficha=ficha,
                activo=True
            ).order_by('-fecha_inicio')
            
            # Personalizar el label de cada medicamento
            self.fields['medicamento_ficha'].label_from_instance = lambda obj: (
                f"{obj.nombre_medicamento} - {obj.dosis} ({obj.via_administracion}) - "
                f"Desde: {obj.fecha_inicio.strftime('%d/%m/%Y')}"
            )
        else:
            # Si no hay ficha, no mostrar medicamentos
            self.fields['medicamento_ficha'].queryset = MedicamentoFicha.objects.none()
        
        # El medicamento_ficha es opcional
        self.fields['medicamento_ficha'].required = False
        
        # Agregar clase de ayuda visual
        self.fields['medicamento_ficha'].widget.attrs.update({
            'class': 'form-select',
            'data-placeholder': 'Seleccione un medicamento de la ficha (opcional)'
        })

    def clean(self):
        """Validaciones adicionales del formulario"""
        cleaned_data = super().clean()
        fecha_aplicacion = cleaned_data.get('fecha_aplicacion')
        
        # Validar que la fecha no sea futura
        if fecha_aplicacion and fecha_aplicacion > timezone.now():
            raise ValidationError({
                'fecha_aplicacion': 'La fecha de aplicación no puede ser futura.'
            })
        
        return cleaned_data