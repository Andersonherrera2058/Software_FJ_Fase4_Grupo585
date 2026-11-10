"""
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
Curso: Programación - Código: 213023
Fase 4: Prácticas Simuladas - Empresa: Software FJ
Módulo: Interfaz Gráfica de Usuario (Tkinter)
Integrantes: Anderson Herrera (Parte 1), Daniel (Parte 2), Nicoll (Parte 3)
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Importamos directamente desde main.py las clases ya validadas
from main import (
    GestorLogs, 
    SoftwareFJError, 
    Cliente, 
    ReservaSalas, 
    AlquilerEquipos, 
    AsesoriaEspecializada, 
    Reserva
)

class SoftwareFJApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software FJ - Sistema Integral de Gestión (Fase 4 - UNAD)")
        self.geometry("980x650")
        self.configure(bg="#f1f5f9")
        self.resizable(False, False)

        # Estructuras de almacenamiento en memoria (sin bases de datos)
        self.clientes = {}
        self.servicios = {}
        self.reservas = {}

        self._cargar_servicios_base()
        self._construir_interfaz()

    def _cargar_servicios_base(self):
        """Inicializa el catálogo de servicios según el Anexo 3."""
        s1 = ReservaSalas("SRV-01", "Sala Magna de Juntas", 50000.0, 20, True)
        s2 = AlquilerEquipos("SRV-02", "Servidor Dedicado GPU", 80000.0, "SERVIDOR", 5)
        s3 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud AWS", 120000.0, "Ing. Carlos Mendoza", "LEAD_ARCHITECT")
        
        self.servicios[s1.identificador] = s1
        self.servicios[s2.identificador] = s2
        self.servicios[s3.identificador] = s3

    def _construir_interfaz(self):
        # Banner superior institucional
        banner = tk.Frame(self, bg="#0f172a", height=70)
        banner.pack(fill="x")
        lbl_titulo = tk.Label(banner, text="SOFTWARE FJ | SISTEMA INTEGRAL DE CLIENTES, SERVICIOS Y RESERVAS", 
                              font=("Segoe UI", 13, "bold"), fg="#ffffff", bg="#0f172a")
        lbl_titulo.pack(pady=6)
        lbl_sub = tk.Label(banner, text="Grupo 585 | Anderson Herrera (Parte 1) - Daniel (Parte 2) - Nicoll (Parte 3)", 
                           font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a")
        lbl_sub.pack()

        # Panel 1: Registro de Clientes
        pnl_cli = tk.LabelFrame(self, text=" 1. Registro de Cliente (Encapsulación y Validaciones) ", 
                                font=("Segoe UI", 10, "bold"), bg="#ffffff", padx=10, pady=8)
        pnl_cli.pack(fill="x", padx=15, pady=8)

        tk.Label(pnl_cli, text="ID Cliente:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.txt_cli_id = tk.Entry(pnl_cli, width=10)
        self.txt_cli_id.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(pnl_cli, text="Nombre Completo:", bg="#ffffff").grid(row=0, column=2, sticky="w")
        self.txt_cli_nom = tk.Entry(pnl_cli, width=20)
        self.txt_cli_nom.grid(row=0, column=3, padx=4, pady=4)

        tk.Label(pnl_cli, text="Correo:", bg="#ffffff").grid(row=0, column=4, sticky="w")
        self.txt_cli_correo = tk.Entry(pnl_cli, width=22)
        self.txt_cli_correo.grid(row=0, column=5, padx=4, pady=4)

        tk.Label(pnl_cli, text="Teléfono:", bg="#ffffff").grid(row=0, column=6, sticky="w")
        self.txt_cli_tel = tk.Entry(pnl_cli, width=12)
        self.txt_cli_tel.grid(row=0, column=7, padx=4, pady=4)

        btn_reg_cli = tk.Button(pnl_cli, text="Registrar Cliente", bg="#0284c7", fg="#ffffff", 
                                font=("Segoe UI", 9, "bold"), command=self._evento_registrar_cliente)
        btn_reg_cli.grid(row=0, column=8, padx=10)

        # Panel 2: Creación de Reservas
        pnl_res = tk.LabelFrame(self, text=" 2. Gestión de Reservas y Sobrecarga de Costos ", 
                                font=("Segoe UI", 10, "bold"), bg="#ffffff", padx=10, pady=8)
        pnl_res.pack(fill="x", padx=15, pady=4)

        tk.Label(pnl_res, text="ID Reserva:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.txt_res_id = tk.Entry(pnl_res, width=10)
        self.txt_res_id.grid(row=0, column=1, padx=4)

        tk.Label(pnl_res, text="Cliente:", bg="#ffffff").grid(row=0, column=2, sticky="w")
        self.cbx_clientes = ttk.Combobox(pnl_res, state="readonly", width=14)
        self.cbx_clientes.grid(row=0, column=3, padx=4)

        tk.Label(pnl_res, text="Servicio:", bg="#ffffff").grid(row=0, column=4, sticky="w")
        self.cbx_servicios = ttk.Combobox(pnl_res, state="readonly", width=25, 
                                          values=list(self.servicios.keys()))
        self.cbx_servicios.grid(row=0, column=5, padx=4)

        tk.Label(pnl_res, text="Duración (h):", bg="#ffffff").grid(row=0, column=6, sticky="w")
        self.txt_duracion = tk.Entry(pnl_res, width=8)
        self.txt_duracion.grid(row=0, column=7, padx=4)

        tk.Label(pnl_res, text="Descuento (%):", bg="#ffffff").grid(row=1, column=0, sticky="w", pady=6)
        self.txt_descuento = tk.Entry(pnl_res, width=8)
        self.txt_descuento.insert(0, "0")
        self.txt_descuento.grid(row=1, column=1, padx=4, pady=6)

        btn_confirmar = tk.Button(pnl_res, text="Confirmar Reserva", bg="#16a34a", fg="#ffffff", 
                                  font=("Segoe UI", 9, "bold"), command=self._evento_confirmar_reserva)
        btn_confirmar.grid(row=1, column=6, columnspan=2, sticky="e")

        # Panel 3: Tabla de Monitoreo
        pnl_tabla = tk.LabelFrame(self, text=" 3. Monitor de Reservas Activas (Sin Base de Datos) ", 
                                  font=("Segoe UI", 10, "bold"), bg="#ffffff", padx=10, pady=8)
        pnl_tabla.pack(fill="both", expand=True, padx=15, pady=8)

        columnas = ("ID", "Estado", "Cliente", "Servicio", "Duracion", "Total")
        self.tabla = ttk.Treeview(pnl_tabla, columns=columnas, show="headings", height=8)
        self.tabla.heading("ID", text="ID Reserva")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Servicio", text="Servicio Contratado")
        self.tabla.heading("Duracion", text="Duración")
        self.tabla.heading("Total", text="Total Liquidado (IVA)")

        self.tabla.column("ID", width=90, anchor="center")
        self.tabla.column("Estado", width=100, anchor="center")
        self.tabla.column("Cliente", width=180)
        self.tabla.column("Servicio", width=220)
        self.tabla.column("Duracion", width=80, anchor="center")
        self.tabla.column("Total", width=120, anchor="e")
        self.tabla.pack(fill="both", expand=True)

        # Botones de Acción Inferiores
        pnl_btn = tk.Frame(self, bg="#f1f5f9")
        pnl_btn.pack(fill="x", padx=15, pady=6)

        btn_cancelar = tk.Button(pnl_btn, text="Cancelar Reserva Seleccionada", bg="#dc2626", fg="#ffffff", 
                                 font=("Segoe UI", 9, "bold"), command=self._evento_cancelar_reserva)
        btn_cancelar.pack(side="left")

        btn_ver_logs = tk.Button(pnl_btn, text="Consultar Auditoría (logs.txt)", bg="#475569", fg="#ffffff", 
                                 font=("Segoe UI", 9), command=self._mostrar_logs)
        btn_ver_logs.pack(side="right")

    def _evento_registrar_cliente(self):
        try:
            c = Cliente(
                self.txt_cli_id.get(),
                self.txt_cli_nom.get(),
                self.txt_cli_correo.get(),
                self.txt_cli_tel.get()
            )
            self.clientes[c.identificador] = c
            self.cbx_clientes["values"] = list(self.clientes.keys())
            messagebox.showinfo("Éxito", f"Cliente registrado exitosamente:\n{c.obtener_resumen()}")
            GestorLogs.registrar_evento("INFO", f"Cliente registrado vía GUI: {c.identificador}", origen="GUI")
            
            self.txt_cli_id.delete(0, tk.END)
            self.txt_cli_nom.delete(0, tk.END)
            self.txt_cli_correo.delete(0, tk.END)
            self.txt_cli_tel.delete(0, tk.END)
        except SoftwareFJError as ex:
            GestorLogs.registrar_error(ex, origen="GUI_RegistrarCliente")
            messagebox.showwarning("Validación de Cliente", str(ex))
        except Exception as ex_gen:
            GestorLogs.registrar_error(ex_gen, origen="GUI_Cliente_Inesperado")
            messagebox.showerror("Error Inesperado", str(ex_gen))

    def _evento_confirmar_reserva(self):
        try:
            id_res = self.txt_res_id.get()
            id_cli = self.cbx_clientes.get()
            id_srv = self.cbx_servicios.get()
            duracion = float(self.txt_duracion.get())
            descuento = float(self.txt_descuento.get())

            if id_cli not in self.clientes:
                messagebox.showwarning("Atención", "Seleccione un cliente válido.")
                return

            reserva = Reserva(id_res, self.clientes[id_cli], self.servicios[id_srv], duracion)
            reserva.confirmar_reserva(porcentaje_descuento=descuento)
            self.reservas[id_res] = reserva

            self.tabla.insert("", tk.END, values=(
                reserva.identificador,
                reserva.estado,
                self.clientes[id_cli].nombre_completo,
                self.servicios[id_srv].nombre,
                f"{duracion} h",
                f"${reserva.costo_total:,.2f}"
            ))
            messagebox.showinfo("Confirmación", f"Reserva registrada con éxito.\nTotal: ${reserva.costo_total:,.2f}")
        except ValueError:
            messagebox.showwarning("Dato Numérico Inválido", "Duración y Descuento deben ser numéricos.")
        except SoftwareFJError as ex:
            GestorLogs.registrar_error(ex, origen="GUI_ConfirmarReserva")
            messagebox.showwarning("Excepción Controlada", str(ex))

    def _evento_cancelar_reserva(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione una reserva de la tabla.")
            return

        item = self.tabla.item(seleccion[0])
        id_res = item["values"][0]

        try:
            reserva = self.reservas.get(id_res)
            if reserva:
                reserva.cancelar_reserva("Cancelación solicitada por el usuario desde la interfaz gráfica")
                self.tabla.item(seleccion[0], values=(
                    reserva.identificador,
                    reserva.estado,
                    item["values"][2],
                    item["values"][3],
                    item["values"][4],
                    item["values"][5]
                ))
                messagebox.showinfo("Cancelación", f"Reserva {id_res} cancelada correctamente.")
        except SoftwareFJError as ex:
            GestorLogs.registrar_error(ex, origen="GUI_CancelarReserva")
            messagebox.showwarning("Aviso", str(ex))

    def _mostrar_logs(self):
        try:
            with open("logs.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()
                ultimas = "".join(lineas[-15:]) if lineas else "Sin registros."
                messagebox.showinfo("Auditoría Reciente (logs.txt)", ultimas)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer logs.txt: {e}")

if __name__ == "__main__":
    app = SoftwareFJApp()
    app.mainloop()