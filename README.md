# Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

**Autor:** Gedinson Castaño Santa  
**Curso:** Programación (213023) – Fase 4: Componente Práctico  

> **Nota sobre la entrega:** Proyecto desarrollado e implementado de manera individual debido a que los demás integrantes asignados al grupo colaborativo no establecieron comunicación ni realizaron aportes durante el desarrollo de la actividad.

---

## Descripción del Proyecto
Solución de software desarrollada en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)** y manejo avanzado de excepciones, diseñada para gestionar clientes, catálogo de servicios especializados y reservas sin dependencia de motores de bases de datos.

## Arquitectura Modular
El proyecto está estructurado en los siguientes módulos independientes:

* **`excepciones.py`**: Implementa `GestorLogs` para el registro cronológico en archivo plano y define la jerarquía de excepciones personalizadas (`ErrorSistemaFJ`, `DatosInvalidosError`, `ParametroFaltanteError`, `ServicioNoDisponibleError`, `ReservaInvalidaError`, `CalculoInconsistenteError`).
* **`modelos.py`**: Contiene las clases abstractas (`EntidadBase`, `Servicio`), la clase encapsulada (`Cliente`), las clases derivadas con polimorfismo (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) y la gestión transaccional de reservas (`Reserva`).
* **`sistema.py`**: Implementa el controlador principal `SistemaSoftwareFJ` con almacenamiento en listas en memoria y control robusto mediante bloques `try/except/else/finally` y encadenamiento de excepciones.
* **`main.py`**: Punto de entrada que ejecuta secuencialmente 15 escenarios operativos (registros válidos e inválidos, cálculos con sobrecarga de parámetros, reservas exitosas/fallidas y cancelaciones) demostrando la estabilidad continua del programa.
* **`sistema_software_fj.log`**: Archivo de auditoría generado automáticamente tras la ejecución secuencial del sistema.

## Instrucciones de Ejecución
1. Clonar o descargar el repositorio.
2. Ejecutar el módulo principal desde la terminal:
   ```bash
   python main.py
