from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ============================================
# GESTIÓN DE SALAS
# ============================================
class Sala(models.Model):
    ESTADOS_SALA = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
        ('EN_LIMPIEZA', 'En Limpieza'),
        ('MANTENIMIENTO', 'Mantenimiento'),
    ]
    
    nombre = models.CharField(max_length=50, unique=True)  # "Sala A", "Sala B", "Sala C"
    codigo = models.CharField(max_length=10, unique=True)  # "A", "B", "C"
    estado = models.CharField(max_length=20, choices=ESTADOS_SALA, default='DISPONIBLE')
    proceso_activo = models.ForeignKey('ingresoPartoApp.FichaParto', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='sala_asignada')
    capacidad_maxima = models.IntegerField(default=10)  # Personas máximas en sala
    activa = models.BooleanField(default=True)  # Por si una sala está temporalmente fuera de servicio
    observaciones = models.TextField(blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gestionprocesos_sala'
        verbose_name = 'Sala de Parto'
        verbose_name_plural = 'Salas de Parto'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.nombre} - {self.estado}"


# ============================================
# PERSONAL Y TURNOS
# ============================================
class PersonalTurno(models.Model):
    ROLES = [
        ('MEDICO', 'Médico Obstetra'),
        ('MATRONA', 'Matrona'),
        ('TENS', 'TENS'),
        ('ANESTESIOLOGO', 'Anestesiólogo'),
    ]
    
    ESTADOS_DISPONIBILIDAD = [
        ('DISPONIBLE', 'Disponible'),
        ('ASIGNADO', 'Asignado a Proceso'),
        ('NO_DISPONIBLE', 'No Disponible'),
        ('FUERA_TURNO', 'Fuera de Turno'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turnos')
    rol = models.CharField(max_length=20, choices=ROLES)
    estado = models.CharField(max_length=20, choices=ESTADOS_DISPONIBILIDAD, default='DISPONIBLE')
    fecha_inicio_turno = models.DateTimeField()
    fecha_fin_turno = models.DateTimeField()
    proceso_asignado = models.ForeignKey('ingresoPartoApp.FichaParto', on_delete=models.SET_NULL, 
                                         null=True, blank=True, related_name='personal_turno')
    
    # Para notificaciones
    token_push = models.TextField(blank=True, null=True)  # Token para Web Push
    dispositivo_activo = models.BooleanField(default=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gestionprocesos_personal_turno'
        verbose_name = 'Personal en Turno'
        verbose_name_plural = 'Personal en Turnos'
        ordering = ['-fecha_inicio_turno']
        indexes = [
            models.Index(fields=['rol', 'estado']),
            models.Index(fields=['fecha_inicio_turno', 'fecha_fin_turno']),
        ]
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_rol_display()} ({self.estado})"


# ============================================
# ASIGNACIÓN DE PERSONAL A PROCESOS
# ============================================
class AsignacionPersonal(models.Model):
    ROLES_PROCESO = [
        ('MEDICO_PRINCIPAL', 'Médico Principal'),
        ('MEDICO_APOYO', 'Médico de Apoyo'),
        ('MATRONA_PRINCIPAL', 'Matrona Principal'),
        ('MATRONA_BEBE_A', 'Matrona Bebé A'),
        ('MATRONA_BEBE_B', 'Matrona Bebé B'),
        ('TENS_BEBE', 'TENS Asignado a Bebé'),
        ('TENS_APOYO', 'TENS de Apoyo'),
        ('ANESTESIOLOGO', 'Anestesiólogo'),
    ]
    
    proceso = models.ForeignKey('ingresoPartoApp.FichaParto', on_delete=models.CASCADE, 
                                related_name='asignaciones_personal')
    personal = models.ForeignKey(PersonalTurno, on_delete=models.CASCADE, 
                                 related_name='asignaciones')
    rol_en_proceso = models.CharField(max_length=30, choices=ROLES_PROCESO)
    
    # Timestamps críticos
    timestamp_notificacion = models.DateTimeField(auto_now_add=True)
    timestamp_confirmacion = models.DateTimeField(null=True, blank=True)
    timestamp_ingreso_sala = models.DateTimeField(null=True, blank=True)
    timestamp_salida_sala = models.DateTimeField(null=True, blank=True)
    
    # Control
    confirmo_asistencia = models.BooleanField(default=False)
    ingreso_a_sala = models.BooleanField(default=False)
    salio_de_sala = models.BooleanField(default=False)
    
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'gestionprocesos_asignacion_personal'
        verbose_name = 'Asignación de Personal'
        verbose_name_plural = 'Asignaciones de Personal'
        unique_together = ['proceso', 'personal', 'rol_en_proceso']
        ordering = ['timestamp_notificacion']
        indexes = [
            models.Index(fields=['proceso', 'confirmo_asistencia']),
            models.Index(fields=['personal', 'timestamp_notificacion']),
        ]
    
    def __str__(self):
        return f"{self.personal.usuario.get_full_name()} - {self.get_rol_en_proceso_display()} - Proceso {self.proceso.numero_ficha}"


# ============================================
# SISTEMA DE NOTIFICACIONES
# ============================================
class Notificacion(models.Model):
    TIPOS_NOTIFICACION = [
        ('URGENTE', 'Urgente - Proceso Normal'),
        ('CODIGO_ROJO', 'Código Rojo - Emergencia'),
        ('INFORMATIVA', 'Informativa'),
    ]
    
    ESTADOS_NOTIFICACION = [
        ('ENVIADA', 'Enviada'),
        ('ENTREGADA', 'Entregada al Dispositivo'),
        ('VISTA', 'Vista por Usuario'),
        ('CONFIRMADA', 'Confirmada'),
        ('EXPIRADA', 'Expirada (Sin Respuesta)'),
        ('ERROR', 'Error al Enviar'),
    ]
    
    proceso = models.ForeignKey('ingresoPartoApp.FichaParto', on_delete=models.CASCADE, 
                                related_name='notificaciones')
    destinatario = models.ForeignKey(PersonalTurno, on_delete=models.CASCADE, 
                                     related_name='notificaciones_recibidas')
    tipo = models.CharField(max_length=20, choices=TIPOS_NOTIFICACION)
    estado = models.CharField(max_length=20, choices=ESTADOS_NOTIFICACION, default='ENVIADA')
    
    # Contenido
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    
    # Timestamps
    timestamp_envio = models.DateTimeField(auto_now_add=True)
    timestamp_entrega = models.DateTimeField(null=True, blank=True)
    timestamp_vista = models.DateTimeField(null=True, blank=True)
    timestamp_confirmacion = models.DateTimeField(null=True, blank=True)
    timestamp_expiracion = models.DateTimeField()  # Envío + 1 minuto
    
    # Datos técnicos
    token_push_usado = models.TextField(blank=True, null=True)
    respuesta_servidor = models.TextField(blank=True, null=True)
    codigo_error = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = 'gestionprocesos_notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-timestamp_envio']
        indexes = [
            models.Index(fields=['proceso', 'estado']),
            models.Index(fields=['destinatario', 'timestamp_envio']),
            models.Index(fields=['estado', 'timestamp_expiracion']),
        ]
    
    def __str__(self):
        return f"{self.tipo} - {self.destinatario.usuario.get_full_name()} - {self.estado}"


# ============================================
# CONFIRMACIONES DE PERSONAL
# ============================================
class ConfirmacionPersonal(models.Model):
    notificacion = models.OneToOneField(Notificacion, on_delete=models.CASCADE, 
                                        related_name='confirmacion')
    asignacion = models.OneToOneField(AsignacionPersonal, on_delete=models.CASCADE, 
                                      related_name='confirmacion')
    
    confirmo = models.BooleanField(default=False)
    timestamp_confirmacion = models.DateTimeField(auto_now_add=True)
    tiempo_respuesta_segundos = models.IntegerField()  # Segundos desde envío hasta confirmación
    dentro_tiempo_limite = models.BooleanField(default=True)  # ¿Confirmó en menos de 1 minuto?
    
    # Datos del dispositivo
    ip_confirmacion = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    dispositivo = models.CharField(max_length=200, blank=True, null=True)  # "Mobile", "Tablet", "Desktop"
    
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'gestionprocesos_confirmacion_personal'
        verbose_name = 'Confirmación de Personal'
        verbose_name_plural = 'Confirmaciones de Personal'
        ordering = ['-timestamp_confirmacion']
    
    def __str__(self):
        return f"Confirmación - {self.asignacion.personal.usuario.get_full_name()} - {self.timestamp_confirmacion}"


# ============================================
# SISTEMA DE DERIVACIONES
# ============================================
class Derivacion(models.Model):
    TIPOS_DERIVACION = [
        ('MATERNA_UCI', 'Materna a UCI'),
        ('NEONATAL_NEO', 'Neonatal a Neonatología'),
        ('MATERNA_OTRO', 'Materna a Otro Servicio'),
        ('NEONATAL_OTRO', 'Neonatal a Otro Servicio'),
    ]
    
    MOTIVOS_DERIVACION = [
        ('PREECLAMPSIA_SEVERA', 'Preeclampsia Severa'),
        ('ECLAMPSIA', 'Eclampsia'),
        ('HEMORRAGIA_MASIVA', 'Hemorragia Post-Parto Masiva'),
        ('SEPSIS', 'Sepsis Puerperal'),
        ('EDEMA_PULMONAR', 'Edema Pulmonar'),
        ('TRAUMA_OBSTETRICO', 'Trauma Obstétrico Severo'),
        ('PREMATURIDAD_EXTREMA', 'Prematuridad Extrema (<32 semanas)'),
        ('DIFICULTAD_RESPIRATORIA', 'Dificultad Respiratoria Severa'),
        ('MALFORMACION_CONGENITA', 'Malformación Congénita'),
        ('APGAR_BAJO', 'APGAR Bajo Persistente'),
        ('OTRO', 'Otro Motivo'),
    ]
    
    ESTADOS_DERIVACION = [
        ('SOLICITADA', 'Solicitada'),
        ('ACEPTADA', 'Aceptada por Destino'),
        ('EN_TRASLADO', 'En Traslado'),
        ('COMPLETADA', 'Completada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    
    # Relaciones
    proceso = models.ForeignKey('ingresoPartoApp.FichaParto', on_delete=models.CASCADE, 
                                related_name='derivaciones')
    registro_recien_nacido = models.ForeignKey('recienNacidoApp.RegistroRecienNacido', 
                                               on_delete=models.CASCADE, null=True, blank=True,
                                               related_name='derivaciones')
    
    tipo = models.CharField(max_length=20, choices=TIPOS_DERIVACION)
    motivo = models.CharField(max_length=50, choices=MOTIVOS_DERIVACION)
    motivo_detallado = models.TextField()  # Descripción completa
    
    # Destino
    servicio_destino = models.CharField(max_length=100)  # "UCI Adultos", "Neonatología", etc.
    medico_receptor = models.CharField(max_length=200, blank=True, null=True)
    
    # Control
    estado = models.CharField(max_length=20, choices=ESTADOS_DERIVACION, default='SOLICITADA')
    medico_solicitante = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                           related_name='derivaciones_solicitadas')
    
    # Timestamps
    timestamp_solicitud = models.DateTimeField(auto_now_add=True)
    timestamp_aceptacion = models.DateTimeField(null=True, blank=True)
    timestamp_traslado = models.DateTimeField(null=True, blank=True)
    timestamp_completado = models.DateTimeField(null=True, blank=True)
    
    # Datos clínicos al momento de derivación
    signos_vitales = models.TextField(blank=True, null=True)  # JSON con PA, FC, FR, Temp, SatO2
    tratamiento_previo = models.TextField(blank=True, null=True)
    examenes_adjuntos = models.TextField(blank=True, null=True)
    
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'gestionprocesos_derivacion'
        verbose_name = 'Derivación'
        verbose_name_plural = 'Derivaciones'
        ordering = ['-timestamp_solicitud']
        indexes = [
            models.Index(fields=['proceso', 'tipo']),
            models.Index(fields=['estado', 'timestamp_solicitud']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - Proceso {self.proceso.numero_ficha} - {self.estado}"


# ============================================
# GENERADOR DE CÓDIGOS ÚNICOS
# ============================================
class GeneradorCodigo(models.Model):
    TIPOS_CODIGO = [
        ('MT', 'Proceso Materno (MT-XXXX)'),
        ('RN', 'Recién Nacido (RN-XXXX)'),
    ]
    
    tipo = models.CharField(max_length=5, choices=TIPOS_CODIGO, unique=True)
    prefijo = models.CharField(max_length=10)  # "MT", "RN"
    ultimo_numero = models.IntegerField(default=0)
    digitos_minimos = models.IntegerField(default=4)  # MT-0001, MT-0002, etc.
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gestionprocesos_generador_codigo'
        verbose_name = 'Generador de Código'
        verbose_name_plural = 'Generadores de Códigos'
    
    def obtener_siguiente_codigo(self):
        """
        Genera el siguiente código único.
        Uso: GeneradorCodigo.objects.get(tipo='MT').obtener_siguiente_codigo()
        Retorna: "MT-0145"
        """
        self.ultimo_numero += 1
        self.save()
        numero_formateado = str(self.ultimo_numero).zfill(self.digitos_minimos)
        return f"{self.prefijo}-{numero_formateado}"
    
    def __str__(self):
        return f"{self.prefijo} (Último: {self.ultimo_numero})"