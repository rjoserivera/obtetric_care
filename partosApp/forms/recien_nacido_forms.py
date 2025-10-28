from django import forms
from django.core.exceptions import ValidationError
from partosApp.models import RegistroRecienNacido, RegistroParto


class RegistroRecienNacidoForm(forms.ModelForm):
    """
    Formulario completo para registrar al recién nacido
    """
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'registro_parto',
            # Datos del RN
            'sexo',
            'peso',
            'talla',
            'ligadura_tardia_cordon',
            'apgar_1_minuto',
            'apgar_5_minutos',
            'fecha_nacimiento',
            # Apego
            'tiempo_apego',
            'apego_canguro',
            # Acompañamiento
            'acompanamiento_preparto',
            'acompanamiento_parto',
            'acompanamiento_rn',
            'motivo_parto_no_acompanado',
            'persona_acompanante',
            'acompanante_secciona_cordon',
        ]
        widgets = {
            'registro_parto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            # Datos del RN
            'sexo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '500',
                'max': '8000',
                'placeholder': 'Gramos',
                'required': True
            }),
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '30',
                'max': '70',
                'placeholder': 'Centímetros',
                'required': True
            }),
            'ligadura_tardia_cordon': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'apgar_1_minuto': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'required': True
            }),
            'apgar_5_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'required': True
            }),
            'fecha_nacimiento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            # Apego
            'tiempo_apego': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Minutos'
            }),
            'apego_canguro': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Acompañamiento
            'acompanamiento_preparto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'acompanamiento_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'acompanamiento_rn': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'motivo_parto_no_acompanado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'persona_acompanante': forms.Select(attrs={
                'class': 'form-select'
            }),
            'acompanante_secciona_cordon': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'registro_parto': 'Registro de Parto',
            'sexo': 'Sexo del Recién Nacido',
            'peso': 'Peso (gramos)',
            'talla': 'Talla (cm)',
            'ligadura_tardia_cordon': 'Ligadura Tardía del Cordón (> 1 minuto)',
            'apgar_1_minuto': 'Apgar al 1er Minuto',
            'apgar_5_minutos': 'Apgar a los 5 Minutos',
            'fecha_nacimiento': 'Fecha y Hora de Nacimiento',
            'tiempo_apego': 'Tiempo de Apego (minutos)',
            'apego_canguro': 'Apego Canguro',
            'acompanamiento_preparto': 'Acompañamiento en Preparto',
            'acompanamiento_parto': 'Acompañamiento en Parto',
            'acompanamiento_rn': 'Acompañamiento con RN',
            'motivo_parto_no_acompanado': 'Motivo Parto NO Acompañado',
            'persona_acompanante': 'Persona Acompañante',
            'acompanante_secciona_cordon': 'Acompañante Secciona Cordón',
        }
        help_texts = {
            'peso': 'Peso al nacer en gramos (500-8000)',
            'talla': 'Longitud del recién nacido en centímetros',
            'apgar_1_minuto': 'Puntaje de 0 a 10',
            'apgar_5_minutos': 'Puntaje de 0 a 10',
        }
    
    def __init__(self, *args, **kwargs):
        # Permitir pasar el registro_parto como parámetro
        registro_parto = kwargs.pop('registro_parto', None)
        super().__init__(*args, **kwargs)
        
        # Si se pasa registro_parto, preseleccionarlo
        if registro_parto:
            self.fields['registro_parto'].initial = registro_parto
            self.fields['registro_parto'].widget = forms.HiddenInput()
        
        # Filtrar solo registros activos
        self.fields['registro_parto'].queryset = RegistroParto.objects.filter(
            activo=True
        ).select_related('ficha__paciente__persona')
        
        # Campos opcionales
        self.fields['tiempo_apego'].required = False
    
    def clean(self):
        """Validaciones"""
        cleaned_data = super().clean()
        
        # Validar Apgar
        apgar_1 = cleaned_data.get('apgar_1_minuto')
        apgar_5 = cleaned_data.get('apgar_5_minutos')
        
        if apgar_1 is not None and (apgar_1 < 0 or apgar_1 > 10):
            raise ValidationError({
                'apgar_1_minuto': 'El Apgar debe estar entre 0 y 10.'
            })
        
        if apgar_5 is not None and (apgar_5 < 0 or apgar_5 > 10):
            raise ValidationError({
                'apgar_5_minutos': 'El Apgar debe estar entre 0 y 10.'
            })
        
        # Validar peso
        peso = cleaned_data.get('peso')
        if peso is not None:
            if peso < 500:
                raise ValidationError({
                    'peso': 'El peso mínimo es 500 gramos.'
                })
            if peso > 8000:
                raise ValidationError({
                    'peso': 'El peso máximo es 8000 gramos.'
                })
        
        # Validar talla
        talla = cleaned_data.get('talla')
        if talla is not None:
            if talla < 30:
                raise ValidationError({
                    'talla': 'La talla mínima es 30 cm.'
                })
            if talla > 70:
                raise ValidationError({
                    'talla': 'La talla máxima es 70 cm.'
                })
        
        return cleaned_data


class DatosRecienNacidoForm(forms.ModelForm):
    """
    Formulario solo con datos básicos del RN
    (para un registro rápido inicial)
    """
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'sexo',
            'peso',
            'talla',
            'apgar_1_minuto',
            'apgar_5_minutos',
            'fecha_nacimiento',
        ]
        widgets = {
            'sexo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '500',
                'max': '8000',
                'placeholder': 'Gramos',
                'required': True
            }),
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '30',
                'max': '70',
                'placeholder': 'Centímetros',
                'required': True
            }),
            'apgar_1_minuto': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'required': True
            }),
            'apgar_5_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'required': True
            }),
            'fecha_nacimiento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
        }


class ApegoAcompanamientoForm(forms.ModelForm):
    """
    Formulario solo para apego y acompañamiento
    (completar después del registro inicial)
    """
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'ligadura_tardia_cordon',
            'tiempo_apego',
            'apego_canguro',
            'acompanamiento_preparto',
            'acompanamiento_parto',
            'acompanamiento_rn',
            'motivo_parto_no_acompanado',
            'persona_acompanante',
            'acompanante_secciona_cordon',
        ]
        widgets = {
            'ligadura_tardia_cordon': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tiempo_apego': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Minutos'
            }),
            'apego_canguro': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'acompanamiento_preparto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'acompanamiento_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'acompanamiento_rn': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'motivo_parto_no_acompanado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'persona_acompanante': forms.Select(attrs={
                'class': 'form-select'
            }),
            'acompanante_secciona_cordon': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }