from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabla de asociación (M-a-M) (sin cambios)
reserva_plato_association = Table(
    'reserva_plato_association', Base.metadata,
    Column('reserva_id', Integer, ForeignKey('reservas.id'), primary_key=True),
    Column('plato_id', Integer, ForeignKey('platos.id'), primary_key=True)
)

class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True) # Hacemos email único
    direccion = Column(String, nullable=False)

    # Relación 1-a-M (sin cambios)
    reservas = relationship("Reserva", back_populates="persona")

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    
    # --- LÍNEA ACTUALIZADA ---
    # Ahora es obligatorio (nullable=False)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    
    fecha = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    personas = Column(Integer, nullable=False)
    ubicacion = Column(String, nullable=False)
    tipo_pedido = Column(String, nullable=False)

    # Relaciones (sin cambios)
    persona = relationship("Persona", back_populates="reservas")
    platos = relationship(
        "Plato",
        secondary=reserva_plato_association,
        back_populates="reservas"
    )
    detalle = relationship(
        "DetalleReserva",
        back_populates="reserva",
        uselist=False,
        cascade="all, delete-orphan"
    )

class Plato(Base):
    __tablename__ = "platos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)

    reservas = relationship(
        "Reserva",
        secondary=reserva_plato_association,
        back_populates="platos"
    )

class DetalleReserva(Base):
    __tablename__ = "detalles_reserva"
    id = Column(Integer, primary_key=True, index=True)
    ocasion = Column(String, nullable=True) 
    nota_especial = Column(String, nullable=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    reserva = relationship("Reserva", back_populates="detalle")