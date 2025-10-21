import re
from django.core.exceptions import ValidationError

def normalizar_rut(rut: str) -> str:
    """
    Limpia puntos y espacios, pasa a mayúsculas.
    Ej: '12.345.678-k' -> '12345678-K'
    """
    return rut.replace(".", "").replace(" ", "").upper()

def _validar_rut(value: str) -> str:
    """
    Función interna que valida el RUT chileno (formato y dígito verificador).
    Lanza ValidationError si no es válido.
    Retorna el RUT normalizado.
    """
    rut = normalizar_rut(value)

    # Validar formato: 7 u 8 dígitos + guion + dígito verificador
    if not re.match(r"^\d{7,8}-[\dkK]$", rut):
        raise ValidationError("Formato RUT inválido. Ej: 12345678-9")

    cuerpo, dv = rut.split("-")
    dv = dv.upper()

    # Calcular dígito verificador
    suma = 0
    multiplicador = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    res = 11 - (suma % 11)
    dv_calc = "0" if res == 11 else "K" if res == 10 else str(res)

    if dv != dv_calc:
        raise ValidationError("Dígito verificador incorrecto.")

    return rut

# Alias público para mantener compatibilidad
validar_rut = _validar_rut
validar_rut_chileno = _validar_rut
