#!/usr/bin/env python
"""
Script para poblar campos vacíos en ControlesPrevios
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from legacyApp.models import ControlesPrevios

# Buscar controles del RUT
rut = '16293109-1'
controles = ControlesPrevios.objects.filter(paciente_rut=rut)

print(f"\n{'='*60}")
print(f"POBLANDO DATOS PARA RUT: {rut}")
print(f"{'='*60}\n")
print(f"Total de controles encontrados: {controles.count()}\n")

for idx, control in enumerate(controles, 1):
    print(f"\n--- Control #{idx} (ID: {control.id}) - Fecha: {control.fecha_control} ---")
    
    # Actualizar campos vacíos con datos realistas
    campos_actualizados = []
    
    # Datos antropométricos
    if not control.altura_uterina_cm:
        # Altura uterina según semanas de gestación (aproximado)
        if control.semanas_gestacion:
            control.altura_uterina_cm = control.semanas_gestacion + 2
            campos_actualizados.append('altura_uterina_cm')
    
    if not control.ganancia_peso_total_kg:
        control.ganancia_peso_total_kg = 3.5
        campos_actualizados.append('ganancia_peso_total_kg')
    
    # Signos vitales
    if not control.saturacion_o2:
        control.saturacion_o2 = 98
        campos_actualizados.append('saturacion_o2')
    
    # Laboratorio
    if not control.proteinuria:
        control.proteinuria = "NEGATIVO"
        campos_actualizados.append('proteinuria')
    
    if not control.leucocitos_orina:
        control.leucocitos_orina = "0-5 por campo"
        campos_actualizados.append('leucocitos_orina')
    
    # Tamizajes
    if not control.vih_orden:
        control.vih_orden = 1
        campos_actualizados.append('vih_orden')
    
    if not control.sgb_resultado:
        control.sgb_resultado = "NEGATIVO"
        campos_actualizados.append('sgb_resultado')
    
    if not control.sgb_fecha_cultivo and control.semanas_gestacion and control.semanas_gestacion >= 35:
        control.sgb_fecha_cultivo = control.fecha_control
        campos_actualizados.append('sgb_fecha_cultivo')
    
    if control.sgb_profilaxis is None:
        control.sgb_profilaxis = False
        campos_actualizados.append('sgb_profilaxis')
    
    if not control.toxoplasma_resultado:
        control.toxoplasma_resultado = "NEGATIVO"
        campos_actualizados.append('toxoplasma_resultado')
    
    if not control.toxoplasma_fecha:
        control.toxoplasma_fecha = control.fecha_control
        campos_actualizados.append('toxoplasma_fecha')
    
    if not control.hepatitis_b_resultado:
        control.hepatitis_b_resultado = "NEGATIVO"
        campos_actualizados.append('hepatitis_b_resultado')
    
    if not control.hepatitis_b_fecha:
        control.hepatitis_b_fecha = control.fecha_control
        campos_actualizados.append('hepatitis_b_fecha')
    
    # Patologías (todas en False si no están definidas)
    patologias = [
        'diabetes_gestacional', 'hipertension_arterial', 'preeclampsia_leve',
        'preeclampsia_severa', 'eclampsia', 'anemia', 'infeccion_urinaria',
        'corioamnionitis', 'amenaza_parto_prematuro', 'rotura_prematura_membranas'
    ]
    
    for patologia in patologias:
        if getattr(control, patologia) is None:
            setattr(control, patologia, False)
            campos_actualizados.append(patologia)
    
    # Nivel de riesgo
    if not control.numero_aro:
        control.numero_aro = f"ARO-2023-{control.id:04d}"
        campos_actualizados.append('numero_aro')
    
    # Medicamentos
    if not control.medicamentos_activos:
        medicamentos = []
        if control.acido_folico:
            medicamentos.append("Acido folico 1mg/dia")
        if control.sulfato_ferroso:
            medicamentos.append("Sulfato ferroso 300mg/dia")
        control.medicamentos_activos = ", ".join(medicamentos) if medicamentos else "Ninguno"
        campos_actualizados.append('medicamentos_activos')
    
    if control.aspirina_profilactica is None:
        control.aspirina_profilactica = False
        campos_actualizados.append('aspirina_profilactica')
    
    # Evaluación clínica
    if not control.edema_grado:
        control.edema_grado = "AUSENTE"
        campos_actualizados.append('edema_grado')
    
    if not control.edema_localizacion:
        control.edema_localizacion = "N/A"
        campos_actualizados.append('edema_localizacion')
    
    if control.varices is None:
        control.varices = False
        campos_actualizados.append('varices')
    
    if not control.reflejos_osteotendinosos:
        control.reflejos_osteotendinosos = "Normales"
        campos_actualizados.append('reflejos_osteotendinosos')
    
    # Plan y seguimiento
    if control.tiene_plan_parto is None:
        control.tiene_plan_parto = True
        campos_actualizados.append('tiene_plan_parto')
    
    if control.realizo_visita_guiada is None:
        control.realizo_visita_guiada = False
        campos_actualizados.append('realizo_visita_guiada')
    
    if not control.motivo_consulta:
        control.motivo_consulta = "Control prenatal de rutina"
        campos_actualizados.append('motivo_consulta')
    
    # Metadatos
    if not control.turno:
        control.turno = "MANANA"
        campos_actualizados.append('turno')
    
    if not control.fecha_hora_registro:
        from datetime import datetime, time
        control.fecha_hora_registro = datetime.combine(control.fecha_control, time(10, 30))
        campos_actualizados.append('fecha_hora_registro')
    
    # Guardar cambios
    if campos_actualizados:
        control.save()
        print(f"  Campos actualizados ({len(campos_actualizados)}): {', '.join(campos_actualizados[:5])}")
        if len(campos_actualizados) > 5:
            print(f"  ... y {len(campos_actualizados) - 5} más")
    else:
        print("  No se requirieron actualizaciones")

print(f"\n{'='*60}")
print("PROCESO COMPLETADO")
print(f"{'='*60}\n")
