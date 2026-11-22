"""
Módulo: excepciones.py
Descripción: Define el gestor de logs en archivo plano y las excepciones personalizadas
             para el sistema de Software FJ.
"""

from datetime import datetime


class GestorLogs:
    """Clase encargada de registrar eventos y errores en un archivo de texto."""

    ARCHIVO_LOG = "sistema_software_fj.log"

    @classmethod
    def registrar(cls, nivel: str, mensaje: str) -> None:
        """Escribe una entrada con marca de tiempo en el archivo de logs."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] [{nivel.upper()}] {mensaje}\n"
        try:
            with open(cls.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except IOError as e:
            print(f"Error crítico al escribir en el log: {e}")


class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores del sistema de Software FJ."""
    pass


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando los datos ingresados no cumplen con el formato o reglas."""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un parámetro obligatorio para una operación."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin cupo."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza ante inconsistencias al crear, confirmar o cancelar una reserva."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo financiero arroja valores negativos o ilógicos."""
    pass
