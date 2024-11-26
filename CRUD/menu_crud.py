import sqlite3
from typing import List, Tuple, Optional

class MenuCRUD:
    def __init__(self, db_path: str = 'restaurante.db'):
        """
        Initialize the MenuCRUD with a database connection
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """
        Create the menus and menu_ingredientes tables if they don't exist
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Tabla de menús
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menus (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    descripcion TEXT NOT NULL
                )
            ''')
            
            # Tabla de ingredientes en menús
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_ingredientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    menu_id INTEGER,
                    ingrediente_id INTEGER,
                    cantidad REAL NOT NULL,
                    FOREIGN KEY (menu_id) REFERENCES menus (id),
                    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes (id)
                )
            ''')
            conn.commit()

    def crear_menu(self, nombre: str, descripcion: str, ingredientes: List[Tuple[int, float]]) -> int:
        """
        Create a new menu with its ingredients
        
        Args:
            nombre (str): Menu name
            descripcion (str): Menu description
            ingredientes (List[Tuple[int, float]]): List of (ingrediente_id, cantidad)
        
        Returns:
            int: ID of the newly created menu
        
        Raises:
            sqlite3.IntegrityError: If menu name already exists
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Insertar menú
            cursor.execute('''
                INSERT INTO menus (nombre, descripcion) 
                VALUES (?, ?)
            ''', (nombre, descripcion))
            menu_id = cursor.lastrowid
            
            # Insertar ingredientes del menú
            for ingrediente_id, cantidad in ingredientes:
                cursor.execute('''
                    INSERT INTO menu_ingredientes (menu_id, ingrediente_id, cantidad) 
                    VALUES (?, ?, ?)
                ''', (menu_id, ingrediente_id, cantidad))
            
            conn.commit()
            return menu_id

    def obtener_menu(self, id: int) -> Optional[Tuple[int, str, str]]:
        """
        Retrieve a menu by its ID
        
        Args:
            id (int): Menu's ID
        
        Returns:
            Optional[Tuple[int, str, str]]: Menu details or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, descripcion FROM menus WHERE id = ?', (id,))
            return cursor.fetchone()

    def listar_menus(self) -> List[Tuple[int, str, str]]:
        """
        List all menus in the database
        
        Returns:
            List[Tuple[int, str, str]]: List of menu details
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, descripcion FROM menus')
            return cursor.fetchall()

    def obtener_ingredientes_menu(self, menu_id: int) -> List[Tuple[int, str, float]]:
        """
        Get ingredients for a specific menu without price information.
        
        Args:
            menu_id (int): Menu's ID
        
        Returns:
            List[Tuple[int, str, float]]: List of (ingrediente_id, nombre_ingrediente, cantidad)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT mi.ingrediente_id, i.nombre, mi.cantidad
                FROM menu_ingredientes mi
                JOIN ingredientes i ON mi.ingrediente_id = i.id
                WHERE mi.menu_id = ?
            ''', (menu_id,))
            return cursor.fetchall()


    def actualizar_menu(self, id: int, nombre: str = None, descripcion: str = None, 
                         ingredientes: List[Tuple[int, float]] = None):
        """
        Update menu information and its ingredients
        
        Args:
            id (int): Menu's ID
            nombre (str, optional): New name
            descripcion (str, optional): New description
            ingredientes (List[Tuple[int, float]], optional): New list of ingredients
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Actualizar detalles del menú
            if nombre or descripcion:
                updates = []
                params = []
                
                if nombre:
                    updates.append('nombre = ?')
                    params.append(nombre)
                
                if descripcion:
                    updates.append('descripcion = ?')
                    params.append(descripcion)
                
                query = f'UPDATE menus SET {", ".join(updates)} WHERE id = ?'
                params.append(id)
                
                cursor.execute(query, tuple(params))
            
            # Actualizar ingredientes si se proporcionan
            if ingredientes is not None:
                # Primero eliminar ingredientes existentes
                cursor.execute('DELETE FROM menu_ingredientes WHERE menu_id = ?', (id,))
                
                # Insertar nuevos ingredientes
                for ingrediente_id, cantidad in ingredientes:
                    cursor.execute('''
                        INSERT INTO menu_ingredientes (menu_id, ingrediente_id, cantidad) 
                        VALUES (?, ?, ?)
                    ''', (id, ingrediente_id, cantidad))
            
            conn.commit()

    def eliminar_menu(self, id: int):
        """
        Delete a menu from the database
        
        Args:
            id (int): Menu's ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Eliminar primero los ingredientes asociados
            cursor.execute('DELETE FROM menu_ingredientes WHERE menu_id = ?', (id,))
            # Luego eliminar el menú
            cursor.execute('DELETE FROM menus WHERE id = ?', (id,))
            conn.commit()

    def obtener_menu_por_nombre(self, nombre: str) -> Optional[Tuple[int, str, str, float]]:
        """
        Get menu details by name, including price.
        
        Args:
            nombre (str): Menu's name
        
        Returns:
            Optional[Tuple[int, str, str, float]]: Menu details (id, name, description, price).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, nombre, descripcion, precio 
                FROM menus 
                WHERE nombre = ?
            ''', (nombre,))
            return cursor.fetchone()
