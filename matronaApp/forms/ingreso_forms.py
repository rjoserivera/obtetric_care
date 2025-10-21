from django import forms
from django.core.exceptions import ValidationError

from matronaApp.models import IngresoPaciente, Paciente


# Construimos "exclude" dinámicamente: siempre 'paciente' y, si existe en el modelo, 'numero_ficha'
_EXCLUDE = ["paciente"]
try:
    if any(f.name == "numero_ficha" for f in IngresoPaciente._meta.get_fields()):
        _EXCLUDE.append("numero_ficha")
except Exception:
    # Si algo falla al introspectar, no agregamos nada extra.
    pass


class IngresoPacienteForm(forms.ModelForm):
    """
    Form de Ingreso:
    - No expone 'paciente' (lo asignamos con paciente_id oculto).
    - Opcionalmente oculta 'numero_ficha' si el modelo lo autogenera.
    - No fija nombres de campos más allá de los comunes; el template puede
      renderizar {{ form }} o cada campo manualmente.
    """
    paciente_id = forms.IntegerField(required=True, widget=forms.HiddenInput())

    class Meta:
        model = IngresoPaciente
        exclude = tuple(_EXCLUDE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajustes de UX si estos campos existen en el modelo/form:
        if "motivo_consulta" in self.fields:
            self.fields["motivo_consulta"].widget = forms.Textarea(attrs={"rows": 3})
        if "observaciones" in self.fields:
            self.fields["observaciones"].widget = forms.Textarea(attrs={"rows": 3})

        # Si tu modelo usa un campo numérico para semanas de EG (por ejemplo 'semanas'):
        if "semanas" in self.fields:
            self.fields["semanas"].widget = forms.NumberInput(attrs={"min": 1, "max": 42})

    def clean_paciente_id(self):
        pk = self.cleaned_data.get("paciente_id")
        try:
            paciente = Paciente.objects.get(pk=pk)
        except (Paciente.DoesNotExist, TypeError, ValueError):
            raise ValidationError("Debe seleccionar un paciente válido.")
        # Guardamos el objeto para usarlo en save()
        self._paciente_obj = paciente
        return pk

    def save(self, commit=True):
        obj = super().save(commit=False)

        paciente = getattr(self, "_paciente_obj", None)
        if paciente is None:
            # Fallback por si alguien modificó cleaned_data entre validación y save
            pk = self.cleaned_data.get("paciente_id")
            try:
                paciente = Paciente.objects.get(pk=pk)
            except Paciente.DoesNotExist:
                raise ValidationError("Debe seleccionar un paciente válido.")

        obj.paciente = paciente

        # Si 'numero_ficha' se autogenera en el modelo, no hay que hacer nada aquí.
        if commit:
            obj.save()
        return obj


