"""
Módulo: main.py
Autor: Gedinson Castaño Santa
Descripción: Punto de entrada principal que simula 15 operaciones completas
             (válidas e inválidas) para validar la robustez del sistema Software FJ.
"""

import os
from excepciones import GestorLogs, ErrorSistemaFJ, ReservaInvalidaError
from modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaSoftwareFJ


def ejecutar_simulacion():
    if os.path.exists(GestorLogs.ARCHIVO_LOG):
        os.remove(GestorLogs.ARCHIVO_LOG)

    sistema = SistemaSoftwareFJ()
    print("\n--- FASE 1: REGISTRO DE CLIENTES ---")
    # Operación 1: Cliente válido
    c1 = sistema.registrar_cliente("C001", "Gedinson Castaño", "gedinson@softwarefj.com", "3105551234")
    # Operación 2: Cliente válido
    c2 = sistema.registrar_cliente("C002", "Laura Gómez", "laura.gomez@empresa.co", "3209876543")
    # Operación 3: Cliente inválido (correo sin @ y teléfono corto)
    sistema.registrar_cliente("C003", "Carlos Ruiz", "carlos.correo.invalido", "123")

    print("\n--- FASE 2: CREACIÓN DE SERVICIOS ---")
    # Operación 4: Sala válida
    s1 = ReservaSala("S001", "Sala Innovación A", tarifa_hora=80000, capacidad_maxima=10, disponible=True)
    sistema.registrar_servicio(s1)

    # Operación 5: Equipo válido
    s2 = AlquilerEquipo("S002", "Portátil Workstation Dell", tarifa_dia=65000, stock=3, disponible=True)
    sistema.registrar_servicio(s2)

    # Operación 6: Asesoría válida
    s3 = AsesoriaEspecializada("S003", "Consultoría Arquitectura Cloud", tarifa_hora=120000, especialidad="Cloud AWS")
    sistema.registrar_servicio(s3)

    # Operación 7: Servicio inactivo
    s4 = ReservaSala("S004", "Sala Auditorio B", tarifa_hora=150000, capacidad_maxima=50, disponible=False)
    sistema.registrar_servicio(s4)

    # Operación 8: Creación incorrecta de servicio (tarifa negativa)
    try:
        s_invalido = AlquilerEquipo("S005", "Servidor Rack", tarifa_dia=-50000, stock=2)
        sistema.registrar_servicio(s_invalido)
    except ErrorSistemaFJ as e:
        GestorLogs.registrar("ERROR", f"Creación de servicio bloqueada: {e}")
        print(f"[ERROR CONTROLADO - CREACIÓN SERVICIO] {e}")

    print("\n--- FASE 3: PROCESAMIENTO DE RESERVAS (EXITOSAS Y FALLIDAS) ---")
    # Operación 9: Reserva exitosa de sala con catering
    sistema.crear_y_confirmar_reserva("R001", c1, s1, duracion=3, asistentes=8, incluir_catering=True)

    # Operación 10: Reserva fallida de sala por exceso de capacidad
    sistema.crear_y_confirmar_reserva("R002", c2, s1, duracion=2, asistentes=15)

    # Operación 11: Reserva exitosa de alquiler de 2 equipos con seguro
    r3 = sistema.crear_y_confirmar_reserva("R003", c2, s2, duracion=4, cantidad=2, seguro_danos=True)

    # Operación 12: Reserva fallida por stock insuficiente
    sistema.crear_y_confirmar_reserva("R004", c1, s2, duracion=2, cantidad=2)

    # Operación 13: Reserva fallida por servicio no disponible
    sistema.crear_y_confirmar_reserva("R005", c1, s4, duracion=1, asistentes=5)

    # Operación 14: Reserva exitosa de asesoría presencial con descuento
    sistema.crear_y_confirmar_reserva("R006", c1, s3, duracion=2, descuento=20000, modalidad="presencial")

    # Operación 15: Cancelación de reserva y validación de doble cancelación
    print("\n--- FASE 4: CANCELACIÓN Y CONTROL DE ESTADOS ---")
    if r3:
        try:
            r3.cancelar()
            print(f"[OK] {r3.obtener_resumen()} (Stock restaurado: {s2.stock})")
            r3.cancelar()
        except ReservaInvalidaError as e:
            GestorLogs.registrar("ERROR", f"Intento inválido de cancelación: {e}")
            print(f"[ERROR CONTROLADO - CANCELACIÓN] {e}")

    GestorLogs.registrar("INFO", "=== FIN DE EJECUCIÓN SIN INTERRUPCIONES ===")
    print("\nSimulación finalizada con éxito. Revise el archivo 'sistema_software_fj.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()
