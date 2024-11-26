import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from app import SistemaGestionRestaurante
from CRUD.cliente_crud import ClienteCRUD
from CRUD.menu_crud import MenuCRUD
from CRUD.ingrediente_crud import IngredienteCRUD
from CRUD.pedido_crud import PedidoCRUD
import sqlite3

class Models():
    def __init__(self):
        self.menu_crud = MenuCRUD()
        self.ingrediente_crud = IngredienteCRUD()
        self.pedido_crud = PedidoCRUD()
        self.cliente_crud = ClienteCRUD()
        self.app = SistemaGestionRestaurante()

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
