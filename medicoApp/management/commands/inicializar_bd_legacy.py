# ============================================
# UBICACIÓN: medicoApp/management/commands/inicializar_bd_legacy.py
# Crea la base de datos legacy y la tabla controles_previos
# ============================================

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Inicializa la base de datos LEGACY y crea la tabla controles_previos'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.WARNING('\n🔧 Inicializando Base de Datos LEGACY...'))
            
            with connection.cursor() as cursor:
                # Crear la base de datos legacy si no existe
                self.stdout.write('  📦 Creando base de datos legacy_obstetric...')
                cursor.execute("CREATE DATABASE IF NOT EXISTS legacy_obstetric CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                
                # Usar la BD legacy
                cursor.execute("USE legacy_obstetric")
                
                # Crear la tabla controles_previos
                self.stdout.write('  📋 Creando tabla controles_previos...')
                
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS `controles_previos` (
                    `id` bigint NOT NULL AUTO_INCREMENT,
                    `paciente_rut` varchar(12) NOT NULL,
                    `fecha_control` date NOT NULL,
                    `numero_control` int unsigned DEFAULT NULL,
                    `tipo_control` varchar(20) DEFAULT NULL,
                    `consultorio_origen` varchar(100) DEFAULT NULL,
                    `profesional_nombre` varchar(150) DEFAULT NULL,
                    `profesional_tipo` varchar(20) DEFAULT NULL,
                    `semanas_gestacion` int unsigned DEFAULT NULL,
                    `dias_gestacion` int unsigned DEFAULT NULL,
                    `fur` date DEFAULT NULL,
                    `fpp` date DEFAULT NULL,
                    `peso_kg` decimal(5,2) DEFAULT NULL,
                    `talla_cm` decimal(5,2) DEFAULT NULL,
                    `imc` decimal(5,2) DEFAULT NULL,
                    `altura_uterina_cm` decimal(5,2) DEFAULT NULL,
                    `ganancia_peso_total_kg` decimal(5,2) DEFAULT NULL,
                    `presion_sistolica` int DEFAULT NULL,
                    `presion_diastolica` int DEFAULT NULL,
                    `frecuencia_cardiaca_materna` smallint DEFAULT NULL,
                    `temperatura_c` decimal(4,1) DEFAULT NULL,
                    `saturacion_o2` int DEFAULT NULL,
                    `fcf_lpm` int DEFAULT NULL,
                    `movimientos_fetales` varchar(20) DEFAULT NULL,
                    `presentacion_fetal` varchar(20) DEFAULT NULL,
                    `situacion_fetal` varchar(20) DEFAULT NULL,
                    `glucosa_mg_dl` decimal(6,2) DEFAULT NULL,
                    `hemoglobina_g_dl` decimal(4,1) DEFAULT NULL,
                    `hematocrito_pct` decimal(5,2) DEFAULT NULL,
                    `grupo_sanguineo` varchar(3) DEFAULT NULL,
                    `factor_rh` varchar(10) DEFAULT NULL,
                    `proteinuria` varchar(20) DEFAULT NULL,
                    `leucocitos_orina` varchar(50) DEFAULT NULL,
                    `vih_resultado` varchar(20) DEFAULT NULL,
                    `vih_fecha_toma` date DEFAULT NULL,
                    `vih_orden` int unsigned DEFAULT NULL,
                    `vdrl_resultado` varchar(20) DEFAULT NULL,
                    `vdrl_fecha` date DEFAULT NULL,
                    `sgb_resultado` varchar(20) DEFAULT NULL,
                    `sgb_fecha_cultivo` date DEFAULT NULL,
                    `sgb_profilaxis` tinyint(1) DEFAULT NULL,
                    `toxoplasma_resultado` varchar(20) DEFAULT NULL,
                    `toxoplasma_fecha` date DEFAULT NULL,
                    `hepatitis_b_resultado` varchar(20) DEFAULT NULL,
                    `hepatitis_b_fecha` date DEFAULT NULL,
                    `diabetes_gestacional` tinyint(1) DEFAULT NULL,
                    `hipertension_arterial` tinyint(1) DEFAULT NULL,
                    `preeclampsia_leve` tinyint(1) DEFAULT NULL,
                    `preeclampsia_severa` tinyint(1) DEFAULT NULL,
                    `eclampsia` tinyint(1) DEFAULT NULL,
                    `anemia` tinyint(1) DEFAULT NULL,
                    `infeccion_urinaria` tinyint(1) DEFAULT NULL,
                    `corioamnionitis` tinyint(1) DEFAULT NULL,
                    `amenaza_parto_prematuro` tinyint(1) DEFAULT NULL,
                    `rotura_prematura_membranas` tinyint(1) DEFAULT NULL,
                    `otras_patologias` text,
                    `numero_aro` varchar(20) DEFAULT NULL,
                    `nivel_riesgo` varchar(10) DEFAULT NULL,
                    `medicamentos_activos` text,
                    `acido_folico` tinyint(1) DEFAULT NULL,
                    `sulfato_ferroso` tinyint(1) DEFAULT NULL,
                    `aspirina_profilactica` tinyint(1) DEFAULT NULL,
                    `otros_tratamientos` text,
                    `numero_gestas` int unsigned DEFAULT NULL,
                    `numero_partos` int unsigned DEFAULT NULL,
                    `partos_vaginales_previos` int unsigned DEFAULT NULL,
                    `cesareas_previas` int unsigned DEFAULT NULL,
                    `numero_abortos` int unsigned DEFAULT NULL,
                    `hijos_vivos` int unsigned DEFAULT NULL,
                    `paridad_formato` varchar(20) DEFAULT NULL,
                    `edema_grado` varchar(15) DEFAULT NULL,
                    `edema_localizacion` varchar(100) DEFAULT NULL,
                    `varices` tinyint(1) DEFAULT NULL,
                    `reflejos_osteotendinosos` varchar(50) DEFAULT NULL,
                    `tiene_plan_parto` tinyint(1) DEFAULT NULL,
                    `realizo_visita_guiada` tinyint(1) DEFAULT NULL,
                    `fecha_proximo_control` date DEFAULT NULL,
                    `observaciones` text,
                    `indicaciones_medicas` text,
                    `motivo_consulta` text,
                    `turno` varchar(10) DEFAULT NULL,
                    `fecha_hora_registro` datetime DEFAULT NULL,
                    `sistema_origen` varchar(10) DEFAULT NULL,
                    PRIMARY KEY (`id`),
                    KEY `idx_paciente_rut` (`paciente_rut`),
                    KEY `idx_fecha_control` (`fecha_control`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
                
                cursor.execute(create_table_sql)
                
                # Volver a la BD principal
                cursor.execute("USE obstetric_carebdd")
                
                self.stdout.write(
                    self.style.SUCCESS(
                        '\n✅ Base de datos LEGACY inicializada correctamente'
                    )
                )
                self.stdout.write('  ✓ Base de datos: legacy_obstetric')
                self.stdout.write('  ✓ Tabla: controles_previos')
                self.stdout.write(
                    self.style.WARNING(
                        '\n💡 SIGUIENTE PASO:'
                    )
                )
                self.stdout.write('  Ejecuta: python manage.py cargar_controles_legacy')
                self.stdout.write('  Para cargar los controles de prueba de Ana Silva Rivas\n')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error al inicializar BD legacy: {str(e)}')
            )
            raise
