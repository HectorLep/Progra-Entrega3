from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import ttk

class SistemaGestionRestaurante(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Restaurante")
        self.geometry("1600x900")

        
        # Crear las pestañas principales
        self.tabview = ctk.CTkTabview(self, width=1600, height=800)
        self.tabview.pack(padx=20, pady=20)
        self.crear_pestanas()

    def crear_pestanas(self):
        # Crear las pestañas
        self.tab_ingredientes = self.tabview.add("Gestión de Ingredientes")
        self.tab_menus = self.tabview.add("Gestión de Menús")
        self.tab_clientes = self.tabview.add("Gestión de Clientes")
        self.tab_pedidos = self.tabview.add("Gestión de Pedidos")
        self.tab_graficos = self.tabview.add("Estadísticas")

        # Configurar cada pestaña
        self.configurar_ingredientes()
        self.configurar_menus()
        self.configurar_clientes()
        self.configurar_pedidos()
        self.configurar_graficos()

    def configurar_ingredientes(self):
        # Configurar interfaz para gestión de ingredientes
        self._crear_formulario(self.tab_ingredientes, "Ingredientes", ["Nombre", "Tipo", "Cantidad", "Unidad de Medida"])
        self._crear_treeview(self.tab_ingredientes, ["Nombre", "Tipo", "Cantidad", "Unidad de Medida"])

    def configurar_menus(self):
        # Configurar interfaz para gestión de menús
        self._crear_formulario(self.tab_menus, "Menús", ["Nombre", "Descripción"])
        self._crear_treeview(self.tab_menus, ["Nombre", "Descripción", "Ingredientes"])

    def configurar_clientes(self):
        # Configurar interfaz para gestión de clientes
        self._crear_formulario(self.tab_clientes, "Clientes", ["Nombre", "Correo Electrónico"])
        self._crear_treeview(self.tab_clientes, ["Nombre", "Correo Electrónico"])

    def configurar_pedidos(self):
        # Configurar interfaz para gestión de pedidos
        self._crear_formulario(self.tab_pedidos, "Pedidos", ["Cliente", "Menú", "Total", "Fecha"])
        self._crear_treeview(self.tab_pedidos, ["Cliente", "Menú", "Total", "Fecha"])

    def configurar_graficos(self):
        # Configurar interfaz para generación de gráficos
        label = ctk.CTkLabel(self.tab_graficos, text="Selecciona un tipo de gráfico:")
        label.pack(pady=10)

        combo = ttk.Combobox(self.tab_graficos, values=["Ventas Diarias", "Ventas Semanales", "Ingredientes Más Utilizados"])
        combo.pack(pady=10)

    def _crear_formulario(self, tab, tipo, campos):
        # Crear formulario básico
        frame_formulario = ctk.CTkFrame(tab)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        for campo in campos:
            label = ctk.CTkLabel(frame_formulario, text=f"{campo}:")
            label.pack(pady=4)
            entry = ctk.CTkEntry(frame_formulario)
            entry.pack(pady=4)

        boton = ctk.CTkButton(frame_formulario, text=f"Agregar {tipo}")
        boton.pack(pady=10)

    def _crear_treeview(self, tab, columnas):
        # Crear treeview básico
        frame_treeview = ctk.CTkFrame(tab)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(frame_treeview, columns=columnas, show="headings")
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        boton = ctk.CTkButton(frame_treeview, text="Eliminar Selección")
        boton.pack(pady=10)
