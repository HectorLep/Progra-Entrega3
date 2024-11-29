from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional
from models import Base, Ingrediente

class IngredienteCRUD:
    def __init__(self, database_url: str = 'sqlite:///restaurante.db'):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def crear_ingrediente(self, nombre: str, tipo: str, cantidad: int, unidad_medida: str) -> Optional[int]:
        session = self.Session()
        try:
            ingrediente = Ingrediente(
                nombre=nombre,
                tipo=tipo,
                cantidad=cantidad,
                unidad_medida=unidad_medida
            )
            session.add(ingrediente)
            session.commit()
            session.refresh(ingrediente)
            return ingrediente.id
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def obtener_ingrediente(self, id: int) -> Optional[Ingrediente]:
    
        session = self.Session()
        try:
            return session.query(Ingrediente).filter(Ingrediente.id == id).first()
        finally:
            session.close()

    def obtener_ingrediente_por_nombre(self, nombre: str) -> Optional[Ingrediente]:

        session = self.Session()
        try:
            return session.query(Ingrediente).filter(Ingrediente.nombre == nombre).first()
        finally:
            session.close()

    def listar_ingredientes(self) -> List[Ingrediente]:

        session = self.Session()
        try:
            return session.query(Ingrediente).all()
        finally:
            session.close()

    def actualizar_ingrediente(self, id: int, nombre: str = None, tipo: str = None,
                             cantidad: float = None, unidad_medida: str = None) -> bool:

        session = self.Session()
        try:
            ingrediente = session.query(Ingrediente).filter(Ingrediente.id == id).first()
            if not ingrediente:
                return False
                
            if nombre is not None:
                ingrediente.nombre = nombre
            if tipo is not None:
                ingrediente.tipo = tipo
            if cantidad is not None:
                ingrediente.cantidad = cantidad
            if unidad_medida is not None:
                ingrediente.unidad_medida = unidad_medida
                
            session.commit()
            return True
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def eliminar_ingrediente(self, id: int) -> bool:
        session = self.Session()
        try:
            ingrediente = session.query(Ingrediente).filter(Ingrediente.id == id).first()
            if ingrediente:
                session.delete(ingrediente)
                session.commit()
                return True
            return False
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def obtener_ingredientes_por_tipo(self, tipo: str) -> List[Ingrediente]:
        session = self.Session()
        try:
            return session.query(Ingrediente).filter(Ingrediente.tipo == tipo).all()
        finally:
            session.close()