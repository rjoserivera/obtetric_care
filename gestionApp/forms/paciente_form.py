from django import forms
from django.core.exceptions import ValidationError
from ..models import Persona, Paciente
from utilidad.rut_validator import normalizar_rut

class PacienteForm(forms.ModelForm):
    """Formulario para vincular paciente a una persona existente"""

    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_paciente'
        }),
        help_text="Ingrese el RUT de la persona a vincular como paciente"
    )

    class Meta:
        model = Paciente
        fields = ['Edad', 'Estado_civil', 'Prevision', 'Acompanante', 'Contacto_emergencia', 'Activo']
        widgets = {
            'Edad': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'Estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'Prevision': forms.Select(attrs={'class': 'form-select'}),
            'Acompanante': forms.TextInput(attrs={'class': 'form-control'}),
            'Contacto_emergencia': forms.TextInput(attrs={'class': 'form-control'}),
            'Activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_rut_persona(self):
        """Validar que la persona exista y no sea ya paciente"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)

                if hasattr(persona, 'paciente'):
                    raise ValidationError('Esta persona ya está registrada como paciente.')

                return persona
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT. '
                    'Por favor, registre primero los datos básicos de la persona.'
                )
        return rut
