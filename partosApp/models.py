# partosApp/models.py
"""
Aplicación para gestionar el PROCESO DE PARTO
Contiene toda la información DURANTE el parto
MODELO COMPLETO Y ACTUALIZADO
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class RegistroParto(models.Model):
    """
    Registro del proceso de parto
    Se crea durante el trabajo de parto
    Contiene TODO lo que sucede DURANTE el parto
    """
    
    # ============================================
    # RELACIONES
    # ============================================
    
    ficha = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.PROTECT,
        related_name='registros_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    ficha_ingreso = models.OneToOneField(
        'ingresoPartoApp.FichaParto',
        on_delete=models.PROTECT,
        related_name='registro_parto',
        null=True,
        blank=True,
        verbose_name='Ficha de Ingreso',
        help_text='Vincula con la ficha de ingreso'
    )
    
    numero_registro = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Registro',
        help_text='Se genera automáticamente: PARTO-000001'
    )
    
    # ============================================
    # FECHAS Y HORAS
    # ============================================
    
    fecha_hora_admision = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Admisión',
        help_text='Cuando ingresa para el parto'
    )
    
    fecha_hora_parto = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora del Parto',
        help_text='Momento exacto del nacimiento'
    )
    
    # ============================================
    # SECCIÓN 1: TRABAJO DE PARTO
    # ============================================
    
    # Edad Gestacional al momento del parto
    edad_gestacional_semanas = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(42)],
        verbose_name='Semanas de Embarazo',
        help_text='Semanas completas al momento del parto'
    )
    
    edad_gestacional_dias = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name='Días adicionales',
        help_text='Ej: 38 semanas y 4 días'
    )
    
    # Monitoreo
    monitor_ttc = models.BooleanField(
        default=False,
        verbose_name='Monitor TTC',
        help_text='¿Se usó monitor de contracciones?'
    )
    
    induccion = models.BooleanField(
        default=False,
        verbose_name='Inducción',
        help_text='¿Se indujo el parto?'
    )
    
    aceleracion_correccion = models.BooleanField(
        default=False,
        verbose_name='Aceleración o Corrección',
        help_text='¿Se aceleró el trabajo de parto?'
    )
    
    # 🆕 CAMPO AGREGADO: Número de Tactos Vaginales
    numero_tactos_vaginales = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Nº de Tactos Vaginales (TV)',
        help_text='Cantidad total de tactos vaginales realizados durante el trabajo de parto'
    )
    
    # Rotura de Membranas
    ROTURA_MEMBRANA_CHOICES = [
        ('IOP', 'IOP (Inicio Parto)'),
        ('RAM', 'RAM (Rotura Artificial)'),
        ('REM', 'REM (Rotura Espontánea)'),
        ('RPM', 'RPM (Rotura Prematura)'),
    ]
    
    rotura_membrana = models.CharField(
        max_length=10,
        choices=ROTURA_MEMBRANA_CHOICES,
        blank=True,
        verbose_name='Rotura de Membrana'
    )
    
    tiempo_membranas_rotas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Membranas Rotas (minutos)',
        help_text='Desde rotura hasta parto'
    )
    
    tiempo_dilatacion = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Dilatación (minutos)',
        help_text='Duración período dilatación'
    )
    
    tiempo_expulsivo = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Expulsivo (minutos)',
        help_text='Duración período expulsivo'
    )
    
    # ============================================
    # SECCIÓN 2: CONDICIONES DEL PARTO
    # ============================================
    
    libertad_movimiento = models.BooleanField(
        default=False,
        verbose_name='Libertad de Movimiento',
        help_text='¿Se permitió moverse libremente?'
    )
    
    TIPO_REGIMEN_CHOICES = [
        ('CERO', 'CERO (Ayuno)'),
        ('LIQUIDO', 'LÍQUIDO'),
        ('COMUN', 'COMÚN'),
        ('OTRO', 'OTRO'),
    ]
    
    tipo_regimen = models.CharField(
        max_length=20,
        choices=TIPO_REGIMEN_CHOICES,
        default='CERO',
        verbose_name='Tipo de Régimen',
        help_text='Alimentación durante trabajo de parto'
    )
    
    # VIH durante el parto
    vih_tomado_prepartos = models.BooleanField(
        default=False,
        verbose_name='VIH tomado en Prepartos'
    )
    
    VIH_SALA_CHOICES = [
        ('NO', 'No'),
        ('SALA_1', 'Sala 1'),
        ('SALA_2', 'Sala 2'),
        ('SALA_3', 'Sala 3'),
    ]
    
    vih_tomado_sala = models.CharField(
        max_length=20,
        choices=VIH_SALA_CHOICES,
        default='NO',
        verbose_name='VIH tomado en Sala'
    )
    
    # ============================================
    # SECCIÓN 3: TIPO E INFORMACIÓN DEL PARTO
    # ============================================
    
    TIPO_PARTO_CHOICES = [
        ('EUTOCICO', 'EUTÓCICO (Normal)'),
        ('DISTOCICO', 'DISTÓCICO (Instrumental)'),
        ('CESAREA_URGENCIA', 'CESÁREA DE URGENCIA'),
        ('CESAREA_ELECTIVA', 'CESÁREA ELECTIVA'),
    ]
    
    tipo_parto = models.CharField(
        max_length=30,
        choices=TIPO_PARTO_CHOICES,
        verbose_name='Tipo de Parto'
    )
    
    alumbramiento_dirigido = models.BooleanField(
        default=False,
        verbose_name='Alumbramiento Dirigido'
    )
    
    # Clasificación de Robson
    CLASIFICACION_ROBSON_CHOICES = [
        ('GRUPO_1', 'GRUPO 1'),
        ('GRUPO_2A', 'GRUPO 2.A'),
        ('GRUPO_2B', 'GRUPO 2.B'),
        ('GRUPO_3', 'GRUPO 3'),
        ('GRUPO_4', 'GRUPO 4'),
        ('GRUPO_5_1', 'GRUPO 5.1'),
        ('GRUPO_5_2', 'GRUPO 5.2'),
        ('GRUPO_6', 'GRUPO 6'),
        ('GRUPO_7', 'GRUPO 7'),
        ('GRUPO_8', 'GRUPO 8'),
        ('GRUPO_9', 'GRUPO 9'),
        ('GRUPO_10', 'GRUPO 10'),
    ]
    
    clasificacion_robson = models.CharField(
        max_length=20,
        choices=CLASIFICACION_ROBSON_CHOICES,
        blank=True,
        verbose_name='Clasificación de Robson',
        help_text='Para clasificación de cesáreas'
    )
    
    # Posición Materna
    POSICION_MATERNA_CHOICES = [
        ('SEMISENTADA', 'SEMISENTADA'),
        ('SENTADA', 'SENTADA'),
        ('LITOTOMIA', 'LITOTOMÍA'),
        ('DORSAL', 'DECÚBITO DORSAL'),
        ('CUADRUPEDA', 'CUADRÚPEDA'),
        ('LATERAL', 'DECÚBITO LATERAL'),
        ('DE_PIE', 'DE PIE'),
        ('CUCLILLAS', 'CUCLILLAS'),
        ('OTRO', 'OTRO'),
    ]
    
    posicion_materna_parto = models.CharField(
        max_length=20,
        choices=POSICION_MATERNA_CHOICES,
        blank=True,
        verbose_name='Posición Materna',
        help_text='Posición durante el parto'
    )
    
    # ============================================
    # SECCIÓN 4: PUERPERIO / COMPLICACIONES
    # ============================================
    
    ofrecimiento_posiciones_alternativas = models.BooleanField(
        default=False,
        verbose_name='Ofrecimiento de Posiciones Alternativas',
        help_text='¿Se ofrecieron posiciones alternativas?'
    )
    
    # Estado del Periné
    ESTADO_PERINE_CHOICES = [
        ('INDEMNE', 'INDEMNE (Indemne)'),
        ('DESGARRO_G1', 'DESGARRO GRADO 1'),
        ('DESGARRO_G2', 'DESGARRO GRADO 2'),
        ('DESGARRO_G3A', 'DESGARRO GRADO 3A'),
        ('DESGARRO_G3B', 'DESGARRO GRADO 3B'),
        ('DESGARRO_G3C', 'DESGARRO GRADO 3C'),
        ('DESGARRO_G4', 'DESGARRO GRADO 4'),
        ('FISURA', 'FISURA'),
        ('EPISIOTOMIA', 'EPISIOTOMÍA'),
    ]
    
    estado_perine = models.CharField(
        max_length=20,
        choices=ESTADO_PERINE_CHOICES,
        verbose_name='Estado del Periné',
        help_text='Condición post-parto'
    )
    
    # Complicaciones
    esterilizacion = models.BooleanField(
        default=False,
        verbose_name='Esterilización'
    )
    
    revision = models.BooleanField(
        default=False,
        verbose_name='Revisión'
    )
    
    inercia_uterina = models.BooleanField(
        default=False,
        verbose_name='Inercia Uterina'
    )
    
    restos_placentarios = models.BooleanField(
        default=False,
        verbose_name='Restos Placentarios'
    )
    
    trauma = models.BooleanField(
        default=False,
        verbose_name='Trauma'
    )
    
    alteracion_coagulacion = models.BooleanField(
        default=False,
        verbose_name='Alteración de la Coagulación'
    )
    
    manejo_quirurgico_inercia = models.BooleanField(
        default=False,
        verbose_name='Manejo Quirúrgico de Inercia'
    )
    
    histerectomia_obstetrica = models.BooleanField(
        default=False,
        verbose_name='Histerectomía Obstétrica',
        help_text='¿Se realizó histerectomía?'
    )
    
    transfusion_sanguinea = models.BooleanField(
        default=False,
        verbose_name='Transfusión Sanguínea',
        help_text='¿Requirió transfusión?'
    )
    
    # ============================================
    # SECCIÓN 5: ANESTESIA Y ANALGESIA
    # ============================================
    
    anestesia_neuroaxial = models.BooleanField(
        default=False,
        verbose_name='Anestesia Neuroaxial'
    )
    
    oxido_nitroso = models.BooleanField(
        default=False,
        verbose_name='Óxido Nitroso'
    )
    
    analgesia_endovenosa = models.BooleanField(
        default=False,
        verbose_name='Analgesia Endovenosa'
    )
    
    anestesia_general = models.BooleanField(
        default=False,
        verbose_name='Anestesia General'
    )
    
    anestesia_local = models.BooleanField(
        default=False,
        verbose_name='Anestesia Local'
    )
    
    # Analgesia No Farmacológica
    analgesia_no_farmacologica = models.BooleanField(
        default=False,
        verbose_name='Analgesia NO Farmacológica'
    )
    
    balon_kinesico = models.BooleanField(
        default=False,
        verbose_name='Balón Kinésico'
    )
    
    lenteja_parto = models.BooleanField(
        default=False,
        verbose_name='Lenteja de Parto'
    )
    
    rebozo = models.BooleanField(
        default=False,
        verbose_name='Rebozo'
    )
    
    aromaterapia = models.BooleanField(
        default=False,
        verbose_name='Aromaterapia'
    )
    
    # Anestesia Peridural
    peridural_solicitada_paciente = models.BooleanField(
        default=False,
        verbose_name='Peridural Solicitada por Paciente'
    )
    
    peridural_indicada_medico = models.BooleanField(
        default=False,
        verbose_name='Peridural Indicada por Médico GO'
    )
    
    peridural_administrada = models.BooleanField(
        default=False,
        verbose_name='Peridural Administrada'
    )
    
    tiempo_espera_peridural = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Espera Peridural (minutos)',
        help_text='Entre indicación y administración'
    )
    
    # ============================================
    # SECCIÓN 6: INFORMACIÓN PROFESIONALES
    # ============================================
    
    profesional_responsable = models.CharField(
        max_length=200,
        verbose_name='Profesional Responsable',
        help_text='Nombre completo del responsable'
    )
    
    alumno = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Alumno',
        help_text='Nombre del alumno (si aplica)'
    )
    
    causa_cesarea = models.TextField(
        blank=True,
        verbose_name='Causa de Cesárea',
        help_text='Indicación médica'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    uso_sala_saip = models.BooleanField(
        default=False,
        verbose_name='Uso de Sala SAIP',
        help_text='¿Se usó Sala Atención Integral?'
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
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Registro Activo'
    )
    
    class Meta:
        ordering = ['-fecha_hora_admision']
        verbose_name = 'Registro de Parto'
        verbose_name_plural = 'Registros de Parto'
        indexes = [
            models.Index(fields=['numero_registro']),
            models.Index(fields=['ficha', '-fecha_hora_admision']),
            models.Index(fields=['-fecha_hora_parto']),
        ]
    
    def __str__(self):
        return f"{self.numero_registro} - {self.ficha.paciente.persona.Nombre}"
    
    def save(self, *args, **kwargs):
        """Generar número automático si no existe"""
        if not self.numero_registro:
            ultimo = RegistroParto.objects.order_by('-id').first()
            if ultimo:
                try:
                    numero = int(ultimo.numero_registro.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_registro = f"PARTO-{numero:06d}"
        super().save(*args, **kwargs)
    
    def duracion_total_parto(self):
        """Calcula duración total del parto en minutos"""
        if self.tiempo_dilatacion and self.tiempo_expulsivo:
            return self.tiempo_dilatacion + self.tiempo_expulsivo
        return None
    
    def tiene_complicaciones(self):
        """Verifica si hubo complicaciones"""
        return (
            self.inercia_uterina or
            self.restos_placentarios or
            self.trauma or
            self.alteracion_coagulacion or
            self.histerectomia_obstetrica or
            self.transfusion_sanguinea
        )
    
    def edad_gestacional_completa(self):
        """Retorna edad gestacional en formato legible"""
        return f"{self.edad_gestacional_semanas} semanas + {self.edad_gestacional_dias} días"