# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Clase Abstracta Entidad (Rol 3 - Daniel Gómez)
# ==============================================================================

from abc import ABC, abstractmethod  # Importa herramientas para definir clases y métodos abstractos


class Entidad(ABC):  # Clase base abstracta que representa cualquier entidad del dominio
    """Define el contrato mínimo de identificación y descripción para entidades."""  # Docstring

    def __init__(self, identificador: str):  # Constructor base que recibe el ID único
        self._identificador = identificador  # Atributo protegido con el identificador de la entidad

    @property
    def identificador(self) -> str:  # Propiedad de solo lectura para consultar el identificador
        """Retorna el identificador único de la entidad."""  # Docstring de propiedad
        return self._identificador  # Devuelve el valor del atributo protegido

    @abstractmethod
    def describir(self) -> str:  # Método abstracto obligatorio para todas las clases hijas
        """Debe ser implementado por cada subclase para retornar su resumen."""  # Docstring
        pass  # Delega la implementación concreta a las clases derivadas