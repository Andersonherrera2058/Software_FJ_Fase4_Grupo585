# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Configuración y Gestión de Logs (Rol 2 - Nicoll Yepes)
# ==============================================================================

import os  # Importa módulo del sistema operativo para gestionar rutas y directorios
from datetime import datetime  # Importa datetime para estampar fecha y hora exacta en cada evento


class GestorRegistro:  # Clase encargada de escribir la auditoría en logs/sistema.log
    """Administra la escritura segura de eventos y errores en sistema.log."""  # Docstring de clase

    RUTA_DIRECTORIO = "logs"  # Define el nombre de la carpeta de auditoría
    RUTA_ARCHIVO = os.path.join(RUTA_DIRECTORIO, "sistema.log")  # Construye la ruta logs/sistema.log

    @classmethod
    def registrar(cls, nivel: str, modulo: str, mensaje: str) -> None:  # Método de clase para registrar eventos
        """Escribe una línea de auditoría asegurando el cierre del recurso con finally."""  # Docstring
        archivo = None  # Inicializa la variable de archivo antes del bloque try
        try:  # Inicia bloque protegido para operaciones de entrada/salida en disco
            os.makedirs(cls.RUTA_DIRECTORIO, exist_ok=True)  # Crea la carpeta logs/ si aún no existe
            marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtiene fecha y hora actual
            linea = f"[{marca_tiempo}] [{nivel.upper()}] [{modulo}] {mensaje}\n"  # Formatea el registro
            archivo = open(cls.RUTA_ARCHIVO, mode="a", encoding="utf-8")  # Abre el log en modo anexar
            archivo.write(linea)  # Escribe la línea de auditoría en el archivo físico
        except OSError as error_io:  # Captura posibles errores de permisos o disco lleno
            print(f"Advertencia crítica de auditoría: no se pudo escribir log ({error_io})")  # Informa en consola
        finally:  # Bloque obligatorio que garantiza el cierre del archivo ocurra o no un error
            if archivo is not None and not archivo.closed:  # Verifica si el descriptor sigue abierto
                archivo.close()  # Cierra el archivo de forma segura liberando recursos del sistema