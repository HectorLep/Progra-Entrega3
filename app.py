import customtkinter as ctk
from CRUD.cliente_crud import ClienteCRUD
from tkinter import ttk, messagebox
import sqlite3

class SistemaGestionRestaurante(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Restaurante")
        self.geometry("1400x800")
        self.resizable(False, False)
        # Initialize ClienteCRUD
        self.cliente_crud = ClienteCRUD()
        
        # Additional setup for clients tab
        self.setup_cliente_crud_events()
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
        # Create form frame
        self.frame_formulario = ctk.CTkFrame(self.tab_clientes, width=1400, height=700)
        self.frame_formulario.place(x=10, y=10)

        # Labels and entries
        self.label_nombre = ctk.CTkLabel(self.frame_formulario, text="Nombre:")
        self.label_nombre.place(x=20, y=20)
        self.entry_nombre = ctk.CTkEntry(self.frame_formulario, width=200)
        self.entry_nombre.place(x=150, y=20)

        self.label_correo = ctk.CTkLabel(self.frame_formulario, text="Email:")
        self.label_correo.place(x=320, y=20)
        self.entry_correo = ctk.CTkEntry(self.frame_formulario, width=200)
        self.entry_correo.place(x=420, y=20)

        # Buttons with event handling
        self.boton_crear = ctk.CTkButton(self.frame_formulario, text="Agregar Cliente", 
                                         command=self.agregar_cliente)
        self.boton_crear.place(x=10, y=80)

        self.boton_act = ctk.CTkButton(self.frame_formulario, text="Actualizar Cliente", 
                                       command=self.actualizar_cliente)
        self.boton_act.place(x=200, y=80)

        self.boton_eliminar = ctk.CTkButton(self.frame_formulario, text="Eliminar Cliente", 
                                            command=self.eliminar_cliente)
        self.boton_eliminar.place(x=390, y=80)

        # Create treeview
        self.frame_treeview = ctk.CTkFrame(self.tab_clientes, width=1350, height=500)
        self.frame_treeview.place(x=10, y=150)

        self.tree = ttk.Treeview(self.frame_treeview, columns=["ID", "Nombre", "Email"], show="headings", height=30)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("Nombre", width=400, anchor="center")
        self.tree.heading("Email", text="Email")
        self.tree.column("Email", width=400, anchor="center")
        self.tree.place(x=10, y=100)
        
        # Add event binding for row selection
        self.tree.bind('<ButtonRelease-1>', self.seleccionar_cliente)

        # Initial population of treeview
        self.actualizar_lista_clientes()

    def setup_cliente_crud_events(self):
        # Additional setup methods can be added here if needed
        pass

    def agregar_cliente(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        
        if not nombre or not correo:
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
        
        try:
            # Create client
            cliente_id = self.cliente_crud.crear_cliente(nombre, correo)
            messagebox.showinfo("Éxito", f"Cliente creado con ID: {cliente_id}")
            
            # Clear entries
            self.entry_nombre.delete(0, 'end')
            self.entry_correo.delete(0, 'end')
            
            # Refresh client list
            self.actualizar_lista_clientes()
        
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El correo electrónico ya existe")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_cliente(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un cliente para actualizar")
            return
        
        # Get current values
        cliente_id = self.tree.item(selected_item[0])['values'][0]
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        
        if not nombre and not correo:
            messagebox.showerror("Error", "Ingrese al menos un campo para actualizar")
            return
        
        try:
            # Update client
            self.cliente_crud.actualizar_cliente(cliente_id, nombre, correo)
            messagebox.showinfo("Éxito", "Cliente actualizado")
            
            # Clear entries
            self.entry_nombre.delete(0, 'end')
            self.entry_correo.delete(0, 'end')
            
            # Refresh client list
            self.actualizar_lista_clientes()
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_cliente(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
            return
        
        # Get client ID
        cliente_id = self.tree.item(selected_item[0])['values'][0]
        
        # Confirm deletion
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?")
        if respuesta:
            try:
                # Delete client
                self.cliente_crud.eliminar_cliente(cliente_id)
                messagebox.showinfo("Éxito", "Cliente eliminado")
                
                # Clear entries
                self.entry_nombre.delete(0, 'end')
                self.entry_correo.delete(0, 'end')
                
                # Refresh client list
                self.actualizar_lista_clientes()
            
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def actualizar_lista_clientes(self):
        # Clear existing items
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Fetch and populate clients
        clientes = self.cliente_crud.listar_clientes()
        for cliente in clientes:
            self.tree.insert('', 'end', values=cliente)

    def seleccionar_cliente(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            # Populate entries with selected client's details
            valores = self.tree.item(selected_item[0])['values']
            
            # Clear existing entries
            self.entry_nombre.delete(0, 'end')
            self.entry_correo.delete(0, 'end')
            
            # Insert selected client's details
            self.entry_nombre.insert(0, valores[1])  # Nombre
            self.entry_correo.insert(0, valores[2])  # Correo


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
