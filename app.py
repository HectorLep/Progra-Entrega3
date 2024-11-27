import customtkinter as ctk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CRUD.cliente_crud import ClienteCRUD
from CRUD.pedido_crud import PedidoCRUD
from CRUD.ingrediente_crud import IngredienteCRUD
from CRUD.menu_crud import MenuCRUD
from sqlalchemy.exc import SQLAlchemyError
import sqlite3

class SistemaGestionRestaurante(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Restaurante")
        self.geometry("1400x800")
        self.resizable(False, False)
        
        # Initialize CRUD classes
        self.cliente_crud = ClienteCRUD()
        self.pedido_crud = PedidoCRUD()
        self.ingrediente_crud = IngredienteCRUD()
        self.menu_crud = MenuCRUD()
                
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

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.place(x=20, y=50)
        self.entry_cantidad_ingrediente = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad_ingrediente.place(x=100, y=50)

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

    def agregar_ingrediente(self):
        try:
            # Obtener y validar datos
            nombre = self.entry_nombre_ingrediente.get().strip()
            tipo = self.entry_tipo_ingrediente.get().strip()
            cantidad_str = self.entry_cantidad_ingrediente.get().strip()
            unidad = self.entry_unidad_ingrediente.get().strip()
            
            # Validaciones específicas
            if not all([nombre, tipo, cantidad_str, unidad]):
                messagebox.showerror("Error", "Todos los campos son requeridos")
                return
            
            try:
                cantidad = int(cantidad_str)
                if cantidad < 0:
                    messagebox.showerror("Error", "La cantidad no puede ser negativa")
                    return
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número entero válido")
                return
            
            # Intentar crear el ingrediente
            ingrediente_id = self.ingrediente_crud.crear_ingrediente(
                nombre=nombre,
                tipo=tipo,
                cantidad=cantidad,
                unidad_medida=unidad
            )
            
            messagebox.showinfo("Éxito", f"Ingrediente creado con ID: {ingrediente_id}")
            self.limpiar_entradas_ingrediente()
            self.actualizar_lista_ingredientes()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except SQLAlchemyError as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo crear el ingrediente: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

            
    def actualizar_lista_ingredientes(self):
        # Limpiar treeview
        for item in self.tree_ingredientes.get_children():
            self.tree_ingredientes.delete(item)
        
        # Obtener y mostrar ingredientes
        try:
            ingredientes = self.ingrediente_crud.listar_ingredientes()
            for ingrediente in ingredientes:
                self.tree_ingredientes.insert('', 'end', values=(
                    ingrediente.id,
                    ingrediente.nombre,
                    ingrediente.tipo,
                    ingrediente.cantidad,
                    ingrediente.unidad_medida
                ))
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"Error al cargar ingredientes: {str(e)}")

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
            actualizado = self.ingrediente_crud.actualizar_ingrediente(
                ingrediente_id, nombre, tipo, cantidad, unidad
            )
            
            if actualizado:
                messagebox.showinfo("Éxito", "Ingrediente actualizado correctamente")
                self.limpiar_entradas_ingrediente()
                self.actualizar_lista_ingredientes()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el ingrediente")
        
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_ingrediente(self):
        selected_item = self.tree_ingredientes.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un ingrediente para eliminar")
            return
        
        ingrediente_id = self.tree_ingredientes.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este ingrediente?"):
            try:
                eliminado = self.ingrediente_crud.eliminar_ingrediente(ingrediente_id)
                if eliminado:
                    messagebox.showinfo("Éxito", "Ingrediente eliminado correctamente")
                    self.limpiar_entradas_ingrediente()
                    self.actualizar_lista_ingredientes()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el ingrediente")
            except SQLAlchemyError as e:
                messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def seleccionar_ingrediente(self, event):
        selected_item = self.tree_ingredientes.selection()
        if selected_item:
            valores = self.tree_ingredientes.item(selected_item[0])['values']
            self.limpiar_entradas_ingrediente()
            
            self.entry_nombre_ingrediente.insert(0, valores[1])
            self.entry_tipo_ingrediente.insert(0, valores[2])
            self.entry_cantidad_ingrediente.insert(0, str(valores[3]))
            self.entry_unidad_ingrediente.insert(0, valores[4])

    def limpiar_entradas_ingrediente(self):
        self.entry_nombre_ingrediente.delete(0, 'end')
        self.entry_tipo_ingrediente.delete(0, 'end')
        self.entry_cantidad_ingrediente.delete(0, 'end')
        self.entry_unidad_ingrediente.delete(0, 'end')

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

        # Entry for ingredient quantity in menu
        label_cantidad_ingrediente = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad_ingrediente.place(x=320, y=60)
        self.entry_cantidad_ingrediente_menu = ctk.CTkEntry(frame_formulario, width=100)
        self.entry_cantidad_ingrediente_menu.place(x=450, y=60)

        # Buttons
        boton_agregar = ctk.CTkButton(frame_formulario, text="Crear Menú")
        boton_agregar.place(x=20, y=250)

        boton_actualizar = ctk.CTkButton(frame_formulario, text="Actualizar Menú")
        boton_actualizar.place(x=200, y=250)

        boton_eliminar = ctk.CTkButton(frame_formulario, text="Eliminar Menú")
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
        self.boton_crear = ctk.CTkButton(self.frame_formulario, text="Agregar Cliente")
        self.boton_crear.place(x=10, y=80)

        self.boton_act = ctk.CTkButton(self.frame_formulario, text="Actualizar Cliente")
        self.boton_act.place(x=200, y=80)

        self.boton_eliminar = ctk.CTkButton(self.frame_formulario, text="Eliminar Cliente")
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

        boton_crear = ctk.CTkButton(frame_formulario, text="Agregar a la compra")
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

        # 1. Agregar un Label y Entry para la cantidad en el formulario
        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.place(x=500, y=20)

        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.place(x=610, y=20)

        boton_crear = ctk.CTkButton(frame_formulario, text="Agregar a la compra")
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
        self.boton_boleta = ctk.CTkButton(frame_formulario, text="Generar Boleta")
        self.boton_boleta.place(x=600, y=600)

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

        # Botón para filtrar por cliente
        boton_filtrar_cliente = ctk.CTkButton(frame_superior, text="Filtrar por Cliente")
        boton_filtrar_cliente.pack(side="left", padx=5)

        # Crear botones para organizar la lista de pedidos
        boton_organizar_fecha = ctk.CTkButton(frame_superior, text="Ordenar por Fecha")
        boton_organizar_fecha.pack(side="left", padx=5)

        boton_organizar_cliente = ctk.CTkButton(frame_superior, text="Ordenar por Cliente")
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

        # Crear un frame inferior para el total y otras acciones
        frame_inferior = ctk.CTkFrame(self.tab_pedidos)
        frame_inferior.pack(side="bottom", fill="x", padx=10, pady=10)

        # Etiqueta para mostrar el total del pedido
        self.label_total = ctk.CTkLabel(frame_inferior, text="Total: 0 CLP", font=("Arial", 14))
        self.label_total.pack(side="left", padx=10)

        # Botón para confirmar la revisión
        boton_confirmar = ctk.CTkButton(frame_inferior, text="Confirmar Pedido")
        boton_confirmar.pack(side="right", padx=10)

    def configurar_graficos(self):
        # Etiqueta y combobox
        label = ctk.CTkLabel(self.tab_graficos, text="Selecciona un tipo de gráfico:")
        label.place(x=20, y=20)

        self.combo_graficos = ttk.Combobox(
            self.tab_graficos,
            values=["Ventas Diarias", "Ventas Semanales", "Ventas Mensuales", "Ventas Anuales"],
            state="readonly"
        )
        self.combo_graficos.place(x=20, y=60)
        self.combo_graficos.bind("<<ComboboxSelected>>", self.actualizar_grafico)

        # Marco para el gráfico
        self.frame_grafico = ctk.CTkFrame(self.tab_graficos, width=1000, height=600)
        self.frame_grafico.place(x=20, y=100)

    def actualizar_grafico(self, event):
        # Limpiar cualquier gráfico anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Obtener la selección actual
        seleccion = self.combo_graficos.get()

        # Crear un nuevo gráfico según la selección
        fig, ax = plt.subplots(figsize=(8, 4))
        if seleccion == "Ventas Diarias":
            ax.plot(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], [200, 450, 300, 400, 600], label="Ventas")
            ax.set_title("Ventas Diarias")
            ax.set_xlabel("Días")
            ax.set_ylabel("Ventas (CLP)")
        elif seleccion == "Ventas Semanales":
            ax.bar(["Semana 1", "Semana 2", "Semana 3", "Semana 4"], [1500, 1800, 1700, 2000], color="blue")
            ax.set_title("Ventas Semanales")
            ax.set_xlabel("Semanas")
            ax.set_ylabel("Ventas (CLP)")
        elif seleccion == "Ventas Mensuales":
            ax.pie([20, 30, 25, 25], labels=["Producto A", "Producto B", "Producto C", "Producto D"], autopct="%1.1f%%")
            ax.set_title("Ventas Mensuales")
        elif seleccion == "Ventas Anuales":
            ax.plot(["Enero", "Febrero", "Marzo", "Abril", "Mayo"], [5000, 5200, 5100, 5300, 5400], label="Ventas")
            ax.set_title("Ventas Anuales")
            ax.set_xlabel("Meses")
            ax.set_ylabel("Ventas (CLP)")

        # Insertar gráfico en el frame
        canvas = FigureCanvasTkAgg(fig, self.frame_grafico)
        canvas.get_tk_widget().pack()
        canvas.draw()
