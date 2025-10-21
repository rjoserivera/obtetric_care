# tensApp/administracion_medicamentos.py
"""
Formularios para que TENS registre la administración de medicamentos
"""
from django import forms
from matronaApp.models import AdministracionMedicamento


class TensRegistrarAdministracionMedicamento(forms.ModelForm):
    """Formulario para que TENS registre cuando administra un medicamento a un paciente"""
    
    class Meta:
        model = AdministracionMedicamento
        fields = [
            'fecha_hora_administracion',
            'se_realizo_lavado',
            'administrado_exitosamente',
            'motivo_no_administracion',
            'observaciones',
            'reacciones_adversas'
        ]
        widgets = {
            'fecha_hora_administracion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            'se_realizo_lavado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'administrado_exitosamente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'motivo_no_administracion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Solo completar si NO se administró'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones generales de la administración'
            }),
            'reacciones_adversas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describir cualquier reacción adversa observada'
            })
        }
        labels = {
            'fecha_hora_administracion': 'Fecha y Hora de Administración',
            'se_realizo_lavado': '¿Se realizó lavado?',
            'administrado_exitosamente': '¿Se administró exitosamente?',
            'motivo_no_administracion': 'Motivo de No Administración',
            'observaciones': 'Observaciones',
            'reacciones_adversas': 'Reacciones Adversas'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        administrado = cleaned_data.get('administrado_exitosamente')
        motivo = cleaned_data.get('motivo_no_administracion')
        
        # Si no se administró, debe haber un motivo
        if not administrado and not motivo:
            raise forms.ValidationError(
                'Si el medicamento NO se administró, debe indicar el motivo.'
            )
        
        return cleaned_data