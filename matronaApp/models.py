from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from gestionApp.models import Paciente, Matrona, Tens
from medicoApp.models import Patologias


# ============================================
# MODELO DE INGRESO HOSPITALARIO
# ============================================

class IngresoPaciente(models.Model):
    """Registro de ingreso de paciente al área de obstetricia"""
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='ingresos',
        verbose_name='Paciente'
    )
    
    fecha_ingreso = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Ingreso'
    )
    
    motivo_consulta = models.TextField(
        verbose_name='Motivo de Consulta',
        help_text='Descripción del motivo de ingreso'
    )
    
    edad_gestacional_sem = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Edad Gestacional (semanas)',
        validators=[MinValueValidator(0), MaxValueValidator(42)]
    )
    
    derivacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Derivación',
        help_text='Hospital o servicio que deriva (si aplica)'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones del Ingreso'
    )
    
    numero_ficha = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha de Ingreso'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        ordering = ['-fecha_ingreso']
        verbose_name = 'Ingreso de Paciente'
        verbose_name_plural = 'Ingresos de Pacientes'
    
    def __str__(self):
        return f"Ingreso {self.numero_ficha} - {self.paciente.persona.Nombre}"
    
    def save(self, *args, **kwargs):
        if not self.numero_ficha:
            # Generar número de ficha automáticamente
            ultimo_ingreso = IngresoPaciente.objects.order_by('-id').first()
            if ultimo_ingreso:
                try:
                    numero = int(ultimo_ingreso.numero_ficha.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_ficha = f"ING-{numero:05d}"
        super().save(*args, **kwargs)


# ============================================
# MODELO DE FICHA OBSTÉTRICA
# ============================================

class FichaObstetrica(models.Model):
    """Ficha clínica obstétrica completa"""
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='fichas_obstetricas',
        verbose_name='Paciente'
    )
    
    numero_ficha = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha'
    )
    
    matrona_responsable = models.ForeignKey(
        Matrona,
        on_delete=models.PROTECT,
        related_name='fichas_asignadas',
        verbose_name='Matrona Responsable'
    )
    
    nombre_acompanante = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nombre del Acompañante'
    )
    
    # ============================================
    # ANTECEDENTES OBSTÉTRICOS
    # ============================================
    
    numero_gestas = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Número de Gestas',
        help_text='Número total de embarazos'
    )
    
    numero_partos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Número de Partos',
        help_text='Número total de partos'
    )
    
    partos_vaginales = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Partos Vaginales'
    )
    
    partos_cesareas = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Partos por Cesárea'
    )
    
    numero_abortos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Número de Abortos'
    )
    
    nacidos_vivos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Nacidos Vivos',
        help_text='Número de hijos nacidos vivos'
    )
    
    # ============================================
    # EMBARAZO ACTUAL
    # ============================================
    
    fecha_ultima_regla = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha Última Regla (FUR)',
        help_text='Fecha del primer día de la última menstruación'
    )
    
    fecha_probable_parto = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha Probable de Parto (FPP)',
        help_text='Fecha estimada del parto'
    )
    
    edad_gestacional_semanas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(42)],
        verbose_name='Edad Gestacional (Semanas)',
        help_text='Semanas completas de embarazo'
    )
    
    edad_gestacional_dias = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name='Edad Gestacional (Días)',
        help_text='Días adicionales a las semanas'
    )
    
    # ============================================
    # DATOS ANTROPOMÉTRICOS
    # ============================================
    
    peso_actual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        verbose_name='Peso Actual (kg)',
        help_text='Peso de la paciente en kilogramos'
    )
    
    talla = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(120), MaxValueValidator(220)],
        verbose_name='Talla (cm)',
        help_text='Estatura de la paciente en centímetros'
    )
    
    # ============================================
    # PATOLOGÍAS
    # ============================================
    
    patologias = models.ManyToManyField(
        Patologias,
        blank=True,
        related_name='fichas_con_patologia',
        verbose_name='Patologías Asociadas'
    )
    
    descripcion_patologias = models.TextField(
        blank=True,
        verbose_name='Descripción Detallada de Patologías',
        help_text='Detalles adicionales sobre las patologías'
    )
    
    # ============================================
    # 🆕 NUEVOS CAMPOS: PATOLOGÍAS CRÍTICAS
    # ============================================
    
    patologias_criticas = models.CharField(
        max_length=100,
        choices=[
            ('NINGUNA', 'Ninguna'),
            ('PREECLAMPSIA_SEVERA', 'Preeclampsia Severa'),
            ('ECLAMPSIA', 'Eclampsia'),
            ('SEPSIS', 'Sepsis o Infección Sistémica Grave'),
            ('CORIOAMNIONITIS', 'Infección Ovular o Corioamnionitis'),
        ],
        default='NINGUNA',
        verbose_name='Patologías Críticas',
        help_text='Patologías de alto riesgo vital'
    )
    
    # ============================================
    # 🆕 NUEVOS CAMPOS: TAMIZAJE VIH
    # ============================================
    
    vih_tomado = models.BooleanField(
        default=False,
        verbose_name='Toma de VIH Realizada',
        help_text='¿Se realizó la prueba de VIH durante el embarazo?'
    )
    
    vih_resultado = models.CharField(
        max_length=20,
        choices=[
            ('PENDIENTE', 'Pendiente'),
            ('NEGATIVO', 'Negativo'),
            ('POSITIVO', 'Positivo'),
            ('NO_REALIZADO', 'No Realizado'),
        ],
        default='PENDIENTE',
        blank=True,
        verbose_name='Resultado VIH',
        help_text='Resultado de la prueba de VIH'
    )
    
    vih_aro = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nº ARO (si otra patología)',
        help_text='Número ARO si se detecta otra patología'
    )
    
    # ============================================
    # 🆕 NUEVOS CAMPOS: TAMIZAJE SGB (Estreptococo Grupo B)
    # ============================================
    
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='Pesquisa SGB Realizada',
        help_text='¿Se realizó pesquisa de Estreptococo Grupo B?'
    )
    
    sgb_resultado = models.CharField(
        max_length=20,
        choices=[
            ('PENDIENTE', 'Pendiente'),
            ('NEGATIVO', 'Negativo'),
            ('POSITIVO', 'Positivo'),
            ('NO_REALIZADO', 'No Realizado'),
        ],
        default='PENDIENTE',
        blank=True,
        verbose_name='Resultado SGB',
        help_text='Resultado de la pesquisa SGB'
    )
    
    sgb_antibiotico = models.BooleanField(
        default=False,
        verbose_name='Antibiótico por SGB (NO POR RPM)',
        help_text='Antibiótico profiláctico por SGB positivo (no por rotura prematura de membranas)'
    )
    
    # ============================================
    # 🆕 NUEVOS CAMPOS: TAMIZAJE VDRL (Sífilis)
    # ============================================
    
    vdrl_resultado = models.CharField(
        max_length=20,
        choices=[
            ('PENDIENTE', 'Pendiente'),
            ('NO_REACTIVO', 'No Reactivo'),
            ('REACTIVO', 'Reactivo'),
            ('NO_REALIZADO', 'No Realizado'),
        ],
        default='PENDIENTE',
        blank=True,
        verbose_name='Resultado VDRL durante embarazo',
        help_text='Resultado de la prueba VDRL para detectar sífilis'
    )
    
    vdrl_tratamiento_atb = models.BooleanField(
        default=False,
        verbose_name='Tratamiento ATB por Sífilis al momento del Parto',
        help_text='¿Se administró tratamiento antibiótico por sífilis?'
    )
    
    # ============================================
    # 🆕 NUEVOS CAMPOS: TAMIZAJE HEPATITIS B
    # ============================================
    
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='Examen Hepatitis B Tomado',
        help_text='¿Se realizó el examen de Hepatitis B?'
    )
    
    hepatitis_b_resultado = models.CharField(
        max_length=20,
        choices=[
            ('PENDIENTE', 'Pendiente'),
            ('NEGATIVO', 'Negativo'),
            ('POSITIVO', 'Positivo'),
            ('NO_REALIZADO', 'No Realizado'),
        ],
        default='PENDIENTE',
        blank=True,
        verbose_name='Resultado Hepatitis B',
        help_text='Resultado del examen de Hepatitis B'
    )
    
    hepatitis_b_derivacion = models.BooleanField(
        default=False,
        verbose_name='Derivación a Gastro-Hepatólogo',
        help_text='¿Se derivó a especialista en gastroenterología/hepatología?'
    )
    
    # ============================================
    # OBSERVACIONES
    # ============================================
    
    observaciones_generales = models.TextField(
        blank=True,
        verbose_name='Observaciones Generales',
        help_text='Observaciones sobre el embarazo actual'
    )
    
    antecedentes_relevantes = models.TextField(
        blank=True,
        verbose_name='Antecedentes Médicos Relevantes',
        help_text='Antecedentes médicos, quirúrgicos, alergias, etc.'
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
        help_text='Indica si la ficha está activa o cerrada'
    )
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Ficha Obstétrica'
        verbose_name_plural = 'Fichas Obstétricas'
        indexes = [
            models.Index(fields=['numero_ficha']),
            models.Index(fields=['paciente', 'activa']),
            models.Index(fields=['-fecha_creacion']),
        ]
    
    def __str__(self):
        return f"Ficha {self.numero_ficha} - {self.paciente.persona.Nombre} {self.paciente.persona.Apellido_Paterno}"
    
    def save(self, *args, **kwargs):
        if not self.numero_ficha:
            # Generar número de ficha automáticamente
            ultima_ficha = FichaObstetrica.objects.order_by('-id').first()
            if ultima_ficha:
                try:
                    numero = int(ultima_ficha.numero_ficha.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_ficha = f"FO-{numero:05d}"
        super().save(*args, **kwargs)
    
    # ============================================
    # MÉTODOS PARA CALCULAR IMC
    # ============================================
    
    def calcular_imc(self):
        """
        Calcula el IMC (Índice de Masa Corporal)
        Fórmula: IMC = peso (kg) / (talla en metros)²
        
        Returns:
            float: IMC redondeado a 2 decimales
            None: Si no se puede calcular
        """
        if self.peso_actual and self.talla and self.talla > 0:
            try:
                talla_metros = float(self.talla) / 100  # Convertir cm a metros
                peso_kg = float(self.peso_actual)
                imc = peso_kg / (talla_metros ** 2)
                return round(imc, 2)
            except (ValueError, ZeroDivisionError):
                return None
        return None
    
    def clasificacion_imc(self):
        """
        Retorna la clasificación del IMC según OMS
        
        Returns:
            str: Clasificación del IMC
        """
        imc = self.calcular_imc()
        if not imc:
            return "No calculable"
        
        if imc < 18.5:
            return "Bajo peso"
        elif imc < 25:
            return "Normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"
    
    def color_imc(self):
        """
        Retorna el color Bootstrap según la clasificación del IMC
        
        Returns:
            str: Clase de color Bootstrap (success, warning, danger, secondary)
        """
        imc = self.calcular_imc()
        if not imc:
            return "secondary"
        
        if imc < 18.5:
            return "warning"
        elif imc < 25:
            return "success"
        elif imc < 30:
            return "warning"
        else:
            return "danger"
    
    def edad_gestacional_completa(self):
        """
        Retorna la edad gestacional completa en formato legible
        
        Returns:
            str: Edad gestacional formateada (ej: "32 semanas y 4 días")
        """
        if self.edad_gestacional_semanas is not None:
            texto = f"{self.edad_gestacional_semanas} semanas"
            if self.edad_gestacional_dias:
                texto += f" y {self.edad_gestacional_dias} días"
            return texto
        return "No registrada"


# ============================================
# MODELO DE MEDICAMENTO EN FICHA
# ============================================

class MedicamentoFicha(models.Model):
    """Medicamentos asignados a una ficha obstétrica"""
    
    VIA_ADMINISTRACION_CHOICES = [
        ('oral', 'Oral'),
        ('endovenosa', 'Endovenosa'),
        ('intramuscular', 'Intramuscular'),
        ('subcutanea', 'Subcutánea'),
        ('topica', 'Tópica'),
    ]
    
    FRECUENCIA_CHOICES = [
        ('1_vez_dia', '1 vez al día'),
        ('2_veces_dia', '2 veces al día'),
        ('3_veces_dia', '3 veces al día'),
        ('Cada_8_horas', 'Cada 8 horas'),
        ('Cada_12_horas', 'Cada 12 horas'),
        ('SOS', 'SOS (según necesidad)'),
    ]
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='medicamentos',
        verbose_name='Ficha Obstétrica'
    )
    
    nombre_medicamento = models.CharField(
        max_length=200,
        verbose_name='Nombre del Medicamento'
    )
    
    dosis = models.CharField(
        max_length=100,
        verbose_name='Dosis'
    )
    
    via_administracion = models.CharField(
        max_length=50,
        choices=VIA_ADMINISTRACION_CHOICES,
        verbose_name='Vía de Administración'
    )
    
    frecuencia = models.CharField(
        max_length=50,
        choices=FRECUENCIA_CHOICES,
        verbose_name='Frecuencia'
    )
    
    fecha_inicio = models.DateField(
        verbose_name='Fecha de Inicio',
        help_text='Fecha en que inicia el tratamiento'
    )
    
    fecha_termino = models.DateField(
        verbose_name='Fecha de Término',
        help_text='Fecha en que finaliza el tratamiento'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones',
        help_text='Indicaciones especiales sobre la medicación'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Medicamento de Ficha'
        verbose_name_plural = 'Medicamentos de Fichas'
        indexes = [
            models.Index(fields=['ficha', 'activo']),
        ]
    
    def __str__(self):
        return f"{self.nombre_medicamento} - {self.ficha.numero_ficha}"


# ============================================
# MODELO DE ADMINISTRACIÓN DE MEDICAMENTO
# ============================================

class AdministracionMedicamento(models.Model):
    """Registro de administración de medicamentos por TENS"""
    
    medicamento_ficha = models.ForeignKey(
        MedicamentoFicha,
        on_delete=models.CASCADE,
        related_name='administraciones',
        verbose_name='Medicamento Asignado'
    )
    
    tens = models.ForeignKey(
        Tens,
        on_delete=models.PROTECT,
        related_name='administraciones_realizadas',
        verbose_name='TENS que Administró'
    )
    
    fecha_hora_administracion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Administración'
    )
    
    se_realizo_lavado = models.BooleanField(
        default=False,
        verbose_name='¿Se realizó lavado de manos?'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones de la Administración'
    )
    
    reacciones_adversas = models.TextField(
        blank=True,
        verbose_name='Reacciones Adversas Observadas'
    )
    
    administrado_exitosamente = models.BooleanField(
        default=True,
        verbose_name='¿Se administró exitosamente?'
    )
    
    motivo_no_administracion = models.TextField(
        blank=True,
        verbose_name='Motivo de No Administración',
        help_text='Completar solo si no se administró'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro en Sistema'
    )
    
    class Meta:
        ordering = ['-fecha_hora_administracion']
        verbose_name = 'Administración de Medicamento'
        verbose_name_plural = 'Administraciones de Medicamentos'
        indexes = [
            models.Index(fields=['medicamento_ficha', '-fecha_hora_administracion']),
            models.Index(fields=['tens', '-fecha_hora_administracion']),
        ]
    
    def __str__(self):
        return f"Administración {self.medicamento_ficha.nombre_medicamento} - {self.fecha_hora_administracion.strftime('%d/%m/%Y %H:%M')}"