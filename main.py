# ============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023
# Fase 4: Prácticas Simuladas - Componente Práctico
# Empresa: Software FJ
# Integrantes: Anderson Herrera (Parte 1), Daniel (Parte 2), Nicoll (Parte 3)
# ============================================================================

import re
import os
from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================================
# PARTE 1: RESPONSABLE -> ANDERSON HERRERA RODRÍGUEZ
# Módulo de Excepciones Personalizadas, Logs y Clases Base
# ============================================================================

class SoftwareFJError(Exception):
    """Clase base de excepción para todo el sistema de Software FJ."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR-GEN-001"):
        super().__init__(f"[{codigo_error}] {mensaje}")
        self.codigo_error = codigo_error
        self.mensaje = mensaje


class ClienteInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los datos personales o formato del cliente son erróneos."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-CLI-002")


class ServicioNoDisponibleError(SoftwareFJError):
    """Excepción lanzada cuando un servicio solicitado supera capacidad, horario o disponibilidad."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-SRV-003")


class ParametroServicioInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los parámetros numéricos de un servicio son inconsistentes."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-SRV-004")


class ReservaIncorrectaError(SoftwareFJError):
    """Excepción lanzada cuando la reserva presenta inconsistencias de estado o procesamiento."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-RES-005")


class ErrorAuditoriaLogs(SoftwareFJError):
    """Excepción lanzada ante fallos en la persistencia del archivo de logs."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-LOG-006")


class GestorLogs:
    """Clase utilitaria para registrar eventos y excepciones en el archivo logs.txt."""
    _ARCHIVO_LOG = "logs.txt"

    @classmethod
    def registrar_evento(cls, nivel: str, mensaje: str, origen: str = "Sistema") -> bool:
        """
        Registra una línea estructurada en logs.txt usando try/except/else/finally.
        """
        descriptor_archivo = None
        operacion_exitosa = False
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = f"[{marca_tiempo}] [{nivel.upper()}] [{origen}] -> {mensaje}\n"

        try:
            # Intento de apertura y escritura en el archivo
            descriptor_archivo = open(cls._ARCHIVO_LOG, mode="a", encoding="utf-8")
            descriptor_archivo.write(linea_log)
        except (IOError, OSError) as error_sistema:
            # Encadenamiento explícito de excepciones (raise ... from ...)
            raise ErrorAuditoriaLogs(f"Fallo crítico al escribir en {cls._ARCHIVO_LOG}") from error_sistema
        else:
            # Se ejecuta si la escritura fue totalmente limpia
            operacion_exitosa = True
        finally:
            # Cierre seguro del descriptor en cualquier caso
            if descriptor_archivo and not descriptor_archivo.closed:
                descriptor_archivo.close()

        return operacion_exitosa

    @classmethod
    def registrar_error(cls, excepcion: Exception, origen: str = "Operación"):
        """Método de conveniencia para registrar excepciones capturadas."""
        cls.registrar_evento(
            nivel="ERROR",
            mensaje=f"Tipo: {type(excepcion).__name__} | Detalle: {str(excepcion)}",
            origen=origen
        )


class EntidadBase(ABC):
    """
    Clase abstracta que define las propiedades y métodos mínimos
    para todas las entidades del sistema (Clientes, Servicios, Reservas).
    """

    def __init__(self, identificador: str):
        if not identificador or not isinstance(identificador, str) or not identificador.strip():
            raise ClienteInvalidoError("El identificador de la entidad no puede ser nulo ni vacío.")
        self._identificador = identificador.strip()
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self) -> str:
        """Getter del identificador único protegido."""
        return self._identificador

    @property
    def fecha_creacion(self) -> datetime:
        """Getter de la fecha de registro en memoria."""
        return self._fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Obliga a cada entidad concreta a retornar una descripción legible."""
        pass

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Obliga a cada entidad a verificar la validez de sus atributos."""
        pass


# ============================================================================
# PARTE 2: RESPONSABLE -> DANIEL
# Módulo de Clientes y Jerarquía de Servicios Especializados (Polimorfismo)
# ============================================================================

