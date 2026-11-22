"""
Módulo: modelos.py
Descripción: Implementa la arquitectura orientada a objetos (abstracción, herencia,
             polimorfismo y encapsulación) para clientes, servicios y reservas.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import (
    GestorLogs,
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, id_entidad: str):
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ParametroFaltanteError("El ID de la entidad es obligatorio y debe ser texto válido.")
        self._id = id_entidad.strip()
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las clases hijas a describirse."""
        pass


class Servicio(EntidadBase, ABC):
    """Clase abstracta que modela un servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre del servicio debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        try:
            valor_num = float(valor)
        except (ValueError, TypeError) as e:
            # Encadenamiento de excepciones
            raise DatosInvalidosError(f"La tarifa '{valor}' no es un número válido.") from e

        if valor_num <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor a cero.")
        self._tarifa_base = valor_num

    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        """Valida parámetros específicos de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """
        Método polimórfico y sobrecargado (mediante argumentos opcionales y **extras)
        para calcular el costo final del servicio.
        """
        pass

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self._id}] {self._nombre} | Tarifa base: ${self._tarifa_base:,.2f} | Estado: {estado}"


class Cliente(EntidadBase):
    """Representa un cliente registrado en Software FJ con datos encapsulados."""

    def __init__(self, id_cliente: str, nombre_completo: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 4:
            raise DatosInvalidosError("El nombre del cliente debe contener al menos 4 caracteres.")
        self._nombre_completo = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        limpio = str(valor).strip()
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatosInvalidosError(f"El teléfono '{valor}' debe contener al menos 7 dígitos numéricos.")
        self._telefono = limpio

    def obtener_resumen(self) -> str:
        return f"Cliente [{self._id}]: {self._nombre_completo} | Email: {self._correo} | Tel: {self._telefono}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad_maxima: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise DatosInvalidosError("La capacidad máxima de la sala debe ser un entero positivo.")
        self.capacidad_maxima = capacidad_maxima

    def validar_parametros(self, **kwargs) -> bool:
        asistentes = kwargs.get("asistentes", 1)
        if asistentes <= 0:
            raise DatosInvalidosError("El número de asistentes debe ser mayor a 0.")
        if asistentes > self.capacidad_maxima:
            raise ReservaInvalidaError(
                f"La sala '{self.nombre}' soporta máximo {self.capacidad_maxima} personas (solicitadas: {asistentes})."
            )
        return True

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """Calcula costo por horas; admite cargo adicional por catering opcional."""
        if duracion <= 0:
            raise CalculoInconsistenteError("La duración en horas de la sala debe ser positiva.")
        subtotal = self.tarifa_base * duracion
        if extras.get("incluir_catering", False):
            subtotal += 50000.0
        total = (subtotal - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El cálculo total de la reserva de sala no puede ser negativo.")
        return round(total, 2)


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, stock: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_dia, disponible)
        if not isinstance(stock, int) or stock < 0:
            raise DatosInvalidosError("El stock de equipos no puede ser negativo.")
        self.stock = stock

    def validar_parametros(self, **kwargs) -> bool:
        cantidad = kwargs.get("cantidad", 1)
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad de equipos a alquilar debe ser mayor a 0.")
        if cantidad > self.stock:
            raise ServicioNoDisponibleError(
                f"Stock insuficiente para '{self.nombre}'. Disponible: {self.stock}, Solicitado: {cantidad}."
            )
        return True

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """Calcula costo por días y cantidad de equipos; admite seguro contra daños."""
        if duracion <= 0:
            raise CalculoInconsistenteError("Los días de alquiler deben ser mayores a cero.")
        cantidad = extras.get("cantidad", 1)
        subtotal = self.tarifa_base * duracion * cantidad
        if extras.get("seguro_danos", False):
            subtotal += 25000.0 * cantidad
        total = (subtotal - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El cálculo total del alquiler de equipo resultó negativo.")
        return round(total, 2)


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría y asesoría en software."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not especialidad or not especialidad.strip():
            raise ParametroFaltanteError("Debe especificar el área de especialidad de la asesoría.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, **kwargs) -> bool:
        modalidad = kwargs.get("modalidad", "virtual").lower()
        if modalidad not in ("virtual", "presencial"):
            raise DatosInvalidosError(f"Modalidad '{modalidad}' no permitida. Use 'virtual' o 'presencial'.")
        return True

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0, **extras) -> float:
        """Calcula costo por horas; recargo del 15% si la asesoría es presencial."""
        if duracion <= 0:
            raise CalculoInconsistenteError("La duración de la asesoría debe ser al menos de 1 hora.")
        subtotal = self.tarifa_base * duracion
        if extras.get("modalidad", "virtual").lower() == "presencial":
            subtotal *= 1.15
        total = (subtotal - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El cálculo total de la asesoría es inconsistente.")
        return round(total, 2)


class Reserva(EntidadBase):
    """Integra Cliente, Servicio, duración y estado con control transaccional."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int, **parametros_extra):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere una instancia válida de Servicio.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no se encuentra disponible.")

        servicio.validar_parametros(**parametros_extra)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.parametros_extra = parametros_extra
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def procesar_y_confirmar(self, impuesto: float = 0.19, descuento: float = 0.0) -> None:
        """Calcula el costo y confirma la reserva si todo es válido."""
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(f"No se puede confirmar la reserva {self._id} porque ya fue cancelada.")
        if self.estado == "CONFIRMADA":
            raise ReservaInvalidaError(f"La reserva {self._id} ya se encuentra confirmada.")

        self.costo_total = self.servicio.calcular_costo(
            self.duracion, impuesto=impuesto, descuento=descuento, **self.parametros_extra
        )
        if isinstance(self.servicio, AlquilerEquipo):
            cantidad = self.parametros_extra.get("cantidad", 1)
            self.servicio.stock -= cantidad

        self.estado = "CONFIRMADA"
        GestorLogs.registrar("INFO", f"Reserva {self._id} CONFIRMADA. Total: ${self.costo_total:,.2f}")

    def cancelar(self) -> None:
        """Cancela una reserva existente y restaura recursos si aplica."""
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self._id} ya estaba cancelada.")
        if self.estado == "CONFIRMADA" and isinstance(self.servicio, AlquilerEquipo):
            cantidad = self.parametros_extra.get("cantidad", 1)
            self.servicio.stock += cantidad

        self.estado = "CANCELADA"
        GestorLogs.registrar("WARNING", f"Reserva {self._id} CANCELADA por solicitud.")

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self._id}] | Estado: {self.estado} | Cliente: {self.cliente.nombre_completo} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | Total: ${self.costo_total:,.2f}"
        )
