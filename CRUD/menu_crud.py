from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Tuple, Optional, Dict
from models import Base, Menu, MenuIngrediente, Ingrediente


class MenuCRUD:
    def __init__(self, database_url: str = 'sqlite:///restaurante.db'):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def crear_menu(self, nombre: str, descripcion: str, precio: float, ingredientes: List[Tuple[int, float]], cantidad: int = 0) -> int:
        session = self.Session()
        try:
            # Crear nuevo menú
            nuevo_menu = Menu(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,  
                cantidad=cantidad  # Add initial quantity

            )
            
            # Agregar ingredientes al menú
            for ingrediente_id, cantidad in ingredientes:
                menu_ingrediente = MenuIngrediente(
                    ingrediente_id=ingrediente_id,
                    cantidad=cantidad
                )
                nuevo_menu.ingredientes_association.append(menu_ingrediente)
            
            session.add(nuevo_menu)
            session.commit()
            session.refresh(nuevo_menu)
            return nuevo_menu.id
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def obtener_menu(self, id: int) -> Optional[Dict]:
        session = self.Session()
        try:
            menu = session.query(Menu).options(
                joinedload(Menu.ingredientes_association).joinedload(MenuIngrediente.ingrediente)
            ).filter(Menu.id == id).first()
            
            if not menu:
                return None
            
            return {
                'id': menu.id,
                'nombre': menu.nombre,
                'descripcion': menu.descripcion,
                'precio': menu.precio,
                'ingredientes': [
                    {
                        'id': ing.ingrediente.id,
                        'nombre': ing.ingrediente.nombre,
                        'cantidad_requerida': ing.cantidad,
                        'unidad_medida': ing.ingrediente.unidad_medida
                    } for ing in menu.ingredientes_association
                ]
            }
        finally:
            session.close()
    
    def obtener_menu_por_nombre(self, nombre: str) -> Optional[Dict]:
        session = self.Session()
        try:
            menu = session.query(Menu).options(
                joinedload(Menu.ingredientes_association).joinedload(MenuIngrediente.ingrediente)
            ).filter(Menu.nombre == nombre).first()
            
            if not menu:
                return None
            
            return {
                'id': menu.id,
                'nombre': menu.nombre,
                'descripcion': menu.descripcion,
                'precio': menu.precio,
                'ingredientes': [
                    {
                        'id': ing.ingrediente.id,
                        'nombre': ing.ingrediente.nombre,
                        'cantidad_requerida': ing.cantidad,
                        'unidad_medida': ing.ingrediente.unidad_medida
                    } for ing in menu.ingredientes_association
                ]
            }
        finally:
            session.close()
        
    def listar_menus(self) -> List[Dict]:
        session = self.Session()
        try:
            menus = session.query(Menu).options(
                joinedload(Menu.ingredientes_association).joinedload(MenuIngrediente.ingrediente)
            ).all()
            
            return [
                {
                    'id': menu.id,
                    'nombre': menu.nombre,
                    'descripcion': menu.descripcion,
                    'precio': menu.precio,
                    'cantidad': menu.cantidad,  # Add this line
                    'ingredientes': [
                        {
                            'id': ing.ingrediente.id,
                            'nombre': ing.ingrediente.nombre,
                            'cantidad_requerida': ing.cantidad,
                            'unidad_medida': ing.ingrediente.unidad_medida
                        } for ing in menu.ingredientes_association
                    ]
                } for menu in menus
            ]
        finally:
            session.close()
                
    def obtener_ingredientes_menu(self, menu_id: int) -> List[Tuple[int, str, float, str]]:
        session = self.Session()
        try:
            menu_ingredientes = session.query(MenuIngrediente).filter(
                MenuIngrediente.menu_id == menu_id
            ).join(Ingrediente).all()
            
            return [
                (
                    mi.ingrediente_id, 
                    mi.ingrediente.nombre, 
                    mi.cantidad,
                    mi.ingrediente.unidad_medida
                ) for mi in menu_ingredientes
            ]
        finally:
            session.close()
    
    def actualizar_menu(self, id: int, nombre: str = None, descripcion: str = None, 
                        precio: float = None, ingredientes: List[Tuple[int, float]] = None):
        session = self.Session()
        try:
            # Obtener el menú existente
            menu = session.query(Menu).filter(Menu.id == id).first()
            if not menu:
                raise ValueError("Menú no encontrado")
            
            # Actualizar campos si se proporcionan
            if nombre:
                menu.nombre = nombre
            if descripcion:
                menu.descripcion = descripcion
            if precio is not None:
                menu.precio = precio
            
            # Actualizar ingredientes si se proporcionan
            if ingredientes is not None:
                # Eliminar ingredientes existentes
                session.query(MenuIngrediente).filter(MenuIngrediente.menu_id == id).delete()
                
                # Agregar nuevos ingredientes
                for ingrediente_id, cantidad in ingredientes:
                    nuevo_ingrediente = MenuIngrediente(
                        menu_id=id,
                        ingrediente_id=ingrediente_id,
                        cantidad=cantidad
                    )
                    session.add(nuevo_ingrediente)
            
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
        
    def eliminar_menu(self, id: int):
        session = self.Session()
        try:
            # Obtener el menú
            menu = session.query(Menu).filter(Menu.id == id).first()
            if not menu:
                raise ValueError("Menú no encontrado")
            
            # Eliminar el menú (cascada eliminará los MenuIngrediente)
            session.delete(menu)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
                
    def buscar_menus(self, termino: str = None, precio_min: float = None, 
                     precio_max: float = None, ingrediente: str = None) -> List[Dict]:
        session = self.Session()
        try:
            # Consulta base
            query = session.query(Menu).options(
                joinedload(Menu.ingredientes_association).joinedload(MenuIngrediente.ingrediente)
            )
            
            # Filtro por término en nombre o descripción
            if termino:
                query = query.filter(
                    (Menu.nombre.ilike(f"%{termino}%")) | 
                    (Menu.descripcion.ilike(f"%{termino}%"))
                )
            
            # Filtro por rango de precio
            if precio_min is not None:
                query = query.filter(Menu.precio >= precio_min)
            if precio_max is not None:
                query = query.filter(Menu.precio <= precio_max)
            
            # Filtro por ingrediente
            if ingrediente:
                query = query.join(Menu.ingredientes_association).join(MenuIngrediente.ingrediente).filter(
                    Ingrediente.nombre.ilike(f"%{ingrediente}%")
                )
            
            # Ejecutar consulta y transformar resultados
            menus = query.all()
            
            return [
                {
                    'id': menu.id,
                    'nombre': menu.nombre,
                    'descripcion': menu.descripcion,
                    'precio': menu.precio,
                    'ingredientes': [
                        {
                            'id': ing.ingrediente.id,
                            'nombre': ing.ingrediente.nombre,
                            'cantidad_requerida': ing.cantidad,
                            'unidad_medida': ing.ingrediente.unidad_medida
                        } for ing in menu.ingredientes_association
                    ]
                } for menu in menus
            ]
        finally:
            session.close()



