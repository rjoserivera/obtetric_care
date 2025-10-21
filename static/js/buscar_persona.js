/**
 * Script para buscar persona por RUT y autocompletar formularios
 */

document.addEventListener('DOMContentLoaded', function() {
    // Obtener el input del RUT según el formulario
    const rutInput = document.querySelector('#rut_persona_medico, #rut_persona_matrona, #rut_persona_tens, #rut_persona_paciente');
    
    if (!rutInput) return; // Si no existe el campo, salir
    
    // Contenedor para mostrar información de la persona
    let infoContainer = document.querySelector('#persona-info');
    if (!infoContainer) {
        infoContainer = document.createElement('div');
        infoContainer.id = 'persona-info';
        infoContainer.className = 'alert mt-3';
        rutInput.parentElement.appendChild(infoContainer);
    }
    
    // Evento cuando se pierde el foco del input (blur)
    rutInput.addEventListener('blur', function() {
        const rut = this.value.trim();
        
        if (!rut) {
            infoContainer.innerHTML = '';
            infoContainer.style.display = 'none';
            return;
        }
        
        // Mostrar mensaje de carga
        infoContainer.innerHTML = '<i class="bi bi-hourglass-split"></i> Buscando...';
        infoContainer.className = 'alert alert-info mt-3';
        infoContainer.style.display = 'block';
        
        // Realizar petición AJAX
        fetch(`/api/persona/buscar/?rut=${encodeURIComponent(rut)}`)
            .then(response => response.json())
            .then(data => {
                if (data.encontrado) {
                    // Persona encontrada - Mostrar información
                    infoContainer.innerHTML = `
                        <i class="bi bi-check-circle-fill text-success"></i> 
                        <strong>Persona encontrada:</strong><br>
                        <strong>Nombre:</strong> ${data.persona.nombre_completo}<br>
                        <strong>Sexo:</strong> ${data.persona.sexo}<br>
                        <strong>Fecha Nac.:</strong> ${data.persona.fecha_nacimiento}<br>
                        <strong>Teléfono:</strong> ${data.persona.telefono || 'No registrado'}<br>
                        <strong>Email:</strong> ${data.persona.email || 'No registrado'}
                    `;
                    infoContainer.className = 'alert alert-success mt-3';
                } else {
                    // Persona no encontrada
                    infoContainer.innerHTML = `
                        <i class="bi bi-exclamation-triangle-fill text-warning"></i> 
                        ${data.mensaje}<br>
                        <small>Por favor, registre primero los datos básicos de la persona en 
                        <a href="/gestion/persona/registrar/" target="_blank">este enlace</a>.</small>
                    `;
                    infoContainer.className = 'alert alert-warning mt-3';
                }
            })
            .catch(error => {
                infoContainer.innerHTML = `
                    <i class="bi bi-x-circle-fill text-danger"></i> 
                    Error al buscar: ${error.message}
                `;
                infoContainer.className = 'alert alert-danger mt-3';
            });
    });
});