from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import MedicamentoFicha, FichaObstetrica
from datetime import date


# ============================================
# FORMULARIO: MEDICAMENTO FICHA
# ============================================
class MedicamentoFichaForm(forms.ModelForm):
    """Formulario para asignar medicamentos a una ficha obstétrica"""
    
    ficha_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'ficha_id',
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'observaciones',
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
            }, format='%Y-%m-%d'),
            'fecha_termino': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }, format='%Y-%m-%d'),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicaciones especiales sobre la medicación'
            }),
        }
        
        labels = {
            'nombre_medicamento': 'Medicamento',
            'dosis': 'Dosis',
            'via_administracion': 'Vía de Administración',
            'frecuencia': 'Frecuencia',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_termino': 'Fecha de Término',
            'observaciones': 'Observaciones',
        }
        
        help_texts = {
            'fecha_inicio': 'Fecha en que inicia el tratamiento',
            'fecha_termino': 'Fecha en que finaliza el tratamiento',
            'observaciones': 'Contraindicaciones, precauciones, etc.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar formato de fecha
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
        self.fields['fecha_termino'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
        
        # Observaciones es opcional
        self.fields['observaciones'].required = False
        
        # Fecha de inicio por defecto es hoy
        if not self.instance.pk:
            self.initial['fecha_inicio'] = date.today()
    
    def clean_ficha_id(self):
        """Validar que la ficha exista"""
        pk = self.cleaned_data.get('ficha_id')
        try:
            ficha = FichaObstetrica.objects.get(pk=pk, activa=True)
        except (FichaObstetrica.DoesNotExist, TypeError, ValueError):
            raise ValidationError('Debe seleccionar una ficha válida.')
        
        self._ficha_obj = ficha
        return pk
    
    def clean_fecha_inicio(self):
        """Validar fecha de inicio"""
        fecha = self.cleaned_data.get('fecha_inicio')
        if fecha:
            if fecha > date.today():
                raise ValidationError('La fecha de inicio no puede ser futura.')
        return fecha
    
    def clean(self):
        """Validaciones cruzadas"""
        cleaned_data = super().clean()
        
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_termino = cleaned_data.get('fecha_termino')
        
        # Validar que fecha de término sea posterior a fecha de inicio
        if fecha_inicio and fecha_termino:
            if fecha_termino < fecha_inicio:
                raise ValidationError({
                    'fecha_termino': 'La fecha de término debe ser posterior o igual a la fecha de inicio.'
                })
            
            # Validar que el tratamiento no sea excesivamente largo
            dias_tratamiento = (fecha_termino - fecha_inicio).days
            if dias_tratamiento > 365:
                raise ValidationError({
                    'fecha_termino': 'El tratamiento no puede durar más de 365 días.'
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        """Guardar medicamento con la ficha correcta"""
        medicamento = super().save(commit=False)
        
        # Asignar la ficha desde el campo oculto
        ficha = getattr(self, '_ficha_obj', None)
        if ficha:
            medicamento.ficha = ficha
        
        if commit:
            medicamento.save()
        
        return medicamento


# ============================================
# FORMULARIO: EDITAR MEDICAMENTO FICHA
# ============================================
class EditarMedicamentoFichaForm(MedicamentoFichaForm):
    """Formulario para editar medicamentos existentes"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # En edición, la ficha no se puede cambiar
        if self.instance and self.instance.pk:
            self.fields['ficha_id'].widget = forms.HiddenInput()


# ============================================
# FORMULARIO: SUSPENDER MEDICAMENTO
# ============================================
class SuspenderMedicamentoForm(forms.Form):
    """Formulario para suspender un medicamento"""
    
    motivo_suspension = forms.CharField(
        label="Motivo de Suspensión",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describa el motivo de la suspensión',
            'required': True
        })
    )
    
    def clean_motivo_suspension(self):
        """Validar que el motivo no esté vacío"""
        motivo = self.cleaned_data.get('motivo_suspension')
        if not motivo or motivo.strip() == '':
            raise ValidationError('Debe especificar el motivo de la suspensión.')
        return motivo.strip()