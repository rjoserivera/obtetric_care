from django.db import models
from matronaApp.models import FichaObstetrica
from gestionApp.models import Tens
from django.utils import timezone


class RegistroTens(models.Model):
    """
    Registro de signos vitales por TENS
    Los TENS registran temperatura, presión arterial, etc.
    """
    
    TURNO_CHOICES = [
        ('MANANA', 'Mañana'),
        ('TARDE', 'Tarde'),
        ('NOCHE', 'Noche'),
    ]
    
    # ============================================
    # RELACIONES
    # ============================================
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='registros_tens',
        verbose_name='Ficha Obstétrica'
    )
    
    tens_responsable = models.ForeignKey(
        Tens,
        on_delete=models.PROTECT,
        related_name='registros_signos_vitales',
        null=True,
        blank=True,
        verbose_name='TENS Responsable'
    )
    
    # ============================================
    # DATOS DEL REGISTRO
    # ============================================
    
    fecha = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha del Registro'
    )
    
    turno = models.CharField(
        max_length=10,
        choices=TURNO_CHOICES,
        blank=True,
        verbose_name='Turno'
    )
    
    # ============================================
    # SIGNOS VITALES
    # ============================================
    
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name='Temperatura (°C)',
        help_text='Ej: 36.5'
    )
    
    frecuencia_cardiaca = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Frecuencia Cardíaca (lpm)',
        help_text='Latidos por minuto'
    )
    
    presion_arterial = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Presión Arterial',
        help_text='Formato: 120/80'
    )
    
    frecuencia_respiratoria = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Frecuencia Respiratoria (rpm)',
        help_text='Respiraciones por minuto'
    )
    
    saturacion_oxigeno = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Saturación de Oxígeno (%)',
        help_text='Porcentaje de saturación (SpO2)'
    )
    
    # ============================================
    # OBSERVACIONES
    # ============================================
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones',
        help_text='Observaciones adicionales del TENS'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro en Sistema'
    )
    
    class Meta:
        ordering = ['-fecha', '-fecha_registro']
        verbose_name = 'Registro TENS'
        verbose_name_plural = 'Registros TENS'
        indexes = [
            models.Index(fields=['ficha', '-fecha']),
            models.Index(fields=['tens_responsable', '-fecha']),
        ]
    
    def __str__(self):
        return f"Registro TENS - {self.ficha.numero_ficha} - {self.fecha}"
    
    def signos_vitales_alterados(self):
        """Verifica si hay signos vitales fuera de rango normal"""
        alterados = []
        
        # Temperatura normal: 36.0 - 37.5°C
        if self.temperatura:
            if self.temperatura < 36.0:
                alterados.append(f"Hipotermia ({self.temperatura}°C)")
            elif self.temperatura > 37.5:
                alterados.append(f"Fiebre ({self.temperatura}°C)")
        
        # Frecuencia cardíaca normal: 60-100 lpm
        if self.frecuencia_cardiaca:
            if self.frecuencia_cardiaca < 60:
                alterados.append(f"Bradicardia ({self.frecuencia_cardiaca} lpm)")
            elif self.frecuencia_cardiaca > 100:
                alterados.append(f"Taquicardia ({self.frecuencia_cardiaca} lpm)")
        
        # Saturación normal: >95%
        if self.saturacion_oxigeno and self.saturacion_oxigeno < 95:
            alterados.append(f"Hipoxemia ({self.saturacion_oxigeno}%)")
        
        # Frecuencia respiratoria normal: 12-20 rpm
        if self.frecuencia_respiratoria:
            if self.frecuencia_respiratoria < 12:
                alterados.append(f"Bradipnea ({self.frecuencia_respiratoria} rpm)")
            elif self.frecuencia_respiratoria > 20:
                alterados.append(f"Taquipnea ({self.frecuencia_respiratoria} rpm)")
        
        return alterados if alterados else None
    
    def estado_signos_vitales(self):
        """Retorna el estado general de los signos vitales"""
        alterados = self.signos_vitales_alterados()
        
        if alterados:
            return f"⚠️ ALTERADOS: {', '.join(alterados)}"
        return "✅ Normales"
    
    def resumen_signos_vitales(self):
        """Retorna un resumen de los signos vitales"""
        signos = []
        
        if self.temperatura:
            signos.append(f"T: {self.temperatura}°C")
        
        if self.frecuencia_cardiaca:
            signos.append(f"FC: {self.frecuencia_cardiaca} lpm")
        
        if self.presion_arterial:
            signos.append(f"PA: {self.presion_arterial}")
        
        if self.frecuencia_respiratoria:
            signos.append(f"FR: {self.frecuencia_respiratoria} rpm")
        
        if self.saturacion_oxigeno:
            signos.append(f"SpO2: {self.saturacion_oxigeno}%")
        
        return " | ".join(signos) if signos else "Sin signos vitales registrados"


