from sqlalchemy import Column, String, Integer, Float, CheckConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo_electronico = Column(String, unique=True, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente(nombre='{self.nombre}', correo_electronico='{self.correo_electronico}')>"

class Pedido(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id', onupdate="CASCADE"), nullable=False)
    menu_id = Column(Integer, ForeignKey('menus.id', onupdate="CASCADE"), nullable=False)
    total = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)  # New column
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    
    cliente = relationship("Cliente", back_populates="pedidos")
    menu = relationship("Menu", back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido(descripcion='{self.descripcion}', cliente_id={self.cliente_id}, total={self.total}, cantidad={self.cantidad})>"

class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    tipo = Column(String(50), nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad_medida = Column(String(20), nullable=False)

    menus = relationship("MenuIngrediente", back_populates="ingrediente")

    __table_args__ = (
        CheckConstraint('cantidad >= 0', name='cantidad_positiva'),
        CheckConstraint("tipo IN ('Verdura', 'Fruta', 'Carne', 'Lácteo', 'Grano', 'Otro')", name='tipo_valido')
    )

    def __repr__(self):
        return f"<Ingrediente(nombre='{self.nombre}', tipo='{self.tipo}', cantidad={self.cantidad} {self.unidad_medida})>"

class MenuIngrediente(Base):
    __tablename__ = 'menu_ingredientes'
    
    menu_id = Column(Integer, ForeignKey('menus.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    ingrediente_id = Column(Integer, ForeignKey('ingredientes.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    cantidad = Column(Float, nullable=False)
    
    menu = relationship("Menu", back_populates="ingredientes_association")
    ingrediente = relationship("Ingrediente", back_populates="menus")

    def __repr__(self):
        return f"<MenuIngrediente(menu_id={self.menu_id}, ingrediente_id={self.ingrediente_id}, cantidad={self.cantidad})>"

class Menu(Base):
    __tablename__ = 'menus'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    precio = Column(Float)
    cantidad = Column(Integer, default=0)  # Add this line

    
    ingredientes_association = relationship("MenuIngrediente", back_populates="menu", cascade="all, delete-orphan")
    pedidos = relationship("Pedido", back_populates="menu", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('precio >= 0', name='precio_positivo'),
    )

    def __repr__(self):
        return f"<Menu(nombre='{self.nombre}', descripcion='{self.descripcion}', precio={self.precio})>"

    @property
    def ingredientes(self):
        """
        Obtiene la lista de ingredientes asociados al menú
        """
        return [assoc.ingrediente for assoc in self.ingredientes_association]