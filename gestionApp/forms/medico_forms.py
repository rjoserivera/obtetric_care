"""
Formularios para la gestión de médicos
"""
from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Medico
from utilidad.rut_validator import normalizar_rut


class MedicoForm(forms.ModelForm):
    """Formulario para vincular médico a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_medico'
        }),
        help_text="Ingrese el RUT de la persona a vincular como médico"
    )
    
    class Meta:
        model = Medico
        fields = ['Especialidad', 'Registro_medico', 'Años_experiencia', 'Turno']
        widgets = {
            'Especialidad': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Registro_medico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de registro médico',
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
            })
        }
        labels = {
            'Especialidad': 'Especialidad Médica',
            'Registro_medico': 'Registro Médico',
            'Años_experiencia': 'Años de Experiencia',
            'Turno': 'Turno de Trabajo'
        }
    
    def clean_rut_persona(self):
        """Validar que la persona exista y no sea ya médico"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                # Verificar si ya es médico
                if hasattr(persona, 'medico'):
                    raise ValidationError(
                        f'Esta persona ya está registrada como médico.'
                    )
                
                return persona
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT. '
                    'Por favor, registre primero los datos básicos de la persona.'
                )
        return rut
    
    def clean_Registro_medico(self):
        """Validar que el registro médico sea único"""
        registro = self.cleaned_data.get('Registro_medico')
        if registro:
            if Medico.objects.filter(Registro_medico=registro).exists():
                raise ValidationError('Este número de registro médico ya existe.')
        return registro