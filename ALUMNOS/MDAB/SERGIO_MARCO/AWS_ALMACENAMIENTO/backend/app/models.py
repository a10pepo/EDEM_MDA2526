from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from .database import Base


class Conductor(Base):
    __tablename__ = "conductores"
    id       = Column(Integer, primary_key=True, index=True)
    dni      = Column(String(20), unique=True, nullable=False)
    nombre   = Column(String(100), nullable=False)
    telefono = Column(String(20))


class Vehiculo(Base):
    __tablename__ = "vehiculos"
    id                 = Column(Integer, primary_key=True, index=True)
    matricula          = Column(String(20), unique=True, nullable=False)
    modelo             = Column(String(50), nullable=False)
    capacidad_carga_kg = Column(Numeric(10, 2), nullable=False)
    fecha_itv          = Column(Date, nullable=False)
    estado             = Column(String(20), default="disponible")


class Ruta(Base):
    __tablename__ = "rutas"
    id           = Column(Integer, primary_key=True, index=True)
    vehiculo_id  = Column(Integer, ForeignKey("vehiculos.id"))
    conductor_id = Column(Integer, ForeignKey("conductores.id"))
    origen_lat   = Column(Numeric(9, 6))
    origen_lng   = Column(Numeric(9, 6))
    destino_lat  = Column(Numeric(9, 6))
    destino_lng  = Column(Numeric(9, 6))
    actual_lat   = Column(Numeric(9, 6))
    actual_lng   = Column(Numeric(9, 6))
    estado       = Column(String(20), default="pendiente")


class Pedido(Base):
    __tablename__ = "pedidos"
    id          = Column(Integer, primary_key=True, index=True)
    ruta_id     = Column(Integer, ForeignKey("rutas.id"))
    peso_kg     = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(String(200))
