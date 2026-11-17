# ==============================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
# Curso: Programación - Código: 213023 | Fase 4 - Software FJ
# Módulo: Graphical User Interface in English (Rol 1 - Anderson Herrera)
# ==============================================================================

import tkinter as tk  # Importa librería estándar Tkinter para interfaces gráficas
from tkinter import ttk, messagebox  # Importa widgets modernos (Treeview, Combobox) y cuadros de diálogo
from modelo.cliente import Cliente  # Importa clase Cliente del Rol 3
from modelo.servicios import (ReservaSalas, AlquilerEquipos,AsesoriaEspecializada,ServicioExpress)  # Importa clases de servicios del Rol 4
from modelo.reserva import Reserva  # Importa clase Reserva
from modelo.excepciones import ErrorSistema  # Importa excepción base del Rol 2

class SoftwareFJApp(tk.Tk):  # Ventana principal de la aplicación en inglés
    """Main desktop GUI window for Software FJ Booking Management System."""  # Docstring en inglés

    def __init__(self):  # Constructor de la interfaz gráfica
        super().__init__()  # Inicializa la ventana raíz de Tkinter
        self.title("Software FJ - Service & Booking Management System (UNAD Group 585)")  # Título en inglés
        self.geometry("920x620")  # Establece dimensiones de la ventana principal
        self.resizable(False, False)  # Bloquea redimensionamiento para mantener alineación
        self._construir_componentes()  # Llama al método que dibuja los controles visuales

    def _construir_componentes(self) -> None:  # Construye etiquetas, entradas, botones y tabla en inglés
        """Creates and places all English UI widgets on the main window."""  # Docstring
        lbl_header = tk.Label(
            self,
            text="SOFTWARE FJ - CLIENT & SERVICE BOOKING PORTAL",
            font=("Segoe UI", 14, "bold"),
            fg="#1B365D",
            pady=10
        )
        lbl_header.pack()  # Ubica el título en la parte superior

        frame_form = ttk.LabelFrame(self, text=" Client & Service Details ", padding=12)  # Contenedor agrupado
        frame_form.pack(fill="x", padx=20, pady=5)  # Expande horizontalmente con márgenes

        ttk.Label(frame_form, text="Document ID:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.ent_doc = ttk.Entry(frame_form, width=25)
        self.ent_doc.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(frame_form, text="Full Name:").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.ent_name = ttk.Entry(frame_form, width=30)
        self.ent_name.grid(row=0, column=3, padx=5, pady=4)

        ttk.Label(frame_form, text="Email Address:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.ent_email = ttk.Entry(frame_form, width=25)
        self.ent_email.grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(frame_form, text="Phone Number:").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        self.ent_phone = ttk.Entry(frame_form, width=30)
        self.ent_phone.grid(row=1, column=3, padx=5, pady=4)

        ttk.Label(frame_form, text="Select Service:").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.cmb_service = ttk.Combobox(
    frame_form,
    values=[
        "Room Booking",
        "Equipment Rental",
        "Specialized Consulting",
        "Express Service"
    ],
    state="readonly",
    width=22
)
        self.cmb_service.current(0)  # Selecciona Room Booking por defecto
        self.cmb_service.grid(row=2, column=1, padx=5, pady=4)

        ttk.Label(frame_form, text="Duration (Hours):").grid(row=2, column=2, sticky="w", padx=5, pady=4)
        self.ent_hours = ttk.Entry(frame_form, width=12)
        self.ent_hours.insert(0, "2")  # Valor inicial sugerido de 2 horas
        self.ent_hours.grid(row=2, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(frame_form, text="Discount (0.0 - 0.5):").grid(row=3, column=0, sticky="w", padx=5, pady=4)
        self.ent_discount = ttk.Entry(frame_form, width=12)
        self.ent_discount.insert(0, "0.0")  # Descuento inicial en 0.0
        self.ent_discount.grid(row=3, column=1, sticky="w", padx=5, pady=4)

        frame_buttons = ttk.Frame(self)  # Contenedor horizontal para botones
        frame_buttons.pack(pady=10)

        btn_book = ttk.Button(frame_buttons, text="Process & Confirm Booking", command=self._procesar_reserva)
        btn_book.grid(row=0, column=0, padx=10)

        btn_clear = ttk.Button(frame_buttons, text="Clear Fields", command=self._limpiar_campos)
        btn_clear.grid(row=0, column=1, padx=10)

        frame_table = ttk.LabelFrame(self, text=" Confirmed Bookings History ", padding=10)
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("code", "client", "service", "hours", "subtotal", "tax", "total", "status")
        self.tree = ttk.Treeview(frame_table, columns=columnas, show="headings", height=12)

        encabezados = {
            "code": "Booking ID",
            "client": "Client Name",
            "service": "Service Type",
            "hours": "Hours",
            "subtotal": "Subtotal",
            "tax": "VAT (19%)",
            "total": "Total ($)",
            "status": "Status"
        }
        anchos = {"code": 90, "client": 150, "service": 160, "hours": 60, "subtotal": 100, "tax": 90, "total": 105, "status": 95}

        for col in columnas:  # Configura columnas y anchos de la tabla
            self.tree.heading(col, text=encabezados[col])
            self.tree.column(col, width=anchos[col], anchor="center")

        self.tree.pack(fill="both", expand=True)

    def _instancia_servicio(self):  # Mapea la selección del Combobox con las clases del Rol 4
        seleccion = self.cmb_service.get()  # Obtiene texto seleccionado
        if seleccion == "Room Booking":
            return ReservaSalas(capacidad=25)  # Retorna instancia de sala
        if seleccion == "Equipment Rental":
            return AlquilerEquipos(cantidad_equipos=2)  # Retorna instancia de equipos
        if seleccion == "Express Service":
            return ServicioExpress(recargo_express=25000.0)  # Retorna instancia de servicio express
        return AsesoriaEspecializada(especialidad="Software Architecture")  # Retorna instancia de asesoría

    def _procesar_reserva(self) -> None:  # Invoca las clases del modelo capturando excepciones
        """Calls domain classes to validate, calculate and register a booking."""  # Docstring
        try:  # Bloque protegido para evitar cierres inesperados de la interfaz
            cliente = Cliente(
                documento=self.ent_doc.get(),
                nombre=self.ent_name.get(),
                correo=self.ent_email.get(),
                telefono=self.ent_phone.get()
            )
            horas = int(self.ent_hours.get())  # Convierte texto de horas a entero
            descuento = float(self.ent_discount.get())  # Convierte texto de descuento a flotante
            servicio = self._instancia_servicio()  # Crea el servicio seleccionado
            reserva = Reserva(cliente=cliente, servicio=servicio, horas=horas, descuento=descuento)
            reserva.confirmar()  # Ejecuta cálculo, validación y registro en logs/sistema.log

            datos = reserva.detalle_financiero  # Extrae valores calculados
            self.tree.insert(
                "",
                "end",
                values=(
                    reserva.codigo,
                    cliente.nombre,
                    servicio.nombre,
                    horas,
                    f"${datos['subtotal']:,.2f}",
                    f"${datos['impuesto']:,.2f}",
                    f"${datos['total']:,.2f}",
                    reserva.estado
                )
            )
            messagebox.showinfo("Booking Confirmed", f"Booking {reserva.codigo} successfully registered!")
        except ValueError:  # Captura errores si escriben texto en campos numéricos
            messagebox.showerror("Input Error", "Hours must be an integer and Discount must be a decimal number.")
        except ErrorSistema as err:  # Captura cualquier excepción personalizada del dominio
            messagebox.showwarning("Validation Alert", str(err))

    def _limpiar_campos(self) -> None:  # Limpia los cuadros de texto del formulario
        """Resets all form inputs to default values."""  # Docstring
        self.ent_doc.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)
        self.ent_hours.delete(0, tk.END)
        self.ent_hours.insert(0, "2")
        self.ent_discount.delete(0, tk.END)
        self.ent_discount.insert(0, "0.0")


def iniciar_gui() -> None:  # Función auxiliar para arrancar la interfaz desde main.py
    """Launches the Tkinter main event loop."""  # Docstring
    app = SoftwareFJApp()  # Instancia la ventana principal
    app.mainloop()  # Mantiene activa la escucha de eventos gráficos


if __name__ == "__main__":  # Permite ejecutar gui.py directamente
    iniciar_gui()  # Inicia la ventana