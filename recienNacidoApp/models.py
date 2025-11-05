# recienNacidoApp/models.py
"""
Aplicación para gestionar el POST-PARTO
Contiene toda la información DESPUÉS del parto: RN, documentos, placenta
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class RegistroRecienNacido(models.Model):
    """
    Registro del recién nacido
    Se crea después del parto
    Contiene datos del RN, apego y acompañamiento
    """
    
    # ============================================
    # RELACIÓN
    # ============================================
    
    registro_parto = models.ForeignKey(
        'partosApp.RegistroParto',
        on_delete=models.CASCADE,
        related_name='recien_nacidos',
        verbose_name='Registro de Parto'
    )
    
    # ============================================
    # SECCIÓN 1: DATOS DEL RECIÉN NACIDO
    # ============================================
    
    SEXO_CHOICES = [
        ('MASCULINO', 'Masculino'),
        ('FEMENINO', 'Femenino'),
        ('INDETERMINADO', 'Indeterminado'),
    ]
    
    sexo = models.CharField(
        max_length=20,
        choices=SEXO_CHOICES,
        verbose_name='Sexo'
    )
    
    peso = models.IntegerField(
        validators=[MinValueValidator(500), MaxValueValidator(8000)],
        verbose_name='Peso (gramos)',
        help_text='Peso al nacer'
    )
    
    talla = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(70)],
        verbose_name='Talla (cm)',
        help_text='Longitud al nacer'
    )
    
    ligadura_tardia_cordon = models.BooleanField(
        default=False,
        verbose_name='Ligadura Tardía del Cordón (> 1 minuto)',
        help_text='¿Se hizo ligadura tardía?'
    )
    
    apgar_1_minuto = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar al Minuto',
        help_text='Puntaje al 1er minuto'
    )
    
    apgar_5_minutos = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar a los 5 Minutos',
        help_text='Puntaje a los 5 minutos'
    )
    
    fecha_nacimiento = models.DateTimeField(
        verbose_name='Fecha y Hora de Nacimiento',
        help_text='Momento exacto del nacimiento'
    )
    
    # ============================================
    # SECCIÓN 2: APEGO
    # ============================================
    
    tiempo_apego = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de Apego (minutos)',
        help_text='Duración del apego piel con piel'
    )
    
    apego_canguro = models.BooleanField(
        default=False,
        verbose_name='Apego Canguro',
        help_text='¿Se hizo método canguro?'
    )
    
    # ============================================
    # SECCIÓN 3: ACOMPAÑAMIENTO
    # ============================================
    
    acompanamiento_preparto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento Preparto'
    )
    
    acompanamiento_parto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento Parto'
    )
    
    acompanamiento_rn = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento RN'
    )
    
    # Motivo NO acompañado
    MOTIVO_NO_ACOMPANADO_CHOICES = [
        ('', '---'),
        ('NO_DESEA', 'NO DESEA'),
        ('NO_LLEGA', 'NO LLEGA'),
        ('URGENCIA', 'URGENCIA'),
        ('NO_TIENE', 'NO TIENE ACOMPAÑANTE'),
        ('RURALIDAD', 'RURALIDAD'),
        ('SIN_PASE', 'SIN PASE DE MOVILIDAD'),
    ]
    
    motivo_parto_no_acompanado = models.CharField(
        max_length=20,
        choices=MOTIVO_NO_ACOMPANADO_CHOICES,
        blank=True,
        verbose_name='Motivo Parto NO Acompañado'
    )
    
    # Persona acompañante
    PERSONA_ACOMPANANTE_CHOICES = [
        ('', '---'),
        ('PAREJA', 'PAREJA'),
        ('MADRE', 'MADRE'),
        ('PADRE', 'PADRE'),
        ('HERMANA', 'HERMANA'),
        ('AMIGA', 'AMIGA'),
        ('OTRO', 'OTRO'),
        ('NADIE', 'NADIE'),
    ]
    
    persona_acompanante = models.CharField(
        max_length=20,
        choices=PERSONA_ACOMPANANTE_CHOICES,
        blank=True,
        verbose_name='Persona Acompañante'
    )
    
    acompanante_secciona_cordon = models.BooleanField(
        default=False,
        verbose_name='Acompañante Secciona Cordón',
        help_text='¿El acompañante cortó el cordón?'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        ordering = ['-fecha_nacimiento']
        verbose_name = 'Registro de Recién Nacido'
        verbose_name_plural = 'Registros de Recién Nacidos'
        indexes = [
            models.Index(fields=['registro_parto', '-fecha_nacimiento']),
        ]
    
    def __str__(self):
        return f"RN {self.sexo} - {self.registro_parto.numero_registro} - {self.peso}g"
    
    def clasificacion_peso(self):
        """Clasifica el peso según OMS"""
        if self.peso < 2500:
            return "Bajo peso al nacer"
        elif self.peso <= 4000:
            return "Peso adecuado"
        else:
            return "Macrosómico"
    
    def estado_apgar(self):
        """Evalúa el estado según Apgar"""
        apgar_5 = self.apgar_5_minutos
        if apgar_5 >= 7:
            return "Normal"
        elif apgar_5 >= 4:
            return "Asfixia moderada"
        else:
            return "Asfixia severa"


class DocumentosParto(models.Model):
    """
    Documentos legales y administrativos del parto
    Se crean después del parto
    Incluye Ley Dominga, placenta y registro civil
    """
    
    # ============================================
    # RELACIÓN
    # ============================================
    
    registro_parto = models.OneToOneField(
        'partosApp.RegistroParto',
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name='Registro de Parto'
    )
    
    # ============================================
    # SECCIÓN 1: LEY N° 21.372 DOMINGA
    # ============================================
    
    recuerdos_entregados = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Recuerdos Entregados',
        help_text='Lista de recuerdos según Ley Dominga'
    )
    
    motivo_no_entrega_recuerdos = models.TextField(
        blank=True,
        verbose_name='Motivo de No Entrega',
        help_text='Justificación si no se entregaron'
    )
    
    # ============================================
    # SECCIÓN 2: PLACENTA
    # ============================================
    
    retira_placenta = models.BooleanField(
        default=False,
        verbose_name='Retira Placenta',
        help_text='¿La familia retira la placenta?'
    )
    
    estampado_placenta = models.BooleanField(
        default=False,
        verbose_name='Estampado de Placenta',
        help_text='¿Se hizo estampado?'
    )
    
    # ============================================
    # SECCIÓN 3: REGISTRO CIVIL
    # ============================================
    
    folio_valido = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Folio Válido',
        help_text='Número de folio del Registro Civil'
    )
    
    folios_nulos = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Folio/s Nulo/s',
        help_text='Folios anulados (si aplica)'
    )
    
    # ============================================
    # SECCIÓN 4: MANEJO DEL DOLOR NO FARMACOLÓGICO
    # ============================================
    
    manejo_dolor_no_farmacologico = models.TextField(
        blank=True,
        verbose_name='Manejo del Dolor No Farmacológico',
        help_text='Descripción de métodos usados'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Modificación'
    )
    
    class Meta:
        verbose_name = 'Documentos de Parto'
        verbose_name_plural = 'Documentos de Partos'
    
    def __str__(self):
        return f"Documentos - {self.registro_parto.numero_registro}"