"""
Formularios para la gestión de matronas
"""
from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Matrona
from utilidad.rut_validator import normalizar_rut


class MatronaForm(forms.ModelForm):
    """Formulario para vincular matrona a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_matrona'
        }),
        help_text="Ingrese el RUT de la persona a vincular como matrona"
    )
    
    class Meta:
        model = Matrona
        fields = ['Especialidad', 'Registro_medico', 'Años_experiencia', 'Turno']
        widgets = {
            'Especialidad': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Registro_medico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de registro profesional',
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
            'Especialidad': 'Especialidad',
            'Registro_medico': 'Registro Profesional',
            'Años_experiencia': 'Años de Experiencia',
            'Turno': 'Turno de Trabajo'
        }
    
    def clean_rut_persona(self):
        """Validar que la persona exista y no sea ya matrona"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if hasattr(persona, 'matrona'):
                    raise ValidationError(
                        f'Esta persona ya está registrada como matrona.'
                    )
                
                return persona
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT. '
                    'Por favor, registre primero los datos básicos de la persona.'
                )
        return rut
    
    def clean_Registro_medico(self):
        """Validar que el registro sea único"""
        registro = self.cleaned_data.get('Registro_medico')
        if registro:
            if Matrona.objects.filter(Registro_medico=registro).exists():
                raise ValidationError('Este número de registro ya existe.')
        return registro