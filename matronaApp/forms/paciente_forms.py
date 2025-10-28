"""
Formularios para la gestión de pacientes obstétricos
"""
from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import Paciente
from gestionApp.models import Persona
from utilidad.rut_validator import normalizar_rut


class PacienteForm(forms.ModelForm):
    """Formulario para vincular paciente a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_paciente',
            'autocomplete': 'off'
        }),
        help_text="Ingrese el RUT de la persona a vincular como paciente"
    )
    
    class Meta:
        model = Paciente
        fields = ['Estado_civil', 'Previcion', 'Acompañante', 'Contacto_emergencia']
        widgets = {

            'Estado_civil': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Previcion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Acompañante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del acompañante'
            }),
            'Contacto_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            })
        }
        labels = {
            'Edad': 'Edad',
            'Estado_civil': 'Estado Civil',
            'Previcion': 'Previsión de Salud',
            'Acompañante': 'Acompañante',
            'Contacto_emergencia': 'Contacto de Emergencia'
        }
    
    def clean_rut_persona(self):
        """Validar que la persona exista y no sea ya paciente"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if hasattr(persona, 'paciente'):
                    raise ValidationError(
                        f'Esta persona ya está registrada como paciente.'
                    )
                
                return persona
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT. '
                    'Por favor, registre primero los datos básicos de la persona.'
                )
        return rut
    
    def clean_Edad(self):
        """Validar rango de edad"""
        edad = self.cleaned_data.get('Edad')
        if edad and (edad < 12 or edad > 60):
            raise ValidationError('La edad debe estar entre 12 y 60 años.')
        return edad