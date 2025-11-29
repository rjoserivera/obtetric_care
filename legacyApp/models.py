# legacyApp/models.py
from django.db import models


class ControlesPrevios(models.Model):
    # --- Choices básicos ---
    TIPO_CONTROL_CHOICES = [
        ("PRENATAL", "Control prenatal"),
        ("EMERGENCIA", "Emergencia"),
        ("INGRESO", "Ingreso"),
    ]

    TIPO_PROFESIONAL_CHOICES = [
        ("MATRONA", "Matrona"),
        ("MEDICO", "Médico"),
        ("TENS", "TENS"),
        ("OTRO", "Otro"),
    ]

    MOV_FETALES_CHOICES = [
        ("PRESENTES", "Presentes"),
        ("DISMINUIDOS", "Disminuidos"),
        ("AUSENTES", "Ausentes"),
    ]

    PRESENTACION_CHOICES = [
        ("CEFALICA", "Cefálica"),
        ("PODALICA", "Podálica"),
        ("TRANSVERSA", "Transversa"),
        ("OTRA", "Otra"),
    ]

    SITUACION_CHOICES = [
        ("LONGITUDINAL", "Longitudinal"),
        ("TRANSVERSA", "Transversa"),
        ("OBLICUA", "Oblicua"),
        ("DESCONOCIDA", "Desconocida"),
    ]

    NIVEL_RIESGO_CHOICES = [
        ("BAJO", "Bajo"),
        ("MEDIO", "Medio"),
        ("ALTO", "Alto"),
        ("CRITICO", "Crítico"),
    ]

    EDENA_GRADO_CHOICES = [
        ("AUSENTE", "Ausente"),
        ("LEVE", "Leve"),
        ("MODERADO", "Moderado"),
        ("SEVERO", "Severo"),
    ]

    # ==============================
    #  IDENTIFICACIÓN DEL CONTROL
    # ==============================
    paciente_rut = models.CharField(max_length=12)  # vínculo con paciente por RUT
    fecha_control = models.DateField()
    numero_control = models.PositiveIntegerField(blank=True, null=True)
    tipo_control = models.CharField(
        max_length=20, choices=TIPO_CONTROL_CHOICES, blank=True, null=True
    )
    consultorio_origen = models.CharField(
        max_length=100, blank=True, null=True
    )  # CESFAM / consultorio
    profesional_nombre = models.CharField(max_length=150, blank=True, null=True)
    profesional_tipo = models.CharField(
        max_length=20, choices=TIPO_PROFESIONAL_CHOICES, blank=True, null=True
    )

    # ==============================
    #  EDAD GESTACIONAL
    # ==============================
    semanas_gestacion = models.PositiveIntegerField(blank=True, null=True)
    dias_gestacion = models.PositiveIntegerField(blank=True, null=True)
    fur = models.DateField("FUR", blank=True, null=True)
    fpp = models.DateField("FPP", blank=True, null=True)

    # ==============================
    #  DATOS ANTROPOMÉTRICOS
    # ==============================
    peso_kg = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    talla_cm = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    altura_uterina_cm = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    ganancia_peso_total_kg = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    # ==============================
    #  SIGNOS VITALES MATERNOS
    # ==============================
    presion_sistolica = models.IntegerField(blank=True, null=True)
    presion_diastolica = models.IntegerField(blank=True, null=True)
    frecuencia_cardiaca_materna = models.SmallIntegerField(blank=True, null=True)
    temperatura_c = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )
    saturacion_o2 = models.IntegerField(blank=True, null=True)

    # ==============================
    #  EVALUACIÓN FETAL
    # ==============================
    fcf_lpm = models.IntegerField(
        "Frecuencia Cardíaca Fetal (lpm)", blank=True, null=True
    )
    movimientos_fetales = models.CharField(
        max_length=20, choices=MOV_FETALES_CHOICES, blank=True, null=True
    )
    presentacion_fetal = models.CharField(
        max_length=20, choices=PRESENTACION_CHOICES, blank=True, null=True
    )
    situacion_fetal = models.CharField(
        max_length=20, choices=SITUACION_CHOICES, blank=True, null=True
    )

    # ==============================
    #  EXÁMENES DE LABORATORIO
    # ==============================
    glucosa_mg_dl = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    hemoglobina_g_dl = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )
    hematocrito_pct = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    grupo_sanguineo = models.CharField(max_length=3, blank=True, null=True)
    factor_rh = models.CharField(max_length=10, blank=True, null=True)
    proteinuria = models.CharField(max_length=20, blank=True, null=True)
    leucocitos_orina = models.CharField(max_length=50, blank=True, null=True)

    # ==============================
    # TAMIZAJES
    # ==============================

    # VIH
    vih_resultado = models.CharField(
        max_length=20, blank=True, null=True
    )  # negativo/positivo/pendiente
    vih_fecha_toma = models.DateField(blank=True, null=True)
    vih_orden = models.PositiveIntegerField(
        blank=True, null=True
    )  # 1, 2, 3 (orden de toma)

    # VDRL
    vdrl_resultado = models.CharField(max_length=20, blank=True, null=True)
    vdrl_fecha = models.DateField(blank=True, null=True)

    # SGB
    sgb_resultado = models.CharField(max_length=20, blank=True, null=True)
    sgb_fecha_cultivo = models.DateField(blank=True, null=True)
    sgb_profilaxis = models.BooleanField(blank=True, null=True)

    # Otros tamizajes
    toxoplasma_resultado = models.CharField(max_length=20, blank=True, null=True)
    toxoplasma_fecha = models.DateField(blank=True, null=True)
    hepatitis_b_resultado = models.CharField(max_length=20, blank=True, null=True)
    hepatitis_b_fecha = models.DateField(blank=True, null=True)

    # ==============================
    # PATOLOGÍAS DETECTADAS
    # ==============================
    diabetes_gestacional = models.BooleanField(blank=True, null=True)
    hipertension_arterial = models.BooleanField(blank=True, null=True)
    preeclampsia_leve = models.BooleanField(blank=True, null=True)
    preeclampsia_severa = models.BooleanField(blank=True, null=True)
    eclampsia = models.BooleanField(blank=True, null=True)
    anemia = models.BooleanField(blank=True, null=True)
    infeccion_urinaria = models.BooleanField(blank=True, null=True)
    corioamnionitis = models.BooleanField(blank=True, null=True)
    amenaza_parto_prematuro = models.BooleanField(blank=True, null=True)
    rotura_prematura_membranas = models.BooleanField(blank=True, null=True)
    otras_patologias = models.TextField(blank=True, null=True)

    # ==============================
    # NIVEL DE RIESGO
    # ==============================
    numero_aro = models.CharField(
        max_length=20, blank=True, null=True
    )  # N° de registro ARO
    nivel_riesgo = models.CharField(
        max_length=10, choices=NIVEL_RIESGO_CHOICES, blank=True, null=True
    )

    # ==============================
    # MEDICAMENTOS ACTIVOS
    # ==============================
    medicamentos_activos = models.TextField(blank=True, null=True)
    acido_folico = models.BooleanField(blank=True, null=True)
    sulfato_ferroso = models.BooleanField(blank=True, null=True)
    aspirina_profilactica = models.BooleanField(blank=True, null=True)
    otros_tratamientos = models.TextField(blank=True, null=True)

    # ==============================
    # ANTECEDENTES OBSTÉTRICOS
    # ==============================
    numero_gestas = models.PositiveIntegerField(blank=True, null=True)
    numero_partos = models.PositiveIntegerField(blank=True, null=True)
    partos_vaginales_previos = models.PositiveIntegerField(blank=True, null=True)
    cesareas_previas = models.PositiveIntegerField(blank=True, null=True)
    numero_abortos = models.PositiveIntegerField(blank=True, null=True)
    hijos_vivos = models.PositiveIntegerField(blank=True, null=True)
    paridad_formato = models.CharField(
        max_length=20, blank=True, null=True
    )  # Ej: G3P2A0

    # ==============================
    # EVALUACIÓN CLÍNICA
    # ==============================
    edema_grado = models.CharField(
        max_length=15, choices=EDENA_GRADO_CHOICES, blank=True, null=True
    )
    edema_localizacion = models.CharField(max_length=100, blank=True, null=True)
    varices = models.BooleanField(blank=True, null=True)
    reflejos_osteotendinosos = models.CharField(max_length=50, blank=True, null=True)

    # ==============================
    # PLAN Y SEGUIMIENTO
    # ==============================
    tiene_plan_parto = models.BooleanField(blank=True, null=True)
    realizo_visita_guiada = models.BooleanField(blank=True, null=True)
    fecha_proximo_control = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    indicaciones_medicas = models.TextField(blank=True, null=True)
    motivo_consulta = models.TextField(blank=True, null=True)

    # ==============================
    # METADATOS
    # ==============================
    turno = models.CharField(max_length=10, blank=True, null=True)  # mañana/tarde/noche
    fecha_hora_registro = models.DateTimeField(blank=True, null=True)
    sistema_origen = models.CharField(
        max_length=10, blank=True, null=True
    )  # Legacy / Nuevo / Otro

    class Meta:
        db_table = "controles_previos"
        # 🔒 Si realmente es solo lectura desde una BD histórica:
        managed = False

    def __str__(self):
        return f"{self.paciente_rut} - {self.fecha_control} (Ctrl {self.numero_control})"

