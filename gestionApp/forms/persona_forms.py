from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona
from utilidad.rut_validator import validar_rut_chileno, normalizar_rut
from datetime import date


# ============================================
# FORMULARIO: PERSONA
# ============================================
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
            'Email',
            'Inmigrante',
            'Nacionalidad',
            'Pueblos_originarios',
            'Discapacidad',
            'Tipo_de_Discapacidad',
            'Privada_de_Libertad',
            'Trans_Masculino'
        ]
        widgets = {
            'Rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9', 'maxlength': '12', 'id': 'rut_input'}),
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre', 'required': True}),
            'Apellido_Paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese apellido paterno', 'required': True}),
            'Apellido_Materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese apellido materno', 'required': True}),
            'Sexo': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'Fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'Telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle, número, comuna'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'Inmigrante': forms.Select(attrs={'class': 'form-select'}),
            'Nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            'Pueblos_originarios': forms.Select(attrs={'class': 'form-select'}),
            'Discapacidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_discapacidad'}),
            'Tipo_de_Discapacidad': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_tipo_discapacidad', 'placeholder': 'Especificar tipo de discapacidad'}),
            'Privada_de_Libertad': forms.Select(attrs={'class': 'form-select'}),
            'Trans_Masculino': forms.Select(attrs={'class': 'form-select'})
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
            'Email': 'Correo Electrónico',
            'Inmigrante': 'Inmigrante',
            'Nacionalidad': 'Nacionalidad',
            'Pueblos_originarios': 'Pueblos Originarios',
            'Discapacidad': 'Discapacidad',
            'Tipo_de_Discapacidad': 'Tipo de Discapacidad',
            'Privada_de_Libertad': 'Privada de Libertad',
            'Trans_Masculino': 'Trans Masculino'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Tipo_de_Discapacidad'].required = False

    def clean_Rut(self):
        """Validación y normalización del RUT"""
        rut = self.cleaned_data.get('Rut')
        if rut:
            try:
                rut_normalizado = normalizar_rut(rut)
                validar_rut_chileno(rut_normalizado)
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

    def clean(self):
        """Validación del campo condicional Tipo_de_Discapacidad"""
        cleaned_data = super().clean()
        discapacidad = cleaned_data.get('Discapacidad')
        tipo_discapacidad = cleaned_data.get('Tipo_de_Discapacidad')
        if discapacidad == 'Si':
            if not tipo_discapacidad or tipo_discapacidad.strip() == '':
                raise ValidationError({'Tipo_de_Discapacidad': 'Debe especificar el tipo de discapacidad si seleccionó "Sí"'})
        if discapacidad == 'No':
            cleaned_data['Tipo_de_Discapacidad'] = None
        return cleaned_data


# ============================================
# FORMULARIO: BUSCAR PERSONA
# ============================================
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
















