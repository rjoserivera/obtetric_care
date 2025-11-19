from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona
from utilidad.rut_validator import validar_rut_chileno, normalizar_rut, RutValidator
from datetime import date


class PersonaForm(forms.ModelForm):
    rut_cuerpo = forms.CharField(
        max_length=12,
        required=True,
        label='RUT (sin dígito verificador)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'maxlength': '12',
            'pattern': '[0-9.]*',
            'title': 'Ingrese solo números'
        })
    )
    
    rut_dv = forms.CharField(
        max_length=1,
        required=True,
        label='DV',
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'K',
            'maxlength': '1',
            'style': 'text-transform: uppercase;'
        })
    )
    
    class Meta:
        model = Persona
        fields = [
            'Nombre', 'Apellido_Paterno', 'Apellido_Materno',
            'Fecha_nacimiento', 'Sexo', 'Telefono', 'Direccion',
            'Email', 'Inmigrante', 'Nacionalidad', 'Pueblos_originarios',
            'Discapacidad', 'Tipo_de_Discapacidad', 'Privada_de_Libertad',
            'Trans_masculino', 'Observaciones', 'Activo'
        ]
        
        widgets = {
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres'
            }),
            'Apellido_Paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido Paterno'
            }),
            'Apellido_Materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido Materno'
            }),
            'Fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': date.today().isoformat()
            }),
            'Sexo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678',
                'pattern': '[0-9+]{8,12}',
                'title': 'Ingrese un número de teléfono válido'
            }),
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle Ejemplo #123, Comuna'
            }),
            'Email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'Inmigrante': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Nacionalidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Pueblos_originarios': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Discapacidad': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_Discapacidad'
            }),
            'Tipo_de_Discapacidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especifique tipo de discapacidad',
                'id': 'id_Tipo_de_Discapacidad'
            }),
            'Privada_de_Libertad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Trans_masculino': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Información adicional relevante...'
            }),
            'Activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk and self.instance.Rut:
            rut_separado = RutValidator.separar_rut(self.instance.Rut)
            self.initial['rut_cuerpo'] = rut_separado['cuerpo']
            self.initial['rut_dv'] = rut_separado['dv']
        
        self.fields['Apellido_Materno'].required = False
        self.fields['Email'].required = False
        self.fields['Direccion'].required = False
        self.fields['Observaciones'].required = False
        self.fields['Tipo_de_Discapacidad'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        
        rut_cuerpo = cleaned_data.get('rut_cuerpo', '').replace('.', '').replace(' ', '')
        rut_dv = cleaned_data.get('rut_dv', '').upper()
        
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            
            if not validar_rut_chileno(rut_completo):
                raise ValidationError({
                    'rut_cuerpo': 'El RUT ingresado no es válido.',
                    'rut_dv': 'El dígito verificador no corresponde.'
                })
            
            rut_normalizado = normalizar_rut(rut_completo)
            
            if self.instance.pk:
                if Persona.objects.filter(Rut=rut_normalizado).exclude(pk=self.instance.pk).exists():
                    raise ValidationError({
                        'rut_cuerpo': 'Ya existe una persona con este RUT.'
                    })
            else:
                if Persona.objects.filter(Rut=rut_normalizado).exists():
                    raise ValidationError({
                        'rut_cuerpo': 'Ya existe una persona con este RUT.'
                    })
            
            cleaned_data['Rut'] = rut_normalizado
        
        fecha_nac = cleaned_data.get('Fecha_nacimiento')
        if fecha_nac and fecha_nac > date.today():
            raise ValidationError({
                'Fecha_nacimiento': 'La fecha de nacimiento no puede ser futura.'
            })
        
        discapacidad = cleaned_data.get('Discapacidad')
        tipo_discapacidad = cleaned_data.get('Tipo_de_Discapacidad')
        
        if discapacidad == 'Si' and not tipo_discapacidad:
            raise ValidationError({
                'Tipo_de_Discapacidad': 'Debe especificar el tipo de discapacidad.'
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        persona = super().save(commit=False)
        
        rut_cuerpo = self.cleaned_data.get('rut_cuerpo', '').replace('.', '').replace(' ', '')
        rut_dv = self.cleaned_data.get('rut_dv', '').upper()
        
        if rut_cuerpo and rut_dv:
            persona.Rut = normalizar_rut(f"{rut_cuerpo}-{rut_dv}")
        
        if commit:
            persona.save()
        
        return persona
