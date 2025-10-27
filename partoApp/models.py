from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Importar modelos existentes
from gestionApp.models import Paciente, Matrona, Persona
from matronaApp.models import FichaObstetrica
from medicoApp.models import Patologias


# ============================================
# MODELO PRINCIPAL: REGISTRO DE PARTO
# ============================================

class RegistroParto(models.Model):
    """Registro completo del proceso de parto"""
    
    # ========================================
    # RELACIONES CON MODELOS EXISTENTES
    # ========================================
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='partos',
        verbose_name='Paciente'
    )
    
    ficha_obstetrica = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='partos',
        verbose_name='Ficha Obstétrica',
        null=True,
        blank=True
    )
    
    matrona_responsable = models.ForeignKey(
        Matrona,
        on_delete=models.PROTECT,
        related_name='partos_atendidos',
        verbose_name='Matrona Responsable'
    )
    
    alumno = models.ForeignKey(
        Persona,
        on_delete=models.SET_NULL,
        related_name='partos_como_alumno',
        verbose_name='Alumno',
        null=True,
        blank=True
    )
    
    # ========================================
    # 1. DATOS DE INGRESO
    # ========================================
    ORIGEN_CHOICES = [
        ('urgencia', 'Urgencia'),
        ('consultorio', 'Consultorio'),
        ('derivacion', 'Derivación'),
        ('particular', 'Particular'),
    ]
    
    fecha_ingreso = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Ingreso'
    )
    
    origen_ingreso = models.CharField(
        max_length=20,
        choices=ORIGEN_CHOICES,
        verbose_name='Origen del Ingreso'
    )
    
    tiene_plan_parto = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Plan de Parto?'
    )
    
    visita_guiada = models.BooleanField(
        default=False,
        verbose_name='¿Realizó Visita Guiada?'
    )
    
    uso_sala_saip = models.BooleanField(
        default=False,
        verbose_name='¿Uso Sala SAIP?'
    )
    
    # ========================================
    # 3. ANTECEDENTES CLÍNICOS
    # ========================================
    imc = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(10), MaxValueValidator(60)],
        verbose_name='IMC',
        null=True,
        blank=True
    )
    
    paridad = models.CharField(
        max_length=50,
        verbose_name='Paridad',
        blank=True,
        help_text='Ejemplo: G3P2A0'
    )
    
    control_prenatal = models.BooleanField(
        default=True,
        verbose_name='¿Tuvo Control Prenatal?'
    )
    
    consultorio_origen = models.CharField(
        max_length=100,
        verbose_name='Consultorio de Origen',
        blank=True
    )
    
    # ========================================
    # 4. PATOLOGÍAS Y COMPLICACIONES
    # ========================================
    patologias = models.ManyToManyField(
        Patologias,
        related_name='partos_con_patologia',
        verbose_name='Patologías',
        blank=True
    )
    
    preeclampsia_severa = models.BooleanField(
        default=False,
        verbose_name='Preeclampsia Severa'
    )
    
    eclampsia = models.BooleanField(
        default=False,
        verbose_name='Eclampsia'
    )
    
    sepsis = models.BooleanField(
        default=False,
        verbose_name='Sepsis o Infección Sistémica Grave'
    )
    
    infeccion_ovular = models.BooleanField(
        default=False,
        verbose_name='Infección Ovular o Corioamnionitis'
    )
    
    otra_patologia = models.TextField(
        blank=True,
        verbose_name='Otra Patología'
    )
    
    es_aro = models.BooleanField(
        default=False,
        verbose_name='¿Es ARO? (Alto Riesgo Obstétrico)'
    )
    
    # ========================================
    # 6. TRABAJO DE PARTO
    # ========================================
    uso_monitor = models.BooleanField(
        default=False,
        verbose_name='Uso de Monitor'
    )
    
    ttc = models.BooleanField(
        default=False,
        verbose_name='TTC'
    )
    
    induccion = models.BooleanField(
        default=False,
        verbose_name='Inducción'
    )
    
    aceleracion_correccion = models.BooleanField(
        default=False,
        verbose_name='Aceleración o Corrección'
    )
    
    numero_tactos_vaginales = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        verbose_name='Número de Tactos Vaginales'
    )
    
    ROTURA_CHOICES = [
        ('espontanea', 'Espontánea'),
        ('artificial', 'Artificial'),
        ('no_aplica', 'No Aplica'),
    ]
    
    rotura_membranas = models.CharField(
        max_length=20,
        choices=ROTURA_CHOICES,
        default='no_aplica',
        verbose_name='Rotura de Membranas'
    )
    
    tiempo_membranas_rotas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Tiempo Membranas Rotas (horas)'
    )
    
    tiempo_dilatacion = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Tiempo de Dilatación (minutos)'
    )
    
    tiempo_expulsivo = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Tiempo Expulsivo (minutos)'
    )
    
    libertad_movimiento = models.BooleanField(
        default=True,
        verbose_name='Libertad de Movimiento en Trabajo de Parto'
    )
    
    REGIMEN_CHOICES = [
        ('cero', 'Régimen Cero'),
        ('liquidos', 'Líquidos'),
        ('liviano', 'Liviano'),
    ]
    
    tipo_regimen = models.CharField(
        max_length=20,
        choices=REGIMEN_CHOICES,
        default='liquidos',
        verbose_name='Tipo de Régimen'
    )
    
    # ========================================
    # 7. PARTO
    # ========================================
    TIPO_PARTO_CHOICES = [
        ('vaginal', 'Vaginal Espontáneo'),
        ('forceps', 'Fórceps'),
        ('ventosa', 'Ventosa'),
        ('cesarea', 'Cesárea'),
    ]
    
    tipo_parto = models.CharField(
        max_length=20,
        choices=TIPO_PARTO_CHOICES,
        verbose_name='Tipo de Parto'
    )
    
    alumbramiento_dirigido = models.BooleanField(
        default=True,
        verbose_name='Alumbramiento Dirigido'
    )
    
    clasificacion_robson = models.CharField(
        max_length=10,
        verbose_name='Clasificación de Robson',
        blank=True,
        help_text='Grupo 1-10'
    )
    
    POSICION_CHOICES = [
        ('litotomia', 'Litotomía'),
        ('semisentada', 'Semisentada'),
        ('cuclillas', 'Cuclillas'),
        ('lateral', 'Lateral'),
        ('cuatro_puntos', 'Cuatro Puntos'),
    ]
    
    posicion_materna = models.CharField(
        max_length=20,
        choices=POSICION_CHOICES,
        verbose_name='Posición Materna en el Parto'
    )
    
    ofrecimiento_posiciones_alternativas = models.BooleanField(
        default=False,
        verbose_name='¿Se Ofrecieron Posiciones Alternativas?'
    )
    
    ESTADO_PERINE_CHOICES = [
        ('integro', 'Íntegro'),
        ('desgarro_1', 'Desgarro Grado I'),
        ('desgarro_2', 'Desgarro Grado II'),
        ('desgarro_3', 'Desgarro Grado III'),
        ('desgarro_4', 'Desgarro Grado IV'),
        ('episiotomia', 'Episiotomía'),
    ]
    
    estado_perine = models.CharField(
        max_length=20,
        choices=ESTADO_PERINE_CHOICES,
        verbose_name='Estado del Periné'
    )
    
    esterilizacion = models.BooleanField(
        default=False,
        verbose_name='Esterilización'
    )
    
    revision = models.BooleanField(
        default=False,
        verbose_name='Revisión'
    )
    
    causa_cesarea = models.TextField(
        blank=True,
        verbose_name='Causa de Cesárea'
    )
    
    # ========================================
    # 11. APEGO Y ACOMPAÑAMIENTO
    # ========================================
    acompanamiento_preparto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento en Preparto'
    )
    
    acompanamiento_parto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento en Parto'
    )
    
    acompanamiento_rn = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento de RN'
    )
    
    motivo_no_acompanado = models.TextField(
        blank=True,
        verbose_name='Motivo de Parto NO Acompañado'
    )
    
    ACOMPANANTE_CHOICES = [
        ('pareja', 'Pareja'),
        ('madre', 'Madre'),
        ('hermana', 'Hermana'),
        ('amiga', 'Amiga'),
        ('otro', 'Otro'),
    ]
    
    tipo_persona_acompanante = models.CharField(
        max_length=20,
        choices=ACOMPANANTE_CHOICES,
        blank=True,
        verbose_name='Persona Acompañante'
    )
    
    acompanante_secciona_cordon = models.BooleanField(
        default=False,
        verbose_name='¿Acompañante Secciona Cordón?'
    )
    
    # ========================================
    # 13. LEY N° 21.372 DOMINGA (Recuerdos)
    # ========================================
    entrega_recuerdos = models.BooleanField(
        default=False,
        verbose_name='¿Se Entregan Recuerdos?'
    )
    
    cuales_recuerdos = models.TextField(
        blank=True,
        verbose_name='¿Cuáles Recuerdos?',
        help_text='Ejemplo: Pinza cordón, pulsera, foto'
    )
    
    motivo_no_entrega = models.TextField(
        blank=True,
        verbose_name='Motivo de No Entrega'
    )
    
    # ========================================
    # 14. PLACENTA
    # ========================================
    retira_placenta = models.BooleanField(
        default=False,
        verbose_name='¿Retira Placenta?'
    )
    
    estampado_placenta = models.BooleanField(
        default=False,
        verbose_name='¿Estampado de Placenta?'
    )
    
    # ========================================
    # 15. REGISTRO CIVIL
    # ========================================
    folio_valido = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Folio Válido'
    )
    
    folios_nulos = models.TextField(
        blank=True,
        verbose_name='Folios Nulos'
    )
    
    # ========================================
    # 16. OBSERVACIONES
    # ========================================
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    # ========================================
    # METADATOS
    # ========================================
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Modificación'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        ordering = ['-fecha_ingreso', '-hora_ingreso']
        verbose_name = 'Registro de Parto'
        verbose_name_plural = 'Registros de Partos'
    
    def __str__(self):
        return f"Parto - {self.paciente.persona.Nombre} - {self.fecha_ingreso}"


