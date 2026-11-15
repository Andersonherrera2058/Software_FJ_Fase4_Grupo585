# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Servicios Especializados y Polimorfismo (Rol 4 - Leonardo Valencia)
# ==============================================================================

from abc import ABC, abstractmethod  # Importa ABC para construir la clase abstracta Servicio
from modelo.excepciones import ServicioNoDisponibleError  # Importa excepción del Rol 2


class Servicio(ABC):  # Clase abstracta base para los servicios ofrecidos por Software FJ
    """Define la interfaz común y sobrecarga de cálculo de costos para servicios."""  # Docstring

    def __init__(self, nombre: str, tarifa_hora: float):  # Constructor base de servicio
        self.nombre = nombre  # Nombre comercial del servicio
        self.tarifa_hora = tarifa_hora  # Tarifa base por hora en pesos

    def validar_parametros(self, horas: int) -> None:  # Valida parámetros comunes antes de calcular
        """Verifica que la duración en horas sea un entero positivo válido."""  # Docstring
        if not isinstance(horas, int) or horas <= 0:  # Comprueba que las horas sean mayores a cero
            raise ServicioNoDisponibleError("La duración del servicio debe ser mayor a 0 horas.")  # Lanza excepción
        if horas > 24:  # Restringe reservas continuas mayores a 24 horas
            raise ServicioNoDisponibleError("No se permiten reservas mayores a 24 horas continuas.")  # Lanza excepción

    @abstractmethod
    def describir(self) -> str:  # Método abstracto para describir cada servicio
        """Retorna la descripción técnica del servicio."""  # Docstring
        pass  # Implementado por cada clase hija

    def calcular_costo(  # Método con sobrecarga mediante parámetros opcionales (impuesto y descuento)
        self,
        horas: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        recargo_extra: float = 0.0
    ) -> dict:
        """Calcula subtotal, descuento, IVA y total con soporte para parámetros opcionales."""  # Docstring
        self.validar_parametros(horas)  # Ejecuta validación previa de horas
        if not (0.0 <= descuento <= 0.5):  # Verifica que el descuento no supere el 50%
            raise ServicioNoDisponibleError("El descuento debe estar entre 0% (0.0) y 50% (0.5).")  # Lanza error
        subtotal_bruto = (self.tarifa_hora * horas) + recargo_extra  # Calcula monto base más extras
        valor_descuento = subtotal_bruto * descuento  # Calcula el monto descontado
        subtotal_neto = subtotal_bruto - valor_descuento  # Aplica el descuento al subtotal
        valor_impuesto = subtotal_neto * impuesto  # Calcula el IVA (19% por defecto)
        total = subtotal_neto + valor_impuesto  # Calcula el valor final a pagar
        return {  # Retorna diccionario estructurado con todo el desglose financiero
            "subtotal": round(subtotal_neto, 2),
            "descuento": round(valor_descuento, 2),
            "impuesto": round(valor_impuesto, 2),
            "total": round(total, 2),
        }


class ReservaSalas(Servicio):  # Primera clase hija especializada: Reserva de Salas
    """Servicio de alquiler de salas tecnológicas y auditorios."""  # Docstring

    def __init__(self, capacidad: int = 20):  # Constructor con capacidad de asistentes
        super().__init__(nombre="Room Booking", tarifa_hora=80000.0)  # Inicializa tarifa base de sala
        self.capacidad = capacidad  # Guarda la capacidad máxima de la sala

    def describir(self) -> str:  # Sobrescribe describir para salas
        return f"{self.nombre} (Capacidad: {self.capacidad} personas - ${self.tarifa_hora:,.0f}/h)"  # Descripción


class AlquilerEquipos(Servicio):  # Segunda clase hija especializada: Alquiler de Equipos
    """Servicio de préstamo de estaciones de trabajo de alto rendimiento."""  # Docstring

    def __init__(self, cantidad_equipos: int = 1):  # Constructor con cantidad de equipos
        super().__init__(nombre="Equipment Rental", tarifa_hora=45000.0)  # Inicializa tarifa unitaria
        self.cantidad_equipos = cantidad_equipos  # Almacena cantidad de equipos solicitados

    def validar_parametros(self, horas: int) -> None:  # Sobrescribe validación para incluir equipos
        super().validar_parametros(horas)  # Ejecuta validación base de horas
        if self.cantidad_equipos <= 0:  # Valida que exista al menos un equipo
            raise ServicioNoDisponibleError("Debe solicitar al menos 1 equipo para el alquiler.")  # Lanza error

    def calcular_costo(self, horas: int, impuesto: float = 0.19, descuento: float = 0.0, recargo_extra: float = 0.0) -> dict:  # Sobrescribe cálculo
        self.validar_parametros(horas)  # Valida horas y cantidad de equipos
        recargo_equipos = self.tarifa_hora * horas * (self.cantidad_equipos - 1)  # Ajusta costo por equipos adicionales
        return super().calcular_costo(horas, impuesto, descuento, recargo_extra + recargo_equipos)  # Delega cálculo final

    def describir(self) -> str:  # Sobrescribe describir para equipos
        return f"{self.nombre} ({self.cantidad_equipos} equipos - ${self.tarifa_hora:,.0f}/h c/u)"  # Descripción


class AsesoriaEspecializada(Servicio):  # Tercera clase hija especializada: Asesoría
    """Servicio de consultoría técnica y arquitectura de software."""  # Docstring

    def __init__(self, especialidad: str = "Arquitectura Cloud"):  # Constructor con área temática
        super().__init__(nombre="Specialized Consulting", tarifa_hora=120000.0)  # Inicializa tarifa consultoría
        self.especialidad = especialidad  # Guarda la especialidad requerida

    def describir(self) -> str:  # Sobrescribe describir para asesoría
        return f"{self.nombre} [{self.especialidad}] (${self.tarifa_hora:,.0f}/h)"  # Descripción