import customtkinter as ctk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CRUD.cliente_crud import ClienteCRUD
from CRUD.pedido_crud import PedidoCRUD
from CRUD.ingrediente_crud import IngredienteCRUD
from CRUD.menu_crud import MenuCRUD
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from models import Menu  # Add this import
from graficos import GraficosVentas, GraficoMenusMasComprados, GraficoUsoIngredientes

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

        # Cargar ingredientes iniciales
        self.cargar_ingredientes_en_treeview()
        self.cargar_menus_en_treeview()
        self.obtener_nombres_clientes()
        self.obtener_nombres_menus()
        self.cargar_ingredientes_en_lista_menus()

    def crear_pestanas(self):
        # Crear las pestañas
        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.tab_menus = self.tabview.add("Menús")
        self.tab_clientes = self.tabview.add("Clientes")
        self.tab_compras = self.tabview.add("Panel de Compra")
        self.tab_pedidos = self.tabview.add("Pedidos")
        self.tab_graficos_ventas = self.tabview.add("Graficos Ventas")
        self.tab_graficos_menus = self.tabview.add("Grafico Menús más comprados")
        self.tab_graficos_ingredientes = self.tabview.add("Grafico Ingredientes")

        # Configurar cada pestaña
        self.configurar_ingredientes()
        self.configurar_menus()
        self.configurar_clientes()
        self.configurar_compras()
        self.configurar_pedidos()
        self.configurar_graficos()

    def configurar_graficos(self):
        self.grafico1 = GraficosVentas(self.tab_graficos_ventas)
        self.grafico2 = GraficoMenusMasComprados(self.tab_graficos_menus)
        self.grafico3 = GraficoUsoIngredientes(self.tab_graficos_ingredientes)

    def configurar_ingredientes(self):
        # Crear formulario manualmente
        frame_formulario = ctk.CTkFrame(self.tab_ingredientes, width=1400, height=700)
        frame_formulario.place(x=10, y=10)

        # Etiquetas y entradas
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre:")
        label_nombre.place(x=20, y=20)
        self.entry_nombre_ingrediente = ctk.CTkEntry(frame_formulario, width=200)
        self.entry_nombre_ingrediente.place(x=100, y=20)

        label_tipo = ctk.CTkLabel(frame_formulario, text="Tipo:")
        label_tipo.place(x=350, y=20)
        
        # Dropdown para tipos de ingredientes
        tipos_ingredientes = ["Verdura", "Fruta", "Carne", "Lácteo", "Grano", "Otro"]
        self.entry_tipo_ingrediente = ctk.CTkOptionMenu(frame_formulario, values=tipos_ingredientes)
        self.entry_tipo_ingrediente.place(x=420, y=20)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.place(x=20, y=50)
        self.entry_cantidad_ingrediente = ctk.CTkEntry(frame_formulario, width=100)
        self.entry_cantidad_ingrediente.place(x=100, y=50)

        label_unidad = ctk.CTkLabel(frame_formulario, text="Unidad de Medida:")
        label_unidad.place(x=250, y=50)
        unidades_medida = ["Unidades", "Kilogramos", "Gramos", "Litros", "Mililitros"]
        self.entry_unidad_ingrediente = ctk.CTkOptionMenu(frame_formulario, values=unidades_medida)
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
        frame_treeview.place(x=10, y=200)

        self.tree_ingredientes = ttk.Treeview(frame_treeview, columns=["ID", "Nombre", "Tipo", "Cantidad", "Unidad"], show="headings", height=20)
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

        # Bind de eventos para seleccionar un ingrediente
        self.tree_ingredientes.bind('<ButtonRelease-1>', self.seleccionar_ingrediente)

    def agregar_ingrediente(self):
        # Validar campos
        nombre = self.entry_nombre_ingrediente.get().strip()
        tipo = self.entry_tipo_ingrediente.get()
        
        try:
            cantidad = float(self.entry_cantidad_ingrediente.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido.")
            return
        
        unidad = self.entry_unidad_ingrediente.get()

        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre del ingrediente no puede estar vacío.")
            return

        # Verificar si ya existe un ingrediente con ese nombre
        ingrediente_existente = self.ingrediente_crud.obtener_ingrediente_por_nombre(nombre)
        if ingrediente_existente:
            messagebox.showerror("Error", f"Ya existe un ingrediente con el nombre '{nombre}'.")
            return

        # Intentar crear ingrediente
        try:
            nuevo_id = self.ingrediente_crud.crear_ingrediente(nombre, tipo, cantidad, unidad)
            if nuevo_id:
                messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' creado con ID {nuevo_id}")
                self.cargar_ingredientes_en_lista_menus()
                # Limpiar campos
                self.entry_nombre_ingrediente.delete(0, 'end')
                self.entry_cantidad_ingrediente.delete(0, 'end')
                
                # Recargar lista de ingredientes
                self.cargar_ingredientes_en_treeview()
            else:
                messagebox.showerror("Error", "No se pudo crear el ingrediente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def cargar_ingredientes_en_treeview(self):
        # Limpiar treeview actual
        for item in self.tree_ingredientes.get_children():
            self.tree_ingredientes.delete(item)
        
        # Obtener todos los ingredientes
        ingredientes = self.ingrediente_crud.listar_ingredientes()
        
        # Insertar ingredientes en el treeview
        for ingrediente in ingredientes:
            self.tree_ingredientes.insert("", "end", values=(
                ingrediente.id, 
                ingrediente.nombre, 
                ingrediente.tipo, 
                ingrediente.cantidad, 
                ingrediente.unidad_medida
            ))

    def seleccionar_ingrediente(self, event):
        # Obtener el ingrediente seleccionado en el treeview
        seleccion = self.tree_ingredientes.selection()
        if not seleccion:
            return
        
        # Obtener valores del ingrediente seleccionado
        valores = self.tree_ingredientes.item(seleccion[0])['values']
        
        # Llenar los campos del formulario
        self.entry_nombre_ingrediente.delete(0, 'end')
        self.entry_nombre_ingrediente.insert(0, valores[1])
        
        self.entry_tipo_ingrediente.set(valores[2])
        
        self.entry_cantidad_ingrediente.delete(0, 'end')
        self.entry_cantidad_ingrediente.insert(0, str(valores[3]))
        
        self.entry_unidad_ingrediente.set(valores[4])

    def actualizar_ingrediente(self):
        # Validar selección
        seleccion = self.tree_ingredientes.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un ingrediente para actualizar.")
            return

        # Obtener ID del ingrediente seleccionado
        id_ingrediente = self.tree_ingredientes.item(seleccion[0])['values'][0]
        
        # Validar campos
        nombre = self.entry_nombre_ingrediente.get().strip()
        tipo = self.entry_tipo_ingrediente.get()
        
        try:
            cantidad = float(self.entry_cantidad_ingrediente.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido.")
            return
        
        unidad = self.entry_unidad_ingrediente.get()

        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre del ingrediente no puede estar vacío.")
            return

        # Intentar actualizar ingrediente
        try:
            resultado = self.ingrediente_crud.actualizar_ingrediente(
                id=id_ingrediente, 
                nombre=nombre, 
                tipo=tipo, 
                cantidad=cantidad, 
                unidad_medida=unidad
            )
            
            if resultado:
                messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' actualizado correctamente")
                self.cargar_ingredientes_en_lista_menus()
                # Recargar lista de ingredientes
                self.cargar_ingredientes_en_treeview()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el ingrediente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def eliminar_ingrediente(self):
        # Validar selección
        seleccion = self.tree_ingredientes.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un ingrediente para eliminar.")
            return

        # Obtener ID y nombre del ingrediente seleccionado
        id_ingrediente = self.tree_ingredientes.item(seleccion[0])['values'][0]
        nombre_ingrediente = self.tree_ingredientes.item(seleccion[0])['values'][1]

        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el ingrediente '{nombre_ingrediente}'?")
        
        if confirmacion:
            try:
                resultado = self.ingrediente_crud.eliminar_ingrediente(id_ingrediente)
                
                if resultado:
                    messagebox.showinfo("Éxito", f"Ingrediente '{nombre_ingrediente}' eliminado correctamente")
                    self.cargar_ingredientes_en_lista_menus()
                    # Limpiar campos
                    self.entry_nombre_ingrediente.delete(0, 'end')
                    self.entry_cantidad_ingrediente.delete(0, 'end')
                    
                    # Recargar lista de ingredientes
                    self.cargar_ingredientes_en_treeview()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el ingrediente.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
   
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
        label_descripcion.place(x=380, y=20)
        self.entry_descripcion_menu = ctk.CTkEntry(frame_formulario, width=300)
        self.entry_descripcion_menu.place(x=480, y=20)
        
        # Agregar después del entry de descripción en configurar_menus()
        label_precio = ctk.CTkLabel(frame_formulario, text="Precio:")
        label_precio.place(x=850, y=20)
        self.entry_precio_menu = ctk.CTkEntry(frame_formulario, width=100)
        self.entry_precio_menu.place(x=915, y=20)

        # Ingredientes selection
        label_ingredientes = ctk.CTkLabel(frame_formulario, text="Ingredientes:")
        label_ingredientes.place(x=20, y=60)
        
        # Multiselect for ingredients
        self.lista_ingredientes = ttk.Treeview(frame_formulario, columns=["Ingrediente", "Cantidad"], show="headings", selectmode="extended", height=5)
        self.lista_ingredientes.heading("Ingrediente", text="Ingrediente")
        self.lista_ingredientes.heading("Cantidad", text="Cantidad")
        self.lista_ingredientes.place(x=20, y=90)

        # Entry for ingredient quantity in menu
        label_cantidad_ingrediente = ctk.CTkLabel(frame_formulario, text="Cant. ingr. :")
        label_cantidad_ingrediente.place(x=360, y=60)
        self.entry_cantidad_ingrediente_menu = ctk.CTkEntry(frame_formulario, width=100)
        self.entry_cantidad_ingrediente_menu.place(x=450, y=60)

        # Agregar label y entry para cantidad de ingredientes
        label_cant_ingredientes = ctk.CTkLabel(frame_formulario, text="stock de menus:")
        label_cant_ingredientes.place(x=600, y=60)
        self.entry_cant_ingredientes_menu = ctk.CTkEntry(frame_formulario, width=100)
        self.entry_cant_ingredientes_menu.place(x=750, y=60)

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

        self.tree_menus = ttk.Treeview(frame_treeview, columns=["Nombre", "Descripción", "Ingredientes", "Precio", "Cantidad"], show="headings", height=20)
        self.tree_menus.heading("Nombre", text="Nombre")
        self.tree_menus.column("Nombre", width=200, anchor="center")
        self.tree_menus.heading("Descripción", text="Descripción")
        self.tree_menus.column("Descripción", width=200, anchor="center")
        self.tree_menus.heading("Ingredientes", text="Ingredientes")
        self.tree_menus.column("Ingredientes", width=300, anchor="center")
        self.tree_menus.heading("Precio", text="Precio")
        self.tree_menus.column("Precio", width=100, anchor="center")
        self.tree_menus.heading("Cantidad", text="Cantidad")
        self.tree_menus.column("Cantidad", width=100, anchor="center")
        self.tree_menus.place(x=10, y=10)
        # Agregar estas líneas al final del método para cargar ingredientes
        self.cargar_ingredientes_en_lista_menus()

    def cargar_ingredientes_en_lista_menus(self):
        # Limpiar lista actual
        for item in self.lista_ingredientes.get_children():
            self.lista_ingredientes.delete(item)
        
        # Obtener todos los ingredientes
        ingredientes = self.ingrediente_crud.listar_ingredientes()
        
        # Insertar ingredientes en la lista
        for ingrediente in ingredientes:
            self.lista_ingredientes.insert("", "end", values=(
                ingrediente.nombre, 
                ingrediente.cantidad
            ))

    def agregar_menu(self):
        nombre = self.entry_nombre_menu.get().strip()
        descripcion = self.entry_descripcion_menu.get().strip()
        precio_str = self.entry_precio_menu.get().strip()
        
        # Validar precio
        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido")
            return        
        
        # Validar cantidad de menú
        try:
            cantidad_menu = int(self.entry_cant_ingredientes_menu.get().strip())
        except ValueError:
            messagebox.showerror("Error", "La cantidad de menú debe ser un número válido")
            return
        
        # Validar selección de ingredientes
        ingredientes_seleccionados = self.lista_ingredientes.selection()
        if not ingredientes_seleccionados:
            messagebox.showerror("Error", "Debe seleccionar al menos un ingrediente")
            return
        
        # Lista para guardar ingredientes del menú
        ingredientes_menu = []
        
        # Validar y procesar ingredientes
        for seleccion in ingredientes_seleccionados:
            ingrediente = self.lista_ingredientes.item(seleccion)['values'][0]
            
            # Obtener cantidad de ingrediente del entry
            cantidad_ingrediente_str = self.entry_cantidad_ingrediente_menu.get().strip()
            
            try:
                cantidad_ingrediente = float(cantidad_ingrediente_str)
            except ValueError:
                messagebox.showerror("Error", "La cantidad de ingrediente debe ser un número válido")
                return
            
            # Obtener el ingrediente de la base de datos
            ingrediente_obj = self.ingrediente_crud.obtener_ingrediente_por_nombre(ingrediente)
            if ingrediente_obj:
                # Calcular cantidad total a descontar
                cantidad_total = cantidad_menu * cantidad_ingrediente
                
                # Verificar si hay suficiente cantidad
                if ingrediente_obj.cantidad < cantidad_total:
                    messagebox.showerror("Error", f"No hay suficiente {ingrediente} en inventario")
                    return
                
                ingredientes_menu.append((ingrediente_obj.id, cantidad_ingrediente))
            
        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre del menú no puede estar vacío")
            return
        
        # Verificar si ya existe un menú con ese nombre
        menu_existente = self.menu_crud.obtener_menu_por_nombre(nombre)
        if menu_existente:
            messagebox.showerror("Error", f"Ya existe un menú con el nombre '{nombre}'")
            return
                
        try:
            # Crear menú con la cantidad de menú específica
            nuevo_id = self.menu_crud.crear_menu(
                nombre, 
                descripcion, 
                precio, 
                ingredientes_menu, 
                cantidad_menu  # Pasar cantidad de menú como un parámetro adicional
            )
            
            if nuevo_id:
                # Descontar ingredientes
                for ingrediente_id, cantidad_ingrediente in ingredientes_menu:
                    ingrediente = self.ingrediente_crud.obtener_ingrediente(ingrediente_id)
                    if ingrediente:
                        # Calcular cantidad total a descontar
                        cantidad_total = cantidad_menu * cantidad_ingrediente
                        
                        # Restar la cantidad usada del ingrediente
                        nueva_cantidad = ingrediente.cantidad - cantidad_total
                        self.ingrediente_crud.actualizar_ingrediente(
                            id=ingrediente_id, 
                            nombre=ingrediente.nombre, 
                            tipo=ingrediente.tipo, 
                            cantidad=nueva_cantidad, 
                            unidad_medida=ingrediente.unidad_medida
                        )
                
                messagebox.showinfo("Éxito", f"Menú '{nombre}' creado con ID {nuevo_id}")
                # Recargar lista de ingredientes después de descontar
                self.cargar_ingredientes_en_lista_menus()
                self.cargar_ingredientes_en_treeview()
                self.cargar_menus_en_treeview()
                self.obtener_nombres_menus()
                
                # Limpiar campos
                self.entry_nombre_menu.delete(0, 'end')
                self.entry_descripcion_menu.delete(0, 'end')
                self.entry_cantidad_ingrediente_menu.delete(0, 'end')
                self.entry_precio_menu.delete(0, 'end')
                self.entry_cant_ingredientes_menu.delete(0, 'end')
            else:
                messagebox.showerror("Error", "No se pudo crear el menú")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
                
    def cargar_menus_en_treeview(self):
        # Limpiar treeview actual
        for item in self.tree_menus.get_children():
            self.tree_menus.delete(item)
        
        # Obtener todos los menús
        menus = self.menu_crud.listar_menus()
        
        # Insertar menús en el treeview
        for menu in menus:
            # Formatear ingredientes
            ingredientes_str = ", ".join([
                f"{ing['nombre']} ({ing['cantidad_requerida']} {ing['unidad_medida']})" 
                for ing in menu['ingredientes']
            ])
            
            # Use 0 as default if 'cantidad' is not in the dictionary
            cantidad = menu.get('cantidad', 0)
            
            self.tree_menus.insert("", "end", values=(
                menu['nombre'],  # Nombre
                menu['descripcion'],  # Descripción
                ingredientes_str,
                menu['precio'],  # Precio
                cantidad  # Cantidad, defaulting to 0 if not present
            ))

    def actualizar_menu(self):
        # Validar selección
        seleccion = self.tree_menus.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un menú para actualizar")
            return
        
        # Obtener nombre del menú seleccionado
        nombre_menu_original = self.tree_menus.item(seleccion[0])['values'][0]
        
        # Obtener detalles del menú original
        menu_original = self.menu_crud.obtener_menu_por_nombre(nombre_menu_original)
        if not menu_original:
            messagebox.showerror("Error", "No se encontró el menú")
            return
        
        # Nuevos datos
        nuevo_nombre = self.entry_nombre_menu.get().strip()
        nueva_descripcion = self.entry_descripcion_menu.get().strip()
        
        # Validar ingredientes
        ingredientes_seleccionados = self.lista_ingredientes.selection()
        ingredientes_menu = []
        
        for seleccion in ingredientes_seleccionados:
            ingrediente = self.lista_ingredientes.item(seleccion)['values'][0]
            cantidad_str = self.entry_cantidad_ingrediente_menu.get()
            
            try:
                cantidad = float(cantidad_str)
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido")
                return
            
            # Obtener el ID del ingrediente
            ingrediente_obj = self.ingrediente_crud.obtener_ingrediente_por_nombre(ingrediente)
            if ingrediente_obj:
                ingredientes_menu.append((ingrediente_obj.id, cantidad))
        
        # Intentar actualizar menú
        try:
            self.menu_crud.actualizar_menu(
                id=menu_original[0], 
                nombre=nuevo_nombre, 
                descripcion=nueva_descripcion, 
                ingredientes=ingredientes_menu
            )
            
            messagebox.showinfo("Éxito", f"Menú '{nuevo_nombre}' actualizado correctamente")
            self.obtener_nombres_menus()
            # Limpiar campos
            self.entry_nombre_menu.delete(0, 'end')
            self.entry_descripcion_menu.delete(0, 'end')
            self.entry_cantidad_ingrediente_menu.delete(0, 'end')
            
            # Recargar lista de menús
            self.cargar_menus_en_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def eliminar_menu(self):
        # Validar selección
        seleccion = self.tree_menus.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un menú para eliminar")
            return
        
        # Obtener nombre del menú seleccionado
        nombre_menu = self.tree_menus.item(seleccion[0])['values'][0]
        
        # Obtener detalles del menú
        menu = self.menu_crud.obtener_menu_por_nombre(nombre_menu)
        if not menu:
            messagebox.showerror("Error", "No se encontró el menú")
            return
        
        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el menú '{nombre_menu}'?")
        
        if confirmacion:
            try:
                # Obtener los ingredientes del menú antes de eliminarlo
                ingredientes_menu = self.menu_crud.obtener_ingredientes_menu(menu['id'])
                
                # Obtener la cantidad de menús eliminados
                cantidad_menu = self.tree_menus.item(seleccion[0])['values'][4]
                
                # Restaurar cantidades de ingredientes
                for ingrediente_id, nombre_ingrediente, cantidad_requerida, unidad_medida in ingredientes_menu:
                    # Obtener el ingrediente
                    ingrediente = self.ingrediente_crud.obtener_ingrediente(ingrediente_id)
                    
                    if ingrediente:
                        # Calcular la cantidad total a restaurar
                        cantidad_total = cantidad_menu * cantidad_requerida
                        
                        # Sumar la cantidad de vuelta al ingrediente
                        nueva_cantidad = ingrediente.cantidad + cantidad_total
                        
                        # Actualizar el ingrediente
                        self.ingrediente_crud.actualizar_ingrediente(
                            id=ingrediente_id, 
                            nombre=ingrediente.nombre, 
                            tipo=ingrediente.tipo, 
                            cantidad=nueva_cantidad, 
                            unidad_medida=ingrediente.unidad_medida
                        )
                
                # Eliminar el menú
                self.menu_crud.eliminar_menu(menu['id'])
                
                messagebox.showinfo("Éxito", f"Menú '{nombre_menu}' eliminado correctamente")
                
                # Actualizar interfaces
                self.obtener_nombres_menus()
                self.cargar_ingredientes_en_lista_menus()
                self.cargar_ingredientes_en_treeview()
                self.cargar_menus_en_treeview()
                
                # Limpiar campos
                self.entry_nombre_menu.delete(0, 'end')
                self.entry_descripcion_menu.delete(0, 'end')
                self.entry_cantidad_ingrediente_menu.delete(0, 'end')
            
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

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
        self.label_correo.place(x=380, y=20)
        self.entry_correo = ctk.CTkEntry(self.frame_formulario, width=200)
        self.entry_correo.place(x=450, y=20)

        # Buttons with event handling
        self.boton_crear = ctk.CTkButton(self.frame_formulario, text="Agregar Cliente", command=self.agregar_cliente)
        self.boton_crear.place(x=10, y=80)

        self.boton_act = ctk.CTkButton(self.frame_formulario, text="Actualizar Cliente", command=self.actualizar_cliente)
        self.boton_act.place(x=200, y=80)

        self.boton_eliminar = ctk.CTkButton(self.frame_formulario, text="Eliminar Cliente", command=self.eliminar_cliente)
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
                
        # Agregar evento de selección al tree
        self.tree.bind('<<TreeviewSelect>>', self.on_select_cliente)
        
        # Cargar clientes existentes
        self.cargar_clientes()

    def cargar_clientes(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener y mostrar clientes
        clientes = self.cliente_crud.listar_clientes()
        for cliente in clientes:
            self.tree.insert("", "end", values=(
                cliente.id,
                cliente.nombre,
                cliente.correo_electronico
            ))

    def agregar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()
        
        # Validaciones
        if not nombre or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validar formato de correo
        if not '@' in correo or not '.' in correo:
            messagebox.showerror("Error", "Formato de correo electrónico inválido")
            return
        
        # Verificar si el correo ya existe
        cliente_existente = self.cliente_crud.buscar_cliente_por_correo(correo)
        if cliente_existente:
            messagebox.showerror("Error", "Ya existe un cliente con ese correo electrónico")
            return
        
        try:
            nuevo_id = self.cliente_crud.crear_cliente(nombre, correo)
            if nuevo_id:
                messagebox.showinfo("Éxito", f"Cliente '{nombre}' creado correctamente")
                self.obtener_nombres_clientes()
                # Limpiar campos
                self.entry_nombre.delete(0, 'end')
                self.entry_correo.delete(0, 'end')
                # Recargar lista
                self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear cliente: {str(e)}")

    def on_select_cliente(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            # Obtener datos del cliente seleccionado
            cliente_data = self.tree.item(seleccion[0])['values']
            # Llenar campos
            self.entry_nombre.delete(0, 'end')
            self.entry_nombre.insert(0, cliente_data[1])
            self.entry_correo.delete(0, 'end')
            self.entry_correo.insert(0, cliente_data[2])

    def actualizar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un cliente para actualizar")
            return
        
        cliente_id = self.tree.item(seleccion[0])['values'][0]
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()
        
        # Validaciones
        if not nombre or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            if self.cliente_crud.actualizar_cliente(cliente_id, nombre, correo):
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                self.obtener_nombres_clientes()
                # Limpiar campos
                self.entry_nombre.delete(0, 'end')
                self.entry_correo.delete(0, 'end')
                # Recargar lista
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el cliente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(e)}")

    def eliminar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
            return
        
        cliente_id = self.tree.item(seleccion[0])['values'][0]
        nombre = self.tree.item(seleccion[0])['values'][1]
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al cliente '{nombre}'?"):
            return
        
        try:
            if self.cliente_crud.eliminar_cliente(cliente_id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.obtener_nombres_clientes()
                # Limpiar campos
                self.entry_nombre.delete(0, 'end')
                self.entry_correo.delete(0, 'end')
                # Recargar lista
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")

    def configurar_compras(self):
        # Frame principal
        frame_formulario = ctk.CTkFrame(self.tab_compras, width=1400, height=700)
        frame_formulario.place(x=10, y=10)

        # Sección de selección
        label_cliente = ctk.CTkLabel(frame_formulario, text="Cliente:")
        label_cliente.place(x=20, y=20)
        self.combo_clientes = ctk.CTkComboBox(frame_formulario, values=self.obtener_nombres_clientes())
        self.combo_clientes.place(x=100, y=20)

        label_menu = ctk.CTkLabel(frame_formulario, text="Menú:")
        label_menu.place(x=260, y=20)
        self.combo_menu = ctk.CTkComboBox(frame_formulario, values=self.obtener_nombres_menus())
        self.combo_menu.place(x=310, y=20)

        # Campo de cantidad
        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.place(x=470, y=20)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario, width=100)
        self.entry_cantidad.place(x=550, y=20)

        # Campo de descripción (NUEVO)
        label_descripcion = ctk.CTkLabel(frame_formulario, text="Descripción:")
        label_descripcion.place(x=670, y=20)
        self.entry_descripcion = ctk.CTkEntry(frame_formulario, width=220)
        self.entry_descripcion.place(x=760, y=20)

        # Botón para agregar a la compra
        boton_agregar = ctk.CTkButton(frame_formulario, text="Agregar a la compra", command=self.insertar_pedido_bd)
        boton_agregar.place(x=1000, y=20)

        # TreeView para items de la compra
        frame_treeview = ctk.CTkFrame(self.tab_compras, width=1350, height=500)
        frame_treeview.place(x=10, y=70)


        # Modificar la definición del TreeView para incluir la columna de descripción
        self.tree_compras = ttk.Treeview(frame_treeview, 
                                        columns=("Menu", "Descripcion", "Cantidad", "Precio Unitario", "Subtotal"), 
                                        show="headings", 
                                        height=20)
        
        self.tree_compras.heading("Menu", text="Menú")
        self.tree_compras.column("Menu", width=300, anchor="center")
        
        # Nueva columna de descripción
        self.tree_compras.heading("Descripcion", text="Descripción")
        self.tree_compras.column("Descripcion", width=200, anchor="center")
        self.tree_compras.heading("Cantidad", text="Cantidad")
        self.tree_compras.column("Cantidad", width=100, anchor="center")
        self.tree_compras.heading("Precio Unitario", text="Precio Unitario")
        self.tree_compras.column("Precio Unitario", width=150, anchor="center")
        self.tree_compras.heading("Subtotal", text="Subtotal")
        self.tree_compras.column("Subtotal", width=150, anchor="center")
        
        self.tree_compras.place(x=10, y=10)
        # Total y Botón de Generar Boleta
        self.label_total = ctk.CTkLabel(frame_formulario, text="Total: $0")
        self.label_total.place(x=20, y=600)

        boton_generar = ctk.CTkButton(frame_formulario, text="Generar Boleta", command=self.generar_boleta)
        boton_generar.place(x=200, y=600)

        # Botón para eliminar item
        boton_eliminar = ctk.CTkButton(frame_formulario, text="Eliminar Item", command=self.eliminar_item_compra)
        boton_eliminar.place(x=400, y=600)
            
    def obtener_nombres_clientes(self):
        """Obtiene la lista de nombres de clientes y actualiza el combobox si existe"""
        clientes = self.cliente_crud.listar_clientes()
        nombres = [cliente.nombre for cliente in clientes] if clientes else []
        
        # Actualizar el combobox si ya existe
        if hasattr(self, 'combo_clientes'):
            self.combo_clientes.configure(values=nombres)
            if not nombres:  # Si la lista está vacía
                self.combo_clientes.set("")  # Establecer texto vacío
        
        return nombres

    def obtener_nombres_menus(self):
        """Obtiene la lista de nombres de menús y actualiza el combobox si existe"""
        menus = self.menu_crud.listar_menus()
        nombres = [menu['nombre'] for menu in menus] if menus else []
        
        # Actualizar el combobox si ya existe
        if hasattr(self, 'combo_menu'):
            self.combo_menu.configure(values=nombres)
            if not nombres:  # Si la lista está vacía
                self.combo_menu.set("")  # Establecer texto vacío
        
        return nombres
                    
    def insertar_pedido_bd(self):
        try:
            menu_nombre = self.combo_menu.get()
            cantidad = float(self.entry_cantidad.get())
            descripcion = self.entry_descripcion.get()
            
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return

            if not descripcion:
                messagebox.showerror("Error", "La descripción es requerida")
                return

            # Obtener detalles del menú y cliente
            menu = self.menu_crud.obtener_menu_por_nombre(menu_nombre)
            cliente_nombre = self.combo_clientes.get()
            cliente = self.cliente_crud.obtener_cliente_por_nombre(cliente_nombre)

            if not menu or not cliente:
                messagebox.showerror("Error", "Menú o cliente no encontrado")
                return

            precio_unitario = menu['precio']
            
            # Verificar items existentes
            item_existente = None
            cantidad_total = cantidad
            for item in self.tree_compras.get_children():
                valores = self.tree_compras.item(item)['values']
                if valores[0] == menu_nombre and valores[1] == descripcion:
                    item_existente = item
                    cantidad_actual = float(valores[2])
                    cantidad_total += cantidad_actual
                    break

            # Preparar sesión de base de datos para verificar y descontar menús
            session = self.menu_crud.Session()
            try:
                menu_db = session.query(Menu).filter(Menu.nombre == menu_nombre).first()
                if menu_db:
                    # Verificar si hay suficientes menús disponibles
                    if menu_db.cantidad is None:
                        menu_db.cantidad = 0
                    
                    if menu_db.cantidad < cantidad_total:
                        messagebox.showerror("Error", f"No hay suficientes menús disponibles. Disponibles: {menu_db.cantidad}")
                        return
                    
                    # Proceder con la inserción o actualización
                    if item_existente:
                        valores_actuales = self.tree_compras.item(item_existente)['values']
                        cantidad_actual = float(valores_actuales[2])
                        nueva_cantidad = cantidad_actual + cantidad
                        nuevo_subtotal = precio_unitario * nueva_cantidad

                        self.tree_compras.item(item_existente, values=(
                            menu_nombre,
                            descripcion,
                            nueva_cantidad,
                            f"${precio_unitario:.2f}",
                            f"${nuevo_subtotal:.2f}"
                        ))

                        pedido = self.pedido_crud.obtener_pedido_por_cliente_menu_descripcion(
                            cliente.id, menu['id'], descripcion)
                        if pedido:
                            self.pedido_crud.actualizar_cantidad_pedido(pedido.id, nuevo_subtotal)
                    else:
                        subtotal = precio_unitario * cantidad
                        pedido_id = self.pedido_crud.crear_pedido(
                            cliente_id=cliente.id,
                            menu_id=menu['id'],
                            total=subtotal,
                            descripcion=descripcion
                        )

                        if pedido_id:
                            self.tree_compras.insert("", "end", values=(
                                menu_nombre,
                                descripcion,
                                cantidad,
                                f"${precio_unitario:.2f}",
                                f"${subtotal:.2f}"
                            ))

                    # Descontar menús
                    menu_db.cantidad -= cantidad
                    session.commit()
                    
                    # Actualizar el treeview de menús después de descontar
                    self.cargar_menus_en_treeview()
                else:
                    messagebox.showerror("Error", "Menú no encontrado")
                    return
            except Exception as e:
                session.rollback()
                messagebox.showerror("Error", f"Error al descontar menús: {str(e)}")
            finally:
                session.close()

            self.cargar_clientes_combobox()
            self.cargar_pedidos()
            self.actualizar_total()
            self.cargar_ingredientes_en_lista_menus()
            self.entry_cantidad.delete(0, 'end')
            self.entry_descripcion.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear pedido: {str(e)}")                          

    def eliminar_item_compra(self):
        seleccion = self.tree_compras.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un item para eliminar")
            return

        # Get the details of the item to be deleted
        item_values = self.tree_compras.item(seleccion[0])['values']
        menu_nombre = item_values[0]
        cantidad_eliminar = float(item_values[2])

        # Restore menu quantity
        session = self.menu_crud.Session()
        try:
            menu_db = session.query(Menu).filter(Menu.nombre == menu_nombre).first()
            if menu_db:
                if menu_db.cantidad is None:
                    menu_db.cantidad = 0
                menu_db.cantidad += cantidad_eliminar
                session.commit()
            else:
                messagebox.showerror("Error", "Menú no encontrado")
                return
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error al restaurar menús: {str(e)}")
        finally:
            session.close()

        # Remove the item from the TreeView
        self.tree_compras.delete(seleccion)
        
        # Update total
        self.actualizar_total()

    def actualizar_total(self):
        total = 0
        for item in self.tree_compras.get_children():
            # Obtener el subtotal y limpiar el símbolo $ antes de convertir a float
            subtotal = float(self.tree_compras.item(item)['values'][4].replace('$', ''))
            total += subtotal
        self.label_total.configure(text=f"Total: ${total:.2f}")

    def generar_boleta(self):
        cliente_nombre = self.combo_clientes.get()
        
        # Verificar si se ha seleccionado un cliente
        if not cliente_nombre:
            messagebox.showwarning("Error", "Seleccione un cliente")
            return
        
        # Verificar si hay items en el TreeView
        items = self.tree_compras.get_children()
        
        if not items:
            messagebox.showwarning("Error", "Agregue al menos un menú")
            return

        # Calcular total
        total = sum(float(self.tree_compras.item(item)['values'][4].replace('$', '')) for item in items)
        
        try:
            # Asegurar que exista el directorio de boletas
            os.makedirs('boletas', exist_ok=True)
            
            # Nombre de archivo único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"boletas/boleta_{cliente_nombre}_{timestamp}.pdf"
            
            # Crear PDF
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            
            # Título
            c.setFont("Helvetica-Bold", 16)
            c.drawString(inch, height - inch, "Boleta de Compra")
            
            # Detalles del cliente
            c.setFont("Helvetica", 12)
            c.drawString(inch, height - (inch * 1.5), f"Cliente: {cliente_nombre}")
            c.drawString(inch, height - (inch * 1.7), f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Línea separadora
            c.line(inch, height - (inch * 2), width - inch, height - (inch * 2))
            
            # Encabezados de la tabla
            c.setFont("Helvetica-Bold", 12)
            y = height - (inch * 2.2)
            c.drawString(inch, y, "Menú")
            c.drawString(inch * 4, y, "Descripción")
            c.drawString(inch * 6, y, "Cantidad")
            c.drawString(inch * 7.5, y, "Precio")
            
            # Línea separadora
            c.line(inch, y - 10, width - inch, y - 10)
            
            # Detalles de los items
            c.setFont("Helvetica", 10)
            y -= 30
            for item in items:
                menu_nombre = self.tree_compras.item(item)['values'][0]
                descripcion_item = self.tree_compras.item(item)['values'][1]
                cantidad = self.tree_compras.item(item)['values'][2]
                precio = self.tree_compras.item(item)['values'][4]
                
                c.drawString(inch, y, menu_nombre)
                c.drawString(inch * 4, y, descripcion_item)
                c.drawString(inch * 6, y, str(cantidad))
                c.drawString(inch * 7.5, y, precio)
                
                y -= 20
            
            # Línea separadora final
            c.line(inch, y, width - inch, y)
            
            # Total
            c.setFont("Helvetica-Bold", 12)
            y -= 20
            c.drawString(inch, y, f"Total: ${total:.2f}")
            
            # Guardar PDF
            c.save()
            
            # Mensaje de éxito
            messagebox.showinfo("Boleta Generada", f"Boleta guardada en {filename}")

            # Limpiar TreeView
            for item in items:
                self.tree_compras.delete(item)
            
            # Resetear total
            self.label_total.configure(text="Total: $0")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar boleta: {str(e)}")
            
    def configurar_pedidos(self):
        # Inicializar atributos de clase
        self.label_total = None
        self.tree_pedidos = None
        self.combobox_cliente = None

        # Crear un frame para la lista de pedidos y opciones de organización
        frame_superior = ctk.CTkFrame(self.tab_pedidos, height=900, width=1300)
        frame_superior.place(x=10, y=10)

        # Combobox para seleccionar cliente
        label_cliente = ctk.CTkLabel(frame_superior, text="Seleccionar Cliente:")
        label_cliente.place(x=10, y=10)

        # Combobox para clientes
        self.combobox_cliente = ctk.CTkComboBox(frame_superior, values=[], width=200)
        self.combobox_cliente.place(x=150, y=10)

        # Botón para filtrar por cliente
        boton_filtrar_cliente = ctk.CTkButton(frame_superior, text="Filtrar por Cliente", width=150)
        boton_filtrar_cliente.place(x=370, y=10)
        boton_filtrar_cliente.configure(command=self.filtrar_por_cliente)

        # Botón para organizar por fecha
        boton_organizar_fecha = ctk.CTkButton(frame_superior, text="Ordenar por Fecha", width=150)
        boton_organizar_fecha.place(x=540, y=10)
        boton_organizar_fecha.configure(command=self.ordenar_por_fecha)

        # Botón para organizar por cliente
        boton_organizar_cliente = ctk.CTkButton(frame_superior, text="Ordenar por Cliente", width=150)
        boton_organizar_cliente.place(x=710, y=10)
        boton_organizar_cliente.configure(command=self.ordenar_por_cliente)

        # Crear un frame para mostrar la lista de pedidos
        frame_treeview = ctk.CTkFrame(self.tab_pedidos, height=400, width=1200)
        frame_treeview.place(x=10, y=220)

        # Crear el Treeview para mostrar los pedidos
        self.tree_pedidos = ttk.Treeview(
            frame_treeview, 
            columns=("ID", "Cliente", "Fecha", "Cantidad", "Descripción", "Total"), 
            show="headings", 
            height=20
        )

        self.tree_pedidos.heading("ID", text="ID Pedido")
        self.tree_pedidos.column("ID", width=100, anchor="center")
        self.tree_pedidos.heading("Cliente", text="Cliente")
        self.tree_pedidos.column("Cliente", width=200, anchor="center")
        self.tree_pedidos.heading("Fecha", text="Fecha")
        self.tree_pedidos.column("Fecha", width=200, anchor="center")
        self.tree_pedidos.heading("Cantidad", text="Cantidad")
        self.tree_pedidos.column("Cantidad", width=100, anchor="center")
        self.tree_pedidos.heading("Descripción", text="Descripción")
        self.tree_pedidos.column("Descripción", width=200, anchor="center")
        self.tree_pedidos.heading("Total", text="Total")
        self.tree_pedidos.column("Total", width=150, anchor="center")
        self.tree_pedidos.place(x=10, y=10)

        # Crear un frame inferior para el total y otras acciones
        frame_inferior = ctk.CTkFrame(self.tab_pedidos, height=50, width=800)
        frame_inferior.place(x=10, y=630)

        # Etiqueta para mostrar el total del pedido
        self.label_total = ctk.CTkLabel(frame_inferior, text="Total: 0 CLP", font=("Arial", 14))
        self.label_total.place(x=10, y=10)

        # Cargar datos iniciales
        self.cargar_clientes_combobox()
        self.cargar_pedidos()

    def cargar_clientes_combobox(self):
        """Carga la lista de clientes con pedidos en el combobox"""
        # Obtener solo los clientes que tienen pedidos
        pedidos = self.pedido_crud.listar_pedidos_con_cliente()
        # Crear un conjunto de nombres únicos de clientes que tienen pedidos
        clientes_con_pedidos = set(cliente.nombre for _, cliente, _ in pedidos)
        # Convertir a lista y agregar "Todos" al inicio
        nombres_clientes = ["Todos"] + sorted(list(clientes_con_pedidos))
        # Configurar el combobox con los nombres filtrados
        self.combobox_cliente.configure(values=nombres_clientes)
        self.combobox_cliente.set("Todos")

    def cargar_pedidos(self):
        """Carga todos los pedidos en el TreeView"""
        # Limpiar TreeView
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)
        
        # Obtener pedidos con información del cliente
        pedidos = self.pedido_crud.listar_pedidos_con_cliente()
        
        # Insertar pedidos en el TreeView
        total_general = 0
        for pedido, cliente, menu in pedidos:
            fecha_formateada = pedido.fecha.strftime("%Y-%m-%d %H:%M")
            self.tree_pedidos.insert("", "end", values=(
                pedido.id,
                cliente.nombre,
                fecha_formateada,
                pedido.cantidad,
                pedido.descripcion,  # Added description
                f"${pedido.total:,.0f}"
            ))
            total_general += pedido.total
        
        # Actualizar el total
        self.label_total.configure(text=f"Total: ${total_general:,.0f} CLP")
            
    def filtrar_por_cliente(self):
        """Filtra los pedidos por el cliente seleccionado"""
        cliente_seleccionado = self.combobox_cliente.get()
        
        # Limpiar TreeView
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)
        
        if cliente_seleccionado == "Todos":
            self.cargar_pedidos()
            return
        
        # Obtener pedidos del cliente seleccionado
        pedidos = self.pedido_crud.listar_pedidos_por_cliente_nombre(cliente_seleccionado)
        
        # Insertar pedidos filtrados
        total_cliente = 0
        for pedido in pedidos:
            fecha_formateada = pedido.fecha.strftime("%Y-%m-%d %H:%M")
            self.tree_pedidos.insert("", "end", values=(
                pedido.id,
                cliente_seleccionado,
                fecha_formateada,
                pedido.cantidad,
                pedido.descripcion,  # Added description
                f"${pedido.total:,.0f}"
            ))
            total_cliente += pedido.total
        
        # Actualizar el total
        self.label_total.configure(text=f"Total: ${total_cliente:,.0f} CLP")
        
    def ordenar_por_fecha(self):
        """Ordena los pedidos por fecha"""
        items = [(self.tree_pedidos.item(item)["values"], item) for item in self.tree_pedidos.get_children()]
        
        # Ordenar por fecha (índice 2)
        items.sort(key=lambda x: x[0][2])
        
        # Reordenar items en el TreeView
        for index, (_, item) in enumerate(items):
            self.tree_pedidos.move(item, "", index)

    def ordenar_por_cliente(self):
        """Ordena los pedidos por nombre de cliente"""
        items = [(self.tree_pedidos.item(item)["values"], item) for item in self.tree_pedidos.get_children()]
        
        # Ordenar por cliente (índice 1)
        items.sort(key=lambda x: x[0][1])
        
        # Reordenar items en el TreeView
        for index, (_, item) in enumerate(items):
            self.tree_pedidos.move(item, "", index)