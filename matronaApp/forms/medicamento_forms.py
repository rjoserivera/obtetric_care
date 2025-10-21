from django import forms
from matronaApp.models import MedicamentoFicha


class MatronaAsignarMedicamento(forms.ModelForm):
    """
    Formulario para que la matrona asigne medicamentos a una ficha
    """
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'observaciones'
        ]
        
        widgets = {
            'nombre_medicamento': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'dosis': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'frecuencia': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'fecha_termino': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicaciones especiales, alergias, etc.'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_termino = cleaned_data.get('fecha_termino')
        
        if fecha_inicio and fecha_termino:
            if fecha_termino < fecha_inicio:
                raise forms.ValidationError(
                    'La fecha de término no puede ser anterior a la fecha de inicio.'
                )
        
        return cleaned_data