from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
import database
import models
import schemas # Importar el nuevo archivo

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Madero"}

# =================== NUEVO ENDPOINT COMBINADO ===================
@app.post("/reservas-completas")
def crear_reserva_completa(datos: schemas.ReservaCompleta):
    db: Session = database.SessionLocal()
    try:
        # 1. Buscar si la persona ya existe por su email
        persona = db.query(models.Persona).filter(models.Persona.email == datos.persona.email).first()
        
        # 2. Si no existe, crearla
        if not persona:
            persona = models.Persona(**datos.persona.model_dump())
            db.add(persona)
            db.commit()
            db.refresh(persona)

        # 3. Crear la reserva con el ID de la persona
        # Usamos model_dump() para convertir el Pydantic a dict
        nueva_reserva = models.Reserva(
            **datos.reserva.model_dump(),
            persona_id=persona.id # Asignamos el ID
        )
        db.add(nueva_reserva)
        db.commit()
        db.refresh(nueva_reserva)
        
        return {"status": "Reserva completa registrada con éxito"}
    
    except Exception as e:
        db.rollback() # Deshacer cambios si algo falla
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    finally:
        db.close()

# =================== RUTAS ANTERIORES ===================
# (Dejamos las rutas GET, pero quitamos las POST que ya no usamos)

@app.get("/personas")
def listar_personas():
    db: Session = database.SessionLocal()
    personas = db.query(models.Persona).all()
    db.close()
    return personas

@app.get("/reservas")
def listar_reservas():
    db: Session = database.SessionLocal()
    reservas = db.query(models.Reserva).options(
        joinedload(models.Reserva.persona),
        joinedload(models.Reserva.platos)
    ).all()
    db.close()
    return reservas

@app.get("/platos")
def listar_platos():
    db: Session = database.SessionLocal()
    platos = db.query(models.Plato).all()
    db.close()
    return platos