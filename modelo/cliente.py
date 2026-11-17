# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Clase Cliente con Validaciones (Rol 3 - Daniel Gómez)
# ==============================================================================

import re  # Importa expresiones regulares para validar formatos de correo y teléfono
from modelo.entidad import Entidad  # Importa la clase abstracta padre Entidad
from modelo.excepciones import DatoInvalidoError  # Importa la excepción personalizada del Rol 2


class Cliente(Entidad):  # Clase concreta Cliente que hereda de Entidad
    """Representa un cliente corporativo o natural con atributos privados y validados."""  # Docstring

    def __init__(self, documento: str, nombre: str, correo: str, telefono: str):  # Constructor con 4 datos
        self.__documento = self._validar_documento(documento)  # Valida y asigna documento privado
        self.__nombre = self._validar_nombre(nombre)  # Valida y asigna nombre privado
        self.__correo = self._validar_correo(correo)  # Valida y asigna correo privado
        self.__telefono = self._validar_telefono(telefono)  # Valida y asigna teléfono privado
        super().__init__(identificador=self.__documento)  # Inicializa la clase padre con el documento

    @staticmethod
    def _validar_documento(documento: str) -> str:  # Validador interno de identificación
        limpio = str(documento).strip()  # Elimina espacios en blanco alrededor
        if not limpio.isdigit() or not (5 <= len(limpio) <= 15):  # Verifica que sean solo números entre 5 y 15 dígitos
            raise DatoInvalidoError("El documento debe ser numérico y tener entre 5 y 15 dígitos.")  # Lanza excepción Rol 2
        return limpio  # Retorna el documento validado

    @staticmethod
    def _validar_nombre(nombre: str) -> str:  # Validador interno de nombre completo
        limpio = str(nombre).strip()  # Elimina espacios innecesarios
        if len(limpio) < 3 or any(char.isdigit() for char in limpio):  # Evita nombres vacíos o con números
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres y no contener números.")  # Lanza excepción
        return limpio  # Retorna el nombre validado

    @staticmethod
    def _validar_correo(correo: str) -> str:  # Validador interno de correo electrónico
        limpio = str(correo).strip()  # Limpia espacios extremos
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"  # Expresión regular estándar para validar email
        if not re.match(patron, limpio):  # Evalúa si el correo cumple el patrón
            raise DatoInvalidoError(f"El correo electrónico '{limpio}' no tiene un formato válido.")  # Lanza excepción
        return limpio  # Retorna el correo validado

    @staticmethod
    def _validar_telefono(telefono: str) -> str:  # Validador interno de número telefónico
        limpio = str(telefono).strip()  # Limpia espacios extremos
        if not limpio.isdigit() or not (7 <= len(limpio) <= 12):  # Valida longitud entre 7 y 12 dígitos
            raise DatoInvalidoError("El teléfono debe contener entre 7 y 12 dígitos numéricos.")  # Lanza excepción
        return limpio  # Retorna el teléfono validado

    @property
    def documento(self) -> str:  # Propiedad de solo lectura para documento
        return self.__documento  # Devuelve el documento privado

    @property
    def nombre(self) -> str:  # Propiedad de solo lectura para nombre
        return self.__nombre  # Devuelve el nombre privado

    @property
    def correo(self) -> str:  # Propiedad de solo lectura para correo
        return self.__correo  # Devuelve el correo privado

    @property
    def telefono(self) -> str:  # Propiedad de solo lectura para teléfono
        return self.__telefono  # Devuelve el teléfono privado

    def obtener_resumen_contacto(self) -> str:  # Devuelve un resumen con los datos de contacto
        """Retorna el nombre, correo y teléfono del cliente."""  # Explica el contenido del resumen
        return f"{self.nombre} | {self.correo} | {self.telefono}"  # Construye y devuelve el resumen

    def validar_longitud_documento(self) -> bool:  # Comprueba la longitud del documento
        """Indica si el documento tiene entre 5 y 15 dígitos."""  # Describe el rango permitido
        return 5 <= len(self.documento) <= 15  # Devuelve True si está dentro del rango

    def describir(self) -> str:  # Implementación obligatoria del método abstracto describir
        """Retorna una cadena descriptiva con los datos del cliente."""  # Docstring
        return f"Cliente {self.__nombre} (ID: {self.__documento}) - {self.__correo}"  # Formatea salida