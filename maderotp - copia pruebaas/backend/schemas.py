from pydantic import BaseModel, EmailStr

# Esquema para los datos de la persona
class PersonaBase(BaseModel):
    nombre: str
    telefono: str
    email: EmailStr
    direccion: str

# Esquema para los datos de la reserva
class ReservaBase(BaseModel):
    fecha: str
    hora: str
    personas: int
    ubicacion: str
    tipo_pedido: str

# Esquema para el formulario combinado
class ReservaCompleta(BaseModel):
    persona: PersonaBase
    reserva: ReservaBase