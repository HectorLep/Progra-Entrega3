from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import ttk

class SistemaGestionRestaurante(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Restaurante")
        self.geometry("1600x900")

        # Crear las pestañas principales
        self.tabview = ctk.CTkTabview(self, width=1360, height=720) 
        self.tabview.place(x=20, y=20)
        self.crear_pestanas()

    def crear_pestanas(self):
        # Crear las pestañas
        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.tab_menus = self.tabview.add("Menús")
        self.tab_clientes = self.tabview.add("Clientes")
        self.tab_compras = self.tabview.add("Panel de Compra")
        self.tab_pedidos = self.tabview.add("Pedidos")
        self.tab_graficos = self.tabview.add("Graficos")

        # Configurar cada pestaña
        self.configurar_ingredientes()
        self.configurar_menus()
        self.configurar_clientes()
        self.configurar_compras()
        self.configurar_pedidos()
        self.configurar_graficos()

    def configurar_ingredientes(self):
        # Crear formulario manualmente
        frame_formulario = ctk.CTkFrame(self.tab_ingredientes, width=1400, height=700)
        frame_formulario.place(x=10, y=10)

        # Etiquetas y entradas
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre:")
        label_nombre.place(x=20, y=20)
        entry_nombre = ctk.CTkEntry(frame_formulario)
        entry_nombre.place(x=100, y=20)

        label_tipo = ctk.CTkLabel(frame_formulario, text="Tipo:")
        label_tipo.place(x=250, y=20)
        entry_tipo = ctk.CTkEntry(frame_formulario)
        entry_tipo.place(x=330, y=20)

        boton_agregar = ctk.CTkButton(frame_formulario, text="Crear Ingrediente")
        boton_agregar.place(x=20, y=80)

        # Crear treeview manualmente
        frame_treeview = ctk.CTkFrame(self.tab_ingredientes, width=1350, height=500)
        frame_treeview.place(x=10, y=150)

        tree = ttk.Treeview(frame_treeview, columns=["Nombre", "Tipo"], show="headings", height=30)
        tree.heading("Nombre", text="Nombre")
        tree.column("Nombre", width=650, anchor="center")
        tree.heading("Tipo", text="Tipo")
        tree.column("Tipo", width=650, anchor="center")
        tree.place(x=10, y=100)



    # Repite este esquema para las demás configuraciones

    def configurar_menus(self):
        # Ejemplo para Menús
        frame_formulario = ctk.CTkFrame(self.tab_menus, width=1400, height=700)
        frame_formulario.place(x=10, y=10)

        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Menú:")
        label_nombre.place(x=20, y=20)
        entry_nombre = ctk.CTkEntry(frame_formulario)
        entry_nombre.place(x=150, y=20)

        label_descripcion = ctk.CTkLabel(frame_formulario, text="Descripción:")
        label_descripcion.place(x=320, y=20)
        entry_descripcion = ctk.CTkEntry(frame_formulario)
        entry_descripcion.place(x=450, y=20)

        boton_agregar = ctk.CTkButton(frame_formulario, text="Crear Menú")
        boton_agregar.place(x=20, y=80)

        frame_treeview = ctk.CTkFrame((self.tab_menus), width=1350, height=500)
        frame_treeview.place(x=10, y=150)

        tree = ttk.Treeview(frame_treeview, columns=["Nombre", "Descripción"], show="headings", height=30)
        tree.heading("Nombre", text="Nombre")
        tree.column("Nombre", width=650, anchor="center")
        tree.heading("Descripción", text="Descripción")
        tree.column("Descripción", width=650, anchor="center")
        tree.place(x=10, y=100)

    def configurar_clientes(self):
        # Crear formulario manualmente
        frame_formulario = ctk.CTkFrame(self.tab_clientes, width=1400, height=700)
        frame_formulario.place(x=10, y=10)

        # Etiquetas y entradas
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre:")
        label_nombre.place(x=20, y=20)
        entry_nombre = ctk.CTkEntry(frame_formulario)
        entry_nombre.place(x=150, y=20)

        label_correo = ctk.CTkLabel(frame_formulario, text="Email:")
        label_correo.place(x=320, y=20)
        entry_correo = ctk.CTkEntry(frame_formulario)
        entry_correo.place(x=420, y=20)

        boton_crear = ctk.CTkButton(frame_formulario, text="Agregar Cliente")
        boton_crear.place(x=10, y=80)

        boton_act = ctk.CTkButton(frame_formulario, text="Agregar Cliente")
        boton_act.place(x=200, y=80)

        boton_eliminar = ctk.CTkButton(frame_formulario, text="Agregar Cliente")
        boton_eliminar.place(x=390, y=80)

        # Crear treeview manualmente
        frame_treeview = ctk.CTkFrame((self.tab_clientes), width=1350, height=500)
        frame_treeview.place(x=10, y=150)

        tree = ttk.Treeview(frame_treeview, columns=["Email", "Nombre"], show="headings", height=30)
        tree.heading("Email", text="Email")
        tree.column("Email", width=650, anchor="center")
        tree.heading("Nombre", text="Nombre")
        tree.column("Nombre", width=650, anchor="center")
        tree.place(x=10, y=100)

    def configurar_compras(self):
        # Crear formulario manualmente
        frame_formulario = ctk.CTkFrame(self.tab_compras, width=1400, height=700)
        frame_formulario.place(x=10, y=10)

        label_menu = ctk.CTkLabel(frame_formulario, text="Menú:")
        label_menu.place(x=20, y=20)

        combo_menu = ctk.CTkComboBox(frame_formulario, values=[])
        combo_menu.place(x=80, y=20)

        boton_crear = ctk.CTkButton(frame_formulario, text="Agregar a la compra")
        boton_crear.place(x=280, y=20)

        # Crear treeview manualmente
        frame_treeview = ctk.CTkFrame((self.tab_compras), width=1350, height=500)
        frame_treeview.place(x=10, y=70)

        tree = ttk.Treeview(frame_treeview, columns=["Nombre", "Cantidad"], show="headings", height=30)
        tree.heading("Nombre", text="Nombre")
        tree.column("Nombre", width=650, anchor="center")
        tree.heading("Cantidad", text="Cantidad")
        tree.column("Cantidad", width=650, anchor="center")
        tree.place(x=10, y=70)

        boton_boleta = ctk.CTkButton(frame_formulario, text="Generar Boleta")
        boton_boleta.place(x=600, y=600)

    def configurar_pedidos(self):


        pass

    def configurar_graficos(self):
        # Configuración de gráficos
        label = ctk.CTkLabel(self.tab_graficos, text="Selecciona un tipo de gráfico:")
        label.place(x=20, y=20)

        combo = ttk.Combobox(self.tab_graficos, values=["Ventas Diarias", "Ventas Semanales", "Ingredientes Más Utilizados"])
        combo.place(x=20, y=60)
