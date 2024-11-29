import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sqlite3
from datetime import datetime


class GraficosVentas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=1200, height=1000)  
        self.place(x=70, y=50)

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
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.set_facecolor("#f9f9f9")
        fig.patch.set_facecolor("#e0e0e0")
        
        # Gráfico según tipo
        if tipo_grafico == "Ventas Diarias":
            ax.plot(etiquetas, totales, label="Ventas", color="red", marker='o')  
            ax.set_title("Ventas Diarias")
            ax.set_xlabel("Fechas")
            ax.set_ylabel("Total (CLP)")
            ax.grid(True) 
            ax.set_ylim(0, max(totales) * 1.1) 
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))  
            plt.xticks(rotation=45, ha="right")
        elif tipo_grafico == "Ventas Semanales":
            ax.bar(etiquetas, totales, color="blue")
            ax.set_title("Ventas Semanales")
            ax.set_xlabel("Semanas")
            ax.set_ylabel("Total (CLP)")
            ax.set_ylim(0, max(totales) * 1.1)
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
            plt.xticks(rotation=45, ha="right")
        elif tipo_grafico == "Ventas Mensuales":
            ax.pie(
                totales,
                labels=etiquetas,
                autopct="%1.1f%%",
                colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
            )
            ax.set_title("Ventas Mensuales")
        elif tipo_grafico == "Ventas Anuales":
            ax.plot(etiquetas, totales, label="Ventas", color="green", marker='o')
            ax.set_title("Ventas Anuales")
            ax.set_xlabel("Años")
            ax.set_ylabel("Total (CLP)")
            ax.set_ylim(0, max(totales) * 1.1)
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
            plt.xticks(rotation=45, ha="right")

        # Insertar gráfico
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        canvas.draw()

class GraficoMenusMasComprados(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=1200, height=1000)
        self.place(x=70, y=50)

        # Etiqueta
        label = ctk.CTkLabel(parent, text="Distribución de los Menús Más Comprados", font=("Arial", 20))
        label.place(x=500, y=20)

        # Obtener y mostrar gráfico
        self.mostrar_grafico()

    def mostrar_grafico(self):
        etiquetas2, totales2 = obtener_datos_menus_mas_comprados()
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.set_facecolor("#f9f9f9")
        fig.patch.set_facecolor("#e0e0e0")

        # Gráfico
        ax.barh(etiquetas2, totales2, color="#66b3ff")
        ax.set_title("Menús Más Comprados", fontsize=18)
        ax.set_xlabel("Cantidad", fontsize=14)
        ax.set_ylabel("Menús", fontsize=14)
        ax.grid(axis="x", linestyle="--")

        # Insertar gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        canvas.draw()

def obtener_datos_pedidos(tipo_grafico):
    conn = sqlite3.connect("restaurante.db") 
    cursor = conn.cursor()

    if tipo_grafico == "Ventas Diarias":
        cursor.execute(f"""SELECT DATE(fecha) AS fecha_solo, SUM(total) FROM pedidos GROUP BY DATE(fecha) ORDER BY fecha_solo""")
    
    elif tipo_grafico == "Ventas Semanales":
        cursor.execute("""SELECT strftime('%Y-%W', fecha) AS semana, SUM(total) FROM pedidos GROUP BY semana ORDER BY strftime('%Y-%m-%d', fecha)""")
   
    elif tipo_grafico == "Ventas Mensuales":
        cursor.execute(f"""SELECT strftime('%m-%Y', fecha) AS mes, SUM(total) FROM pedidos GROUP BY mes ORDER BY mes""")
    
    elif tipo_grafico == "Ventas Anuales":
        cursor.execute(f"""SELECT strftime('%Y', fecha) AS año, SUM(total) FROM pedidos GROUP BY año ORDER BY año""")

    resultados = cursor.fetchall()
    conn.close()

    etiquetas = [fila[0] for fila in resultados]
    totales = [fila[1] for fila in resultados]
    return etiquetas, totales


def obtener_datos_menus_mas_comprados():
    conn = sqlite3.connect("restaurante.db")
    cursor = conn.cursor()

    # Consulta para obtener menús más comprados
    cursor.execute("""SELECT menus.nombre, SUM(pedidos.cantidad) FROM pedidos JOIN menus ON pedidos.menu_id = menus.id GROUP BY pedidos.menu_id ORDER BY SUM(pedidos.cantidad) DESC""")

    resultados = cursor.fetchall()
    conn.close()

    etiquetas2 = [fila[0] for fila in resultados]
    totales2 = [fila[1] for fila in resultados]
    return etiquetas2, totales2