# partosApp/admin.py
"""
Configuración del panel de administración para partosApp
ACTUALIZADO: Con FichaParto y campos nuevos
"""

from django.contrib import admin
from django.utils.html import format_html
from partosApp.models import FichaParto, RegistroParto, RegistroRecienNacido, DocumentosParto


# ============================================
# ADMIN: FICHA DE PARTO (NUEVO)
# ============================================

@admin.register(FichaParto)
class FichaPartoAdmin(admin.ModelAdmin):
    """Administración de Fichas de Parto"""
    
    list_display = [
        'numero_ficha_parto',
        'get_paciente_nombre',
        'get_paciente_rut',
        'tipo_paciente',
        'origen_ingreso',
        'fecha_ingreso',
        'activa_badge',
    ]
    
    list_filter = [
        'tipo_paciente',
        'origen_ingreso',
        'fecha_ingreso',
        'activa',
        'plan_de_parto',
        'visita_guiada',
        'preeclampsia_severa',
        'eclampsia',
        'sepsis_infeccion_sistemica',
    ]
    
    search_fields = [
        'numero_ficha_parto',
        'ficha_obstetrica__numero_ficha',
        'ficha_obstetrica__paciente__persona__Rut',
        'ficha_obstetrica__paciente__persona__Nombre',
        'ficha_obstetrica__paciente__persona__Apellido_Paterno',
    ]
    
    readonly_fields = [
        'numero_ficha_parto',
        'fecha_creacion',
        'fecha_modificacion',
    ]
    
    fieldsets = (
        ('Información General', {
            'fields': (
                'numero_ficha_parto',
                'ficha_obstetrica',
                'tipo_paciente',
                'origen_ingreso',
            )
        }),
        ('Fecha y Hora de Ingreso', {
            'fields': (
                'fecha_ingreso',
                'hora_ingreso',
            )
        }),
        ('Plan de Parto', {
            'fields': (
                'plan_de_parto',
                'visita_guiada',
            )
        }),
        ('Datos Adicionales', {
            'fields': (
                'control_prenatal',
                'consultorio_origen',
            )
        }),
        ('Patologías al Ingreso', {
            'fields': (
                'preeclampsia_severa',
                'eclampsia',
                'sepsis_infeccion_sistemica',
                'infeccion_ovular_corioamnionitis',
                'otra_patologia_texto',
                'numero_aro',
            )
        }),
        ('Tamizaje VIH', {
            'fields': (
                'se_toma_vih_prepartos',
                'se_tomo_vih_sala',
            )
        }),
        ('Tamizaje SGB', {
            'fields': (
                'sgb_pesquisa',
                'sgb_resultado',
                'sgb_antibiotico',
            )
        }),
        ('Tamizaje VDRL', {
            'fields': (
                'vdrl_resultado',
                'vdrl_tratamiento_atb',
            )
        }),
        ('Tamizaje Hepatitis B', {
            'fields': (
                'hepatitis_b_tomado',
                'hepatitis_b_resultado',
                'hepatitis_b_derivacion',
            )
        }),
        ('Observaciones', {
            'fields': (
                'observaciones_ingreso',
            )
        }),
        ('Estado', {
            'fields': (
                'activa',
                'fecha_creacion',
                'fecha_modificacion',
            )
        }),
    )
    
    def get_paciente_nombre(self, obj):
        """Obtener nombre completo del paciente"""
        paciente = obj.ficha_obstetrica.paciente
        return f"{paciente.persona.Nombre} {paciente.persona.Apellido_Paterno}"
    get_paciente_nombre.short_description = 'Paciente'
    
    def get_paciente_rut(self, obj):
        """Obtener RUT del paciente"""
        return obj.ficha_obstetrica.paciente.persona.Rut
    get_paciente_rut.short_description = 'RUT'
    
    def activa_badge(self, obj):
        """Badge de estado activo/inactivo"""
        if obj.activa:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Activa</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Cerrada</span>'
        )
    activa_badge.short_description = 'Estado'


# ============================================
# ADMIN: REGISTRO DE PARTO (ACTUALIZADO)
# ============================================

