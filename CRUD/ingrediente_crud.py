from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional
from models import Base, Ingrediente

class IngredienteCRUD:
    def __init__(self, database_url: str = 'sqlite:///restaurante.db'):
        """
        Initialize the IngredienteCRUD with a database connection
        
        Args:
            database_url (str): SQLAlchemy database URL
        """
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def crear_ingrediente(self, nombre: str, tipo: str, cantidad: int, unidad_medida: str) -> Optional[int]:
        """
        Create a new ingredient in the database
        
        Args:
            nombre (str): Ingredient name
            tipo (str): Ingredient type
            cantidad (int): Quantity
            unidad_medida (str): Unit of measurement
        
        Returns:
            Optional[int]: ID of the newly created ingredient or None if creation fails
        
        Raises:
            SQLAlchemyError: If there's a database error
        """
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
        """
        Retrieve an ingredient by its ID
        
        Args:
            id (int): Ingredient's ID
        
        Returns:
            Optional[Ingrediente]: Ingredient object or None if not found
        """
        session = self.Session()
        try:
            return session.query(Ingrediente).filter(Ingrediente.id == id).first()
        finally:
            session.close()

    def obtener_ingrediente_por_nombre(self, nombre: str) -> Optional[Ingrediente]:
        """
        Retrieve an ingredient by its name
        
        Args:
            nombre (str): Ingredient's name
        
        Returns:
            Optional[Ingrediente]: Ingredient object or None if not found
        """
        session = self.Session()
        try:
            return session.query(Ingrediente).filter(Ingrediente.nombre == nombre).first()
        finally:
            session.close()

    def listar_ingredientes(self) -> List[Ingrediente]:
        """
        List all ingredients in the database
        
        Returns:
            List[Ingrediente]: List of ingredient objects
        """
        session = self.Session()
        try:
            return session.query(Ingrediente).all()
        finally:
            session.close()

    def actualizar_ingrediente(self, id: int, nombre: str = None, tipo: str = None,
                             cantidad: float = None, unidad_medida: str = None) -> bool:
        """
        Update ingredient information
        
        Args:
            id (int): Ingredient's ID
            nombre (str, optional): New name
            tipo (str, optional): New type
            cantidad (float, optional): New quantity
            unidad_medida (str, optional): New unit of measurement
            
        Returns:
            bool: True if update was successful, False otherwise
        """
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
        """
        Delete an ingredient from the database
        
        Args:
            id (int): Ingredient's ID
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
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
        """
        Get all ingredients of a specific type
        
        Args:
            tipo (str): Type of ingredient to filter by
            
        Returns:
            List[Ingrediente]: List of ingredient objects of the specified type
        """
        session = self.Session()
        try:
            return session.query(Ingrediente).filter(Ingrediente.tipo == tipo).all()
        finally:
            session.close()