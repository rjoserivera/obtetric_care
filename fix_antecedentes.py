import os

content = """{# Tab: Antecedentes Obstétricos y Plan de Parto #}
<div class="tab-pane fade" id="antecedentes" role="tabpanel">
    <div class="row">
        <div class="col-md-6">
            <h6 class="text-danger border-bottom pb-2">Antecedentes Obstétricos</h6>
            <p><strong>Fórmula Obstétrica:</strong> {{ legacy_selected.paridad_formato|default:"No registrada" }}</p>
            <p><strong>Número de Gestas:</strong> {{ legacy_selected.numero_gestas|default:"--" }}</p>
            <p><strong>Número de Partos:</strong> {{ legacy_selected.numero_partos|default:"--" }}</p>
            <p><strong>Partos Vaginales:</strong> {{ legacy_selected.partos_vaginales_previos|default:"--" }}</p>
            <p><strong>Cesáreas:</strong> {{ legacy_selected.cesareas_previas|default:"--" }}</p>
            <p><strong>Abortos:</strong> {{ legacy_selected.numero_abortos|default:"--" }}</p>
            <p><strong>Hijos Vivos:</strong> {{ legacy_selected.hijos_vivos|default:"--" }}</p>
        </div>
        <div class="col-md-6">
            <h6 class="text-danger border-bottom pb-2">Plan de Parto</h6>
            <p><strong>Tiene Plan de Parto:</strong> {% if legacy_selected.tiene_plan_parto %}Sí{% elif legacy_selected.tiene_plan_parto == False %}No{% else %}No especificado{% endif %}</p>
            <p><strong>Realizó Visita Guiada:</strong> {% if legacy_selected.realizo_visita_guiada %}Sí{% elif legacy_selected.realizo_visita_guiada == False %}No{% else %}No especificado{% endif %}</p>
            {% if legacy_selected.fecha_proximo_control %}
            <p><strong>Próximo Control:</strong> {{ legacy_selected.fecha_proximo_control|date:"d/m/Y" }}</p>
            {% endif %}
            {% if legacy_selected.numero_aro %}
            <p><strong>N° ARO:</strong> {{ legacy_selected.numero_aro }}</p>
            {% endif %}
        </div>
    </div>
</div>"""

file_path = r"c:\Users\Cristian Machuca\Documents\GitHub\obtetric_care-cambios2\templates\Matrona\Data\_control_tab_antecedentes.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Archivo {file_path} reescrito correctamente.")
