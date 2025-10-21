from django.db import models
from matronaApp.models import FichaObstetrica, MedicamentoFicha
from gestionApp.models import Tens, Paciente

from django.utils import timezone

class RegistroTens(models.Model):
    TURNO_CHOICES = [
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
    ]
    
    ficha = models.ForeignKey(FichaObstetrica, on_delete=models.CASCADE, related_name='registros_tens')
    tens_responsable = models.ForeignKey(Tens, on_delete=models.PROTECT, related_name='registros_signos_vitales', null=True, blank=True)
    fecha = models.DateField(blank=True, null=True)
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES, blank=True, null=True)

    # Signos Vitales
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    frecuencia_cardiaca = models.PositiveBigIntegerField(blank=True, null=True)
    presion_arterial = models.CharField(max_length=20, blank=True, null=True)
    frecuencia_respiratoria = models.PositiveBigIntegerField(blank=True, null=True)
    saturacion_oxigeno = models.PositiveBigIntegerField(blank=True, null=True)

    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registro TENS - {self.ficha.numero_ficha} - {self.fecha}"
    
    class Meta:
        ordering = ['-fecha', '-fecha_registro']


# tratamientos por f

class Tratamiento_aplicado(models.Model):
    VIA_ADMINISTRACION_CHOICES = [
        ('VO', 'Oral (VO)'),
        ('IM', 'Intramuscular (IM)'),
        ('IV', 'Intravenosa (IV)'),
        ('TP', 'Tópica'),
        ('OT', 'Otras'),
    ]

    # 🔹 Relaciones
    tens = models.ForeignKey(Tens, on_delete=models.PROTECT, related_name='tratamientos_aplicados')
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='tratamientos_aplicados')
    ficha = models.ForeignKey(FichaObstetrica, on_delete=models.CASCADE, related_name='tratamientos_tens')
    medicamento_ficha = models.ForeignKey(MedicamentoFicha, on_delete=models.SET_NULL, null=True, blank=True)
    

    # 🔹 Datos clínicos
    nombre_medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=100, blank=True, null=True)
    via_administracion = models.CharField(max_length=2, choices=VIA_ADMINISTRACION_CHOICES)
    fecha_aplicacion = models.DateTimeField(default=timezone.now)
    hora_aplicacion = models.TimeField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_medicamento} ({self.paciente.persona.Nombre})"

    class Meta:
        verbose_name = "Tratamiento Aplicado"
        verbose_name_plural = "Tratamientos Aplicados"