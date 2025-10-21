from django.db import models
from utilidad.rut_validator import validar_rut, normalizar_rut, validar_rut_chileno

# ============================================
# MODELO BASE: PERSONA
# ============================================
class Persona(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]

    Rut = models.CharField(
        max_length=100,
        unique=True,
        validators=[validar_rut_chileno],
        verbose_name="RUT",
        help_text="Ingrese RUT de la persona (formato: 12345678-9)"
    )
    Nombre = models.CharField(max_length=100, verbose_name="Nombre")
    Apellido_Paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    Apellido_Materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    Sexo = models.CharField(max_length=100, choices=SEXO_CHOICES, verbose_name="Sexo")
    Fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    Telefono = models.CharField(max_length=100, verbose_name="Telefono", blank=True)
    Direccion = models.CharField(max_length=100, verbose_name="Direccion", blank=True)
    Email = models.CharField(max_length=100, verbose_name="Email", blank=True)
    Activo = models.BooleanField(default=True, verbose_name="Activo")

    def save(self, *args, **kwargs):
        if self.Rut:
            self.Rut = normalizar_rut(self.Rut)
            validar_rut_chileno(self.Rut)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.Nombre} {self.Apellido_Paterno} {self.Apellido_Materno} - {self.Rut}"

# ============================================
# MODELO MÉDICO
# ============================================
class Medico(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Obstetricia General', 'Obstetricia General'),
        ('Ginecología', 'Ginecología'),
        ('Medicina Materno Fetal', 'Medicina Materno Fetal'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]

    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    Registro_medico = models.CharField(max_length=100, unique=True)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno} - {self.Especialidad}"

# ============================================
# MODELO PACIENTE
# ============================================
class Paciente(models.Model):
    """Rol de Paciente vinculado a Persona"""
    
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERA', 'Soltera'),
        ('CASADA', 'Casada'),
        ('CONVIVIENTE', 'Conviviente'),
        ('DIVORCIADA', 'Divorciada'),
        ('VIUDA', 'Viuda'),
    ]
    
    PREVISION_CHOICES = [
        ('FONASA_A', 'FONASA A'),
        ('FONASA_B', 'FONASA B'),
        ('FONASA_C', 'FONASA C'),
        ('FONASA_D', 'FONASA D'),
        ('ISAPRE', 'Isapre'),
        ('PARTICULAR', 'Particular'),
    ]
    
    # Relación OneToOne con Persona
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='paciente',
        primary_key=True
    )
    
    # Datos específicos de Paciente
    Edad = models.PositiveSmallIntegerField(
        help_text="Edad entre 12 y 60 años"
    )
    Estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES)
    Previcion = models.CharField("Previsión", max_length=20, choices=PREVISION_CHOICES)
    
    Acompañante = models.CharField(max_length=120, blank=True)
    Contacto_emergencia = models.CharField(max_length=30, blank=True)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Edad and (self.Edad < 12 or self.Edad > 60):
            raise ValidationError({'Edad': 'La edad debe estar entre 12 y 60 años.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Paciente: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno} ({self.persona.Rut})"
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

# ============================================
# MODELO MATRONA
# ============================================
class Matrona(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Atención del Parto', 'Atención del Parto'),
        ('Control Prenatal', 'Control Prenatal'),
        ('Neonatología', 'Neonatología'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]

    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    Registro_medico = models.CharField(max_length=100, unique=True)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Matrona: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno}"


# ============================================
# MODELO TENS
# ============================================
class Tens(models.Model):
    NIVEL_CHOICES = [
        ('Preparto', 'Preparto'),
        ('Parto', 'Parto'),
        ('Puerperio', 'Puerperio'),
        ('Neonatología', 'Neonatología'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]
    CERTIFICACION_CHOICES = [
        ('SVB', 'Soporte Vital Básico'),
        ('Parto Normal', 'Certificación en Parto Normal'),
    ]

    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Nivel = models.CharField(max_length=100, choices=NIVEL_CHOICES)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Certificaciones = models.CharField(max_length=100, choices=CERTIFICACION_CHOICES)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"TENS: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno} - {self.Nivel}"