class Cliente(EntidadBase):
    """Clase que representa a los clientes de Software FJ con encapsulación estricta."""

    def __init__(self, identificador: str, nombre_completo: str, correo_electronico: str, telefono: str):
        super().__init__(identificador)
        self._nombre_completo = ""
        self._correo_electronico = ""
        self._telefono = ""

        # Asignaciones a través de setters validados
        self.nombre_completo = nombre_completo
        self.correo_electronico = correo_electronico
        self.telefono = telefono
        self.validar_integridad()

    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres.")
        self._nombre_completo = valor.strip()

    @property
    def correo_electronico(self) -> str:
        return self._correo_electronico

    @correo_electronico.setter
    def correo_electronico(self, valor: str):
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not re.match(patron_email, valor.strip()):
            raise ClienteInvalidoError(f"Formato de correo inválido: '{valor}'.")
        self._correo_electronico = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        limpio = valor.strip() if valor else ""
        if not limpio.isdigit() or len(limpio) < 7 or len(limpio) > 10:
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'. Debe contener entre 7 y 10 dígitos numéricos.")
        self._telefono = limpio

    def obtener_resumen(self) -> str:
        return f"Cliente: {self._nombre_completo} (ID: {self._identificador}) | Correo: {self._correo_electronico}"

    def validar_integridad(self) -> bool:
        if not (self._identificador and self._nombre_completo and self._correo_electronico and self._telefono):
            raise ClienteInvalidoError("Inconsistencia en los datos personales del cliente.")
        return True