# ============================================
# MODELO: RECIÉN NACIDO
# ============================================

class RecienNacido(models.Model):
    """Datos del recién nacido"""
    
    registro_parto = models.OneToOneField(
        RegistroParto,
        on_delete=models.CASCADE,
        related_name='recien_nacido',
        verbose_name='Registro de Parto'
    )
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('I', 'Intersexual'),
    ]
    
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name='Sexo'
    )
    
    peso = models.PositiveIntegerField(
        validators=[MinValueValidator(500), MaxValueValidator(7000)],
        verbose_name='Peso (gramos)'
    )
    
    talla = models.PositiveIntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(70)],
        verbose_name='Talla (cm)'
    )
    
    ligadura_tardia_cordon = models.BooleanField(
        default=True,
        verbose_name='Ligadura Tardía del Cordón (> 1 minuto)'
    )
    
    apgar_1_minuto = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)],
        verbose_name='APGAR al 1 minuto'
    )
    
    apgar_5_minutos = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)],
        verbose_name='APGAR a los 5 minutos'
    )
    
    tiempo_apego = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Tiempo de Apego (minutos)'
    )
    
    apego_canguro = models.BooleanField(
        default=False,
        verbose_name='Apego Canguro'
    )
    
    class Meta:
        verbose_name = 'Recién Nacido'
        verbose_name_plural = 'Recién Nacidos'
    
    def __str__(self):
        return f"RN - {self.get_sexo_display()} - {self.peso}g"


