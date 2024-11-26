import sqlite3
from typing import List, Tuple, Optional

class ClienteCRUD:
    def __init__(self, db_path: str = 'restaurante.db'):
        """
        Initialize the ClienteCRUD with a database connection
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        """
        Create the clientes table if it doesn't exist
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo_electronico TEXT UNIQUE NOT NULL
                )
            ''')
            conn.commit()

    def crear_cliente(self, nombre: str, correo_electronico: str) -> int:
        """
        Create a new client in the database
        
        Args:
            nombre (str): Client's name
            correo_electronico (str): Client's email
        
        Returns:
            int: ID of the newly created client
        
        Raises:
            sqlite3.IntegrityError: If email already exists
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clientes (nombre, correo_electronico) 
                VALUES (?, ?)
            ''', (nombre, correo_electronico))
            conn.commit()
            return cursor.lastrowid

    def obtener_cliente(self, id: int) -> Optional[Tuple[int, str, str]]:
        """
        Retrieve a client by their ID
        
        Args:
            id (int): Client's ID
        
        Returns:
            Optional[Tuple[int, str, str]]: Client details or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, correo_electronico FROM clientes WHERE id = ?', (id,))
            return cursor.fetchone()

    def listar_clientes(self) -> List[Tuple[int, str, str]]:
        """
        List all clients in the database
        
        Returns:
            List[Tuple[int, str, str]]: List of client details
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, correo_electronico FROM clientes')
            return cursor.fetchall()

    def actualizar_cliente(self, id: int, nombre: str = None, correo_electronico: str = None):
        """
        Update client information
        
        Args:
            id (int): Client's ID
            nombre (str, optional): New name
            correo_electronico (str, optional): New email
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            updates = []
            params = []
            
            if nombre:
                updates.append('nombre = ?')
                params.append(nombre)
            
            if correo_electronico:
                updates.append('correo_electronico = ?')
                params.append(correo_electronico)
            
            if updates:
                query = f'UPDATE clientes SET {", ".join(updates)} WHERE id = ?'
                params.append(id)
                
                cursor.execute(query, tuple(params))
                conn.commit()

    def eliminar_cliente(self, id: int):
        """
        Delete a client from the database
        
        Args:
            id (int): Client's ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
            conn.commit()

    def buscar_cliente_por_correo(self, correo_electronico: str) -> Optional[Tuple[int, str, str]]:
        """
        Search for a client by email address
        
        Args:
            correo_electronico (str): Client's email
        
        Returns:
            Optional[Tuple[int, str, str]]: Client details or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, correo_electronico FROM clientes WHERE correo_electronico = ?', (correo_electronico,))
            return cursor.fetchone()
