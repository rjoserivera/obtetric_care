# Script para corregir todas las etiquetas Django divididas en múltiples líneas

$files = @(
    "templates\Matrona\Data\_controles_legacy.html",
    "templates\Matrona\Data\_control_tab_general.html",
    "templates\Matrona\Data\_control_tab_signos.html",
    "templates\Matrona\Data\_control_tab_fetal.html",
    "templates\Matrona\Data\_control_tab_examenes.html",
    "templates\Matrona\Data\_control_tab_antecedentes.html"
)

foreach ($file in $files) {
    Write-Host "Procesando: $file"
    
    # Leer el contenido del archivo
    $content = Get-Content $file -Raw
    
    # Reemplazar todas las etiquetas Django divididas en múltiples líneas
    # Patrón: {{ ... \n ... }}
    $content = $content -replace '\{\{([^}]*)\r?\n\s*([^}]*)\}\}', '{{ $1 $2 }}'
    
    # Repetir para casos con más de 2 líneas
    $content = $content -replace '\{\{([^}]*)\r?\n\s*([^}]*)\}\}', '{{ $1 $2 }}'
    $content = $content -replace '\{\{([^}]*)\r?\n\s*([^}]*)\}\}', '{{ $1 $2 }}'
    
    # Limpiar espacios múltiples dentro de las etiquetas
    $content = $content -replace '\{\{\s+', '{{ '
    $content = $content -replace '\s+\}\}', ' }}'
    $content = $content -replace '\{\{\s+([^}]+)\s+\}\}', '{{ $1 }}'
    
    # Guardar el archivo
    Set-Content -Path $file -Value $content -Encoding UTF8 -NoNewline
    
    Write-Host "Corregido: $file"
}

Write-Host ""
Write-Host "Todos los archivos han sido corregidos."
Write-Host "Por favor, reinicia el servidor Django y refresca tu navegador."
