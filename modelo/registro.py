# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Configuración y Gestión de Logs (Rol 2 - Nicoll Yepes)
# ==============================================================================

import os
from datetime import datetime


class GestorRegistro:  #Clase encargada de escribir la auditoría en logs/sistema.log
    """Administra la escritura segura de eventos y errores en sistema.log."""

    RUTA_DIRECTORIO = "logs"
    RUTA_ARCHIVO = os.path.join(RUTA_DIRECTORIO, "sistema.log")

    @classmethod
    def registrar(cls, nivel: str, modulo: str, mensaje: str) -> None:
        """Escribe una línea de auditoría asegurando el cierre del recurso con finally."""
        archivo = None  # Inicializa la variable de archivo antes del bloque try
        
        try:
            os.makedirs(cls.RUTA_DIRECTORIO, exist_ok=True)
            marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            linea = f"[{marca_tiempo}] [{nivel.upper()}] [{modulo}] {mensaje}\n"
            archivo = open(cls.RUTA_ARCHIVO, mode="a", encoding="utf-8")
            archivo.write(linea)
        
        except OSError as error_io:
            print(f"Advertencia crítica de auditoría: no se pudo escribir log ({error_io})")
        
        finally:
            if archivo is not None and not archivo.closed:
                archivo.close()

    @classmethod
    def obtener_estadisticas(cls) -> dict:
        """Lee el archivo sistema.log y devuelve un conteo de eventos por nivel."""
        conteo = {"INFO": 0, "WARNING": 0, "ERROR": 0}
        try:
            with open(cls.RUTA_ARCHIVO, mode="r", encoding="utf-8") as archivo:
                for linea in archivo:
                    if "[INFO]" in linea:
                        conteo["INFO"] += 1
                    elif "[WARNING]" in linea:
                        conteo["WARNING"] += 1
                    elif "[ERROR]" in linea:
                        conteo["ERROR"] += 1
        except FileNotFoundError:
            pass  # Si el archivo aún no existe, retorna los contadores en cero
        return conteo