# ============================================
# MODELO: EXÁMENES DEL PARTO
# ============================================

class ExamenesParto(models.Model):
    """Exámenes y tamizajes realizados durante el parto"""
    
    registro_parto = models.OneToOneField(
        RegistroParto,
        on_delete=models.CASCADE,
        related_name='examenes',
        verbose_name='Registro de Parto'
    )
    
    # ========== VIH ==========
    se_toma_vih_prepartos = models.BooleanField(
        default=False,
        verbose_name='¿Se Toma VIH en Prepartos?'
    )
    
    se_tomo_vih_sala = models.BooleanField(
        default=False,
        verbose_name='¿Se Tomó VIH en Sala?'
    )
    
    TRIMESTRE_CHOICES = [
        ('1', 'Primer Trimestre'),
        ('2', 'Segundo Trimestre'),
        ('3', 'Tercer Trimestre'),
    ]
    
    trimestre_pesquisa_vih = models.CharField(
        max_length=1,
        choices=TRIMESTRE_CHOICES,
        blank=True,
        verbose_name='Trimestre de Pesquisa VIH'
    )
    
    RESULTADO_CHOICES = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
        ('no_realizado', 'No Realizado'),
    ]
    
    resultado_vih = models.CharField(
        max_length=20,
        choices=RESULTADO_CHOICES,
        default='no_realizado',
        verbose_name='Resultado VIH'
    )
    
    # ========== STREPTOCOCO GRUPO B (SGB) ==========
    antibiotico_sgb = models.BooleanField(
        default=False,
        verbose_name='Antibiótico por SGB (NO por RPM)'
    )
    
    # ========== VDRL (Sífilis) ==========
    resultado_vdrl = models.CharField(
        max_length=20,
        choices=RESULTADO_CHOICES,
        default='no_realizado',
        verbose_name='Resultado VDRL'
    )
    
    tratamiento_atb_sifilis = models.BooleanField(
        default=False,
        verbose_name='Tratamiento ATB por Sífilis'
    )
    
    # ========== HEPATITIS B ==========
    examen_hepatitis_b = models.BooleanField(
        default=False,
        verbose_name='Examen Hepatitis B Tomado'
    )
    
    derivacion_gastro = models.BooleanField(
        default=False,
        verbose_name='Derivación a Gastro-Hepatólogo'
    )
    
    class Meta:
        verbose_name = 'Exámenes del Parto'
        verbose_name_plural = 'Exámenes de Partos'
    
    def __str__(self):
        return f"Exámenes - Parto {self.registro_parto.id}"


