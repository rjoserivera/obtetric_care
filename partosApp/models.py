# partosApp/models.py
"""
Modelos para el módulo de Partos
Incluye: FichaParto, RegistroParto, RegistroRecienNacido, DocumentosParto
ACTUALIZADO: Con todos los campos obligatorios faltantes
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from matronaApp.models import FichaObstetrica


# ============================================
# MODELO: FICHA DE PARTO (NUEVO)
# ============================================

class FichaParto(models.Model):
    """
    Ficha específica para el proceso de parto
    Contiene todos los datos generales y de admisión
    """
    
    # ============================================
    # RELACIÓN CON FICHA OBSTÉTRICA
    # ============================================
    
    ficha_obstetrica = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.PROTECT,
        related_name='fichas_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    numero_ficha_parto = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha de Parto',
        help_text='Número único de identificación de la ficha de parto'
    )
    
    # ============================================
    # SECCIÓN 1: DATOS GENERALES
    # ============================================
    
    TIPO_PACIENTE_CHOICES = [
        ('NORMAL', 'Normal'),
        ('ARO', 'Alto Riesgo Obstétrico (ARO)'),
    ]
    
    tipo_paciente = models.CharField(
        max_length=20,
        choices=TIPO_PACIENTE_CHOICES,
        default='NORMAL',
        verbose_name='Tipo de Paciente',
        help_text='Clasificación de riesgo de la paciente'
    )
    
    ORIGEN_INGRESO_CHOICES = [
        ('SALA', 'Sala'),
        ('UEGO', 'UEGO (Unidad de Emergencia Gineco-Obstétrica)'),
    ]
    
    origen_ingreso = models.CharField(
        max_length=20,
        choices=ORIGEN_INGRESO_CHOICES,
        verbose_name='Origen de Ingreso',
        help_text='Lugar de procedencia del ingreso'
    )
    
    fecha_ingreso = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Ingreso',
        help_text='Fecha de ingreso al servicio'
    )
    
    hora_ingreso = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Ingreso',
        help_text='Hora de ingreso al servicio'
    )
    
    plan_de_parto = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Plan de Parto?',
        help_text='Indica si la paciente presentó un plan de parto'
    )
    
    visita_guiada = models.BooleanField(
        default=False,
        verbose_name='¿Realizó Visita Guiada?',
        help_text='Indica si la paciente realizó visita guiada previa'
    )
    
    # ============================================
    # DATOS ADICIONALES DEL PACIENTE
    # ============================================
    # Los datos personales (nombre, RUN, etc.) están en Persona
    # IMC, Paridad están en FichaObstetrica
    # Agregamos campos específicos del parto:
    
    control_prenatal = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Control Prenatal',
        help_text='Descripción de controles prenatales realizados'
    )
    
    consultorio_origen = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Consultorio de Origen',
        help_text='Consultorio o centro de salud de procedencia'
    )
    
    # ============================================
    # PATOLOGÍAS ESPECÍFICAS AL INGRESO
    # ============================================
    
    preeclampsia_severa = models.BooleanField(
        default=False,
        verbose_name='Preeclampsia Severa',
        help_text='¿Diagnóstico de preeclampsia severa?'
    )
    
    eclampsia = models.BooleanField(
        default=False,
        verbose_name='Eclampsia',
        help_text='¿Diagnóstico de eclampsia?'
    )
    
    sepsis_infeccion_sistemica = models.BooleanField(
        default=False,
        verbose_name='Sepsis o Infección Sistémica Grave',
        help_text='¿Presenta sepsis o infección sistémica?'
    )
    
    infeccion_ovular_corioamnionitis = models.BooleanField(
        default=False,
        verbose_name='Infección Ovular o Corioamnionitis',
        help_text='¿Presenta infección ovular o corioamnionitis?'
    )
    
    otra_patologia_texto = models.TextField(
        blank=True,
        verbose_name='Otra Patología',
        help_text='Descripción de otras patologías presentes'
    )
    
    numero_aro = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nº ARO',
        help_text='Número de Alto Riesgo Obstétrico (si aplica)'
    )
    
    # ============================================
    # TAMIZAJES AL INGRESO
    # ============================================
    
    # VIH
    VIH_RESULTADO_CHOICES = [
        ('NO_TOMADO', 'No Tomado'),
        ('PRIMERO', '1° (Primer Examen)'),
        ('SEGUNDO', '2° (Segundo Examen)'),
        ('TERCERO', '3° (Tercer Examen)'),
    ]
    
    se_toma_vih_prepartos = models.BooleanField(
        default=False,
        verbose_name='Se toma VIH en Prepartos',
        help_text='¿Se realizó toma de VIH en prepartos?'
    )
    
    se_tomo_vih_sala = models.CharField(
        max_length=20,
        choices=VIH_RESULTADO_CHOICES,
        default='NO_TOMADO',
        verbose_name='Se tomó VIH en Sala',
        help_text='Número de examen de VIH realizado en sala'
    )
    
    # SGB (Streptococcus del Grupo B)
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='SGB - Pesquisa',
        help_text='¿Se realizó pesquisa de SGB?'
    )
    
    SGB_RESULTADO_CHOICES = [
        ('NO_REALIZADO', 'No Realizado'),
        ('POSITIVO', 'Positivo'),
        ('NEGATIVO', 'Negativo'),
    ]
    
    sgb_resultado = models.CharField(
        max_length=20,
        choices=SGB_RESULTADO_CHOICES,
        default='NO_REALIZADO',
        verbose_name='SGB - Resultado',
        help_text='Resultado de la pesquisa de SGB'
    )
    
    sgb_antibiotico = models.BooleanField(
        default=False,
        verbose_name='Antibiótico por SGB (NO por RPM)',
        help_text='¿Recibió antibiótico por SGB positivo? (no por rotura prematura de membranas)'
    )
    
    # VDRL (Sífilis)
    VDRL_RESULTADO_CHOICES = [
        ('NO_REALIZADO', 'No Realizado'),
        ('REACTIVO', 'Reactivo'),
        ('NO_REACTIVO', 'No Reactivo'),
    ]
    
    vdrl_resultado = models.CharField(
        max_length=20,
        choices=VDRL_RESULTADO_CHOICES,
        default='NO_REALIZADO',
        verbose_name='VDRL - Resultado durante embarazo',
        help_text='Resultado de VDRL'
    )
    
    vdrl_tratamiento_atb = models.BooleanField(
        default=False,
        verbose_name='Tratamiento ATB por Sífilis al momento del Parto',
        help_text='¿Recibió tratamiento antibiótico por sífilis?'
    )
    
    # Hepatitis B
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='Examen Hepatitis B - Tomado',
        help_text='¿Se realizó examen de Hepatitis B?'
    )
    
    HEPATITIS_B_RESULTADO_CHOICES = [
        ('NO_REALIZADO', 'No Realizado'),
        ('POSITIVO', 'Positivo'),
        ('NEGATIVO', 'Negativo'),
    ]
    
    hepatitis_b_resultado = models.CharField(
        max_length=20,
        choices=HEPATITIS_B_RESULTADO_CHOICES,
        default='NO_REALIZADO',
        verbose_name='Hepatitis B - Resultado'
    )
    
    hepatitis_b_derivacion = models.BooleanField(
        default=False,
        verbose_name='Derivación a Especialista (Gastro-Hepatólogo)',
        help_text='¿Se derivó a especialista por Hepatitis B positivo?'
    )
    
    # ============================================
    # OBSERVACIONES
    # ============================================
    
    observaciones_ingreso = models.TextField(
        blank=True,
        verbose_name='Observaciones de Ingreso',
        help_text='Observaciones generales al momento del ingreso'
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
        verbose_name='Fecha de Última Modificación'
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Ficha Activa',
        help_text='Indica si la ficha de parto está activa'
    )
    
    class Meta:
        ordering = ['-fecha_ingreso', '-hora_ingreso']
        verbose_name = 'Ficha de Parto'
        verbose_name_plural = 'Fichas de Parto'
        indexes = [
            models.Index(fields=['numero_ficha_parto']),
            models.Index(fields=['ficha_obstetrica', 'activa']),
            models.Index(fields=['-fecha_ingreso']),
        ]
    
    def __str__(self):
        paciente = self.ficha_obstetrica.paciente.persona
        return f"Ficha Parto {self.numero_ficha_parto} - {paciente.Nombre} {paciente.Apellido_Paterno}"
    
    def save(self, *args, **kwargs):
        if not self.numero_ficha_parto:
            # Generar número de ficha de parto automáticamente
            ultima_ficha = FichaParto.objects.order_by('-id').first()
            if ultima_ficha:
                try:
                    numero = int(ultima_ficha.numero_ficha_parto.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_ficha_parto = f"FP-{numero:06d}"
        super().save(*args, **kwargs)


# ============================================
# MODELO: REGISTRO DE PARTO (ACTUALIZADO)
# ============================================

class RegistroParto(models.Model):
    """
    Registro completo del proceso de parto
    ACTUALIZADO: Con todos los campos obligatorios
    """
    
    # ============================================
    # RELACIONES
    # ============================================
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.PROTECT,
        related_name='registros_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    ficha_parto = models.OneToOneField(
        FichaParto,
        on_delete=models.PROTECT,
        related_name='registro_parto',
        null=True,
        blank=True,
        verbose_name='Ficha de Parto',
        help_text='Ficha de parto asociada (contiene datos de ingreso)'
    )
    
    numero_registro = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Registro',
        help_text='Número único de registro de parto'
    )
    
    # ============================================
    # FECHAS Y HORAS
    # ============================================
    
    fecha_hora_admision = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Admisión',
        help_text='Momento en que la paciente ingresa para el parto'
    )
    
    fecha_hora_parto = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora del Parto',
        help_text='Momento exacto del nacimiento'
    )
    
    # ============================================
    # SECCIÓN: TRABAJO DE PARTO
    # ============================================
    
    # Edad Gestacional
    edad_gestacional_semanas = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(42)],
        verbose_name='Edad Gestacional (semanas)',
        help_text='Semanas completas al momento del parto'
    )
    
    edad_gestacional_dias = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name='Edad Gestacional (días)',
        help_text='Días adicionales'
    )
    
    # Monitorización y Procedimientos
    monitor_ttc = models.BooleanField(
        default=False,
        verbose_name='Monitor TTC',
        help_text='¿Se utilizó monitor de contracciones?'
    )
    
    induccion = models.BooleanField(
        default=False,
        verbose_name='Inducción',
        help_text='¿Se realizó inducción del parto?'
    )
    
    aceleracion_correccion = models.BooleanField(
        default=False,
        verbose_name='Aceleración o Corrección',
        help_text='¿Se aceleró o corrigió el trabajo de parto?'
    )
    
    numero_tactos_vaginales = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Nº TV (Tactos Vaginales)',
        help_text='Número de tactos vaginales realizados'
    )
    
    # Rotura de Membranas
    ROTURA_MEMBRANA_CHOICES = [
        ('IOP', 'IOP (Inicio Parto)'),
        ('RAM', 'RAM (Rotura Artificial Membranas)'),
        ('REM', 'REM (Rotura Espontánea Membranas)'),
        ('RPM', 'RPM (Rotura Prematura Membranas)'),
    ]
    
    rotura_membrana = models.CharField(
        max_length=10,
        choices=ROTURA_MEMBRANA_CHOICES,
        blank=True,
        verbose_name='Rotura de Membrana',
        help_text='Tipo de rotura de membranas'
    )
    
    tiempo_membranas_rotas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Membranas Rotas (minutos)',
        help_text='Tiempo transcurrido desde rotura hasta el parto (IOP)'
    )
    
    tiempo_dilatacion = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Dilatación (minutos)',
        help_text='Duración del período de dilatación'
    )
    
    tiempo_expulsivo = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Expulsivo (minutos)',
        help_text='Duración del período expulsivo'
    )
    
    # ============================================
    # SECCIÓN: PARTO - NUEVOS CAMPOS
    # ============================================
    
    libertad_movimiento = models.BooleanField(
        default=False,
        verbose_name='Libertad de Movimiento en Trabajo de Parto',
        help_text='¿Se permitió libertad de movimiento durante el trabajo de parto?'
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
        verbose_name='Tipo de Régimen en Trabajo de Parto',
        help_text='Tipo de alimentación permitida durante el trabajo de parto'
    )
    
    # VIH durante el parto
    vih_tomado_prepartos = models.BooleanField(
        default=False,
        verbose_name='VIH tomado en Prepartos',
        help_text='¿Se tomó VIH al ingresar a prepartos?'
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
        verbose_name='VIH tomado en Sala',
        help_text='Sala donde se tomó el VIH (si aplica)'
    )
    
    # ============================================
    # SECCIÓN: TIPO E INFORMACIÓN DEL PARTO
    # ============================================
    
    TIPO_PARTO_CHOICES = [
        ('EUTOCICO', 'EUTÓCICO (Parto Normal)'),
        ('DISTOCICO', 'DISTÓCICO (Parto Instrumental)'),
        ('CESAREA_URGENCIA', 'CESÁREA DE URGENCIA'),
        ('CESAREA_ELECTIVA', 'CESÁREA ELECTIVA'),
    ]
    
    tipo_parto = models.CharField(
        max_length=30,
        choices=TIPO_PARTO_CHOICES,
        verbose_name='Tipo de Parto',
        help_text='Clasificación del tipo de parto'
    )
    
    alumbramiento_dirigido = models.BooleanField(
        default=False,
        verbose_name='Alumbramiento Dirigido',
        help_text='¿Se realizó alumbramiento dirigido?'
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
        help_text='Clasificación de Robson para cesáreas'
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
        verbose_name='Posición Materna en el Parto',
        help_text='Posición adoptada por la madre durante el parto'
    )
    
    # ============================================
    # SECCIÓN: PUERPERIO / COMPLICACIONES
    # ============================================
    
    ofrecimiento_posiciones_alternativas = models.BooleanField(
        default=False,
        verbose_name='Ofrecimiento de Posiciones Alternativas del Parto',
        help_text='¿Se ofrecieron posiciones alternativas para el parto?'
    )
    
    # Estado del Periné
    ESTADO_PERINE_CHOICES = [
        ('INDEPNE', 'INDEPNE (Indemne)'),
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
        help_text='Condición del periné post-parto'
    )
    
    # Complicaciones
    esterilizacion = models.BooleanField(
        default=False,
        verbose_name='Esterilización',
        help_text='¿Se realizó esterilización?'
    )
    
    revision = models.BooleanField(
        default=False,
        verbose_name='Revisión',
        help_text='¿Se realizó revisión uterina?'
    )
    
    inercia_uterina = models.BooleanField(
        default=False,
        verbose_name='Inercia Uterina',
        help_text='¿Presentó inercia uterina?'
    )
    
    restos_placentarios = models.BooleanField(
        default=False,
        verbose_name='Restos Placentarios',
        help_text='¿Se detectaron restos placentarios?'
    )
    
    trauma = models.BooleanField(
        default=False,
        verbose_name='Trauma',
        help_text='¿Presentó trauma obstétrico?'
    )
    
    alteracion_coagulacion = models.BooleanField(
        default=False,
        verbose_name='Alteración de la Coagulación',
        help_text='¿Presentó alteraciones de la coagulación?'
    )
    
    manejo_quirurgico_inercia = models.BooleanField(
        default=False,
        verbose_name='Manejo Quirúrgico de Inercia Uterina',
        help_text='¿Requirió manejo quirúrgico por inercia uterina?'
    )
    
    # NUEVOS CAMPOS DE COMPLICACIONES
    histerectomia_obstetrica = models.BooleanField(
        default=False,
        verbose_name='Histerectomía Obstétrica',
        help_text='¿Se realizó histerectomía obstétrica?'
    )
    
    transfusion_sanguinea = models.BooleanField(
        default=False,
        verbose_name='Transfusión Sanguínea',
        help_text='¿Requirió transfusión sanguínea?'
    )
    
    # ============================================
    # SECCIÓN: ANESTESIA Y ANALGESIA
    # ============================================
    
    # Tipos de Anestesia/Analgesia
    anestesia_neuroaxial = models.BooleanField(
        default=False,
        verbose_name='Anestesia Neuroaxial',
        help_text='¿Se administró anestesia neuroaxial?'
    )
    
    oxido_nitroso = models.BooleanField(
        default=False,
        verbose_name='Óxido Nitroso',
        help_text='¿Se utilizó óxido nitroso?'
    )
    
    analgesia_endovenosa = models.BooleanField(
        default=False,
        verbose_name='Analgesia Endovenosa',
        help_text='¿Se administró analgesia endovenosa?'
    )
    
    anestesia_general = models.BooleanField(
        default=False,
        verbose_name='Anestesia General',
        help_text='¿Se administró anestesia general?'
    )
    
    anestesia_local = models.BooleanField(
        default=False,
        verbose_name='Anestesia Local',
        help_text='¿Se administró anestesia local?'
    )
    
    # Analgesia No Farmacológica
    analgesia_no_farmacologica = models.BooleanField(
        default=False,
        verbose_name='Analgesia NO Farmacológica',
        help_text='¿Se utilizaron métodos no farmacológicos?'
    )
    
    balon_kinesico = models.BooleanField(
        default=False,
        verbose_name='Balón Kinésico',
        help_text='¿Se utilizó balón kinésico?'
    )
    
    lenteja_parto = models.BooleanField(
        default=False,
        verbose_name='Lenteja de Parto',
        help_text='¿Se utilizó lenteja de parto?'
    )
    
    rebozo = models.BooleanField(
        default=False,
        verbose_name='Rebozo',
        help_text='¿Se utilizó técnica de rebozo?'
    )
    
    aromaterapia = models.BooleanField(
        default=False,
        verbose_name='Aromaterapia',
        help_text='¿Se aplicó aromaterapia?'
    )
    
    # Anestesia Peridural
    peridural_solicitada_paciente = models.BooleanField(
        default=False,
        verbose_name='Anest. Peridural Solicitada por Paciente',
        help_text='¿La paciente solicitó anestesia peridural?'
    )
    
    peridural_indicada_medico = models.BooleanField(
        default=False,
        verbose_name='Anest. Peridural Indicada por Médico GO',
        help_text='¿El médico gineco-obstetra indicó peridural?'
    )
    
    peridural_administrada = models.BooleanField(
        default=False,
        verbose_name='Anest. Peridural Administrada',
        help_text='¿Se administró la anestesia peridural?'
    )
    
    tiempo_espera_peridural = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de Espera entre Indicación y Administración (minutos)',
        help_text='Tiempo entre indicación médica y administración de peridural'
    )
    
    # ============================================
    # SECCIÓN: INFORMACIÓN PROFESIONALES
    # ============================================
    
    profesional_responsable = models.CharField(
        max_length=200,
        verbose_name='Profesional Responsable (nombre y apellido)',
        help_text='Nombre completo del profesional responsable del parto'
    )
    
    alumno = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Alumno (nombre y apellido)',
        help_text='Nombre del alumno que participó (si aplica)'
    )
    
    causa_cesarea = models.TextField(
        blank=True,
        verbose_name='Causa de Cesárea',
        help_text='Indicación médica para cesárea'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones',
        help_text='Observaciones generales del parto'
    )
    
    uso_sala_saip = models.BooleanField(
        default=False,
        verbose_name='Uso de Sala SAIP (Sí/No)',
        help_text='¿Se utilizó Sala de Atención Integral del Parto?'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación del Registro'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Última Modificación'
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
        return f"Parto {self.numero_registro} - {self.ficha.paciente.persona.Nombre}"
    
    def save(self, *args, **kwargs):
        if not self.numero_registro:
            # Generar número de registro automáticamente
            ultimo_registro = RegistroParto.objects.order_by('-id').first()
            if ultimo_registro:
                try:
                    numero = int(ultimo_registro.numero_registro.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_registro = f"PARTO-{numero:06d}"
        super().save(*args, **kwargs)


# ============================================
# MODELO: REGISTRO DE RECIÉN NACIDO
# ============================================

class RegistroRecienNacido(models.Model):
    """
    Registro del recién nacido, apego y acompañamiento
    """
    
    # ============================================
    # RELACIÓN
    # ============================================
    
    registro_parto = models.ForeignKey(
        RegistroParto,
        on_delete=models.CASCADE,
        related_name='recien_nacidos',
        verbose_name='Registro de Parto'
    )
    
    # ============================================
    # DATOS DEL RECIÉN NACIDO
    # ============================================
    
    SEXO_CHOICES = [
        ('MASCULINO', 'Masculino'),
        ('FEMENINO', 'Femenino'),
        ('INDETERMINADO', 'Indeterminado'),
    ]
    
    sexo = models.CharField(
        max_length=20,
        choices=SEXO_CHOICES,
        verbose_name='Sexo',
        help_text='Sexo del recién nacido'
    )
    
    peso = models.IntegerField(
        validators=[MinValueValidator(500), MaxValueValidator(8000)],
        verbose_name='Peso (gramos)',
        help_text='Peso al nacer en gramos'
    )
    
    talla = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(70)],
        verbose_name='Talla (cm)',
        help_text='Longitud al nacer en centímetros'
    )
    
    ligadura_tardia_cordon = models.BooleanField(
        default=False,
        verbose_name='Ligadura Tardía del Cordón (> 1 minuto)',
        help_text='¿Se realizó ligadura tardía del cordón umbilical?'
    )
    
    apgar_1_minuto = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar al Minuto',
        help_text='Puntaje de Apgar al primer minuto'
    )
    
    apgar_5_minutos = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar a los 5 Minutos',
        help_text='Puntaje de Apgar a los 5 minutos'
    )
    
    # ============================================
    # APEGO
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
        help_text='¿Se realizó apego método canguro?'
    )
    
    # ============================================
    # ACOMPAÑAMIENTO
    # ============================================
    
    acompanamiento_preparto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento Preparto',
        help_text='¿Tuvo acompañamiento durante el preparto?'
    )
    
    acompanamiento_parto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento Parto',
        help_text='¿Tuvo acompañamiento durante el parto?'
    )
    
    acompanamiento_rn = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento RN',
        help_text='¿Tuvo acompañamiento con el recién nacido?'
    )
    
    # Motivo parto NO acompañado
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
        verbose_name='Motivo Parto NO Acompañado',
        help_text='Razón por la cual el parto no fue acompañado'
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
        verbose_name='Persona Acompañante',
        help_text='Relación de la persona que acompañó'
    )
    
    acompanante_secciona_cordon = models.BooleanField(
        default=False,
        verbose_name='Acompañante Secciona Cordón',
        help_text='¿El/la acompañante seccionó el cordón umbilical?'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_nacimiento = models.DateTimeField(
        verbose_name='Fecha y Hora de Nacimiento',
        help_text='Momento exacto del nacimiento'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación del Registro'
    )
    
    class Meta:
        ordering = ['-fecha_nacimiento']
        verbose_name = 'Registro de Recién Nacido'
        verbose_name_plural = 'Registros de Recién Nacidos'
        indexes = [
            models.Index(fields=['registro_parto', '-fecha_nacimiento']),
        ]
    
    def __str__(self):
        return f"RN {self.sexo} - Parto {self.registro_parto.numero_registro} - {self.peso}g"
    
    def clasificacion_peso(self):
        """Clasifica el peso del RN según OMS"""
        if self.peso < 2500:
            return "Bajo peso al nacer"
        elif self.peso <= 4000:
            return "Peso adecuado"
        else:
            return "Macrosómico"


# ============================================
# MODELO: DOCUMENTOS DEL PARTO
# ============================================

class DocumentosParto(models.Model):
    """
    Documentos legales y administrativos del parto
    """
    
    # ============================================
    # RELACIÓN
    # ============================================
    
    registro_parto = models.OneToOneField(
        RegistroParto,
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name='Registro de Parto'
    )
    
    # ============================================
    # LEY N° 21.372 DOMINGA
    # ============================================
    
    recuerdos_entregados = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Recuerdos Entregados',
        help_text='Lista de recuerdos entregados según Ley Dominga'
    )
    
    motivo_no_entrega_recuerdos = models.TextField(
        blank=True,
        verbose_name='Motivo de No Entrega de Recuerdos',
        help_text='Justificación si no se entregaron recuerdos'
    )
    
    # ============================================
    # PLACENTA
    # ============================================
    
    retira_placenta = models.BooleanField(
        default=False,
        verbose_name='Retira Placenta',
        help_text='¿La familia retira la placenta?'
    )
    
    estampado_placenta = models.BooleanField(
        default=False,
        verbose_name='Estampado de Placenta',
        help_text='¿Se realizó estampado de placenta?'
    )
    
    # ============================================
    # REGISTRO CIVIL
    # ============================================
    
    folio_valido = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Folio Válido',
        help_text='Número de folio válido del Registro Civil'
    )
    
    folios_nulos = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Folio/s Nulo/s',
        help_text='Folios anulados (si aplica)'
    )
    
    # ============================================
    # MANEJO DEL DOLOR NO FARMACOLÓGICO
    # ============================================
    
    manejo_dolor_no_farmacologico = models.TextField(
        blank=True,
        verbose_name='Manejo del Dolor No Farmacológico',
        help_text='Descripción de métodos no farmacológicos utilizados'
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
        verbose_name='Fecha de Última Modificación'
    )
    
    class Meta:
        verbose_name = 'Documentos de Parto'
        verbose_name_plural = 'Documentos de Partos'
    
    def __str__(self):
        return f"Documentos - Parto {self.registro_parto.numero_registro}"