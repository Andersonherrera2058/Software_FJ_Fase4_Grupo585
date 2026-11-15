# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Archivo Principal: main.py (Rol 1 - Anderson Herrera)
# ==============================================================================

from simulaciones import ejecutar_simulaciones  # Importa las 12 simulaciones automatizadas
from gui import iniciar_gui  # Importa la interfaz gráfica en inglés
from modelo.registro import GestorRegistro  # Importa el gestor de auditoría


def main() -> None:  # Función principal que orquesta simulaciones y arranque de GUI
    """Ejecuta las simulaciones de validación y lanza la interfaz gráfica en inglés."""  # Docstring
    GestorRegistro.registrar("INFO", "Main", "Iniciando ejecución integral de Software FJ...")  # Audita inicio
    print("===============================================================")
    print(" SOFTWARE FJ - EJECUTANDO SIMULACIONES DE VALIDACIÓN (12 CASOS)")
    print("===============================================================")
    ejecutar_simulaciones()  # Corre las 12 operaciones válidas e inválidas generando logs/sistema.log
    print("\nSimulaciones completadas. Abriendo interfaz gráfica (Tkinter en inglés)...")
    iniciar_gui()  # Despliega la interfaz gráfica principal


if __name__ == "__main__":  # Verifica que el script se ejecute como programa principal
    main()  # Ejecuta el sistema completo sin detenerse ante errores