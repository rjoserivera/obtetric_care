from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona
from matronaApp.models import Paciente
from utilidad.rut_validator import normalizar_rut, RutValidator
from datetime import date


class PacienteForm(forms.ModelForm):
    rut_persona_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT de la Persona',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'pattern': '[0-9]{7,8}'
        }),
        help_text='Ingrese el RUT de la persona a vincular como paciente'
    )
    
    rut_persona_dv = forms.CharField(
        max_length=1,
        required=True,
        label='DV',
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'K',
            'maxlength': '1',
            'pattern': '[0-9Kk]',
            'style': 'text-transform: uppercase;'
        })
    )
    
    class Meta:
        model = Paciente
        fields = [
            'Estado_civil',
            'Previcion',
            'paridad',
            'Ductus_Venosus',
            'control_prenatal',
            'consultorio',
            'imc',
            'alergias',
            'observaciones',
            'Activo'
        ]
        
        widgets = {
            'Estado_civil': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Previcion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'paridad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'Ductus_Venosus': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Valor del Ductus Venosus'
            }),
            'control_prenatal': forms.Select(attrs={
                'class': 'form-select'
            }),
            'consultorio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del consultorio'
            }),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '10',
                'max': '60',
                'placeholder': '25.5'
            }),
            'alergias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Especifique alergias conocidas...'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Información médica adicional relevante...'
            }),
            'Activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'Estado_civil': 'Estado Civil',
            'Previcion': 'Previsión de Salud',
            'paridad': 'Paridad',
            'Ductus_Venosus': 'Ductus Venosus',
            'control_prenatal': '¿Tuvo Control Prenatal?',
            'consultorio': 'Consultorio de Atención',
            'imc': 'IMC (Índice de Masa Corporal)',
            'alergias': 'Alergias',
            'observaciones': 'Observaciones Médicas',
            'Activo': '¿Paciente Activo?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk and hasattr(self.instance, 'persona'):
            datos_rut = RutValidator.separar_rut(self.instance.persona.Rut)
            self.fields['rut_persona_cuerpo'].initial = datos_rut['cuerpo']
            self.fields['rut_persona_dv'].initial = datos_rut['dv']
            
            self.fields['rut_persona_cuerpo'].disabled = True
            self.fields['rut_persona_dv'].disabled = True
            self.fields['rut_persona_cuerpo'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_dv'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_cuerpo'].help_text = 'El RUT no se puede modificar'
        
        self.fields['alergias'].required = False
        self.fields['observaciones'].required = False
        self.fields['paridad'].required = False
        self.fields['Ductus_Venosus'].required = False
        self.fields['consultorio'].required = False
        self.fields['imc'].required = False
    
    def clean_rut_persona_cuerpo(self):
        rut_cuerpo = self.cleaned_data.get('rut_persona_cuerpo', '').strip()
        
        if not rut_cuerpo:
            raise ValidationError('El RUT de la persona es obligatorio.')
        
        if not rut_cuerpo.isdigit():
            raise ValidationError('El RUT debe contener solo números.')
        
        if len(rut_cuerpo) < 7 or len(rut_cuerpo) > 8:
            raise ValidationError('El RUT debe tener 7 u 8 dígitos.')
        
        return rut_cuerpo
    
    def clean_rut_persona_dv(self):
        rut_dv = self.cleaned_data.get('rut_persona_dv', '').strip().upper()
        
        if not rut_dv:
            raise ValidationError('El dígito verificador es obligatorio.')
        
        if len(rut_dv) != 1:
            raise ValidationError('El dígito verificador debe ser un solo carácter.')
        
        if not (rut_dv.isdigit() or rut_dv == 'K'):
            raise ValidationError('El dígito verificador debe ser un número o K.')
        
        return rut_dv
    
    def clean(self):
        cleaned_data = super().clean()
        
        if not self.instance.pk:
            rut_cuerpo = cleaned_data.get('rut_persona_cuerpo')
            rut_dv = cleaned_data.get('rut_persona_dv')
            
            if rut_cuerpo and rut_dv:
                rut_completo = f"{rut_cuerpo}-{rut_dv}"
                rut_normalizado = normalizar_rut(rut_completo)
                
                try:
                    persona = Persona.objects.get(Rut=rut_normalizado)
                    
                    if Paciente.objects.filter(persona=persona).exists():
                        raise ValidationError({
                            'rut_persona_cuerpo': (
                                'Esta persona ya está registrada como paciente. '
                                'No se puede duplicar el registro.'
                            )
                        })
                    
                    self._persona_obj = persona
                    
                except Persona.DoesNotExist:
                    raise ValidationError({
                        'rut_persona_cuerpo': (
                            'No existe una persona registrada con este RUT. '
                            'Registre primero los datos básicos de la persona.'
                        )
                    })
        
        imc = cleaned_data.get('imc')
        if imc and (imc < 10 or imc > 60):
            raise ValidationError({
                'imc': 'El IMC debe estar entre 10 y 60.'
            })
        
        paridad = cleaned_data.get('paridad')
        if paridad and paridad < 0:
            raise ValidationError({
                'paridad': 'La paridad no puede ser negativa.'
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        paciente = super().save(commit=False)
        
        if not self.instance.pk:
            persona = getattr(self, '_persona_obj', None)
            if persona:
                paciente.persona = persona
        
        if commit:
            paciente.save()
        
        return paciente