class Servicio(EntidadBase):
    """Clase base abstracta para todos los servicios ofrecidos por Software FJ."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(identificador)
        if not nombre or not isinstance(nombre, str):
            raise ParametroServicioInvalidoError("El nombre del servicio no puede estar vacío.")
        if tarifa_base <= 0:
            raise ParametroServicioInvalidoError(f"La tarifa base debe ser positiva. Valor recibido: {tarifa_base}")
        
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def calcular_costo(self, duracion_horas: float) -> float:
        """Método polimórfico obligatorio para calcular el costo según duración."""
        pass

    def validar_integridad(self) -> bool:
        if self._tarifa_base <= 0:
            raise ParametroServicioInvalidoError("Tarifa base inválida para el servicio.")
        return True


class ReservaSalas(Servicio):
    """Subclase polimórfica para el servicio de alquiler de salas de conferencias/juntas."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, capacidad_personas: int, tiene_proyector: bool = True):
        super().__init__(identificador, nombre, tarifa_base)
        if capacidad_personas < 2 or capacidad_personas > 100:
            raise ParametroServicioInvalidoError(f"Capacidad de sala inválida: {capacidad_personas}. Rango permitido: 2-100.")
        self._capacidad_personas = capacidad_personas
        self._tiene_proyector = tiene_proyector

    def calcular_costo(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise ParametroServicioInvalidoError(f"Duración de sala inválida: {duracion_horas} horas.")
        costo = self._tarifa_base * duracion_horas
        if self._tiene_proyector:
            costo += 25000.0  # Recargo tecnológico
        return round(costo, 2)

    def obtener_resumen(self) -> str:
        proyector = "Con proyector" if self._tiene_proyector else "Sin proyector"
        return f"[Sala] {self._nombre} | Capacidad: {self._capacidad_personas} pers. | {proyector} | Tarifa/h: ${self._tarifa_base:,.2f}"


class AlquilerEquipos(Servicio):
    """Subclase polimórfica para el alquiler de equipos de cómputo y servidores."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, gama_equipo: str, stock_disponible: int):
        super().__init__(identificador, nombre, tarifa_base)
        gamas_validas = ["BAJA", "MEDIA", "ALTA", "SERVIDOR"]
        if gama_equipo.upper() not in gamas_validas:
            raise ParametroServicioInvalidoError(f"Gama '{gama_equipo}' inválida. Opciones: {gamas_validas}")
        if stock_disponible < 0:
            raise ParametroServicioInvalidoError(f"Stock no puede ser negativo: {stock_disponible}")
        
        self._gama_equipo = gama_equipo.upper()
        self._stock_disponible = stock_disponible

    def calcular_costo(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise ParametroServicioInvalidoError(f"Duración de alquiler inválida: {duracion_horas} horas.")
        if self._stock_disponible <= 0:
            raise ServicioNoDisponibleError(f"No hay stock disponible para el equipo '{self._nombre}'.")
        
        multiplicadores = {"BAJA": 1.0, "MEDIA": 1.25, "ALTA": 1.5, "SERVIDOR": 2.0}
        factor = multiplicadores.get(self._gama_equipo, 1.0)
        return round(self._tarifa_base * duracion_horas * factor, 2)

    def obtener_resumen(self) -> str:
        return f"[Equipo] {self._nombre} | Gama: {self._gama_equipo} | Stock: {self._stock_disponible} und | Tarifa/h: ${self._tarifa_base:,.2f}"


class AsesoriaEspecializada(Servicio):
    """Subclase polimórfica para consultoría técnica y arquitectura de software."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, consultor_asignado: str, nivel_seniority: str):
        super().__init__(identificador, nombre, tarifa_base)
        niveles_validos = ["JUNIOR", "SEMI-SENIOR", "SENIOR", "LEAD_ARCHITECT"]
        if nivel_seniority.upper() not in niveles_validos:
            raise ParametroServicioInvalidoError(f"Nivel '{nivel_seniority}' inválido. Opciones: {niveles_validos}")
        if not consultor_asignado or len(consultor_asignado.strip()) < 3:
            raise ParametroServicioInvalidoError("El nombre del consultor asignado no es válido.")

        self._consultor_asignado = consultor_asignado.strip()
        self._nivel_seniority = nivel_seniority.upper()

    def calcular_costo(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise ParametroServicioInvalidoError(f"Duración de asesoría inválida: {duracion_horas} horas.")
        
        multiplicador_seniority = {
            "JUNIOR": 1.0,
            "SEMI-SENIOR": 1.3,
            "SENIOR": 1.7,
            "LEAD_ARCHITECT": 2.2
        }
        factor = multiplicador_seniority.get(self._nivel_seniority, 1.0)
        return round(self._tarifa_base * duracion_horas * factor, 2)

    def obtener_resumen(self) -> str:
        return f"[Asesoría] {self._nombre} | Consultor: {self._consultor_asignado} ({self._nivel_seniority}) | Tarifa/h: ${self._tarifa_base:,.2f}"


# ============================================================================
# PARTE 3: RESPONSABLE -> NICOLL
# Módulo de Reservas, Métodos Sobrecargados y Script de Simulación
# ============================================================================

class Reserva(EntidadBase):
    """Clase integradora que gestiona la reserva entre Cliente y Servicio."""

    ESTADOS_VALIDOS = ["EN_PROCESO", "CONFIRMADA", "CANCELADA"]

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion_horas: float):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ReservaIncorrectaError("La reserva debe vincular una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ReservaIncorrectaError("La reserva debe vincular una instancia válida de Servicio.")
        if duracion_horas <= 0 or duracion_horas > 72:
            raise ReservaIncorrectaError(f"Duración {duracion_horas}h inválida. Rango permitido: 0.5 a 72 horas.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = float(duracion_horas)
        self._estado = "EN_PROCESO"
        self._costo_total = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def calcular_costo_final(self, porcentaje_descuento: float = 0.0, porcentaje_impuesto: float = 19.0, recargo_urgencia: float = 0.0) -> float:
        """Calcula el costo final aplicando sobrecarga con parámetros opcionales."""
        if porcentaje_descuento < 0 or porcentaje_descuento > 50:
            raise ParametroServicioInvalidoError(f"Descuento fuera de rango (0-50%): {porcentaje_descuento}%")
        if porcentaje_impuesto < 0:
            raise ParametroServicioInvalidoError(f"Impuesto no puede ser negativo: {porcentaje_impuesto}%")
        if recargo_urgencia < 0:
            raise ParametroServicioInvalidoError("El recargo de urgencia no puede ser negativo.")

        subtotal = self._servicio.calcular_costo(self._duracion_horas)
        descuento = subtotal * (porcentaje_descuento / 100.0)
        base_imponible = (subtotal - descuento) + recargo_urgencia
        impuesto = base_imponible * (porcentaje_impuesto / 100.0)
        self._costo_total = round(base_imponible + impuesto, 2)
        return self._costo_total

    def confirmar_reserva(self, porcentaje_descuento: float = 0.0):
        """Procesa y confirma la reserva si el servicio está disponible."""
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' no se encuentra disponible actualmente.")
        if self._estado == "CONFIRMADA":
            raise ReservaIncorrectaError("La reserva ya ha sido confirmada previamente.")

        self.calcular_costo_final(porcentaje_descuento=porcentaje_descuento)
        self._estado = "CONFIRMADA"
        GestorLogs.registrar_evento("INFO", f"Reserva {self._identificador} CONFIRMADA con éxito. Total: ${self._costo_total:,.2f}", origen="Reserva")

    def cancelar_reserva(self, motivo: str):
        """Cancela la reserva registrando la causa en logs."""
        if self._estado == "CANCELADA":
            raise ReservaIncorrectaError("La reserva ya se encuentra cancelada.")
        if not motivo or len(motivo.strip()) < 5:
            raise ReservaIncorrectaError("Debe proporcionar un motivo válido de cancelación (mínimo 5 caracteres).")

        self._estado = "CANCELADA"
        GestorLogs.registrar_evento("WARNING", f"Reserva {self._identificador} CANCELADA. Causa: {motivo}", origen="Reserva")

    def obtener_resumen(self) -> str:
        return (f"Reserva: {self._identificador} [{self._estado}] | Cliente: {self._cliente.nombre_completo} | "
                f"Servicio: {self._servicio.nombre} ({self._duracion_horas}h) | Total: ${self._costo_total:,.2f}")

    def validar_integridad(self) -> bool:
        if self._estado not in self.ESTADOS_VALIDOS:
            raise ReservaIncorrectaError(f"Estado de reserva anómalo: {self._estado}")
        return True


# ============================================================================
# SCRIPT DE SIMULACIÓN (10+ OPERACIONES COMPLETAS SEGÚN ANEXO 3)
# ============================================================================

def ejecutar_simulacion():
    print("=" * 80)
    print("       SOFTWARE FJ - SIMULACIÓN DE GESTIÓN Y TOLERANCIA A FALLOS")
    print("=" * 80)
    
    GestorLogs.registrar_evento("INFO", "INICIO DE SIMULACIÓN DE OPERACIONES DEL SISTEMA", origen="Simulacion")

    clientes_bd = {}
    servicios_bd = {}
    reservas_bd = {}

    operaciones = [
        # Operaciones válidas (éxito)
        (1, "REGISTRO CLIENTE VÁLIDO 1", lambda: registrar_cliente(clientes_bd, "CLI-01", "Anderson Herrera", "anderson@unad.edu.co", "3101234567")),
        (2, "REGISTRO CLIENTE VÁLIDO 2", lambda: registrar_cliente(clientes_bd, "CLI-02", "Daniel Torres", "daniel.torres@gmail.com", "3209876543")),
        (3, "CREACIÓN SERVICIO SALA VÁLIDO", lambda: crear_servicio(servicios_bd, ReservaSalas("SRV-01", "Sala Magna de Juntas", 50000.0, 20, True))),
        (4, "CREACIÓN SERVICIO EQUIPO VÁLIDO", lambda: crear_servicio(servicios_bd, AlquilerEquipos("SRV-02", "Servidor Dedicado GPU", 80000.0, "SERVIDOR", 5))),
        (5, "CREACIÓN ASESORÍA VÁLIDA", lambda: crear_servicio(servicios_bd, AsesoriaEspecializada("SRV-03", "Arquitectura Cloud AWS", 120000.0, "Ing. Carlos Mendoza", "LEAD_ARCHITECT"))),
        (6, "RESERVA EXITOSA CON DESCUENTO", lambda: procesar_reserva(reservas_bd, "RES-01", clientes_bd["CLI-01"], servicios_bd["SRV-01"], duracion=4.0, descuento=10.0)),
        (7, "RESERVA EXITOSA DE EQUIPOS", lambda: procesar_reserva(reservas_bd, "RES-02", clientes_bd["CLI-02"], servicios_bd["SRV-02"], duracion=8.0, descuento=0.0)),

        # Operaciones con fallos controlados (captura de excepciones y logs)
        (8, "FALLO: CLIENTE CON EMAIL INVÁLIDO", lambda: registrar_cliente(clientes_bd, "CLI-ERR", "Usuario Fallido", "correo_sin_arroba_ni_dominio", "3001112233")),
        (9, "FALLO: SALA CON CAPACIDAD NEGATIVA", lambda: crear_servicio(servicios_bd, ReservaSalas("SRV-ERR1", "Sala Ilegal", 40000.0, -10, False))),
        (10, "FALLO: RESERVA CON SERVICIO NO DISPONIBLE", lambda: provocar_reserva_no_disponible(reservas_bd, clientes_bd.get("CLI-01"), servicios_bd.get("SRV-03"))),
        (11, "FALLO: CANCELACIÓN DE RESERVA YA CANCELADA", lambda: provocar_doble_cancelacion(reservas_bd.get("RES-01"))),
        (12, "FALLO: RESERVA CON DURACIÓN ILÍCITA (0 HORAS)", lambda: procesar_reserva(reservas_bd, "RES-ERR", clientes_bd.get("CLI-02"), servicios_bd.get("SRV-02"), duracion=0.0, descuento=0.0))
    ]

    for numero, descripcion, accion in operaciones:
        print(f"\n[Operación #{numero:02d}] Ejecutando: {descripcion}...")
        try:
            resultado = accion()
            print(f"  --> Resultado: ÉXITO | {resultado}")
        except SoftwareFJError as err_negocio:
            print(f"  --> [EXCEPCIÓN CONTROLADA CAPTURADA]: {err_negocio}")
            GestorLogs.registrar_error(err_negocio, origen=f"Op#{numero}_{descripcion}")
        except Exception as err_imprevisto:
            print(f"  --> [ERROR NO CONTROLADO]: {err_imprevisto}")
            GestorLogs.registrar_error(err_imprevisto, origen=f"Op#{numero}_CRITICO")
        else:
            GestorLogs.registrar_evento("INFO", f"Operación #{numero} completada satisfactoriamente", origen="Simulacion")
        finally:
            print(f"  --> Estado de seguridad: Aplicación Software FJ estable y en ejecución.")

    print("\n" + "=" * 80)
    print("SIMULACIÓN FINALIZADA CON ÉXITO: 0 CAÍDAS DEL SISTEMA (ROBUSTEZ DEMOSTRADA)")
    print(f"Verifique todos los eventos y errores auditados en el archivo: '{GestorLogs._ARCHIVO_LOG}'")
    print("=" * 80)


def registrar_cliente(bd, id_c, nombre, email, tel):
    c = Cliente(id_c, nombre, email, tel)
    bd[id_c] = c
    return c.obtener_resumen()

def crear_servicio(bd, servicio):
    servicio.validar_integridad()
    bd[servicio.identificador] = servicio
    return servicio.obtener_resumen()

def procesar_reserva(bd, id_r, cliente, servicio, duracion, descuento):
    reserva = Reserva(id_r, cliente, servicio, duracion)
    reserva.confirmar_reserva(porcentaje_descuento=descuento)
    bd[id_r] = reserva
    return reserva.obtener_resumen()

def provocar_reserva_no_disponible(bd, cliente, servicio):
    servicio.disponible = False
    reserva = Reserva("RES-FALLA-DISP", cliente, servicio, 3.0)
    reserva.confirmar_reserva()

def provocar_doble_cancelacion(reserva):
    reserva.cancelar_reserva("Reunión pospuesta por el cliente")
    reserva.cancelar_reserva("Intento de cancelar por segunda vez")


if __name__ == "__main__":
    ejecutar_simulacion()