@admin.register(RegistroParto)
class RegistroPartoAdmin(admin.ModelAdmin):
    """Administración de Registros de Parto"""
    
    list_display = [
        'numero_registro',
        'get_paciente_nombre',
        'tipo_parto_badge',
        'fecha_hora_admision',
        'fecha_hora_parto',
        'clasificacion_robson',
        'activo_badge',
    ]
    
    list_filter = [
        'tipo_parto',
        'fecha_hora_admision',
        'fecha_hora_parto',
        'clasificacion_robson',
        'activo',
        'tipo_regimen',
        'libertad_movimiento',
        'esterilizacion',
        'histerectomia_obstetrica',
        'transfusion_sanguinea',
    ]
    
    search_fields = [
        'numero_registro',
        'ficha__numero_ficha',
        'ficha__paciente__persona__Rut',
        'ficha__paciente__persona__Nombre',
        'profesional_responsable',
    ]
    
    readonly_fields = [
        'numero_registro',
        'fecha_creacion',
        'fecha_modificacion',
    ]
    
    fieldsets = (
        ('Información General', {
            'fields': (
                'numero_registro',
                'ficha',
                'ficha_parto',
                'fecha_hora_admision',
                'fecha_hora_parto',
            )
        }),
        ('Trabajo de Parto', {
            'fields': (
                'edad_gestacional_semanas',
                'edad_gestacional_dias',
                'monitor_ttc',
                'induccion',
                'aceleracion_correccion',
                'numero_tactos_vaginales',
                'rotura_membrana',
                'tiempo_membranas_rotas',
                'tiempo_dilatacion',
                'tiempo_expulsivo',
            )
        }),
        ('Condiciones del Parto', {
            'fields': (
                'libertad_movimiento',
                'tipo_regimen',
                'vih_tomado_prepartos',
                'vih_tomado_sala',
            )
        }),
        ('Tipo e Información del Parto', {
            'fields': (
                'tipo_parto',
                'alumbramiento_dirigido',
                'clasificacion_robson',
                'posicion_materna_parto',
            )
        }),
        ('Puerperio / Complicaciones', {
            'fields': (
                'ofrecimiento_posiciones_alternativas',
                'estado_perine',
                'esterilizacion',
                'revision',
                'inercia_uterina',
                'restos_placentarios',
                'trauma',
                'alteracion_coagulacion',
                'manejo_quirurgico_inercia',
                'histerectomia_obstetrica',
                'transfusion_sanguinea',
            )
        }),
        ('Anestesia y Analgesia', {
            'fields': (
                'anestesia_neuroaxial',
                'oxido_nitroso',
                'analgesia_endovenosa',
                'anestesia_general',
                'anestesia_local',
                'analgesia_no_farmacologica',
                'balon_kinesico',
                'lenteja_parto',
                'rebozo',
                'aromaterapia',
                'peridural_solicitada_paciente',
                'peridural_indicada_medico',
                'peridural_administrada',
                'tiempo_espera_peridural',
            )
        }),
        ('Información Profesionales', {
            'fields': (
                'profesional_responsable',
                'alumno',
                'causa_cesarea',
                'observaciones',
                'uso_sala_saip',
            )
        }),
        ('Metadatos', {
            'fields': (
                'activo',
                'fecha_creacion',
                'fecha_modificacion',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_paciente_nombre(self, obj):
        """Obtener nombre del paciente"""
        paciente = obj.ficha.paciente
        return f"{paciente.persona.Nombre} {paciente.persona.Apellido_Paterno}"
    get_paciente_nombre.short_description = 'Paciente'
    
    def tipo_parto_badge(self, obj):
        """Badge con color según tipo de parto"""
        colores = {
            'EUTOCICO': '#28a745',
            'DISTOCICO': '#ffc107',
            'CESAREA_URGENCIA': '#dc3545',
            'CESAREA_ELECTIVA': '#007bff',
        }
        color = colores.get(obj.tipo_parto, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_tipo_parto_display()
        )
    tipo_parto_badge.short_description = 'Tipo de Parto'
    
    def activo_badge(self, obj):
        """Badge de estado activo/inactivo"""
        if obj.activo:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Activo</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">Inactivo</span>'
        )
    activo_badge.short_description = 'Estado'


# ============================================
# ADMIN: RECIÉN NACIDO
# ============================================

@admin.register(RegistroRecienNacido)
class RegistroRecienNacidoAdmin(admin.ModelAdmin):
    """Administración de Registros de Recién Nacidos"""
    
    list_display = [
        'get_numero_parto',
        'sexo',
        'peso',
        'talla',
        'apgar_1_minuto',
        'apgar_5_minutos',
        'fecha_nacimiento',
        'clasificacion_peso_badge',
    ]
    
    list_filter = [
        'sexo',
        'fecha_nacimiento',
        'ligadura_tardia_cordon',
        'apego_canguro',
        'acompanamiento_parto',
    ]
    
    search_fields = [
        'registro_parto__numero_registro',
        'registro_parto__ficha__paciente__persona__Nombre',
    ]
    
    readonly_fields = [
        'fecha_creacion',
        'clasificacion_peso_display',
    ]
    
    fieldsets = (
        ('Información del Parto', {
            'fields': ('registro_parto',)
        }),
        ('Datos del Recién Nacido', {
            'fields': (
                'sexo',
                'peso',
                'talla',
                'ligadura_tardia_cordon',
                'apgar_1_minuto',
                'apgar_5_minutos',
                'fecha_nacimiento',
                'clasificacion_peso_display',
            )
        }),
        ('Apego', {
            'fields': (
                'tiempo_apego',
                'apego_canguro',
            )
        }),
        ('Acompañamiento', {
            'fields': (
                'acompanamiento_preparto',
                'acompanamiento_parto',
                'acompanamiento_rn',
                'motivo_parto_no_acompanado',
                'persona_acompanante',
                'acompanante_secciona_cordon',
            )
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    def get_numero_parto(self, obj):
        """Obtener número de registro del parto"""
        return obj.registro_parto.numero_registro
    get_numero_parto.short_description = 'Nº Parto'
    
    def clasificacion_peso_display(self, obj):
        """Mostrar clasificación del peso"""
        return obj.clasificacion_peso()
    clasificacion_peso_display.short_description = 'Clasificación de Peso'
    
    def clasificacion_peso_badge(self, obj):
        """Badge con color según clasificación de peso"""
        clasificacion = obj.clasificacion_peso()
        if 'Bajo peso' in clasificacion:
            color = '#dc3545'
        elif 'Macrosómico' in clasificacion:
            color = '#ffc107'
        else:
            color = '#28a745'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            clasificacion
        )
    clasificacion_peso_badge.short_description = 'Clasificación'


# ============================================
# ADMIN: DOCUMENTOS DEL PARTO
# ============================================

@admin.register(DocumentosParto)
class DocumentosPartoAdmin(admin.ModelAdmin):
    """Administración de Documentos de Parto"""
    
    list_display = [
        'get_numero_parto',
        'recuerdos_entregados_display',
        'retira_placenta',
        'estampado_placenta',
        'folio_valido',
    ]
    
    list_filter = [
        'retira_placenta',
        'estampado_placenta',
        'fecha_creacion',
    ]
    
    search_fields = [
        'registro_parto__numero_registro',
        'folio_valido',
        'recuerdos_entregados',
    ]
    
    readonly_fields = [
        'fecha_creacion',
        'fecha_modificacion',
    ]
    
    fieldsets = (
        ('Registro de Parto', {
            'fields': ('registro_parto',)
        }),
        ('Ley N° 21.372 Dominga', {
            'fields': (
                'recuerdos_entregados',
                'motivo_no_entrega_recuerdos',
            )
        }),
        ('Placenta', {
            'fields': (
                'retira_placenta',
                'estampado_placenta',
            )
        }),
        ('Registro Civil', {
            'fields': (
                'folio_valido',
                'folios_nulos',
            )
        }),
        ('Manejo del Dolor', {
            'fields': ('manejo_dolor_no_farmacologico',)
        }),
        ('Metadatos', {
            'fields': (
                'fecha_creacion',
                'fecha_modificacion',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_numero_parto(self, obj):
        """Obtener número de registro del parto"""
        return obj.registro_parto.numero_registro
    get_numero_parto.short_description = 'Nº Parto'
    
    def recuerdos_entregados_display(self, obj):
        """Mostrar si se entregaron recuerdos"""
        if obj.recuerdos_entregados:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Sí</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">No</span>'
        )
    recuerdos_entregados_display.short_description = 'Recuerdos'