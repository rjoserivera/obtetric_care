# ============================================
# UBICACIÓN: medicoApp/management/commands/cargar_controles_legacy.py
# Carga controles previos en la BD LEGACY para Ana Silva Rivas
# ============================================

from django.core.management.base import BaseCommand
from django.db import connection
from datetime import date, datetime


class Command(BaseCommand):
    help = 'Carga controles previos en BD LEGACY para Ana Silva Rivas (RUT: 16293109-1)'

    def handle(self, *args, **options):
        try:
            rut_paciente = '16293109-1'
            
            self.stdout.write(self.style.WARNING('\n📋 Cargando controles previos en BD LEGACY...'))
            self.stdout.write(f'  👤 Paciente: Ana Silva Rivas')
            self.stdout.write(f'  🆔 RUT: {rut_paciente}\n')
            
            # Datos de los 5 controles previos
            controles = [
                {
                    'fecha_control': '2023-01-15',
                    'numero_control': 1,
                    'tipo_control': 'PRENATAL',
                    'consultorio_origen': 'CESFAM Coronel',
                    'profesional_nombre': 'Dra. María González',
                    'profesional_tipo': 'MEDICO',
                    'semanas_gestacion': 8,
                    'dias_gestacion': 3,
                    'fur': '2022-11-20',
                    'fpp': '2023-08-27',
                    'peso_kg': 62.5,
                    'talla_cm': 162.0,
                    'imc': 23.8,
                    'presion_sistolica': 110,
                    'presion_diastolica': 70,
                    'frecuencia_cardiaca_materna': 72,
                    'temperatura_c': 36.5,
                    'fcf_lpm': 145,
                    'movimientos_fetales': 'PRESENTES',
                    'presentacion_fetal': 'CEFALICA',
                    'situacion_fetal': 'LONGITUDINAL',
                    'glucosa_mg_dl': 85.0,
                    'hemoglobina_g_dl': 12.5,
                    'hematocrito_pct': 38.0,
                    'grupo_sanguineo': 'O',
                    'factor_rh': '+',
                    'vih_resultado': 'NEGATIVO',
                    'vih_fecha_toma': '2023-01-15',
                    'vdrl_resultado': 'NO_REACTIVO',
                    'vdrl_fecha': '2023-01-15',
                    'nivel_riesgo': 'BAJO',
                    'numero_gestas': 2,
                    'numero_partos': 1,
                    'partos_vaginales_previos': 1,
                    'cesareas_previas': 0,
                    'numero_abortos': 0,
                    'hijos_vivos': 1,
                    'paridad_formato': 'G2P1A0',
                    'acido_folico': True,
                    'sulfato_ferroso': True,
                    'fecha_proximo_control': '2023-02-15',
                    'observaciones': 'Embarazo de curso normal. Paciente sin antecedentes mórbidos.',
                    'indicaciones_medicas': 'Continuar con ácido fólico y sulfato ferroso. Control en 4 semanas.',
                    'sistema_origen': 'Legacy'
                },
                {
                    'fecha_control': '2023-02-20',
                    'numero_control': 2,
                    'tipo_control': 'PRENATAL',
                    'consultorio_origen': 'CESFAM Coronel',
                    'profesional_nombre': 'Matrona Carmen Rojas',
                    'profesional_tipo': 'MATRONA',
                    'semanas_gestacion': 13,
                    'dias_gestacion': 2,
                    'fur': '2022-11-20',
                    'fpp': '2023-08-27',
                    'peso_kg': 64.0,
                    'talla_cm': 162.0,
                    'imc': 24.4,
                    'altura_uterina_cm': 12.0,
                    'ganancia_peso_total_kg': 1.5,
                    'presion_sistolica': 115,
                    'presion_diastolica': 72,
                    'frecuencia_cardiaca_materna': 75,
                    'temperatura_c': 36.6,
                    'fcf_lpm': 150,
                    'movimientos_fetales': 'PRESENTES',
                    'presentacion_fetal': 'CEFALICA',
                    'situacion_fetal': 'LONGITUDINAL',
                    'glucosa_mg_dl': 88.0,
                    'hemoglobina_g_dl': 12.2,
                    'hematocrito_pct': 37.5,
                    'nivel_riesgo': 'BAJO',
                    'numero_gestas': 2,
                    'numero_partos': 1,
                    'partos_vaginales_previos': 1,
                    'cesareas_previas': 0,
                    'numero_abortos': 0,
                    'hijos_vivos': 1,
                    'paridad_formato': 'G2P1A0',
                    'acido_folico': True,
                    'sulfato_ferroso': True,
                    'edema_grado': 'AUSENTE',
                    'varices': False,
                    'fecha_proximo_control': '2023-03-20',
                    'observaciones': 'Embarazo evolucionando favorablemente. Ecografía de 12 semanas normal.',
                    'indicaciones_medicas': 'Continuar suplementación. Control mensual.',
                    'sistema_origen': 'Legacy'
                },
                {
                    'fecha_control': '2023-04-10',
                    'numero_control': 3,
                    'tipo_control': 'PRENATAL',
                    'consultorio_origen': 'CESFAM Coronel',
                    'profesional_nombre': 'Matrona Carmen Rojas',
                    'profesional_tipo': 'MATRONA',
                    'semanas_gestacion': 20,
                    'dias_gestacion': 5,
                    'fur': '2022-11-20',
                    'fpp': '2023-08-27',
                    'peso_kg': 67.5,
                    'talla_cm': 162.0,
                    'imc': 25.7,
                    'altura_uterina_cm': 18.0,
                    'ganancia_peso_total_kg': 5.0,
                    'presion_sistolica': 118,
                    'presion_diastolica': 75,
                    'frecuencia_cardiaca_materna': 78,
                    'temperatura_c': 36.7,
                    'saturacion_o2': 98,
                    'fcf_lpm': 148,
                    'movimientos_fetales': 'PRESENTES',
                    'presentacion_fetal': 'CEFALICA',
                    'situacion_fetal': 'LONGITUDINAL',
                    'glucosa_mg_dl': 90.0,
                    'hemoglobina_g_dl': 11.8,
                    'hematocrito_pct': 36.8,
                    'sgb_resultado': 'PENDIENTE',
                    'nivel_riesgo': 'BAJO',
                    'numero_gestas': 2,
                    'numero_partos': 1,
                    'partos_vaginales_previos': 1,
                    'cesareas_previas': 0,
                    'numero_abortos': 0,
                    'hijos_vivos': 1,
                    'paridad_formato': 'G2P1A0',
                    'acido_folico': True,
                    'sulfato_ferroso': True,
                    'edema_grado': 'LEVE',
                    'edema_localizacion': 'Tobillos',
                    'varices': False,
                    'tiene_plan_parto': True,
                    'fecha_proximo_control': '2023-05-10',
                    'observaciones': 'Ecografía morfológica normal. Feto único, sexo femenino. Movimientos fetales activos.',
                    'indicaciones_medicas': 'Continuar suplementación. Elevar piernas para edema leve. Control en 4 semanas.',
                    'sistema_origen': 'Legacy'
                },
                {
                    'fecha_control': '2023-06-15',
                    'numero_control': 4,
                    'tipo_control': 'PRENATAL',
                    'consultorio_origen': 'CESFAM Coronel',
                    'profesional_nombre': 'Dra. María González',
                    'profesional_tipo': 'MEDICO',
                    'semanas_gestacion': 29,
                    'dias_gestacion': 1,
                    'fur': '2022-11-20',
                    'fpp': '2023-08-27',
                    'peso_kg': 72.0,
                    'talla_cm': 162.0,
                    'imc': 27.4,
                    'altura_uterina_cm': 27.0,
                    'ganancia_peso_total_kg': 9.5,
                    'presion_sistolica': 120,
                    'presion_diastolica': 78,
                    'frecuencia_cardiaca_materna': 80,
                    'temperatura_c': 36.6,
                    'saturacion_o2': 98,
                    'fcf_lpm': 142,
                    'movimientos_fetales': 'PRESENTES',
                    'presentacion_fetal': 'CEFALICA',
                    'situacion_fetal': 'LONGITUDINAL',
                    'glucosa_mg_dl': 92.0,
                    'hemoglobina_g_dl': 11.5,
                    'hematocrito_pct': 36.0,
                    'sgb_resultado': 'NEGATIVO',
                    'sgb_fecha_cultivo': '2023-06-10',
                    'sgb_profilaxis': False,
                    'nivel_riesgo': 'BAJO',
                    'numero_gestas': 2,
                    'numero_partos': 1,
                    'partos_vaginales_previos': 1,
                    'cesareas_previas': 0,
                    'numero_abortos': 0,
                    'hijos_vivos': 1,
                    'paridad_formato': 'G2P1A0',
                    'acido_folico': True,
                    'sulfato_ferroso': True,
                    'edema_grado': 'LEVE',
                    'edema_localizacion': 'Tobillos y pies',
                    'varices': True,
                    'tiene_plan_parto': True,
                    'realizo_visita_guiada': True,
                    'fecha_proximo_control': '2023-07-15',
                    'observaciones': 'Tercer trimestre. Cultivo SGB negativo. Visita guiada al servicio de maternidad realizada.',
                    'indicaciones_medicas': 'Continuar suplementación. Uso de medias de compresión para varices. Control en 4 semanas.',
                    'sistema_origen': 'Legacy'
                },
                {
                    'fecha_control': '2023-07-25',
                    'numero_control': 5,
                    'tipo_control': 'PRENATAL',
                    'consultorio_origen': 'CESFAM Coronel',
                    'profesional_nombre': 'Matrona Carmen Rojas',
                    'profesional_tipo': 'MATRONA',
                    'semanas_gestacion': 34,
                    'dias_gestacion': 4,
                    'fur': '2022-11-20',
                    'fpp': '2023-08-27',
                    'peso_kg': 75.0,
                    'talla_cm': 162.0,
                    'imc': 28.6,
                    'altura_uterina_cm': 32.0,
                    'ganancia_peso_total_kg': 12.5,
                    'presion_sistolica': 122,
                    'presion_diastolica': 80,
                    'frecuencia_cardiaca_materna': 82,
                    'temperatura_c': 36.8,
                    'saturacion_o2': 98,
                    'fcf_lpm': 140,
                    'movimientos_fetales': 'PRESENTES',
                    'presentacion_fetal': 'CEFALICA',
                    'situacion_fetal': 'LONGITUDINAL',
                    'glucosa_mg_dl': 95.0,
                    'hemoglobina_g_dl': 11.2,
                    'hematocrito_pct': 35.5,
                    'nivel_riesgo': 'BAJO',
                    'numero_gestas': 2,
                    'numero_partos': 1,
                    'partos_vaginales_previos': 1,
                    'cesareas_previas': 0,
                    'numero_abortos': 0,
                    'hijos_vivos': 1,
                    'paridad_formato': 'G2P1A0',
                    'acido_folico': True,
                    'sulfato_ferroso': True,
                    'edema_grado': 'MODERADO',
                    'edema_localizacion': 'Tobillos, pies y manos',
                    'varices': True,
                    'tiene_plan_parto': True,
                    'realizo_visita_guiada': True,
                    'fecha_proximo_control': '2023-08-08',
                    'observaciones': 'Embarazo de término cercano. Feto en presentación cefálica. Edema moderado fisiológico.',
                    'indicaciones_medicas': 'Continuar suplementación. Reposo relativo. Signos de alarma explicados. Control semanal hasta el parto.',
                    'motivo_consulta': 'Control prenatal de rutina',
                    'sistema_origen': 'Legacy'
                }
            ]
            
            # Insertar controles en la BD legacy usando SQL directo
            with connection.cursor() as cursor:
                # Cambiar a la BD legacy
                cursor.execute("USE legacy_obstetric")
                
                controles_insertados = 0
                
                for control in controles:
                    # Construir la consulta INSERT
                    campos = ', '.join(f"`{k}`" for k in control.keys())
                    valores_placeholders = ', '.join(['%s'] * len(control))
                    valores = [control[k] for k in control.keys()]
                    
                    # Agregar el RUT del paciente
                    campos = f"`paciente_rut`, {campos}"
                    valores_placeholders = f"%s, {valores_placeholders}"
                    valores = [rut_paciente] + valores
                    
                    query = f"""
                        INSERT INTO controles_previos ({campos})
                        VALUES ({valores_placeholders})
                    """
                    
                    try:
                        cursor.execute(query, valores)
                        controles_insertados += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✅ Control #{control["numero_control"]} - {control["fecha_control"]} ({control["semanas_gestacion"]}+{control["dias_gestacion"]} sem)'
                            )
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  ❌ Error en control #{control["numero_control"]}: {str(e)}'
                            )
                        )
                
                # Volver a la BD principal
                cursor.execute("USE obstetric_carebdd")
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ PROCESO COMPLETADO'
                )
            )
            self.stdout.write(f'  📊 Controles insertados: {controles_insertados}/5')
            self.stdout.write(
                self.style.WARNING(
                    '\n💡 INSTRUCCIONES:'
                )
            )
            self.stdout.write('  1. Busca la paciente Ana Silva Rivas (RUT: 16293109-1)')
            self.stdout.write('  2. En el detalle verás la sección "Controles de Rutina Previos (LEGACY)"')
            self.stdout.write('  3. Aparecerán los 5 controles históricos automáticamente')
            self.stdout.write('  4. Podrás ver todos los detalles de cada control previo\n')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error al cargar controles legacy: {str(e)}')
            )
            raise
