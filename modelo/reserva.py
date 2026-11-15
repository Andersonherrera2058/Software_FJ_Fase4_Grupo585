# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Gestión de Reservas (Integración - Anderson Herrera)
# ==============================================================================

from modelo.cliente import Cliente  # Importa clase Cliente del Rol 3
from modelo.servicios import Servicio  # Importa clase base Servicio del Rol 4
from modelo.excepciones import ReservaInvalidaError, ErrorSistema  # Importa excepciones del Rol 2
from modelo.registro import GestorRegistro  # Importa auditoría del Rol 2


class Reserva:  # Clase integradora que asocia un Cliente, un Servicio y su estado operativo
    """Gestiona el ciclo de vida de una reserva: PENDIENTE -> CONFIRMADA / CANCELADA."""  # Docstring

    _contador = 1000  # Contador interno para generar códigos consecutivos de reserva

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: int, descuento: float = 0.0):  # Constructor
        if not isinstance(cliente, Cliente):  # Verifica que se reciba una instancia válida de Cliente
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente válido.")  # Lanza excepción
        if not isinstance(servicio, Servicio):  # Verifica que se reciba una instancia válida de Servicio
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio válido.")  # Lanza excepción

        Reserva._contador += 1  # Incrementa el consecutivo de reservas
        self.codigo = f"RES-{Reserva._contador}"  # Asigna código único (ej. RES-1001)
        self.cliente = cliente  # Asocia el objeto Cliente
        self.servicio = servicio  # Asocia el objeto Servicio
        self.horas = horas  # Guarda duración solicitada
        self.descuento = descuento  # Guarda porcentaje de descuento aplicable
        self.estado = "PENDIENTE"  # Estado inicial obligatorio de toda reserva
        self.detalle_financiero = {}  # Diccionario que almacenará subtotal, IVA y total

    def procesar(self) -> dict:  # Calcula costos y valida la viabilidad técnica de la reserva
        """Calcula tarifas y valida reglas de negocio encadenando excepciones con 'from'."""  # Docstring
        try:  # Bloque protegido para ejecutar el cálculo del servicio
            self.detalle_financiero = self.servicio.calcular_costo(  # Invoca método polimórfico
                horas=self.horas,
                descuento=self.descuento
            )
        except ErrorSistema as err_origen:  # Captura error de servicio o datos
            GestorRegistro.registrar("ERROR", "Reserva", f"Fallo al procesar {self.codigo}: {err_origen}")  # Audita
            raise ReservaInvalidaError(  # Relanza como ReservaInvalidaError preservando causa raíz
                f"No fue posible procesar la reserva {self.codigo} debido a un parámetro inválido."
            ) from err_origen  # Encadenamiento explícito exigido en el criterio 1
        else:  # Se ejecuta únicamente si el bloque try finalizó sin excepciones
            self.estado = "PROCESADA"  # Actualiza el estado tras cálculo exitoso
            GestorRegistro.registrar(  # Registra operación exitosa en logs/sistema.log
                "INFO",
                "Reserva",
                f"{self.codigo} procesada para {self.cliente.nombre} | Total: ${self.detalle_financiero['total']:,.2f}"
            )
            return self.detalle_financiero  # Retorna el desglose calculado

    def confirmar(self) -> None:  # Cambia el estado a CONFIRMADA si ya fue procesada
        """Confirma oficialmente una reserva previamente procesada."""  # Docstring
        if self.estado == "CANCELADA":  # Impide confirmar una reserva ya anulada
            raise ReservaInvalidaError(f"La reserva {self.codigo} está CANCELADA y no puede confirmarse.")  # Error
        if not self.detalle_financiero:  # Si no se ha procesado el costo aún, lo procesa primero
            self.procesar()  # Ejecuta procesamiento previo
        self.estado = "CONFIRMADA"  # Actualiza estado a CONFIRMADA
        GestorRegistro.registrar("INFO", "Reserva", f"Reserva {self.codigo} CONFIRMADA.")  # Registra en log

    def cancelar(self, motivo: str = "Solicitud del cliente") -> None:  # Anula la reserva registrando motivo
        """Cancela la reserva y deja trazabilidad en el archivo de logs."""  # Docstring
        if self.estado == "CANCELADA":  # Evita doble cancelación
            raise ReservaInvalidaError(f"La reserva {self.codigo} ya se encuentra CANCELADA.")  # Lanza error
        self.estado = "CANCELADA"  # Cambia estado a CANCELADA
        GestorRegistro.registrar("WARNING", "Reserva", f"Reserva {self.codigo} CANCELADA. Motivo: {motivo}")  # Log