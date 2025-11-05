# ingresoPartoApp/models.py
"""
Aplicación para gestionar el INGRESO y ADMISIÓN de pacientes para el parto
Contiene toda la información ANTES del parto: tamizajes, patologías, etc.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class FichaParto(models.Model):
    """
    Ficha de ingreso para el proceso de parto
    Se crea cuando la paciente ingresa a la unidad
    Contiene TODOS los datos de admisión y tamizajes
    """
    
    # ============================================
    # RELACIÓN CON FICHA OBSTÉTRICA
    # ============================================
    
    ficha_obstetrica = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.PROTECT,
        related_name='fichas_ingreso_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    numero_ficha_parto = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha de Parto',
        help_text='Se genera automáticamente: FP-000001'
    )
    
    # ============================================
    # SECCIÓN 1: DATOS GENERALES DEL INGRESO
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
        help_text='Clasificación de riesgo'
    )
    
    ORIGEN_INGRESO_CHOICES = [
        ('SALA', 'Sala'),
        ('UEGO', 'UEGO (Unidad Emergencia Gineco-Obstétrica)'),
    ]
    
    origen_ingreso = models.CharField(
        max_length=20,
        choices=ORIGEN_INGRESO_CHOICES,
        verbose_name='Origen de Ingreso',
        help_text='De dónde viene la paciente'
    )
    
    fecha_ingreso = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Ingreso'
    )
    
    plan_de_parto = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Plan de Parto?',
        help_text='¿La paciente presentó plan de parto?'
    )
    
    visita_guiada = models.BooleanField(
        default=False,
        verbose_name='¿Realizó Visita Guiada?',
        help_text='¿Hizo visita previa a la unidad?'
    )
    
    # ============================================
    # SECCIÓN 2: DATOS ADICIONALES
    # ============================================
    
    control_prenatal = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Control Prenatal',
        help_text='Descripción de controles prenatales'
    )
    
    consultorio_origen = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Consultorio de Origen',
        help_text='Centro de salud de procedencia'
    )
    
    # ============================================
    # SECCIÓN 3: PATOLOGÍAS AL INGRESO
    # ============================================
    
    preeclampsia_severa = models.BooleanField(
        default=False,
        verbose_name='Preeclampsia Severa'
    )
    
    eclampsia = models.BooleanField(
        default=False,
        verbose_name='Eclampsia'
    )
    
    sepsis_infeccion_sistemica = models.BooleanField(
        default=False,
        verbose_name='Sepsis o Infección Sistémica Grave'
    )
    
    infeccion_ovular_corioamnionitis = models.BooleanField(
        default=False,
        verbose_name='Infección Ovular o Corioamnionitis'
    )
    
    otra_patologia_texto = models.TextField(
        blank=True,
        verbose_name='Otra Patología',
        help_text='Descripción de otras patologías'
    )
    
    numero_aro = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nº ARO',
        help_text='Número de Alto Riesgo Obstétrico'
    )
    
    # ============================================
    # SECCIÓN 4: TAMIZAJE VIH
    # ============================================
    
    VIH_RESULTADO_CHOICES = [
        ('NO_TOMADO', 'No Tomado'),
        ('PRIMERO', '1° (Primer Examen)'),
        ('SEGUNDO', '2° (Segundo Examen)'),
        ('TERCERO', '3° (Tercer Examen)'),
    ]
    
    se_toma_vih_prepartos = models.BooleanField(
        default=False,
        verbose_name='Se toma VIH en Prepartos'
    )
    
    se_tomo_vih_sala = models.CharField(
        max_length=20,
        choices=VIH_RESULTADO_CHOICES,
        default='NO_TOMADO',
        verbose_name='Se tomó VIH en Sala (1°-2°-3°)'
    )
    
    # ============================================
    # SECCIÓN 5: TAMIZAJE SGB
    # ============================================
    
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='SGB - Pesquisa',
        help_text='¿Se realizó pesquisa de Streptococcus Grupo B?'
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
        verbose_name='SGB - Resultado'
    )
    
    sgb_antibiotico = models.BooleanField(
        default=False,
        verbose_name='Antibiótico por SGB (NO por RPM)',
        help_text='ATB por SGB positivo (no por rotura prematura)'
    )
    
    # ============================================
    # SECCIÓN 6: TAMIZAJE VDRL (SÍFILIS)
    # ============================================
    
    VDRL_RESULTADO_CHOICES = [
        ('NO_REALIZADO', 'No Realizado'),
        ('REACTIVO', 'Reactivo'),
        ('NO_REACTIVO', 'No Reactivo'),
    ]
    
    vdrl_resultado = models.CharField(
        max_length=20,
        choices=VDRL_RESULTADO_CHOICES,
        default='NO_REALIZADO',
        verbose_name='VDRL - Resultado durante embarazo'
    )
    
    vdrl_tratamiento_atb = models.BooleanField(
        default=False,
        verbose_name='Tratamiento ATB por Sífilis',
        help_text='¿Recibió tratamiento antibiótico?'
    )
    
    # ============================================
    # SECCIÓN 7: TAMIZAJE HEPATITIS B
    # ============================================
    
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='Examen Hepatitis B - Tomado'
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
        verbose_name='Derivación a Especialista',
        help_text='¿Se derivó a Gastro-Hepatólogo?'
    )
    
    # ============================================
    # OBSERVACIONES
    # ============================================
    
    observaciones_ingreso = models.TextField(
        blank=True,
        verbose_name='Observaciones de Ingreso'
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
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Ficha Activa',
        help_text='¿Está en proceso activo?'
    )
    
    class Meta:
        ordering = ['-fecha_ingreso', '-hora_ingreso']
        verbose_name = 'Ficha de Ingreso al Parto'
        verbose_name_plural = 'Fichas de Ingreso al Parto'
        indexes = [
            models.Index(fields=['numero_ficha_parto']),
            models.Index(fields=['ficha_obstetrica', 'activa']),
            models.Index(fields=['-fecha_ingreso']),
        ]
    
    def __str__(self):
        paciente = self.ficha_obstetrica.paciente.persona
        return f"{self.numero_ficha_parto} - {paciente.Nombre} {paciente.Apellido_Paterno}"
    
    def save(self, *args, **kwargs):
        """Generar número automático si no existe"""
        if not self.numero_ficha_parto:
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
    
    def tiene_patologias_criticas(self):
        """Verifica si tiene alguna patología crítica"""
        return (
            self.preeclampsia_severa or 
            self.eclampsia or 
            self.sepsis_infeccion_sistemica or 
            self.infeccion_ovular_corioamnionitis
        )
    
    def tamizajes_completos(self):
        """Verifica si todos los tamizajes están realizados"""
        return (
            self.se_toma_vih_prepartos or self.se_tomo_vih_sala != 'NO_TOMADO'
        ) and (
            self.sgb_pesquisa
        ) and (
            self.vdrl_resultado != 'NO_REALIZADO'
        ) and (
            self.hepatitis_b_tomado
        )