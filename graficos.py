import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime


class Graficos(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=1200, height=700)  
        self.place(x=170, y=50)

        # Etiqueta y combobox
        label = ctk.CTkLabel(parent, text="Selecciona un tipo de gráfico:")
        label.place(x=500, y=20)

        self.combo_graficos = ttk.Combobox(
            parent,
            values=["Ventas Diarias", "Ventas Semanales", "Ventas Mensuales", "Ventas Anuales"],
            state="readonly"
        )
        self.combo_graficos.place(x=845, y=32)
        self.combo_graficos.bind("<<ComboboxSelected>>", self.actualizar_grafico)

    def actualizar_grafico(self, event):
        # Cambiar gráfico
        for widget in self.winfo_children():
            widget.destroy()
        tipo_grafico = self.combo_graficos.get()

        # Datos
        etiquetas, totales = obtener_datos_pedidos(tipo_grafico)

        # Ajuste 
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_facecolor("#f9f9f9")
        fig.patch.set_facecolor("#e0e0e0")
        
        # Gráfico según tipo
        if tipo_grafico == "Ventas Diarias":
            ax.plot(etiquetas, totales, label="Ventas", color="red")
            ax.set_title("Ventas Diarias")
            ax.set_xlabel("Fechas")
            ax.set_ylabel("Total (CLP)")
        elif tipo_grafico == "Ventas Semanales":
            ax.bar(etiquetas, totales, color="blue")
            ax.set_title("Ventas Semanales")
            ax.set_xlabel("Semanas")
            ax.set_ylabel("Total (CLP)")
        elif tipo_grafico == "Ventas Mensuales":
            ax.pie(
                totales,
                labels=etiquetas,
                autopct="%1.1f%%",
                colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
            )
            ax.set_title("Ventas Mensuales")
        elif tipo_grafico == "Ventas Anuales":
            ax.plot(etiquetas, totales, label="Ventas", color="green")
            ax.set_title("Ventas Anuales")
            ax.set_xlabel("Años")
            ax.set_ylabel("Total (CLP)")

        # Insertar gráfico
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        canvas.draw()


def obtener_datos_pedidos(tipo_grafico):
    conn = sqlite3.connect("restaurante.db") 
    cursor = conn.cursor()

    if tipo_grafico == "Ventas Diarias":
        cursor.execute(f"""SELECT fecha, SUM(total) FROM pedidos GROUP BY fecha ORDER BY fecha""")
    
    elif tipo_grafico == "Ventas Semanales":
        cursor.execute(f"""SELECT strftime('%W-%Y', fecha) AS semana, SUM(total) FROM pedidos GROUP BY semana ORDER BY semana""")
   
    elif tipo_grafico == "Ventas Mensuales":
        cursor.execute(f"""SELECT strftime('%m-%Y', fecha) AS mes, SUM(total) FROM pedidos GROUP BY mes ORDER BY mes""")
    
    elif tipo_grafico == "Ventas Anuales":
        cursor.execute(f"""SELECT strftime('%Y', fecha) AS año, SUM(total) FROM pedidos GROUP BY año ORDER BY año""")

    resultados = cursor.fetchall()
    conn.close()

    etiquetas = [fila[0] for fila in resultados]
    totales = [fila[1] for fila in resultados]
    return etiquetas, totales
