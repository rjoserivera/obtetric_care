from django import forms
from partosApp.models import DocumentosParto, RegistroParto


class DocumentosPartoForm(forms.ModelForm):
    """
    Formulario completo para documentos del parto
    """
    class Meta:
        model = DocumentosParto
        fields = [
            'registro_parto',
            # Ley Dominga
            'recuerdos_entregados',
            'motivo_no_entrega_recuerdos',
            # Placenta
            'retira_placenta',
            'estampado_placenta',
            # Registro Civil
            'folio_valido',
            'folios_nulos',
            # Manejo del Dolor
            'manejo_dolor_no_farmacologico',
        ]
        widgets = {
            'registro_parto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            # Ley Dominga
            'recuerdos_entregados': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Huella, foto, mechas de cabello'
            }),
            'motivo_no_entrega_recuerdos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Justifique si no se entregaron recuerdos'
            }),
            # Placenta
            'retira_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'estampado_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Registro Civil
            'folio_valido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de folio'
            }),
            'folios_nulos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Folios anulados (si aplica)'
            }),
            # Manejo del Dolor
            'manejo_dolor_no_farmacologico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa los métodos no farmacológicos utilizados'
            }),
        }
        labels = {
            'registro_parto': 'Registro de Parto',
            'recuerdos_entregados': 'Recuerdos Entregados (Ley Dominga)',
            'motivo_no_entrega_recuerdos': 'Motivo de No Entrega',
            'retira_placenta': '¿Retira Placenta?',
            'estampado_placenta': '¿Estampado de Placenta?',
            'folio_valido': 'Folio Válido Registro Civil',
            'folios_nulos': 'Folios Nulos',
            'manejo_dolor_no_farmacologico': 'Manejo del Dolor No Farmacológico',
        }
        help_texts = {
            'recuerdos_entregados': 'Lista de recuerdos entregados según Ley N° 21.372',
            'motivo_no_entrega_recuerdos': 'Completar solo si NO se entregaron recuerdos',
            'folio_valido': 'Número de folio del certificado de nacimiento',
        }
    
    def __init__(self, *args, **kwargs):
        # Permitir pasar el registro_parto como parámetro
        registro_parto = kwargs.pop('registro_parto', None)
        super().__init__(*args, **kwargs)
        
        # Si se pasa registro_parto, preseleccionarlo y ocultarlo
        if registro_parto:
            self.fields['registro_parto'].initial = registro_parto
            self.fields['registro_parto'].widget = forms.HiddenInput()
        
        # Filtrar solo registros activos
        self.fields['registro_parto'].queryset = RegistroParto.objects.filter(
            activo=True
        ).select_related('ficha__paciente__persona')
        
        # Todos los campos son opcionales excepto registro_parto
        for field_name in self.fields:
            if field_name != 'registro_parto':
                self.fields[field_name].required = False


class LeyDomingaForm(forms.ModelForm):
    """
    Formulario solo para Ley Dominga
    """
    class Meta:
        model = DocumentosParto
        fields = [
            'recuerdos_entregados',
            'motivo_no_entrega_recuerdos',
        ]
        widgets = {
            'recuerdos_entregados': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lista de recuerdos entregados'
            }),
            'motivo_no_entrega_recuerdos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Justificación (solo si no se entregaron)'
            }),
        }
        labels = {
            'recuerdos_entregados': 'Recuerdos Entregados',
            'motivo_no_entrega_recuerdos': 'Motivo de No Entrega',
        }


class PlacentaForm(forms.ModelForm):
    """
    Formulario solo para información de placenta
    """
    class Meta:
        model = DocumentosParto
        fields = [
            'retira_placenta',
            'estampado_placenta',
        ]
        widgets = {
            'retira_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'estampado_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'retira_placenta': 'La familia retira la placenta',
            'estampado_placenta': 'Se realizó estampado de placenta',
        }


class RegistroCivilForm(forms.ModelForm):
    """
    Formulario solo para Registro Civil
    """
    class Meta:
        model = DocumentosParto
        fields = [
            'folio_valido',
            'folios_nulos',
        ]
        widgets = {
            'folio_valido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 7787343'
            }),
            'folios_nulos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Folios anulados (separados por coma)'
            }),
        }
        labels = {
            'folio_valido': 'Folio Válido',
            'folios_nulos': 'Folios Nulos',
        }