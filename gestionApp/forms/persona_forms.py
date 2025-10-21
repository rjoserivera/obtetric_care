"""
Formularios para la gestión de personas (datos básicos)
"""
from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona
from utilidad.rut_validator import validar_rut_chileno, normalizar_rut
from datetime import date


class PersonaForm(forms.ModelForm):
    """Formulario para registro de personas (datos básicos)"""
    
    class Meta:
        model = Persona
        fields = [
            'Rut',
            'Nombre',
            'Apellido_Paterno',
            'Apellido_Materno',
            'Sexo',
            'Fecha_nacimiento',
            'Telefono',
            'Direccion',
            'Email'
        ]
        widgets = {
            'Rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9',
                'maxlength': '12',
                'id': 'rut_input'
            }),
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre',
                'required': True
            }),
            'Apellido_Paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido paterno',
                'required': True
            }),
            'Apellido_Materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido materno',
                'required': True
            }),
            'Sexo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            }),
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle, número, comuna'
            }),
            'Email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            })
        }
        labels = {
            'Rut': 'RUT',
            'Nombre': 'Nombre',
            'Apellido_Paterno': 'Apellido Paterno',
            'Apellido_Materno': 'Apellido Materno',
            'Sexo': 'Sexo',
            'Fecha_nacimiento': 'Fecha de Nacimiento',
            'Telefono': 'Teléfono',
            'Direccion': 'Dirección',
            'Email': 'Correo Electrónico'
        }

    def clean_Rut(self):
        """Validación y normalización del RUT"""
        rut = self.cleaned_data.get('Rut')
        if rut:
            try:
                rut_normalizado = normalizar_rut(rut)
                validar_rut_chileno(rut_normalizado)
                
                # Verificar duplicados solo al crear
                if not self.instance.pk:
                    if Persona.objects.filter(Rut=rut_normalizado).exists():
                        raise ValidationError('Este RUT ya está registrado.')
                
                return rut_normalizado
            except ValidationError as e:
                raise ValidationError(str(e))
        return rut

    def clean_Fecha_nacimiento(self):
        """Validar que la fecha de nacimiento sea coherente"""
        fecha = self.cleaned_data.get('Fecha_nacimiento')
        if fecha:
            hoy = date.today()
            edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
            
            if edad < 0:
                raise ValidationError('La fecha de nacimiento no puede ser futura.')
            if edad > 120:
                raise ValidationError('La fecha de nacimiento no es válida.')
        
        return fecha


class BuscarPersonaForm(forms.Form):
    """Formulario para búsqueda rápida de personas por RUT"""
    
    rut = forms.CharField(
        max_length=12,
        label="Buscar por RUT",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'buscar_rut',
            'autocomplete': 'off'
        })
    )
    
    def clean_rut(self):
        """Normalizar RUT para búsqueda"""
        rut = self.cleaned_data.get('rut')
        if rut:
            return normalizar_rut(rut)
        return rut
