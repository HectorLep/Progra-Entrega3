import customtkinter as ctk
from CRUD.cliente_crud import ClienteCRUD
from CRUD.pedido_crud import PedidoCRUD
from CRUD.ingrediente_crud import IngredienteCRUD
from CRUD.menu_crud import MenuCRUD
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
        # Initialize PedidoCRUD
        self.pedido_crud = PedidoCRUD()
        # Additional setup for clients tab
        # Initialize IngredienteCRUD
        self.ingrediente_crud = IngredienteCRUD()
        # Initialize MenuCRUD
        self.menu_crud = MenuCRUD()
        self.setup_crud_events()
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
        self.entry_nombre_ingrediente = ctk.CTkEntry(frame_formulario)
        self.entry_nombre_ingrediente.place(x=100, y=20)

        label_tipo = ctk.CTkLabel(frame_formulario, text="Tipo:")
        label_tipo.place(x=250, y=20)
        self.entry_tipo_ingrediente = ctk.CTkEntry(frame_formulario)
        self.entry_tipo_ingrediente.place(x=330, y=20)

        # Etiqueta y entrada para Cantidad
        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.place(x=20, y=50)
        self.entry_cantidad_ingrediente = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad_ingrediente.place(x=100, y=50)

        # Etiqueta y entrada para Unidad de Medida
        label_unidad = ctk.CTkLabel(frame_formulario, text="Unidad de Medida:")
        label_unidad.place(x=250, y=50)
        self.entry_unidad_ingrediente = ctk.CTkEntry(frame_formulario)
        self.entry_unidad_ingrediente.place(x=400, y=50)

        # Botones de acción
        boton_agregar = ctk.CTkButton(frame_formulario, text="Crear Ingrediente", command=self.agregar_ingrediente)
        boton_agregar.place(x=20, y=100)

        boton_actualizar = ctk.CTkButton(frame_formulario, text="Actualizar Ingrediente", command=self.actualizar_ingrediente)
        boton_actualizar.place(x=200, y=100)

        boton_eliminar = ctk.CTkButton(frame_formulario, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        boton_eliminar.place(x=380, y=100)

        # Crear treeview manualmente
        frame_treeview = ctk.CTkFrame(self.tab_ingredientes, width=1350, height=500)
        frame_treeview.place(x=10, y=150)

        self.tree_ingredientes = ttk.Treeview(frame_treeview, columns=["ID", "Nombre", "Tipo", "Cantidad", "Unidad"], show="headings", height=30)
        self.tree_ingredientes.heading("ID", text="ID")
        self.tree_ingredientes.column("ID", width=50, anchor="center")
        self.tree_ingredientes.heading("Nombre", text="Nombre")
        self.tree_ingredientes.column("Nombre", width=300, anchor="center")
        self.tree_ingredientes.heading("Tipo", text="Tipo")
        self.tree_ingredientes.column("Tipo", width=250, anchor="center")
        self.tree_ingredientes.heading("Cantidad", text="Cantidad")
        self.tree_ingredientes.column("Cantidad", width=250, anchor="center")
        self.tree_ingredientes.heading("Unidad", text="Unidad")
        self.tree_ingredientes.column("Unidad", width=250, anchor="center")
        self.tree_ingredientes.place(x=10, y=10)

        # Enlazar evento de selección
        self.tree_ingredientes.bind('<ButtonRelease-1>', self.seleccionar_ingrediente)

        # Actualizar lista inicial
        self.actualizar_lista_ingredientes()

    def configurar_menus(self):
        # Frame for menu form
        frame_formulario = ctk.CTkFrame(self.tab_menus, width=1400, height=700)
        frame_formulario.place(x=10, y=10)

        # Labels and entries for menu details
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Menú:")
        label_nombre.place(x=20, y=20)
        self.entry_nombre_menu = ctk.CTkEntry(frame_formulario, width=200)
        self.entry_nombre_menu.place(x=150, y=20)

        label_descripcion = ctk.CTkLabel(frame_formulario, text="Descripción:")
        label_descripcion.place(x=320, y=20)
        self.entry_descripcion_menu = ctk.CTkEntry(frame_formulario, width=300)
        self.entry_descripcion_menu.place(x=450, y=20)

        # Ingredientes selection
        label_ingredientes = ctk.CTkLabel(frame_formulario, text="Ingredientes:")
        label_ingredientes.place(x=20, y=60)
        
        # Multiselect for ingredients
        self.lista_ingredientes = ttk.Treeview(frame_formulario, columns=["Ingrediente", "Cantidad"], show="headings", selectmode="extended", height=5)
        self.lista_ingredientes.heading("Ingrediente", text="Ingrediente")
        self.lista_ingredientes.heading("Cantidad", text="Cantidad")
        self.lista_ingredientes.place(x=20, y=90)

        # Populate ingredients from database
        ingredientes = self.ingrediente_crud.listar_ingredientes()
        for ingrediente in ingredientes:
            self.lista_ingredientes.insert('', 'end', values=(ingrediente[1], ingrediente[3]))

        # Entry for ingredient quantity in menu
        label_cantidad_ingrediente = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad_ingrediente.place(x=320, y=60)
        self.entry_cantidad_ingrediente_menu = ctk.CTkEntry(frame_formulario, width=100)
        self.entry_cantidad_ingrediente_menu.place(x=450, y=60)

        # Buttons
        boton_agregar = ctk.CTkButton(frame_formulario, text="Crear Menú", command=self.agregar_menu)
        boton_agregar.place(x=20, y=250)

        boton_actualizar = ctk.CTkButton(frame_formulario, text="Actualizar Menú", command=self.actualizar_menu)
        boton_actualizar.place(x=200, y=250)

        boton_eliminar = ctk.CTkButton(frame_formulario, text="Eliminar Menú", command=self.eliminar_menu)
        boton_eliminar.place(x=380, y=250)

        # Treeview for displaying menus
        frame_treeview = ctk.CTkFrame(self.tab_menus, width=1350, height=400)
        frame_treeview.place(x=10, y=300)

        self.tree_menus = ttk.Treeview(frame_treeview, columns=["Nombre", "Descripción", "Ingredientes"], show="headings", height=20)
        self.tree_menus.heading("Nombre", text="Nombre")
        self.tree_menus.column("Nombre", width=300, anchor="center")
        self.tree_menus.heading("Descripción", text="Descripción")
        self.tree_menus.column("Descripción", width=300, anchor="center")
        self.tree_menus.heading("Ingredientes", text="Ingredientes")
        self.tree_menus.column("Ingredientes", width=700, anchor="center")
        self.tree_menus.place(x=10, y=10)

        # Method to add methods for menu management
        self.actualizar_lista_menus()



    def actualizar_menu(self):
        selected_item = self.tree_menus.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un menú para actualizar")
            return
        
        nombre = self.entry_nombre_menu.get()
        descripcion = self.entry_descripcion_menu.get()
        
        # Obtener el menú seleccionado
        menu_nombre = self.tree_menus.item(selected_item[0])['values'][0]
        menu = self.menu_crud.obtener_menu_por_nombre(menu_nombre)
        
        if not menu:
            messagebox.showerror("Error", "Menú no encontrado")
            return
        
        # Collect selected ingredients with quantities
        ingredientes_menu = []
        for selected_ingrediente in self.lista_ingredientes.selection():
            ingrediente = self.lista_ingredientes.item(selected_ingrediente)['values']
            cantidad = self.entry_cantidad_ingrediente_menu.get()
            
            try:
                cantidad = float(cantidad)
                # Obtener el ID del ingrediente de la base de datos
                ingredientes = self.ingrediente_crud.listar_ingredientes()
                ingrediente_id = next(ing[0] for ing in ingredientes if ing[1] == ingrediente[0])
                ingredientes_menu.append((ingrediente_id, cantidad))
            except (ValueError, StopIteration):
                messagebox.showerror("Error", "Error al procesar ingredientes")
                return
        
        try:
            # Actualizar menú en la base de datos
            self.menu_crud.actualizar_menu(menu[0], nombre, descripcion, ingredientes_menu)
            messagebox.showinfo("Éxito", "Menú actualizado")
            
            # Limpiar entradas
            self.entry_nombre_menu.delete(0, 'end')
            self.entry_descripcion_menu.delete(0, 'end')
            self.entry_cantidad_ingrediente_menu.delete(0, 'end')
            
            # Actualizar lista de menús
            self.actualizar_lista_menus()
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_menu(self):
        selected_item = self.tree_menus.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un menú para eliminar")
            return
        
        # Obtener el menú seleccionado
        menu_nombre = self.tree_menus.item(selected_item[0])['values'][0]
        menu = self.menu_crud.obtener_menu_por_nombre(menu_nombre)
        
        if not menu:
            messagebox.showerror("Error", "Menú no encontrado")
            return
        
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este menú?")
        if respuesta:
            try:
                # Eliminar menú de la base de datos
                self.menu_crud.eliminar_menu(menu[0])
                messagebox.showinfo("Éxito", "Menú eliminado")
                
                # Limpiar entradas
                self.entry_nombre_menu.delete(0, 'end')
                self.entry_descripcion_menu.delete(0, 'end')
                self.entry_cantidad_ingrediente_menu.delete(0, 'end')
                
                # Actualizar lista de menús
                self.actualizar_lista_menus()
            except Exception as e:
                messagebox.showerror("Error", str(e))



    def agregar_menu(self):
        nombre = self.entry_nombre_menu.get()
        descripcion = self.entry_descripcion_menu.get()
        
        if not nombre or not descripcion:
            messagebox.showerror("Error", "Nombre y descripción son requeridos")
            return
        
        # Collect selected ingredients with quantities
        ingredientes_menu = []
        for selected_item in self.lista_ingredientes.selection():
            ingrediente = self.lista_ingredientes.item(selected_item)['values']
            cantidad = self.entry_cantidad_ingrediente_menu.get()
            
            try:
                cantidad = float(cantidad)
                # Obtener el ID del ingrediente de la base de datos
                ingredientes = self.ingrediente_crud.listar_ingredientes()
                ingrediente_id = next(ing[0] for ing in ingredientes if ing[1] == ingrediente[0])
                ingredientes_menu.append((ingrediente_id, cantidad))
            except (ValueError, StopIteration):
                messagebox.showerror("Error", "Error al procesar ingredientes")
                return
        
        if not ingredientes_menu:
            messagebox.showerror("Error", "Seleccione al menos un ingrediente")
            return
        
        try:
            # Crear menú en la base de datos
            menu_id = self.menu_crud.crear_menu(nombre, descripcion, ingredientes_menu)
            messagebox.showinfo("Éxito", f"Menú creado con ID: {menu_id}")
            
            # Limpiar entradas
            self.entry_nombre_menu.delete(0, 'end')
            self.entry_descripcion_menu.delete(0, 'end')
            self.entry_cantidad_ingrediente_menu.delete(0, 'end')
            
            # Actualizar lista de menús
            self.actualizar_lista_menus()
        
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El menú ya existe")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista_menus(self):
        # Limpiar elementos existentes
        for i in self.tree_menus.get_children():
            self.tree_menus.delete(i)
        
        # Obtener y poblar menús
        menus = self.menu_crud.listar_menus()
        for menu in menus:
            # Obtener ingredientes del menú
            ingredientes = self.menu_crud.obtener_ingredientes_menu(menu[0])
            ingredientes_str = ", ".join([f"{ing[1]} ({ing[2]})" for ing in ingredientes])
            
            # Insertar en el treeview
            self.tree_menus.insert('', 'end', values=(menu[1], menu[2], ingredientes_str))

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

    def setup_crud_events(self):
        # Este método se ejecutará durante la inicialización
        # Configurar valores de combos en la pestaña de Compras
        
        # Obtener clientes
        try:
            clientes = self.cliente_crud.listar_clientes()
            cliente_nombres = [cliente[1] for cliente in clientes]
            
            # Buscar el ComboBox de clientes en la pestaña de Compras
            # IMPORTANTE: Ajusta esto según cómo hayas definido el combo de clientes
            self.combo_clientes.configure(values=cliente_nombres)
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
        
        # Aquí podrías agregar lógica similar para menús si los tienes

    def agregar_ingrediente(self):
        nombre = self.entry_nombre_ingrediente.get()
        tipo = self.entry_tipo_ingrediente.get()
        cantidad = self.entry_cantidad_ingrediente.get()
        unidad = self.entry_unidad_ingrediente.get()
        
        if not nombre or not tipo or not cantidad or not unidad:
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
        
        try:
            cantidad = float(cantidad)
            ingrediente_id = self.ingrediente_crud.crear_ingrediente(nombre, tipo, cantidad, unidad)
            messagebox.showinfo("Éxito", f"Ingrediente creado con ID: {ingrediente_id}")
            
            # Limpiar entradas
            self.limpiar_entradas_ingrediente()
            
            # Actualizar lista
            self.actualizar_lista_ingredientes()
        
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El ingrediente ya existe")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_ingrediente(self):
        selected_item = self.tree_ingredientes.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un ingrediente para actualizar")
            return
        
        ingrediente_id = self.tree_ingredientes.item(selected_item[0])['values'][0]
        
        nombre = self.entry_nombre_ingrediente.get()
        tipo = self.entry_tipo_ingrediente.get()
        cantidad = self.entry_cantidad_ingrediente.get()
        unidad = self.entry_unidad_ingrediente.get()
        
        try:
            cantidad = float(cantidad) if cantidad else None
            self.ingrediente_crud.actualizar_ingrediente(ingrediente_id, nombre, tipo, cantidad, unidad)
            messagebox.showinfo("Éxito", "Ingrediente actualizado")
            
            # Limpiar entradas
            self.limpiar_entradas_ingrediente()
            
            # Actualizar lista
            self.actualizar_lista_ingredientes()
        
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_ingrediente(self):
        selected_item = self.tree_ingredientes.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un ingrediente para eliminar")
            return
        
        ingrediente_id = self.tree_ingredientes.item(selected_item[0])['values'][0]
        
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este ingrediente?")
        if respuesta:
            try:
                self.ingrediente_crud.eliminar_ingrediente(ingrediente_id)
                messagebox.showinfo("Éxito", "Ingrediente eliminado")
                
                # Limpiar entradas
                self.limpiar_entradas_ingrediente()
                
                # Actualizar lista
                self.actualizar_lista_ingredientes()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def seleccionar_ingrediente(self, event):
        selected_item = self.tree_ingredientes.selection()
        if selected_item:
            valores = self.tree_ingredientes.item(selected_item[0])['values']
            
            # Limpiar entradas
            self.limpiar_entradas_ingrediente()
            
            # Insertar detalles del ingrediente seleccionado
            self.entry_nombre_ingrediente.insert(0, valores[1])
            self.entry_tipo_ingrediente.insert(0, valores[2])
            self.entry_cantidad_ingrediente.insert(0, str(valores[3]))
            self.entry_unidad_ingrediente.insert(0, valores[4])

    def actualizar_lista_ingredientes(self):
        # Limpiar elementos existentes
        for i in self.tree_ingredientes.get_children():
            self.tree_ingredientes.delete(i)
        
        # Obtener y poblar ingredientes
        ingredientes = self.ingrediente_crud.listar_ingredientes()
        for ingrediente in ingredientes:
            self.tree_ingredientes.insert('', 'end', values=ingrediente)

    def limpiar_entradas_ingrediente(self):
        # Limpiar todas las entradas de ingredientes
        self.entry_nombre_ingrediente.delete(0, 'end')
        self.entry_tipo_ingrediente.delete(0, 'end')
        self.entry_cantidad_ingrediente.delete(0, 'end')
        self.entry_unidad_ingrediente.delete(0, 'end')


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

        self.combo_menu = ctk.CTkComboBox(frame_formulario, values=[])
        self.combo_menu.place(x=70, y=20)

        label_clientes = ctk.CTkLabel(frame_formulario, text="Cliente:")
        label_clientes.place(x=250, y=20)

        self.combo_clientes = ctk.CTkComboBox(frame_formulario, values=[])
        self.combo_clientes.place(x=320, y=20)

        boton_crear = ctk.CTkButton(frame_formulario, text="Agregar a la compra", 
                                command=lambda: [self.debug_pedido(), self.agregar_a_compra()])
        boton_crear.place(x=500, y=20)

    def configurar_compras(self):
        # Primero inicializamos los atributos de la clase
        self.combo_clientes = None
        self.combo_menu = None
        self.tree_compras = None

        # Crear formulario manualmente
        frame_formulario = ctk.CTkFrame(self.tab_compras, width=1400, height=700)
        frame_formulario.place(x=10, y=10)

        label_menu = ctk.CTkLabel(frame_formulario, text="Menú:")
        label_menu.place(x=20, y=20)

        # Inicializar combo_menu
        self.combo_menu = ctk.CTkComboBox(frame_formulario, values=[])
        self.combo_menu.place(x=70, y=20)

        label_clientes = ctk.CTkLabel(frame_formulario, text="Cliente:")
        label_clientes.place(x=250, y=20)

        # Inicializar combo_clientes
        self.combo_clientes = ctk.CTkComboBox(frame_formulario, values=[])
        self.combo_clientes.place(x=320, y=20)

        # Cargar los datos en los combos
        self.cargar_combos_compras()

        # 1. Agregar un Label y Entry para la cantidad en el formulario
        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.place(x=500, y=20)

        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.place(x=610, y=20)

        boton_crear = ctk.CTkButton(frame_formulario, text="Agregar a la compra", command=self.agregar_a_compra)
        boton_crear.place(x=800, y=20)

        # Crear frame para el treeview
        self.frame_treeview = ctk.CTkFrame(self.tab_compras, width=1350, height=500)
        self.frame_treeview.place(x=10, y=70)

        # Inicializar tree_compras
        self.tree_compras = ttk.Treeview(self.frame_treeview, columns=("Nombre", "Cantidad", "Precio"), show="headings", height=30)
        self.tree_compras.heading("Nombre", text="Nombre")
        self.tree_compras.column("Nombre", width=450, anchor="center")
        self.tree_compras.heading("Cantidad", text="Cantidad")
        self.tree_compras.column("Cantidad", width=450, anchor="center")
        self.tree_compras.heading("Precio", text="Precio")
        self.tree_compras.column("Precio", width=450, anchor="center")
        self.tree_compras.place(x=10, y=10)

        # Botón de generar boleta
        self.boton_boleta = ctk.CTkButton(frame_formulario, text="Generar Boleta", command=self.generar_boleta)
        self.boton_boleta.place(x=600, y=600)
            
    def cargar_combos_compras(self):
        try:
            if hasattr(self, 'combo_clientes') and self.combo_clientes is not None:
                # Cargar clientes
                clientes = self.cliente_crud.listar_clientes()
                cliente_nombres = [cliente[1] for cliente in clientes]
                self.combo_clientes.configure(values=cliente_nombres)
                if cliente_nombres:
                    self.combo_clientes.set(cliente_nombres[0])

            if hasattr(self, 'combo_menu') and self.combo_menu is not None:
                # Cargar menús
                menus = self.menu_crud.listar_menus()
                menu_nombres = [menu[1] for menu in menus]
                self.combo_menu.configure(values=menu_nombres)
                if menu_nombres:
                    self.combo_menu.set(menu_nombres[0])

        except Exception as e:
            print(f"Error al cargar combos: {str(e)}")
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")
                
    # 2. Modificar el método agregar_a_compra para obtener la cantidad
    def agregar_a_compra(self):
        cliente_seleccionado = self.combo_clientes.get()
        menu_seleccionado = self.combo_menu.get()
        cantidad = self.entry_cantidad.get()

        # Validar que la cantidad sea un número y mayor que 0
        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Cantidad no válida")
            return
        
        cantidad = int(cantidad)  # Convertir cantidad a entero

        print(f"[DEBUG] Cliente seleccionado: {cliente_seleccionado}")
        print(f"[DEBUG] Menú seleccionado: {menu_seleccionado}")
        print(f"[DEBUG] Cantidad: {cantidad}")

        if not cliente_seleccionado or not menu_seleccionado:
            messagebox.showerror("Error", "Seleccione cliente y menú")
            print("[DEBUG] Error: Cliente o menú no seleccionados")
            return

        try:
            # Obtener IDs de cliente y menú
            cliente = self.cliente_crud.obtener_cliente_por_nombre(cliente_seleccionado)
            menu = self.menu_crud.obtener_menu_por_nombre(menu_seleccionado)

            print(f"[DEBUG] Cliente obtenido: {cliente}")
            print(f"[DEBUG] Menú obtenido: {menu}")

            if not cliente or not menu:
                messagebox.showerror("Error", "Cliente o menú no encontrado")
                print("[DEBUG] Error: Cliente o menú no encontrados en la base de datos")
                return

            cliente_id = cliente[0]
            menu_id = menu[0]

            # Obtener ingredientes del menú
            ingredientes_menu = self.menu_crud.obtener_ingredientes_menu(menu_id)
            print(f"[DEBUG] Ingredientes del menú: {ingredientes_menu}")

            # Calcular total del pedido usando el precio del menú
            total = menu[3] * cantidad  # Precio del menú multiplicado por la cantidad
            print(f"[DEBUG] Total del pedido calculado: {total}")

            # Crear pedido en la base de datos
            pedido_id = self.pedido_crud.crear_pedido(cliente_id, menu_id, total)
            print(f"[DEBUG] Pedido creado con ID: {pedido_id}")

            # Agregar al treeview con la cantidad
            self.tree_compras.insert('', 'end', values=(menu[1], cantidad, menu[3]))

            messagebox.showinfo("Éxito", f"Pedido {pedido_id} creado")

        except Exception as e:
            error_message = str(e)
            print(f"[DEBUG] Error inesperado: {error_message}")
            messagebox.showerror("Error", error_message)

    def generar_boleta(self):
        # Implementar generación de boleta
        messagebox.showinfo("Boleta", "Función de generación de boleta pendiente")


    def configurar_pedidos(self):

        # Inicializar atributos de clase
        self.label_total = None
        self.tree_pedidos = None
        self.combobox_cliente = None

        # Crear un frame para la lista de pedidos y opciones de organización
        frame_superior = ctk.CTkFrame(self.tab_pedidos, height=200)
        frame_superior.pack(side="top", fill="x", expand=False, padx=10, pady=10)

        # Combobox para seleccionar cliente
        label_cliente = ctk.CTkLabel(frame_superior, text="Seleccionar Cliente:")
        label_cliente.pack(side="left", padx=5)
        
        # Populate clients ComboBox
        self.combobox_cliente = ctk.CTkComboBox(frame_superior, values=[])
        self.combobox_cliente.pack(side="left", padx=5)

        # Cargar clientes al inicializar
        self.cargar_clientes_pedidos()

        # Botón para filtrar por cliente
        boton_filtrar_cliente = ctk.CTkButton(frame_superior, text="Filtrar por Cliente", command=self.filtrar_pedidos_por_cliente)
        boton_filtrar_cliente.pack(side="left", padx=5)

        # Crear botones para organizar la lista de pedidos
        boton_organizar_fecha = ctk.CTkButton(frame_superior, text="Ordenar por Fecha", command=self.ordenar_pedidos_por_fecha)
        boton_organizar_fecha.pack(side="left", padx=5)

        boton_organizar_cliente = ctk.CTkButton(frame_superior, text="Ordenar por Cliente", command=self.ordenar_pedidos_por_cliente)
        boton_organizar_cliente.pack(side="left", padx=5)

        # Crear un frame para mostrar la lista de pedidos
        frame_treeview = ctk.CTkFrame(self.tab_pedidos)
        frame_treeview.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Crear el Treeview para mostrar los pedidos
        self.tree_pedidos = ttk.Treeview(frame_treeview, columns=("ID", "Cliente", "Fecha", "Total"), show="headings")
        self.tree_pedidos.heading("ID", text="ID Pedido")
        self.tree_pedidos.heading("Cliente", text="Cliente")
        self.tree_pedidos.heading("Fecha", text="Fecha")
        self.tree_pedidos.heading("Total", text="Total")
        self.tree_pedidos.pack(expand=True, fill="both")

        # Cargar pedidos inicialmente
        self.cargar_pedidos()

        # Crear un frame inferior para el total y otras acciones
        frame_inferior = ctk.CTkFrame(self.tab_pedidos)
        frame_inferior.pack(side="bottom", fill="x", padx=10, pady=10)

        # Etiqueta para mostrar el total del pedido
        self.label_total = ctk.CTkLabel(frame_inferior, text="Total: 0 CLP", font=("Arial", 14))
        self.label_total.pack(side="left", padx=10)

        # Botón para confirmar la revisión
        boton_confirmar = ctk.CTkButton(frame_inferior, text="Confirmar Pedido", command=self.confirmar_pedido)
        boton_confirmar.pack(side="right", padx=10)

    def cargar_clientes_pedidos(self):
        try:
            # Cargar clientes
            clientes = self.cliente_crud.listar_clientes()
            cliente_nombres = [cliente[1] for cliente in clientes]
            self.combobox_cliente.configure(values=cliente_nombres)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los clientes: {e}")

    def cargar_pedidos(self):
        try:
            # Obtener todos los pedidos con información de cliente
            pedidos = self.pedido_crud.listar_pedidos_con_cliente()
            
            # Limpiar treeview existente
            for i in self.tree_pedidos.get_children():
                self.tree_pedidos.delete(i)
            
            # Insertar pedidos en el treeview
            total_pedidos = 0
            for pedido in pedidos:
                total_pedidos += pedido[3]
                self.tree_pedidos.insert('', 'end', values=(pedido[0], pedido[1], pedido[2], pedido[3]))
            
            # Actualizar etiqueta de total
            self.label_total.configure(text=f"Total: {total_pedidos} CLP")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los pedidos: {e}")
            
    def filtrar_pedidos_por_cliente(self):
        cliente_seleccionado = self.combobox_cliente.get()
        
        if not cliente_seleccionado:
            self.cargar_pedidos()
            return
        
        try:
            # Obtener pedidos del cliente seleccionado
            pedidos = self.pedido_crud.listar_pedidos_por_cliente(cliente_seleccionado)
            
            # Limpiar treeview existente
            for i in self.tree_pedidos.get_children():
                self.tree_pedidos.delete(i)
            
            # Insertar pedidos en el treeview
            total_pedidos = 0
            for pedido in pedidos:
                total_pedidos += pedido[3]
                self.tree_pedidos.insert('', 'end', values=(pedido[0], pedido[1], pedido[2], pedido[3]))
            
            # Actualizar etiqueta de total
            self.label_total.configure(text=f"Total: {total_pedidos} CLP")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron filtrar los pedidos: {e}")

    def ordenar_pedidos_por_fecha(self):
        # Lógica para ordenar pedidos por fecha
        messagebox.showinfo("Ordenar", "Función de ordenamiento por fecha pendiente")

    def ordenar_pedidos_por_cliente(self):
        # Lógica para ordenar pedidos por cliente
        messagebox.showinfo("Ordenar", "Función de ordenamiento por cliente pendiente")

    def confirmar_pedido(self):
        # Lógica para confirmar pedido
        messagebox.showinfo("Confirmar", "Función de confirmación de pedido pendiente")
        
    def configurar_graficos(self):
        # Configuración de gráficos
        label = ctk.CTkLabel(self.tab_graficos, text="Selecciona un tipo de gráfico:")
        label.place(x=20, y=20)

        combo = ttk.Combobox(self.tab_graficos, values=["Ventas Diarias", "Ventas Semanales", "Ventas Mensuales", "Ventas Anuales"])
        combo.place(x=20, y=60)

    def debug_pedido(self):
        print("\n=== Debug Información ===")
        print(f"Cliente seleccionado: {self.combo_clientes.get()}")
        print(f"Menú seleccionado: {self.combo_menu.get()}")
        print("\nClientes disponibles:")
        clientes = self.cliente_crud.listar_clientes()
        for cliente in clientes:
            print(f"ID: {cliente[0]}, Nombre: {cliente[1]}")
        print("\nMenús disponibles:")
        menus = self.menu_crud.listar_menus()
        for menu in menus:
            print(f"ID: {menu[0]}, Nombre: {menu[1]}")  