# ============================================
# MODELO: ANESTESIA DEL PARTO
# ============================================

class AnestesiaParto(models.Model):
    """Anestesia y analgesia durante el parto"""
    
    registro_parto = models.OneToOneField(
        RegistroParto,
        on_delete=models.CASCADE,
        related_name='anestesia',
        verbose_name='Registro de Parto'
    )
    
    # ========== ANESTESIA FARMACOLÓGICA ==========
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
    
    # ========== PERIDURAL ==========
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
    
    tiempo_espera_peridural = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Tiempo de Espera Peridural (minutos)'
    )
    
    # ========== ANALGESIA NO FARMACOLÓGICA ==========
    uso_analgesia_no_farmacologica = models.BooleanField(
        default=False,
        verbose_name='¿Uso Analgesia NO Farmacológica?'
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
    
    class Meta:
        verbose_name = 'Anestesia del Parto'
        verbose_name_plural = 'Anestesias de Partos'
    
    def __str__(self):
        return f"Anestesia - Parto {self.registro_parto.id}"


# ============================================
# MODELO: COMPLICACIONES DEL PUERPERIO
# ============================================

class ComplicacionesPuerperio(models.Model):
    """Complicaciones durante el puerperio inmediato"""
    
    registro_parto = models.OneToOneField(
        RegistroParto,
        on_delete=models.CASCADE,
        related_name='complicaciones',
        verbose_name='Registro de Parto'
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
        verbose_name='Manejo Quirúrgico de Inercia Uterina'
    )
    
    histerectomia_obstetrica = models.BooleanField(
        default=False,
        verbose_name='Histerectomía Obstétrica'
    )
    
    transfusion_sanguinea = models.BooleanField(
        default=False,
        verbose_name='Transfusión Sanguínea'
    )
    
    class Meta:
        verbose_name = 'Complicaciones del Puerperio'
        verbose_name_plural = 'Complicaciones del Puerperio'
    
    def __str__(self):
        return f"Complicaciones - Parto {self.registro_parto.id}"