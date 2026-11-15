# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Batería de Simulaciones (12 Casos Válidos e Inválidos)
# ==============================================================================

from modelo.cliente import Cliente  # Importa clase Cliente
from modelo.servicios import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada  # Importa servicios
from modelo.reserva import Reserva  # Importa clase Reserva
from modelo.excepciones import ErrorSistema  # Importa excepción raíz
from modelo.registro import GestorRegistro  # Importa gestor de auditoría


def ejecutar_simulaciones() -> list:  # Función principal que ejecuta las 12 pruebas automatizadas
    """Ejecuta 12 operaciones válidas e inválidas comprobando estabilidad y logs."""  # Docstring
    GestorRegistro.registrar("INFO", "Simulaciones", "=== INICIO DE BATERÍA DE SIMULACIONES (12 CASOS) ===")  # Log
    reservas_exitosas = []  # Lista para recolectar las reservas válidas procesadas

    escenarios = [  # Definición de los 12 casos de prueba (6 válidos y 6 inválidos)
        ("CASO 01 [Válido - Sala]", lambda: Reserva(Cliente("1010123456", "Carlos Mendoza", "carlos@unad.edu.co", "3105551122"), ReservaSalas(30), 4)),
        ("CASO 02 [Válido - Equipos c/Descuento]", lambda: Reserva(Cliente("1020987654", "Laura Martínez", "laura.m@empresa.com", "3204443322"), AlquilerEquipos(3), 5, descuento=0.10)),
        ("CASO 03 [Válido - Asesoría]", lambda: Reserva(Cliente("80123456", "Andrés Gómez", "agomez@tech.co", "6017458963"), AsesoriaEspecializada("Ciberseguridad"), 2)),
        ("CASO 04 [Inválido - Documento]", lambda: Reserva(Cliente("ABC123", "Pedro Pérez", "pedro@mail.com", "3112223344"), ReservaSalas(), 2)),
        ("CASO 05 [Inválido - Correo]", lambda: Reserva(Cliente("1030456789", "Sofía Castro", "sofiacastro.com", "3158889900"), AsesoriaEspecializada(), 3)),
        ("CASO 06 [Inválido - 0 Horas]", lambda: Reserva(Cliente("1040789456", "Diana Rojas", "diana@correo.org", "3001112233"), ReservaSalas(), 0)),
        ("CASO 07 [Inválido - >24 Horas]", lambda: Reserva(Cliente("1050321654", "Jorge Ruiz", "jorge@correo.net", "3129998877"), AlquilerEquipos(2), 30)),
        ("CASO 08 [Inválido - Teléfono]", lambda: Reserva(Cliente("1060654987", "Marta Silva", "marta@dominio.com", "123"), ReservaSalas(), 3)),
        ("CASO 09 [Inválido - Descuento 80%]", lambda: Reserva(Cliente("1070147258", "Luis Torres", "luis@dominio.co", "3187776655"), AsesoriaEspecializada(), 4, descuento=0.80)),
        ("CASO 10 [Válido - Ciclo Cancelación]", lambda: Reserva(Cliente("1080369258", "Elena Vargas", "elena@unad.edu.co", "3196665544"), ReservaSalas(15), 3)),
        ("CASO 11 [Inválido - Nombre Numérico]", lambda: Reserva(Cliente("1090258147", "User1234", "user@mail.com", "3145556677"), ReservaSalas(), 2)),
        ("CASO 12 [Válido - 1 Equipo]", lambda: Reserva(Cliente("1100963852", "Camila Ortiz", "camila@empresa.co", "3174445566"), AlquilerEquipos(1), 6)),
    ]

    for titulo, constructor_reserva in escenarios:  # Recorre cada uno de los 12 escenarios
        try:  # Protege la ejecución para que ningún fallo detenga el ciclo
            reserva = constructor_reserva()  # Instancia cliente, servicio y reserva
            reserva.confirmar()  # Procesa costos y confirma la reserva
            if "Cancelación" in titulo:  # Prueba específica de cambio de estado a CANCELADA
                reserva.cancelar("Reprogramación solicitada en simulación")  # Ejecuta cancelación
            reservas_exitosas.append(reserva)  # Almacena reserva exitosa
            print(f"[OK] {titulo} -> {reserva.codigo} | Estado: {reserva.estado} | Total: ${reserva.detalle_financiero['total']:,.2f}")
        except ErrorSistema as error_controlado:  # Captura cualquier excepción del dominio
            GestorRegistro.registrar("ERROR", "Simulaciones", f"{titulo} falló: {error_controlado}")  # Registra en log
            print(f"[CONTROLADO] {titulo} -> {error_controlado}")  # Muestra error controlado en consola

    GestorRegistro.registrar("INFO", "Simulaciones", f"=== FIN SIMULACIONES: {len(reservas_exitosas)} exitosas ===")  # Log final
    return reservas_exitosas  # Devuelve la lista de reservas válidas generadas


if __name__ == "__main__":  # Permite ejecutar este archivo directamente para probar las simulaciones
    ejecutar_simulaciones()  # Llama a la batería de 12 pruebas