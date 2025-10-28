from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from matronaApp.models import FichaObstetrica


# ============================================
# MODELO: REGISTRO DE PARTO
# ============================================

class RegistroParto(models.Model):
    """
    Registro completo del trabajo de parto, parto y puerperio inmediato
    """
    
    # ============================================
    # RELACIONES
    # ============================================
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='registros_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    numero_registro = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Registro',
        help_text='Número único de registro de parto'
    )
    
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
    # SECCIÓN: VIH AL INGRESO A PARTO
    # ============================================
    
    vih_tomado_prepartos = models.BooleanField(
        default=False,
        verbose_name='VIH tomado en Prepartos',
        help_text='¿Se tomó VIH al ingresar a prepartos?'
    )
    
    vih_tomado_sala = models.CharField(
        max_length=20,
        choices=[
            ('NO', 'No'),
            ('SALA_1', 'Sala 1'),
            ('SALA_2', 'Sala 2'),
            ('SALA_3', 'Sala 3'),
        ],
        default='NO',
        verbose_name='VIH tomado en Sala',
        help_text='Sala donde se tomó el VIH (si aplica)'
    )
    
    # ============================================
    # SECCIÓN: TRABAJO DE PARTO
    # ============================================
    
    edad_gestacional_semanas = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(42)],
        verbose_name='Edad Gestacional (semanas)',
        help_text='Semanas completas al momento del parto'
    )
    
    edad_gestacional_dias = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        default=0,
        verbose_name='Edad Gestacional (días)',
        help_text='Días adicionales'
    )
    
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
        verbose_name='Número de Tactos Vaginales',
        help_text='Cantidad total de tactos vaginales realizados'
    )
    
    rotura_membrana = models.CharField(
        max_length=20,
        choices=[
            ('ESPONTANEA', 'Espontánea'),
            ('ARTIFICIAL', 'Artificial'),
            ('MEMBRANAS_INTEGRAS', 'Membranas Íntegras'),
        ],
        verbose_name='Rotura de Membrana',
        help_text='Tipo de rotura de membranas'
    )
    
    tiempo_membranas_rotas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Membranas Rotas (horas)',
        help_text='Horas transcurridas desde la rotura de membranas'
    )
    
    tiempo_dilatacion = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de Dilatación (minutos)',
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
    # SECCIÓN: INFORMACIÓN DEL PARTO
    # ============================================
    
    libertad_movimiento = models.BooleanField(
        default=False,
        verbose_name='Libertad de Movimiento en Trabajo de Parto',
        help_text='¿Se permitió libertad de movimiento?'
    )
    
    tipo_regimen = models.CharField(
        max_length=30,
        choices=[
            ('CERO', 'Cero'),
            ('LIQUIDO', 'Líquido'),
            ('COMUN', 'Común'),
            ('OTRO', 'Otro'),
        ],
        verbose_name='Tipo de Régimen en Trabajo de Parto',
        help_text='Tipo de alimentación durante el trabajo de parto'
    )
    
    tipo_parto = models.CharField(
        max_length=30,
        choices=[
            ('EUTOCICO', 'Eutócico'),
            ('DISTOCICO', 'Distócico'),
            ('CESAREA_URGENCIA', 'Cesárea de Urgencia'),
            ('CESAREA_ELECTIVA', 'Cesárea Electiva'),
        ],
        verbose_name='Tipo de Parto',
        help_text='Clasificación del tipo de parto'
    )
    
    alumbramiento_dirigido = models.BooleanField(
        default=False,
        verbose_name='Alumbramiento Dirigido',
        help_text='¿Se realizó alumbramiento dirigido?'
    )
    
    clasificacion_robson = models.CharField(
        max_length=20,
        choices=[
            ('GRUPO_1', 'Grupo 1 - Nulíparas, único, cefálico, ≥37 sem, trabajo parto espontáneo'),
            ('GRUPO_2A', 'Grupo 2.A - Nulíparas, único, cefálico, ≥37 sem, inducido'),
            ('GRUPO_2B', 'Grupo 2.B - Nulíparas, único, cefálico, ≥37 sem, cesárea antes trabajo parto'),
            ('GRUPO_3', 'Grupo 3 - Multíparas sin cesárea previa, único, cefálico, ≥37 sem, espontáneo'),
            ('GRUPO_4', 'Grupo 4 - Multíparas sin cesárea previa, único, cefálico, ≥37 sem, inducido'),
            ('GRUPO_5_1', 'Grupo 5.1 - Multíparas con cesárea previa, único, cefálico, ≥37 sem, espontáneo'),
            ('GRUPO_5_2', 'Grupo 5.2 - Multíparas con cesárea previa, único, cefálico, ≥37 sem, inducido'),
            ('GRUPO_6', 'Grupo 6 - Nulíparas con feto único en presentación podálica'),
            ('GRUPO_7', 'Grupo 7 - Multíparas con feto único en presentación podálica'),
            ('GRUPO_8', 'Grupo 8 - Embarazos múltiples'),
            ('GRUPO_9', 'Grupo 9 - Presentaciones oblícuas o transversas'),
            ('GRUPO_10', 'Grupo 10 - Fetos únicos, cefálico, ≤36 semanas'),
        ],
        verbose_name='Clasificación de Robson',
        help_text='Clasificación de Robson para análisis de cesáreas'
    )
    
    posicion_materna_parto = models.CharField(
        max_length=30,
        choices=[
            ('SEMISENTADA', 'Semisentada'),
            ('SENTADA', 'Sentada'),
            ('LITOTOMIA', 'Litotomía'),
            ('DORSAL', 'Decúbito Dorsal'),
            ('CUADRUPEDA', 'Cuadrúpeda'),
            ('LATERAL', 'Decúbito Lateral'),
            ('DE_PIE', 'De Pie'),
            ('CUCLILLAS', 'Cuclillas'),
            ('OTRO', 'Otro'),
        ],
        verbose_name='Posición Materna en Parto',
        help_text='Posición adoptada por la madre durante el parto'
    )
    
    # ============================================
    # SECCIÓN: PUERPERIO
    # ============================================
    
    ofrecimiento_posiciones_alternativas = models.BooleanField(
        default=False,
        verbose_name='Ofrecimiento de Posiciones Alternativas',
        help_text='¿Se ofrecieron posiciones alternativas para el parto?'
    )
    
    estado_perine = models.CharField(
        max_length=30,
        choices=[
            ('INDEMNE', 'Indemne'),
            ('DESGARRO_G1', 'Desgarro Grado 1'),
            ('DESGARRO_G2', 'Desgarro Grado 2'),
            ('DESGARRO_G3A', 'Desgarro Grado 3A'),
            ('DESGARRO_G3B', 'Desgarro Grado 3B'),
            ('DESGARRO_G3C', 'Desgarro Grado 3C'),
            ('DESGARRO_G4', 'Desgarro Grado 4'),
            ('FISURA', 'Fisura'),
            ('EPISIOTOMIA', 'Episiotomía'),
        ],
        verbose_name='Estado del Periné',
        help_text='Condición del periné post-parto'
    )
    
    esterilizacion = models.BooleanField(
        default=False,
        verbose_name='Esterilización',
        help_text='¿Se realizó esterilización?'
    )
    
    revision = models.BooleanField(
        default=False,
        verbose_name='Revisión',
        help_text='¿Se realizó revisión de cavidad uterina?'
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
        help_text='¿Hubo trauma durante el parto?'
    )
    
    alteracion_coagulacion = models.BooleanField(
        default=False,
        verbose_name='Alteración de la Coagulación',
        help_text='¿Presentó alteración de la coagulación?'
    )
    
    manejo_quirurgico_inercia = models.BooleanField(
        default=False,
        verbose_name='Manejo Quirúrgico de Inercia Uterina',
        help_text='¿Requirió manejo quirúrgico por inercia uterina?'
    )
    
    # ============================================
    # SECCIÓN: ANESTESIA Y ANALGESIA
    # ============================================
    
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
        help_text='¿Se utilizó anestesia general?'
    )
    
    anestesia_local = models.BooleanField(
        default=False,
        verbose_name='Anestesia Local',
        help_text='¿Se aplicó anestesia local?'
    )
    
    # Analgesia NO Farmacológica
    analgesia_no_farmacologica = models.BooleanField(
        default=False,
        verbose_name='Analgesia NO Farmacológica',
        help_text='¿Se utilizaron métodos de analgesia no farmacológica?'
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
        help_text='¿Se utilizó rebozo?'
    )
    
    aromaterapia = models.BooleanField(
        default=False,
        verbose_name='Aromaterapia',
        help_text='¿Se utilizó aromaterapia?'
    )
    
    # Anestesia Peridural
    peridural_solicitada_paciente = models.BooleanField(
        default=False,
        verbose_name='Peridural Solicitada por Paciente',
        help_text='¿La paciente solicitó anestesia peridural?'
    )
    
    peridural_indicada_medico = models.BooleanField(
        default=False,
        verbose_name='Peridural Indicada por Médico GO',
        help_text='¿El médico gineco-obstetra indicó peridural?'
    )
    
    peridural_administrada = models.BooleanField(
        default=False,
        verbose_name='Peridural Administrada',
        help_text='¿Se administró la anestesia peridural?'
    )
    
    tiempo_espera_peridural = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de Espera Peridural (minutos)',
        help_text='Tiempo entre indicación médica y administración de peridural'
    )
    
    # ============================================
    # SECCIÓN: INFORMACIÓN PROFESIONALES
    # ============================================
    
    profesional_responsable = models.CharField(
        max_length=200,
        verbose_name='Profesional Responsable',
        help_text='Nombre completo del profesional responsable del parto'
    )
    
    alumno = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Alumno',
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
        verbose_name='Uso de Sala SAIP',
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
    
    sexo = models.CharField(
        max_length=20,
        choices=[
            ('MASCULINO', 'Masculino'),
            ('FEMENINO', 'Femenino'),
            ('INDETERMINADO', 'Indeterminado'),
        ],
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
        help_text='Puntaje Apgar al primer minuto'
    )
    
    apgar_5_minutos = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar a los 5 Minutos',
        help_text='Puntaje Apgar a los cinco minutos'
    )
    
    # ============================================
    # APEGO Y ACOMPAÑAMIENTO
    # ============================================
    
    tiempo_apego = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de Apego (minutos)',
        help_text='Tiempo de contacto piel con piel'
    )
    
    apego_canguro = models.BooleanField(
        default=False,
        verbose_name='Apego Canguro',
        help_text='¿Se realizó apego canguro?'
    )
    
    acompanamiento_preparto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento Preparto',
        help_text='¿Hubo acompañamiento en preparto?'
    )
    
    acompanamiento_parto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento Parto',
        help_text='¿Hubo acompañamiento durante el parto?'
    )
    
    acompanamiento_rn = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento RN',
        help_text='¿Hubo acompañamiento con el recién nacido?'
    )
    
    motivo_parto_no_acompanado = models.CharField(
        max_length=50,
        choices=[
            ('NA', 'No Aplica - Fue Acompañado'),
            ('NO_DESEA', 'No Desea'),
            ('NO_LLEGA', 'No Llega'),
            ('URGENCIA', 'Urgencia'),
            ('NO_TIENE', 'No Tiene Acompañante'),
            ('RURALIDAD', 'Ruralidad'),
            ('SIN_PASE', 'Sin Pase de Movilidad'),
        ],
        default='NA',
        verbose_name='Motivo Parto NO Acompañado',
        help_text='Razón por la cual el parto no fue acompañado'
    )
    
    persona_acompanante = models.CharField(
        max_length=50,
        choices=[
            ('NADIE', 'Nadie'),
            ('PAREJA', 'Pareja'),
            ('MADRE', 'Madre'),
            ('HERMANA', 'Hermana'),
            ('AMIGA', 'Amiga'),
            ('OTRO', 'Otro'),
        ],
        default='NADIE',
        verbose_name='Persona Acompañante',
        help_text='Quién acompañó a la madre'
    )
    
    acompanante_secciona_cordon = models.BooleanField(
        default=False,
        verbose_name='Acompañante Secciona Cordón',
        help_text='¿El acompañante cortó el cordón umbilical?'
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