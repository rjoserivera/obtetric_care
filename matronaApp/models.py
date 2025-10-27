from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date, timedelta
from gestionApp.models import Paciente, Matrona, Tens
from medicoApp.models import Patologias


# ============================================
# MODELO DE FICHA OBSTÉTRICA
# ============================================
class FichaObstetrica(models.Model):
    """Ficha clínica obstétrica completa"""
    
    ORIGEN_DE_INGRESO_CHOICES = [
        ('SIN_ESPECIFICAR', 'Sin Especificar'),
        ('UEGO', 'UEGO (Unidad de Emergencias Gineco-obstétricas)'),
        ('SALA', 'Sala (Ingreso programado o derivado)'),
        ('PROGRAMADO', 'Programado'),
        ('DERIVADO', 'Derivado'),
    ]
    TIPO_DE_PACIENTE_CHOICES = [
        ('INSTITUCIONAL', 'Institucional'),
        ('PREHOSPITALIARIO', 'Prehospitalario'),
        ('FUERA_DE_LA_RED_ASISTENCIAL', 'Fuera de la Red Asistencial'),
        ('DOMICILIO_CON_ATENCION_PROFESIONAL', 'Domicilio con Atención Profesional'),
        ('DOMICILIO_SIN_ATENCION_PROFESIONAL', 'Domicilio sin Atención Profesional'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='fichas_obstetricas', verbose_name='Paciente')
    numero_ficha = models.CharField(max_length=20, unique=True, verbose_name='Número de Ficha')
    matrona_responsable = models.ForeignKey(Matrona, on_delete=models.PROTECT, related_name='fichas_asignadas', verbose_name='Matrona Responsable')
    Origen_de_ingreso = models.CharField(max_length=50, choices=ORIGEN_DE_INGRESO_CHOICES, default='SIN_ESPECIFICAR', verbose_name='Origen de Ingreso')
    Tipo_de_paciente = models.CharField(max_length=50, choices=TIPO_DE_PACIENTE_CHOICES, default='INSTITUCIONAL', verbose_name='Tipo de Paciente')
    nombre_acompanante = models.CharField(max_length=200, blank=True, verbose_name='Nombre del Acompañante')
    nacidos_vivos = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(20)], verbose_name='Nacidos Vivos', help_text='Número de hijos nacidos vivos')
    fecha_ultima_regla = models.DateField(null=True, blank=True, verbose_name='Fecha Última Regla (FUR)', help_text='Fecha del primer día de la última menstruación')
    fecha_probable_parto = models.DateField(null=True, blank=True, verbose_name='Fecha Probable de Parto (FPP)', help_text='Fecha estimada del parto')
    edad_gestacional_semanas = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(42)], verbose_name='Edad Gestacional (Semanas)', help_text='Calculado automáticamente desde FPP')
    edad_gestacional_dias = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(6)], verbose_name='Edad Gestacional (Días)', help_text='Días adicionales calculados automáticamente')
    patologias = models.ManyToManyField(Patologias, blank=True, related_name='fichas_con_patologia', verbose_name='Patologías Asociadas')
    descripcion_patologias = models.TextField(blank=True, verbose_name='Descripción de Patologías', help_text='Generado automáticamente desde patologías seleccionadas')
    observaciones_generales = models.TextField(blank=True, verbose_name='Observaciones Generales', help_text='Observaciones sobre el embarazo actual')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Última Modificación')
    activa = models.BooleanField(default=True, verbose_name='Ficha Activa', help_text='Indica si la ficha está activa o cerrada')
    
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
    
    def calcular_edad_gestacional_desde_fpp(self):
        """Calcula la edad gestacional actual basándose en la Fecha Probable de Parto (FPP). Un embarazo normal dura 280 días (40 semanas) desde la FUR."""
        if not self.fecha_probable_parto:
            return None, None
        hoy = date.today()
        dias_gestacion_normal = 280
        dias_desde_fur = dias_gestacion_normal - (self.fecha_probable_parto - hoy).days
        if dias_desde_fur < 0:
            return 0, 0
        semanas = dias_desde_fur // 7
        dias = dias_desde_fur % 7
        return semanas, dias
    
    def calcular_edad_gestacional_desde_fur(self):
        """Calcula la edad gestacional actual basándose en la Fecha de Última Regla (FUR)."""
        if not self.fecha_ultima_regla:
            return None, None
        hoy = date.today()
        dias_desde_fur = (hoy - self.fecha_ultima_regla).days
        if dias_desde_fur < 0:
            return 0, 0
        semanas = dias_desde_fur // 7
        dias = dias_desde_fur % 7
        return semanas, dias
    
    def actualizar_edad_gestacional(self):
        """Actualiza automáticamente la edad gestacional. Prioriza cálculo desde FPP, si no existe usa FUR."""
        if self.fecha_probable_parto:
            semanas, dias = self.calcular_edad_gestacional_desde_fpp()
        elif self.fecha_ultima_regla:
            semanas, dias = self.calcular_edad_gestacional_desde_fur()
        else:
            semanas, dias = None, None
        self.edad_gestacional_semanas = semanas
        self.edad_gestacional_dias = dias
    
    def generar_descripcion_patologias(self):
        """Genera automáticamente la descripción de patologías basándose en las patologías seleccionadas."""
        if not self.pk:
            return ""
        patologias_lista = self.patologias.all()
        if not patologias_lista:
            return "Sin patologías registradas"
        descripciones = []
        for patologia in patologias_lista:
            desc = f"• {patologia.nombre}"
            if hasattr(patologia, 'nivel_de_riesgo') and patologia.nivel_de_riesgo:
                desc += f" (Riesgo: {patologia.nivel_de_riesgo})"
            if hasattr(patologia, 'descripcion') and patologia.descripcion:
                desc += f"\n  {patologia.descripcion}"
            descripciones.append(desc)
        return "\n".join(descripciones)
    
    def save(self, *args, **kwargs):
        es_creacion = not self.pk
        if not self.numero_ficha:
            ultima_ficha = FichaObstetrica.objects.order_by('-id').first()
            if ultima_ficha:
                try:
                    numero = int(ultima_ficha.numero_ficha.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_ficha = f"FO-{numero:05d}"
        self.actualizar_edad_gestacional()
        if es_creacion:
            super().save(*args, **kwargs)
            self.descripcion_patologias = self.generar_descripcion_patologias()
            super().save(update_fields=['descripcion_patologias'])
        else:
            campos_modificados = []
            if self.pk:
                ficha_anterior = FichaObstetrica.objects.get(pk=self.pk)
                campos_a_comparar = ['Origen_de_ingreso', 'Tipo_de_paciente', 'nombre_acompanante', 'nacidos_vivos', 'fecha_ultima_regla', 'fecha_probable_parto', 'observaciones_generales', 'activa']
                for campo in campos_a_comparar:
                    valor_anterior = getattr(ficha_anterior, campo)
                    valor_actual = getattr(self, campo)
                    if valor_anterior != valor_actual:
                        campos_modificados.append(f"{campo}: '{valor_anterior}' → '{valor_actual}'")
            super().save(*args, **kwargs)
            self.descripcion_patologias = self.generar_descripcion_patologias()
            super().save(update_fields=['descripcion_patologias'])
            if campos_modificados:
                HistorialCambioFicha.objects.create(ficha=self, usuario=self.matrona_responsable.persona.Nombre, cambios_realizados="\n".join(campos_modificados))
    
    def edad_gestacional_completa(self):
        """Retorna la edad gestacional completa en formato legible"""
        if self.edad_gestacional_semanas is not None:
            texto = f"{self.edad_gestacional_semanas} semanas"
            if self.edad_gestacional_dias:
                texto += f" y {self.edad_gestacional_dias} días"
            return texto
        return "No calculada"


# ============================================
# MODELO DE HISTORIAL DE CAMBIOS DE FICHA
# ============================================
class HistorialCambioFicha(models.Model):
    """Registra todos los cambios realizados en una ficha obstétrica"""
    
    ficha = models.ForeignKey(FichaObstetrica, on_delete=models.CASCADE, related_name='historial_cambios', verbose_name='Ficha')
    fecha_cambio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha del Cambio')
    usuario = models.CharField(max_length=200, verbose_name='Usuario que Modificó', help_text='Nombre del usuario que realizó el cambio')
    cambios_realizados = models.TextField(verbose_name='Cambios Realizados', help_text='Detalle de los cambios efectuados')
    
    class Meta:
        ordering = ['-fecha_cambio']
        verbose_name = 'Historial de Cambio de Ficha'
        verbose_name_plural = 'Historiales de Cambios de Fichas'
        indexes = [
            models.Index(fields=['ficha', '-fecha_cambio']),
        ]
    
    def __str__(self):
        return f"Cambio en {self.ficha.numero_ficha} - {self.fecha_cambio.strftime('%d/%m/%Y %H:%M')} por {self.usuario}"


# ============================================
# MODELO DE MEDICAMENTOS EN FICHAS
# ============================================
class MedicamentoFicha(models.Model):
    """Medicamentos asignados a una ficha obstétrica por la matrona"""
    
    MEDICAMENTO_CHOICES = [
        ('Acido_Folico', 'Ácido Fólico'),
        ('Sulfato_Ferroso', 'Sulfato Ferroso'),
        ('Calcio', 'Calcio'),
        ('Aspirina', 'Aspirina'),
        ('Metildopa', 'Metildopa'),
        ('Insulina', 'Insulina'),
        ('Nifedipino', 'Nifedipino'),
        ('Otro', 'Otro'),
    ]
    VIA_CHOICES = [
        ('Oral', 'Oral'),
        ('Intramuscular', 'Intramuscular'),
        ('Intravenosa', 'Intravenosa'),
        ('Subcutanea', 'Subcutánea'),
    ]
    FRECUENCIA_CHOICES = [
        ('1_vez_dia', '1 vez al día'),
        ('2_veces_dia', '2 veces al día'),
        ('3_veces_dia', '3 veces al día'),
        ('Cada_8_horas', 'Cada 8 horas'),
        ('Cada_12_horas', 'Cada 12 horas'),
        ('SOS', 'SOS (según necesidad)'),
    ]
    DOSIS_CHOICES = [
        ('1_mg', '1 mg'),
        ('5_mg', '5 mg'),
        ('10_mg', '10 mg'),
        ('50_mg', '50 mg'),
        ('100_mg', '100 mg'),
        ('250_mg', '250 mg'),
        ('500_mg', '500 mg'),
        ('1_g', '1 g'),
        ('Otra', 'Otra dosis'),
    ]
    
    ficha = models.ForeignKey(FichaObstetrica, on_delete=models.CASCADE, related_name='medicamentos', verbose_name='Ficha Obstétrica')
    nombre_medicamento = models.CharField(max_length=100, choices=MEDICAMENTO_CHOICES, verbose_name='Medicamento')
    dosis = models.CharField(max_length=50, choices=DOSIS_CHOICES, verbose_name='Dosis')
    via_administracion = models.CharField(max_length=50, choices=VIA_CHOICES, verbose_name='Vía de Administración')
    frecuencia = models.CharField(max_length=50, choices=FRECUENCIA_CHOICES, verbose_name='Frecuencia')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio', help_text='Fecha en que inicia el tratamiento')
    fecha_termino = models.DateField(verbose_name='Fecha de Término', help_text='Fecha en que finaliza el tratamiento')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones', help_text='Indicaciones especiales sobre la medicación')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    
    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Medicamento de Ficha'
        verbose_name_plural = 'Medicamentos de Fichas'
        indexes = [
            models.Index(fields=['ficha', 'activo']),
        ]
    
    def __str__(self):
        return f"{self.get_nombre_medicamento_display()} - {self.get_dosis_display()} - {self.get_frecuencia_display()}"


# ============================================
# MODELO ADMINISTRACIÓN DE MEDICAMENTOS (TENS)
# ============================================
class AdministracionMedicamento(models.Model):
    """Registro de administración de medicamentos por TENS"""
    
    medicamento_ficha = models.ForeignKey(MedicamentoFicha, on_delete=models.CASCADE, related_name='administraciones', verbose_name='Medicamento Asignado')
    tens = models.ForeignKey(Tens, on_delete=models.PROTECT, related_name='administraciones_realizadas', verbose_name='TENS que Administró')
    fecha_hora_administracion = models.DateTimeField(default=timezone.now, verbose_name='Fecha y Hora de Administración')
    se_realizo_lavado = models.BooleanField(default=False, verbose_name='¿Se realizó lavado de manos?')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones de la Administración')
    reacciones_adversas = models.TextField(blank=True, verbose_name='Reacciones Adversas Observadas')
    administrado_exitosamente = models.BooleanField(default=True, verbose_name='¿Se administró exitosamente?')
    motivo_no_administracion = models.TextField(blank=True, verbose_name='Motivo de No Administración', help_text='Completar solo si no se administró')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro en Sistema')
    
    class Meta:
        ordering = ['-fecha_hora_administracion']
        verbose_name = 'Administración de Medicamento'
        verbose_name_plural = 'Administraciones de Medicamentos'
        indexes = [
            models.Index(fields=['medicamento_ficha', '-fecha_hora_administracion']),
            models.Index(fields=['tens', '-fecha_hora_administracion']),
        ]
    
    def __str__(self):
        fecha_str = self.fecha_hora_administracion.strftime('%d/%m/%Y %H:%M')
        tens_nombre = f"{self.tens.persona.Nombre} {self.tens.persona.Apellido_Paterno}"
        return f"{self.medicamento_ficha.get_nombre_medicamento_display()} - {fecha_str} - {tens_nombre}"