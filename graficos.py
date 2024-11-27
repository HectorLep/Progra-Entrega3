import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Graficos(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=600)
        self.place(x=20, y=100)

        # Etiqueta y combobox
        label = ctk.CTkLabel(parent, text="Selecciona un tipo de gráfico:")
        label.place(x=20, y=20)

        self.combo_graficos = ttk.Combobox(
            parent,
            values=["Ventas Diarias", "Ventas Semanales", "Ventas Mensuales", "Ventas Anuales"],
            state="readonly"
        )
        self.combo_graficos.place(x=20, y=60)
        self.combo_graficos.bind("<<ComboboxSelected>>", self.actualizar_grafico)

    def actualizar_grafico(self, event):
        # Limpiar cualquier gráfico anterior
        for widget in self.winfo_children():
            widget.destroy()

        # Obtener el tipo de gráfico seleccionado
        tipo_grafico = self.combo_graficos.get()

        # Crear un nuevo gráfico según el tipo seleccionado
        fig, ax = plt.subplots(figsize=(8, 4))
        if tipo_grafico == "Ventas Diarias":
            ax.plot(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], [200, 450, 300, 400, 600], label="Ventas")
            ax.set_title("Ventas Diarias")
            ax.set_xlabel("Días")
            ax.set_ylabel("Ventas (CLP)")
        elif tipo_grafico == "Ventas Semanales":
            ax.bar(["Semana 1", "Semana 2", "Semana 3", "Semana 4"], [1500, 1800, 1700, 2000], color="blue")
            ax.set_title("Ventas Semanales")
            ax.set_xlabel("Semanas")
            ax.set_ylabel("Ventas (CLP)")
        elif tipo_grafico == "Ventas Mensuales":
            ax.pie([20, 30, 25, 25], labels=["Producto A", "Producto B", "Producto C", "Producto D"], autopct="%1.1f%%")
            ax.set_title("Ventas Mensuales")
        elif tipo_grafico == "Ventas Anuales":
            ax.plot(["Enero", "Febrero", "Marzo", "Abril", "Mayo"], [5000, 5200, 5100, 5300, 5400], label="Ventas")
            ax.set_title("Ventas Anuales")
            ax.set_xlabel("Meses")
            ax.set_ylabel("Ventas (CLP)")

        # Insertar gráfico en el frame
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        canvas.draw()
