import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime

class PedidoCRUD:
    def __init__(self, db_path: str = 'restaurante.db'):
        """
        Initialize the PedidoCRUD with a database connection
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """
        Create the pedidos table if it doesn't exist
        Assumes existence of clientes and menus tables
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    menu_id INTEGER NOT NULL,
                    total REAL NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                    FOREIGN KEY (menu_id) REFERENCES menus (id)
                )
            ''')
            conn.commit()

    def crear_pedido(self, cliente_id: int, menu_id: int, total: float, fecha: str = None) -> int:
        """
        Create a new order in the database
        
        Args:
            cliente_id (int): ID of the client placing the order
            menu_id (int): ID of the menu ordered
            total (float): Total cost of the order
            fecha (str, optional): Date of the order. Defaults to current date
        
        Returns:
            int: ID of the newly created order
        """
        if fecha is None:
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pedidos (cliente_id, menu_id, total, fecha) 
                VALUES (?, ?, ?, ?)
            ''', (cliente_id, menu_id, total, fecha))
            conn.commit()
            return cursor.lastrowid

    def obtener_pedido(self, id: int) -> Optional[Tuple[int, int, int, float, str]]:
        """
        Retrieve an order by its ID
        
        Args:
            id (int): Order's ID
        
        Returns:
            Optional[Tuple[int, int, int, float, str]]: Order details or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, cliente_id, menu_id, total, fecha 
                FROM pedidos 
                WHERE id = ?
            ''', (id,))
            return cursor.fetchone()

    def listar_pedidos(self) -> List[Tuple[int, int, int, float, str]]:
        """
        List all orders in the database
        
        Returns:
            List[Tuple[int, int, int, float, str]]: List of order details
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, cliente_id, menu_id, total, fecha FROM pedidos')
            return cursor.fetchall()

    def actualizar_pedido(self, id: int, cliente_id: int = None, menu_id: int = None, 
                           total: float = None, fecha: str = None):
        """
        Update order information
        
        Args:
            id (int): Order's ID
            cliente_id (int, optional): New client ID
            menu_id (int, optional): New menu ID
            total (float, optional): New total
            fecha (str, optional): New date
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            updates = []
            params = []
            
            if cliente_id is not None:
                updates.append('cliente_id = ?')
                params.append(cliente_id)
            
            if menu_id is not None:
                updates.append('menu_id = ?')
                params.append(menu_id)
            
            if total is not None:
                updates.append('total = ?')
                params.append(total)
            
            if fecha is not None:
                updates.append('fecha = ?')
                params.append(fecha)
            
            if updates:
                query = f'UPDATE pedidos SET {", ".join(updates)} WHERE id = ?'
                params.append(id)
                
                cursor.execute(query, tuple(params))
                conn.commit()

    def eliminar_pedido(self, id: int):
        """
        Delete an order from the database
        
        Args:
            id (int): Order's ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM pedidos WHERE id = ?', (id,))
            conn.commit()

    def obtener_pedidos_por_cliente(self, cliente_id: int) -> List[Tuple[int, int, int, float, str]]:
        """
        Retrieve all orders for a specific client
        
        Args:
            cliente_id (int): Client's ID
        
        Returns:
            List[Tuple[int, int, int, float, str]]: List of order details
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, cliente_id, menu_id, total, fecha 
                FROM pedidos 
                WHERE cliente_id = ?
            ''', (cliente_id,))
            return cursor.fetchall()

    def obtener_total_ventas_por_fecha(self, fecha: str) -> float:
        """
        Calculate total sales for a specific date
        
        Args:
            fecha (str): Date in 'YYYY-MM-DD' format
        
        Returns:
            float: Total sales for the given date
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(total) 
                FROM pedidos 
                WHERE date(fecha) = ?
            ''', (fecha,))
            return cursor.fetchone()[0] or 0.0


    def listar_pedidos_con_cliente(self) -> List[Tuple[int, str, str, float]]:
        """
        List all orders with client names
        
        Returns:
            List[Tuple[int, str, str, float]]: List of order details (id, client name, date, total)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, c.nombre, p.fecha, p.total 
                FROM pedidos p
                JOIN clientes c ON p.cliente_id = c.id
            ''')
            return cursor.fetchall()

    def listar_pedidos_por_cliente(self, cliente_nombre: str) -> List[Tuple[int, str, str, float]]:
        """
        Retrieve orders for a specific client by name
        
        Args:
            cliente_nombre (str): Client's name
        
        Returns:
            List[Tuple[int, str, str, float]]: List of order details (id, client name, date, total)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, c.nombre, p.fecha, p.total 
                FROM pedidos p
                JOIN clientes c ON p.cliente_id = c.id
                WHERE c.nombre = ?
            ''', (cliente_nombre,))
            return cursor.fetchall()