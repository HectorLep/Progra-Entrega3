from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import ttk

class SistemaGestionRestaurante(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Restaurante")
        self.geometry("1400x800")

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
        # Etiqueta y entrada para Cantidad
        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.place(x=20, y=50)
        entry_cantidad = ctk.CTkEntry(frame_formulario)
        entry_cantidad.place(x=100, y=50)

        # Etiqueta y entrada para Unidad de Medida
        label_unidad = ctk.CTkLabel(frame_formulario, text="Unidad de Medida:")
        label_unidad.place(x=250, y=50)
        entry_unidad = ctk.CTkEntry(frame_formulario)
        entry_unidad.place(x=400, y=50)


        # Conectar botón con función
        boton_agregar = ctk.CTkButton(frame_formulario, text="Crear Ingrediente")
        boton_agregar.place(x=20, y=100)

        # Crear treeview manualmente
        frame_treeview = ctk.CTkFrame(self.tab_ingredientes, width=1350, height=500)
        frame_treeview.place(x=10, y=150)

        tree = ttk.Treeview(frame_treeview, columns=["Nombre", "Tipo", "Cantidad", "Unidad"], show="headings", height=30)
        tree.heading("Nombre", text="Nombre")
        tree.column("Nombre", width=325, anchor="center")
        tree.heading("Tipo", text="Tipo")
        tree.column("Tipo", width=325, anchor="center")
        tree.heading("Cantidad", text="Cantidad")
        tree.column("Cantidad", width=325, anchor="center")
        tree.heading("Unidad", text="Unidad")
        tree.column("Unidad", width=325, anchor="center")
        tree.place(x=10, y=100)


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

        boton_act = ctk.CTkButton(frame_formulario, text="Actualizar Cliente")
        boton_act.place(x=200, y=80)

        boton_eliminar = ctk.CTkButton(frame_formulario, text="Eliminar Cliente")
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
        combo_menu.place(x=70, y=20)

        label_clientes = ctk.CTkLabel(frame_formulario, text="Cliente:")
        label_clientes.place(x=250, y=20)

        combo_clientes = ctk.CTkComboBox(frame_formulario, values=[])
        combo_clientes.place(x=320, y=20)

        boton_crear = ctk.CTkButton(frame_formulario, text="Agregar a la compra")
        boton_crear.place(x=500, y=20)

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
        # Crear un frame para la lista de pedidos y opciones de organización
        frame_superior = ctk.CTkFrame(self.tab_pedidos, height=200)
        frame_superior.pack(side="top", fill="x", expand=False, padx=10, pady=10)

        # Etiqueta para el panel de pedidos
        label_panel = ctk.CTkLabel(frame_superior, text="Panel de Pedidos", font=("Arial", 16, "bold"))
        label_panel.pack(side="top", pady=5)

        # Combobox para seleccionar cliente
        label_cliente = ctk.CTkLabel(frame_superior, text="Seleccionar Cliente:")
        label_cliente.pack(side="left", padx=5)
        combobox_cliente = ttk.Combobox(frame_superior)
        combobox_cliente.pack(side="left", padx=5)

        # Crear botones para organizar la lista de pedidos
        boton_organizar_fecha = ctk.CTkButton(frame_superior, text="Ordenar por Fecha")
        boton_organizar_fecha.pack(side="left", padx=5)

        boton_organizar_cliente = ctk.CTkButton(frame_superior, text="Ordenar por Cliente")
        boton_organizar_cliente.pack(side="left", padx=5)

        # Crear un frame para mostrar la lista de pedidos
        frame_treeview = ctk.CTkFrame(self.tab_pedidos)
        frame_treeview.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Crear el Treeview para mostrar los pedidos
        tree = ttk.Treeview(frame_treeview, columns=("Cliente", "Fecha", "Total"), show="headings")
        tree.heading("Cliente", text="Cliente")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Total", text="Total")
        tree.pack(expand=True, fill="both")

        # Crear un frame inferior para el total y otras acciones
        frame_inferior = ctk.CTkFrame(self.tab_pedidos)
        frame_inferior.pack(side="bottom", fill="x", padx=10, pady=10)

        # Etiqueta para mostrar el total del pedido
        label_total = ctk.CTkLabel(frame_inferior, text="Total: 0 CLP", font=("Arial", 14))
        label_total.pack(side="left", padx=10)

        # Botón para confirmar la revisión
        boton_confirmar = ctk.CTkButton(frame_inferior, text="Confirmar Pedido")
        boton_confirmar.pack(side="right", padx=10)

    def configurar_graficos(self):
        # Configuración de gráficos
        label = ctk.CTkLabel(self.tab_graficos, text="Selecciona un tipo de gráfico:")
        label.place(x=20, y=20)

        combo = ttk.Combobox(self.tab_graficos, values=["Ventas Diarias", "Ventas Semanales", "Ventas Mensuales", "Ventas Anuales"])
        combo.place(x=20, y=60)
