# matronaApp/forms/ficha_forms.py
"""
Formularios para la gestión de Fichas Obstétricas
"""
from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import FichaObstetrica
from medicoApp.models import Patologias
from gestionApp.models import Matrona, Paciente


class FichaObstetricaForm(forms.ModelForm):
    """
    Formulario para crear y editar fichas obstétricas
    """
    # Campo oculto para el ID del paciente
    paciente_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'paciente_id',
            'matrona_responsable',
            'nombre_acompanante',
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'hijos_vivos',
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla',
            'patologias',
            'descripcion_patologias',
            'observaciones_generales',
            'antecedentes_relevantes',
        ]
        
        widgets = {
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del acompañante'
            }),
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20',
                'value': '0'
            }),
            'numero_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20',
                'value': '0'
            }),
            'partos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20',
                'value': '0'
            }),
            'partos_cesareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20',
                'value': '0'
            }),
            'numero_abortos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20',
                'value': '0'
            }),
            'hijos_vivos': forms.NumberInput(attrs={
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
                'min': '0',
                'max': '42',
                'placeholder': '0-42'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6',
                'placeholder': '0-6'
            }),
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 65.5',
                'min': '30',
                'max': '200',
                'step': '0.1'
            }),
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 160',
                'min': '120',
                'max': '220',
                'step': '0.1'
            }),
            'patologias': forms.CheckboxSelectMultiple(),
            'descripcion_patologias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa las patologías y su estado actual'
            }),
            'observaciones_generales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones generales del embarazo'
            }),
            'antecedentes_relevantes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Antecedentes médicos, quirúrgicos, alergias, etc.'
            }),
        }
        
        labels = {
            'matrona_responsable': 'Matrona Responsable',
            'nombre_acompanante': 'Nombre del Acompañante',
            'numero_gestas': 'Número de Gestas',
            'numero_partos': 'Número de Partos',
            'partos_vaginales': 'Partos Vaginales',
            'partos_cesareas': 'Cesáreas',
            'numero_abortos': 'Número de Abortos',
            'hijos_vivos': 'Hijos Vivos',
            'fecha_ultima_regla': 'Fecha Última Regla (FUR)',
            'fecha_probable_parto': 'Fecha Probable de Parto (FPP)',
            'edad_gestacional_semanas': 'Semanas',
            'edad_gestacional_dias': 'Días',
            'peso_actual': 'Peso Actual',
            'talla': 'Talla',
            'patologias': 'Patologías Asociadas',
            'descripcion_patologias': 'Descripción de Patologías',
            'observaciones_generales': 'Observaciones Generales',
            'antecedentes_relevantes': 'Antecedentes Relevantes',
        }
        
        help_texts = {
            'talla': 'Estatura en centímetros',
            'peso_actual': 'Peso en kilogramos',
            'edad_gestacional_semanas': 'Semanas completas de gestación (0-42)',
            'edad_gestacional_dias': 'Días adicionales (0-6)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ✅ IMPORTANTE: Configurar formato de fecha para input type="date"
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
        
        # Hacer algunos campos opcionales
        self.fields['nombre_acompanante'].required = False
        self.fields['fecha_ultima_regla'].required = False
        self.fields['fecha_probable_parto'].required = False
        self.fields['peso_actual'].required = False
        self.fields['talla'].required = False
        self.fields['edad_gestacional_semanas'].required = False
        self.fields['edad_gestacional_dias'].required = False
        self.fields['descripcion_patologias'].required = False
        self.fields['observaciones_generales'].required = False
        self.fields['antecedentes_relevantes'].required = False
    
    def clean_paciente_id(self):
        """Validar que el paciente exista"""
        pk = self.cleaned_data.get('paciente_id')
        try:
            paciente = Paciente.objects.get(pk=pk, activo=True)
        except (Paciente.DoesNotExist, TypeError, ValueError):
            raise ValidationError('Debe seleccionar un paciente válido.')
        
        # Guardar el objeto para usarlo en save()
        self._paciente_obj = paciente
        return pk
    
    def clean(self):
        """Validaciones cruzadas"""
        cleaned_data = super().clean()
        
        # Validar que partos vaginales + cesáreas = número de partos
        num_partos = cleaned_data.get('numero_partos', 0)
        partos_vag = cleaned_data.get('partos_vaginales', 0)
        partos_ces = cleaned_data.get('partos_cesareas', 0)
        
        if (partos_vag + partos_ces) > num_partos:
            raise ValidationError({
                'numero_partos': 'La suma de partos vaginales y cesáreas no puede ser mayor al número total de partos.'
            })
        
        # Validar edad gestacional
        semanas = cleaned_data.get('edad_gestacional_semanas')
        if semanas is not None and (semanas < 0 or semanas > 42):
            raise ValidationError({
                'edad_gestacional_semanas': 'La edad gestacional debe estar entre 0 y 42 semanas.'
            })
        
        dias = cleaned_data.get('edad_gestacional_dias')
        if dias is not None and (dias < 0 or dias > 6):
            raise ValidationError({
                'edad_gestacional_dias': 'Los días deben estar entre 0 y 6.'
            })
        
        # Validar talla
        talla = cleaned_data.get('talla')
        if talla is not None and (talla < 120 or talla > 220):
            raise ValidationError({
                'talla': 'La talla debe estar entre 120 y 220 cm.'
            })
        
        # Validar peso
        peso = cleaned_data.get('peso_actual')
        if peso is not None and (peso < 30 or peso > 200):
            raise ValidationError({
                'peso_actual': 'El peso debe estar entre 30 y 200 kg.'
            })
        
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