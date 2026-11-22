"""
Módulo: sistema.py
Descripción: Controlador principal que administra las listas internas en memoria
             (sin base de datos) y controla las excepciones de operación.
"""

from excepciones import GestorLogs, ErrorSistemaFJ, DatosInvalidosError
from modelos import Cliente, Servicio, Reserva


class SistemaSoftwareFJ:
    """Gestiona las colecciones en memoria sin base de datos y controla excepciones."""

    def __init__(self):
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []
        GestorLogs.registrar("INFO", "=== INICIO DE EJECUCIÓN DEL SISTEMA SOFTWARE FJ ===")

    def registrar_cliente(self, id_c: str, nombre: str, correo: str, telefono: str) -> Cliente | None:
        nuevo_cliente = None
        try:
            nuevo_cliente = Cliente(id_c, nombre, correo, telefono)
        except ErrorSistemaFJ as e:
            GestorLogs.registrar("ERROR", f"Fallo al registrar cliente ({id_c}): {e}")
            print(f"[ERROR CONTROLADO - CLIENTE] {e}")
        else:
            self.clientes.append(nuevo_cliente)
            GestorLogs.registrar("INFO", f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}")
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
        finally:
            pass
        return nuevo_cliente

    def registrar_servicio(self, servicio: Servicio) -> None:
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("El objeto proporcionado no es un Servicio válido.")
            self.servicios.append(servicio)
        except ErrorSistemaFJ as e:
            GestorLogs.registrar("ERROR", f"Fallo al registrar servicio: {e}")
            print(f"[ERROR CONTROLADO - SERVICIO] {e}")
        else:
            GestorLogs.registrar("INFO", f"Servicio registrado: {servicio.obtener_resumen()}")
            print(f"[OK] {servicio.obtener_resumen()}")

    def crear_y_confirmar_reserva(
        self, id_r: str, cliente: Cliente, servicio: Servicio, duracion: int,
        impuesto: float = 0.19, descuento: float = 0.0, **extras
    ) -> Reserva | None:
        reserva = None
        try:
            reserva = Reserva(id_r, cliente, servicio, duracion, **extras)
            reserva.procesar_y_confirmar(impuesto=impuesto, descuento=descuento)
        except ErrorSistemaFJ as e:
            GestorLogs.registrar("ERROR", f"Fallo en reserva ({id_r}): {type(e).__name__} -> {e}")
            print(f"[ERROR CONTROLADO - RESERVA {id_r}] {e}")
        except Exception as e:
            error_encadenado = ErrorSistemaFJ(f"Error inesperado procesando reserva {id_r}")
            GestorLogs.registrar("CRITICAL", f"{error_encadenado}: {e}")
            print(f"[ERROR CRÍTICO CONTROLADO] {error_encadenado}")
        else:
            self.reservas.append(reserva)
            print(f"[OK] {reserva.obtener_resumen()}")
        finally:
            GestorLogs.registrar("DEBUG", f"Intento de transacción finalizado para ID: {id_r}")
        return reserva
