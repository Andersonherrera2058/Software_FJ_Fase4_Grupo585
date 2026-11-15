# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Jerarquía de Excepciones Personalizadas (Rol 2 - Nicoll Yepes)
# ==============================================================================

class ErrorSistema(Exception):  # Clase base para todas las excepciones controladas del sistema
    """Excepción raíz de Software FJ."""  # Documentación de la clase base

    def __init__(self, mensaje: str, codigo: str = "ERR-000"):  # Constructor con mensaje y código de error
        self.mensaje = mensaje  # Almacena la descripción del fallo ocurrido
        self.codigo = codigo  # Almacena el identificador técnico del error
        super().__init__(f"[{self.codigo}] {self.mensaje}")  # Llama al constructor padre Exception


class DatoInvalidoError(ErrorSistema):  # Excepción lanzada cuando un dato de entrada incumple el formato
    """Falla por formato incorrecto en documento, correo, nombre o teléfono."""  # Docstring descriptivo

    def __init__(self, mensaje: str):  # Constructor específico para datos inválidos
        super().__init__(mensaje, codigo="ERR-DATO-001")  # Asigna código estándar de validación de datos


class ServicioNoDisponibleError(ErrorSistema):  # Excepción para parámetros o disponibilidad de servicios
    """Falla cuando un servicio no está disponible o recibe parámetros erróneos."""  # Docstring descriptivo

    def __init__(self, mensaje: str):  # Constructor específico para fallos de servicio
        super().__init__(mensaje, codigo="ERR-SERV-002")  # Asigna código estándar de servicio


class ReservaInvalidaError(ErrorSistema):  # Excepción para transiciones de estado o reglas de reserva
    """Falla al intentar confirmar, cancelar o procesar una reserva inválida."""  # Docstring descriptivo

    def __init__(self, mensaje: str):  # Constructor específico para fallos en reservas
        super().__init__(mensaje, codigo="ERR-RESV-003")  # Asigna código estándar de reserva