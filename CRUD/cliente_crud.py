from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional
from models import Base, Cliente

class ClienteCRUD:
    def __init__(self, database_url: str = 'sqlite:///restaurante.db'):
        """
        Initialize the ClienteCRUD with a database connection
        
        Args:
            database_url (str): SQLAlchemy database URL
        """
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def crear_cliente(self, nombre: str, correo_electronico: str) -> Optional[int]:
        """
        Create a new client in the database
        
        Args:
            nombre (str): Client's name
            correo_electronico (str): Client's email
        
        Returns:
            Optional[int]: ID of the newly created client or None if creation fails
        
        Raises:
            IntegrityError: If email already exists
        """
        session = self.Session()
        try:
            nuevo_cliente = Cliente(
                nombre=nombre,
                correo_electronico=correo_electronico
            )
            session.add(nuevo_cliente)
            session.commit()
            return nuevo_cliente.id
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def obtener_cliente(self, id: int) -> Optional[Cliente]:
        """
        Retrieve a client by their ID
        
        Args:
            id (int): Client's ID
        
        Returns:
            Optional[Cliente]: Client object or None if not found
        """
        session = self.Session()
        try:
            return session.query(Cliente).filter(Cliente.id == id).first()
        finally:
            session.close()

    def obtener_cliente_por_nombre(self, nombre: str) -> Optional[Cliente]:
        """
        Retrieve a client by their name
        
        Args:
            nombre (str): Client's name
        
        Returns:
            Optional[Cliente]: Client object or None if not found
        """
        session = self.Session()
        try:
            return session.query(Cliente).filter(Cliente.nombre == nombre).first()
        finally:
            session.close()

    def listar_clientes(self) -> List[Cliente]:
        """
        List all clients in the database
        
        Returns:
            List[Cliente]: List of client objects
        """
        session = self.Session()
        try:
            return session.query(Cliente).all()
        finally:
            session.close()

    def actualizar_cliente(self, id: int, nombre: str = None, correo_electronico: str = None) -> bool:
        """
        Update client information
        
        Args:
            id (int): Client's ID
            nombre (str, optional): New name
            correo_electronico (str, optional): New email
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        session = self.Session()
        try:
            cliente = session.query(Cliente).filter(Cliente.id == id).first()
            if not cliente:
                return False
                
            if nombre is not None:
                cliente.nombre = nombre
            if correo_electronico is not None:
                cliente.correo_electronico = correo_electronico
                
            session.commit()
            return True
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def eliminar_cliente(self, id: int) -> bool:
        """
        Delete a client from the database
        
        Args:
            id (int): Client's ID
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        session = self.Session()
        try:
            cliente = session.query(Cliente).filter(Cliente.id == id).first()
            if cliente:
                session.delete(cliente)
                session.commit()
                return True
            return False
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def buscar_cliente_por_correo(self, correo_electronico: str) -> Optional[Cliente]:
        """
        Search for a client by email address
        
        Args:
            correo_electronico (str): Client's email
        
        Returns:
            Optional[Cliente]: Client object or None if not found
        """
        session = self.Session()
        try:
            return session.query(Cliente).filter(
                Cliente.correo_electronico == correo_electronico
            ).first()
        finally:
            session.close()