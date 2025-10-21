# ============================================
# CREAR: matronaApp/forms/patologias_ficha_forms.py
# ============================================

from django import forms
from matronaApp.models import FichaObstetrica
from medicoApp.models import Patologias


class AsignarPatologiasFichaForm(forms.ModelForm):
    """
    Formulario para que la MATRONA asocie patologías existentes a una ficha.
    Las patologías son gestionadas por el MÉDICO, la matrona solo las selecciona.
    """
    
    patologias = forms.ModelMultipleChoiceField(
        queryset=Patologias.objects.filter(estado=True).order_by('nombre'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        label='Seleccione las patologías diagnosticadas',
        help_text='Seleccione una o varias patologías del catálogo'
    )
    
    class Meta:
        model = FichaObstetrica
        fields = ['patologias']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ordenar patologías por código CIE-10 y nombre
        self.fields['patologias'].queryset = Patologias.objects.filter(
            estado=True
        ).order_by('codigo_cie_10', 'nombre')


class BuscarPatologiaForm(forms.Form):
    """
    Formulario simple para buscar patologías en el catálogo
    """
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre o código CIE-10...',
            'id': 'buscar_patologia'
        }),
        label='Buscar en el Catálogo'
    )