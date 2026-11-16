# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Jerarquía de Excepciones Personalizadas (Rol 2 - Nicoll Yepes)
# ==============================================================================

from datetime import datetime


class ErrorSistema(Exception):  # Clase base para todas las excepciones controladas del sistema
    """Excepción raíz de Software FJ con marca de tiempo y severidad."""

    def __init__(self, mensaje: str, codigo: str = "ERR-000", severidad: str = "ERROR"):
        self.mensaje = mensaje
        self.codigo = codigo
        self.severidad = severidad
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        super().__init__(f"[{self.codigo}] ({self.severidad}) {self.mensaje}")


class DatoInvalidoError(ErrorSistema):
    """Falla por formato incorrecto en documento, correo, nombre o teléfono."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-DATO-001", severidad="Error")  #Asigna código estándar de validación de datos


class ServicioNoDisponibleError(ErrorSistema):
    """Falla cuando un servicio no está disponible o recibe parámetros erróneos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-SERV-002", severidad="Aviso")  #Asigna código estándar de servicio


class ReservaInvalidaError(ErrorSistema):
    """Falla al intentar confirmar, cancelar o procesar una reserva inválida."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-RESV-003", severidad="Fallo")  #Asigna código estándar de reserva

class CalculoInconsistenteError(ErrorSistema):
    """Falla cuando el cálculo financiero genera valores negativos o incongruentes."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-CALC-004", severidad="Fallo grave")  # Asigna código estándar de cálculo y nivel de gravedad

