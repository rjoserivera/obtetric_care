"""
Formularios para búsqueda de pacientes
"""
from django import forms
from utilidad.rut_validator import normalizar_rut


class BuscarPacienteForm(forms.Form):
    """Formulario para búsqueda de pacientes"""
    
    BUSCAR_POR_CHOICES = [
        ('rut', 'RUT'),
        ('nombre', 'Nombre'),
        ('ficha', 'Número de Ficha'),
    ]
    
    buscar_por = forms.ChoiceField(
        choices=BUSCAR_POR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'buscar_por'
        }),
        label="Buscar por"
    )
    
    termino = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese término de búsqueda',
            'id': 'termino_busqueda',
            'autocomplete': 'off'
        }),
        label="Término de búsqueda"
    )
    
    def clean_termino(self):
        """Normalizar término de búsqueda"""
        termino = self.cleaned_data.get('termino')
        buscar_por = self.cleaned_data.get('buscar_por')
        
        if buscar_por == 'rut' and termino:
            return normalizar_rut(termino)
        
        return termino.strip()