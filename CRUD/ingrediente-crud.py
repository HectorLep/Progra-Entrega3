import sqlite3
from typing import List, Tuple, Optional

class IngredienteCRUD:
    def __init__(self, db_path: str = 'restaurante.db'):
        """
        Initialize the IngredienteCRUD with a database connection
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        """
        Create the ingredientes table if it doesn't exist
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ingredientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    tipo TEXT NOT NULL,
                    cantidad REAL NOT NULL,
                    unidad_medida TEXT NOT NULL
                )
            ''')
            conn.commit()

    def crear_ingrediente(self, nombre: str, tipo: str, cantidad: float, unidad_medida: str) -> int:
        """
        Create a new ingredient in the database
        
        Args:
            nombre (str): Ingredient name
            tipo (str): Ingredient type
            cantidad (float): Quantity in stock
            unidad_medida (str): Unit of measurement
        
        Returns:
            int: ID of the newly created ingredient
        
        Raises:
            sqlite3.IntegrityError: If ingredient name already exists
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ingredientes (nombre, tipo, cantidad, unidad_medida) 
                VALUES (?, ?, ?, ?)
            ''', (nombre, tipo, cantidad, unidad_medida))
            conn.commit()
            return cursor.lastrowid

    def obtener_ingrediente(self, id: int) -> Optional[Tuple[int, str, str, float, str]]:
        """
        Retrieve an ingredient by its ID
        
        Args:
            id (int): Ingredient's ID
        
        Returns:
            Optional[Tuple[int, str, str, float, str]]: Ingredient details or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, tipo, cantidad, unidad_medida FROM ingredientes WHERE id = ?', (id,))
            return cursor.fetchone()

    def listar_ingredientes(self) -> List[Tuple[int, str, str, float, str]]:
        """
        List all ingredients in the database
        
        Returns:
            List[Tuple[int, str, str, float, str]]: List of ingredient details
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, tipo, cantidad, unidad_medida FROM ingredientes')
            return cursor.fetchall()

    def actualizar_ingrediente(self, id: int, nombre: str = None, tipo: str = None, 
                                cantidad: float = None, unidad_medida: str = None):
        """
        Update ingredient information
        
        Args:
            id (int): Ingredient's ID
            nombre (str, optional): New name
            tipo (str, optional): New type
            cantidad (float, optional): New quantity
            unidad_medida (str, optional): New unit of measurement
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            updates = []
            params = []
            
            if nombre:
                updates.append('nombre = ?')
                params.append(nombre)
            
            if tipo:
                updates.append('tipo = ?')
                params.append(tipo)
            
            if cantidad is not None:
                updates.append('cantidad = ?')
                params.append(cantidad)
            
            if unidad_medida:
                updates.append('unidad_medida = ?')
                params.append(unidad_medida)
            
            if updates: