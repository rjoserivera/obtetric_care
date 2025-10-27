from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import FichaObstetrica
from medicoApp.models import Patologias
from gestionApp.models import Matrona, Paciente


# ============================================
# FORMULARIO: FICHA OBSTÉTRICA
# ============================================
class FichaObstetricaForm(forms.ModelForm):
    """Formulario para crear y editar fichas obstétricas"""
    
    paciente_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'paciente_id',
            'matrona_responsable',
            'Origen_de_ingreso',
            'Tipo_de_paciente',
            'nombre_acompanante',
            'nacidos_vivos',
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'patologias',
            'descripcion_patologias',
            'observaciones_generales',
        ]
        
        widgets = {
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Origen_de_ingreso': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Tipo_de_paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del acompañante'
            }),
            'nacidos_vivos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20',
                'value': '0'
            }),
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }, format='%Y-%m-%d'),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }, format='%Y-%m-%d'),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'placeholder': 'Se calcula automáticamente'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'placeholder': 'Se calcula automáticamente'
            }),
            'patologias': forms.CheckboxSelectMultiple(),
            'descripcion_patologias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'readonly': True,
                'placeholder': 'Se genera automáticamente al seleccionar patologías'
            }),
            'observaciones_generales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones generales sobre el embarazo actual'
            }),
        }
        
        labels = {
            'matrona_responsable': 'Matrona Responsable',
            'Origen_de_ingreso': 'Origen de Ingreso',
            'Tipo_de_paciente': 'Tipo de Paciente',
            'nombre_acompanante': 'Nombre del Acompañante',
            'nacidos_vivos': 'Nacidos Vivos',
            'fecha_ultima_regla': 'Fecha Última Regla (FUR)',
            'fecha_probable_parto': 'Fecha Probable de Parto (FPP)',
            'edad_gestacional_semanas': 'Edad Gestacional - Semanas',
            'edad_gestacional_dias': 'Edad Gestacional - Días',
            'patologias': 'Patologías Asociadas',
            'descripcion_patologias': 'Descripción de Patologías',
            'observaciones_generales': 'Observaciones Generales',
        }
        
        help_texts = {
            'nacidos_vivos': 'Número de hijos nacidos vivos',
            'fecha_ultima_regla': 'Primer día de la última menstruación',
            'fecha_probable_parto': 'Se calculará la edad gestacional automáticamente',
            'edad_gestacional_semanas': 'Calculado automáticamente desde FPP o FUR',
            'edad_gestacional_dias': 'Días adicionales calculados automáticamente',
            'patologias': 'Seleccione una o más patologías',
            'descripcion_patologias': 'Se genera automáticamente al guardar',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar formato de fecha para input type="date"
        self.fields['fecha_ultima_regla'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
        self.fields['fecha_probable_parto'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
        
        # Filtrar solo matronas activas
        self.fields['matrona_responsable'].queryset = Matrona.objects.filter(
            Activo=True
        ).select_related('persona')
        
        # Filtrar solo patologías activas
        self.fields['patologias'].queryset = Patologias.objects.filter(
            estado='Activo'
        ).order_by('nivel_de_riesgo', 'nombre')
        
        # Hacer campos opcionales
        self.fields['nombre_acompanante'].required = False
        self.fields['fecha_ultima_regla'].required = False
        self.fields['fecha_probable_parto'].required = False
        self.fields['edad_gestacional_semanas'].required = False
        self.fields['edad_gestacional_dias'].required = False
        self.fields['descripcion_patologias'].required = False
        self.fields['observaciones_generales'].required = False
        
        # Edad gestacional y descripción patologías son readonly (se calculan auto)
        self.fields['edad_gestacional_semanas'].disabled = True
        self.fields['edad_gestacional_dias'].disabled = True
        self.fields['descripcion_patologias'].disabled = True
    
    def clean_paciente_id(self):
        """Validar que el paciente exista"""
        pk = self.cleaned_data.get('paciente_id')
        try:
            paciente = Paciente.objects.get(pk=pk, activo=True)
        except (Paciente.DoesNotExist, TypeError, ValueError):
            raise ValidationError('Debe seleccionar un paciente válido.')
        
        self._paciente_obj = paciente
        return pk
    
    def clean_nacidos_vivos(self):
        """Validar nacidos vivos"""
        nacidos = self.cleaned_data.get('nacidos_vivos')
        if nacidos is not None and (nacidos < 0 or nacidos > 20):
            raise ValidationError('El número de nacidos vivos debe estar entre 0 y 20.')
        return nacidos
    
    def clean(self):
        """Validaciones cruzadas"""
        cleaned_data = super().clean()
        
        # Validar que al menos tenga FUR o FPP para calcular edad gestacional
        fur = cleaned_data.get('fecha_ultima_regla')
        fpp = cleaned_data.get('fecha_probable_parto')
        
        if not fur and not fpp:
            raise ValidationError(
                'Debe ingresar al menos la Fecha de Última Regla (FUR) o la Fecha Probable de Parto (FPP) '
                'para calcular la edad gestacional.'
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        """Guardar la ficha con el paciente correcto"""
        ficha = super().save(commit=False)
        
        # Asignar el paciente desde el campo oculto
        paciente = getattr(self, '_paciente_obj', None)
        if paciente:
            ficha.paciente = paciente
        
        if commit:
            ficha.save()
            # Guardar las relaciones ManyToMany (patologías)
            self.save_m2m()
        
        return ficha


# ============================================
# FORMULARIO: EDITAR FICHA OBSTÉTRICA
# ============================================
class EditarFichaObstetricaForm(FichaObstetricaForm):
    """Formulario para editar fichas obstétricas existentes"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # En edición, el paciente no se puede cambiar
        if self.instance and self.instance.pk:
            self.fields['paciente_id'].widget = forms.HiddenInput()


# ============================================
# FORMULARIO: BUSCAR FICHA
# ============================================
class BuscarFichaForm(forms.Form):
    """Formulario para búsqueda de fichas por número"""
    
    numero_ficha = forms.CharField(
        max_length=20,
        label="Buscar Ficha",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'FO-00001',
            'id': 'buscar_numero_ficha',
            'autocomplete': 'off'
        })
    )
    
    def clean_numero_ficha(self):
        """Validar formato de número de ficha"""
        numero = self.cleaned_data.get('numero_ficha')
        if numero:
            numero = numero.strip().upper()
            if not numero.startswith('FO-'):
                numero = f'FO-{numero}'
        return numero
















