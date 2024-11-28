from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List, Optional
from models import Base, Pedido, Cliente, Menu

class PedidoCRUD:
    def __init__(self, database_url: str = 'sqlite:///restaurante.db'):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def crear_pedido(self, cliente_id: int, menu_id: int, total: float, descripcion: str, fecha: datetime = None) -> Optional[int]:
        if fecha is None:
            fecha = datetime.now()
        
        session = self.Session()
        try:
            nuevo_pedido = Pedido(
                cliente_id=cliente_id,
                menu_id=menu_id,
                total=total,
                descripcion=descripcion,
                fecha=fecha
            )
            session.add(nuevo_pedido)
            session.commit()
            return nuevo_pedido.id
        except SQLAlchemyError:
            session.rollback()
            return None
        finally:
            session.close()

    def obtener_pedido(self, id: int) -> Optional[Pedido]:
        """
        Retrieve an order by its ID
        
        Args:
            id (int): Order's ID
        
        Returns:
            Optional[Pedido]: Order object or None if not found
        """
        session = self.Session()
        try:
            return session.query(Pedido).filter(Pedido.id == id).first()
        finally:
            session.close()

    def listar_pedidos(self) -> List[Pedido]:
        """
        List all orders in the database
        
        Returns:
            List[Pedido]: List of order objects
        """
        session = self.Session()
        try:
            return session.query(Pedido).all()
        finally:
            session.close()

    def actualizar_pedido(self, id: int, cliente_id: int = None, menu_id: int = None,
                         total: float = None, descripcion: str = None, fecha: datetime = None) -> bool:
        """
        Update order information
        
        Args:
            id (int): Order's ID
            cliente_id (int, optional): New client ID
            menu_id (int, optional): New menu ID
            total (float, optional): New total
            fecha (datetime, optional): New date
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        session = self.Session()
        try:
            pedido = session.query(Pedido).filter(Pedido.id == id).first()
            if not pedido:
                return False
                
            if cliente_id is not None:
                pedido.cliente_id = cliente_id
            if menu_id is not None:
                pedido.menu_id = menu_id
            if total is not None:
                pedido.total = total
            if descripcion is not None:
                pedido.descripcion = descripcion
            if fecha is not None:
                pedido.fecha = fecha
                
            session.commit()
            return True
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def eliminar_pedido(self, id: int) -> bool:
        """
        Delete an order from the database
        
        Args:
            id (int): Order's ID
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        session = self.Session()
        try:
            pedido = session.query(Pedido).filter(Pedido.id == id).first()
            if pedido:
                session.delete(pedido)
                session.commit()
                return True
            return False
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def obtener_pedidos_por_cliente(self, cliente_id: int) -> List[Pedido]:
        """
        Retrieve all orders for a specific client
        
        Args:
            cliente_id (int): Client's ID
        
        Returns:
            List[Pedido]: List of order objects
        """
        session = self.Session()
        try:
            return session.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()
        finally:
            session.close()

    def obtener_total_ventas_por_fecha(self, fecha: datetime) -> float:
        """
        Calculate total sales for a specific date
        
        Args:
            fecha (datetime): Date to calculate sales for
        
        Returns:
            float: Total sales for the given date
        """
        session = self.Session()
        try:
            return session.query(func.sum(Pedido.total))\
                .filter(func.date(Pedido.fecha) == fecha.date())\
                .scalar() or 0.0
        finally:
            session.close()

    def listar_pedidos_con_cliente(self) -> List[Pedido]:
        """
        List all orders with client and menu information
        
        Returns:
            List[Pedido]: List of order objects with related client and menu information
        """
        session = self.Session()
        try:
            return session.query(Pedido, Cliente, Menu)\
                .join(Cliente)\
                .join(Menu)\
                .all()
        finally:
            session.close()

    def listar_pedidos_por_cliente_nombre(self, cliente_nombre: str) -> List[Pedido]:
        """
        Retrieve orders for a specific client by name
        
        Args:
            cliente_nombre (str): Client's name
        
        Returns:
            List[Pedido]: List of order objects
        """
        session = self.Session()
        try:
            return session.query(Pedido)\
                .join(Cliente)\
                .filter(Cliente.nombre == cliente_nombre)\
                .all()
        finally:
            session.close()


    def actualizar_cantidad_pedido(self, pedido_id: int, nueva_cantidad: float) -> bool:
        """
        Actualizar la cantidad y el total de un pedido existente
        
        Args:
            pedido_id (int): ID del pedido a actualizar
            nueva_cantidad (float): Nueva cantidad total
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        session = self.Session()
        try:
            pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
            if pedido:
                pedido.total = nueva_cantidad
                session.commit()
                return True
            return False
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def obtener_pedido_por_cliente_menu_descripcion(self, cliente_id: int, menu_id: int, descripcion: str) -> Optional[Pedido]:
        """
        Obtiene un pedido basado en el cliente, menú y descripción
        
        Args:
            cliente_id (int): ID del cliente
            menu_id (int): ID del menú
            descripcion (str): Descripción del pedido
            
        Returns:
            Optional[Pedido]: Pedido si existe, None si no se encuentra
        """
        session = self.Session()
        try:
            return session.query(Pedido).filter(
                Pedido.cliente_id == cliente_id,
                Pedido.menu_id == menu_id,
                Pedido.descripcion == descripcion
            ).first()
        finally:
            session.close()