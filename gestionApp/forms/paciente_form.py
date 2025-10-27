from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Paciente
from utilidad.rut_validator import normalizar_rut


# ============================================
# FORMULARIO: PACIENTE
# ============================================
class PacienteForm(forms.ModelForm):
    """Formulario para vincular paciente a una persona existente"""

    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_paciente'
        }),
        help_text="Ingrese el RUT de la persona a vincular como paciente"
    )
    
    peso_kg = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label="Peso (kg)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 65.5',
            'min': '30',
            'max': '200',
            'step': '0.1',
            'id': 'id_peso'
        }),
        help_text="Peso en kilogramos para calcular IMC"
    )
    
    talla_cm = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label="Talla (cm)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 165',
            'min': '120',
            'max': '220',
            'step': '0.1',
            'id': 'id_talla'
        }),
        help_text="Estatura en centímetros para calcular IMC"
    )

    class Meta:
        model = Paciente
        fields = [
            'rut_persona',
            'Estado_civil',
            'Previcion',
            'paridad',
            'Ductus_Venosus',
            'control_prenatal',
            'Consultorio',
            'peso_kg',
            'talla_cm',
            'imc',
            'Preeclampsia_Severa',
            'Eclampsia',
            'Sepsis_o_Infeccion_SiST',
            'Infeccion_Ovular_o_Corioamnionitis',
            'Acompañante',
            'Contacto_emergencia'
        ]
        widgets = {
            'Estado_civil': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'Previcion': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'paridad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: G3P2A0'}),
            'Ductus_Venosus': forms.Select(attrs={'class': 'form-select'}),
            'control_prenatal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Consultorio': forms.Select(attrs={'class': 'form-select'}),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'id': 'id_imc',
                'placeholder': 'Se calcula automáticamente'
            }),
            'Preeclampsia_Severa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Eclampsia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Sepsis_o_Infeccion_SiST': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Infeccion_Ovular_o_Corioamnionitis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Acompañante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'Contacto_emergencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
        }
        labels = {
            'Estado_civil': 'Estado Civil',
            'Previcion': 'Previsión',
            'paridad': 'Paridad',
            'Ductus_Venosus': 'Ductus Venosus',
            'control_prenatal': '¿Tuvo Control Prenatal?',
            'Consultorio': 'Consultorio de Origen',
            'imc': 'IMC (Índice de Masa Corporal)',
            'Preeclampsia_Severa': 'Preeclampsia Severa',
            'Eclampsia': 'Eclampsia',
            'Sepsis_o_Infeccion_SiST': 'Sepsis o Infección Sistémica Grave',
            'Infeccion_Ovular_o_Corioamnionitis': 'Infección Ovular o Corioamnionitis',
            'Acompañante': 'Acompañante',
            'Contacto_emergencia': 'Contacto de Emergencia'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imc'].required = False
        self.fields['paridad'].required = False
        self.fields['Acompañante'].required = False
        self.fields['Contacto_emergencia'].required = False

    def clean_rut_persona(self):
        """Validar que la persona exista y no sea ya paciente"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                if hasattr(persona, 'paciente'):
                    raise ValidationError('Esta persona ya está registrada como paciente.')
                return persona
            except Persona.DoesNotExist:
                raise ValidationError('No existe una persona registrada con este RUT. Por favor, registre primero los datos básicos de la persona.')
        return rut

    def clean_peso_kg(self):
        """Validar peso"""
        peso = self.cleaned_data.get('peso_kg')
        if peso is not None:
            if peso < 30 or peso > 200:
                raise ValidationError('El peso debe estar entre 30 y 200 kg.')
        return peso

    def clean_talla_cm(self):
        """Validar talla"""
        talla = self.cleaned_data.get('talla_cm')
        if talla is not None:
            if talla < 120 or talla > 220:
                raise ValidationError('La talla debe estar entre 120 y 220 cm.')
        return talla

    def clean(self):
        """Validaciones cruzadas y cálculo de IMC"""
        cleaned_data = super().clean()
        peso = cleaned_data.get('peso_kg')
        talla = cleaned_data.get('talla_cm')
        
        # Calcular IMC si hay peso y talla
        if peso and talla:
            talla_m = talla / 100
            imc = round(peso / (talla_m ** 2), 2)
            if imc < 10 or imc > 60:
                raise ValidationError({'imc': f'El IMC calculado ({imc}) está fuera del rango válido (10-60).'})
            cleaned_data['imc'] = imc
        
        return cleaned_data

    def save(self, commit=True):
        """Guardar paciente con persona asociada"""
        paciente = super().save(commit=False)
        persona = self.cleaned_data.get('rut_persona')
        if isinstance(persona, Persona):
            paciente.persona = persona
        
        if commit:
            paciente.save()
        
        return paciente


# ============================================
# FORMULARIO: BUSCAR PACIENTE
# ============================================
class BuscarPacienteForm(forms.Form):
    """Formulario para búsqueda rápida de pacientes por RUT"""
    
    rut = forms.CharField(
        max_length=12,
        label="Buscar Paciente por RUT",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'buscar_rut_paciente',
            'autocomplete': 'off'
        })
    )
    
    def clean_rut(self):
        """Normalizar RUT para búsqueda"""
        rut = self.cleaned_data.get('rut')
        if rut:
            return normalizar_rut(rut)
        return rut