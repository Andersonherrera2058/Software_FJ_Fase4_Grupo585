# Software FJ - Sistema de Gestión de Clientes, Servicios y Reservas (Fase 4)

**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Curso:** Programación (Código: 213023) — Grupo 585  
**Tutor:** Frank Rodríguez Achury  

---

## 1. Integrantes y Distribución de Roles

| Integrante | Rol Asignado | Rama en GitHub | Módulos Responsables |
| :--- | :--- | :--- | :--- |
| **Anderson Herrera** | **Rol 1** (Líder Integrador e Interfaz Gráfica) | `feature/integracion-gui` | `main.py`, `gui.py`, `modelo/reserva.py`, `simulaciones.py`, `README.md` |
| **Nicoll Yepes** | **Rol 2** (Excepciones y Auditoría) | `feature/excepciones-logs` | `modelo/excepciones.py`, `modelo/registro.py` |
| **Daniel Gómez** | **Rol 3** (Entidad Base y Clientes) | `feature/clientes` | `modelo/entidad.py`, `modelo/cliente.py` |
| **Leonardo Valencia** | **Rol 4** (Servicios Especializados) | `feature/servicios` | `modelo/servicios.py` |

---

## 2. Estructura del Proyecto

```text
Software_FJ_Fase4_Grupo585/
├── modelo/
│   ├── __init__.py
│   ├── excepciones.py      # Jerarquía ErrorSistema
│   ├── registro.py         # Auditoría en logs/sistema.log con try/except/finally
│   ├── entidad.py          # Clase abstracta Entidad
│   ├── cliente.py          # Validación de atributos privados de Cliente
│   ├── servicios.py        # Clase abstracta Servicio + 3 hijas con sobrecarga
│   └── reserva.py          # Ciclo de vida de Reserva + encadenamiento raise ... from
├── logs/
│   └── sistema.log         # Bitácora generada automáticamente al ejecutar
├── docs/
│   └── capturas/           # Evidencias gráficas del funcionamiento
├── main.py                 # Punto de entrada principal del sistema
├── gui.py                  # Interfaz gráfica en Tkinter (en inglés)
├── simulaciones.py         # 12 simulaciones válidas e inválidas
└── README.md