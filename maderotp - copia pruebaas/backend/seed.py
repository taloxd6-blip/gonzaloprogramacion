from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models  # Importará los modelos actualizados, incluyendo DetalleReserva
from faker import Faker
import random

# Inicializar Faker para datos de prueba
fake = Faker('es_ES') 

def seed_database():
    db: Session = SessionLocal()
    
    # 1. Verificar si la base de datos ya tiene datos
    if db.query(models.Persona).count() > 0:
        print("La base de datos ya contiene datos. No se agregarán nuevos.")
        db.close()
        return

    print("Poblando la base de datos con datos de prueba...")

    # 2. Crear 10 Personas
    personas = []
    for _ in range(10):
        persona = models.Persona(
            nombre=fake.name(),
            telefono=fake.phone_number(),
            email=fake.email(),
            direccion=fake.address()
        )
        personas.append(persona)
    db.add_all(personas)
    db.commit()
    print(f"Se crearon {len(personas)} personas.")

    # 3. Crear 10 Platos
    nombres_platos = [
        "Milanesa Napolitana", "Bife de Chorizo", "Pastel de Papas",
        "Empanadas (docena)", "Asado de Tira", "Pollo al Ajillo",
        "Ensalada César", "Parrillada (2 pers.)", "Ñoquis con Estofado",
        "Ravioles de Ricota"
    ]
    platos = []
    for nombre in nombres_platos:
        plato = models.Plato(
            nombre=nombre,
            descripcion=fake.sentence(nb_words=6),
            precio=round(random.uniform(5000, 15000), 2)
        )
        platos.append(plato)
    db.add_all(platos)
    db.commit()
    print(f"Se crearon {len(platos)} platos.")

    # 4. Crear 15 Reservas (más de 10)
    reservas = []
    ubicaciones = ["adentro", "afuera"]
    tipos = ["Almuerzo", "Cena"]
    ocasiones = ["Cumpleaños", "Aniversario", "Reunión de negocios"]
    
    for i in range(15):
        persona = random.choice(personas)
        
        reserva = models.Reserva(
            persona_id=persona.id,
            fecha=fake.date_between(start_date='-1w', end_date='+1w').isoformat(),
            hora=fake.time(),
            personas=random.randint(1, 6),
            ubicacion=random.choice(ubicaciones),
            tipo_pedido=random.choice(tipos)
        )
        
        platos_asignados = random.sample(platos, k=random.randint(1, 3))
        reserva.platos.extend(platos_asignados)
        
        # --- BLOQUE NUEVO (AÑADIDO) ---
        # Añadir un detalle aleatorio (aprox. 50% de las veces)
        if random.random() < 0.5:
            detalle = models.DetalleReserva(
                ocasion=random.choice(ocasiones),
                nota_especial=f"Mesa para {reserva.personas}, {fake.sentence(nb_words=3)}"
            )
            # Así se crea la relación 1-a-1
            reserva.detalle = detalle
        
        reservas.append(reserva)

    # El 'cascade' en el modelo se encarga de guardar los detalles
    db.add_all(reservas)
    db.commit()
    print(f"Se crearon {len(reservas)} reservas (y algunos detalles).")

    db.close()

if __name__ == "__main__":
    print("Creando tablas (si no existen)...")
    # Esto crea TODAS las tablas nuevas (incluyendo DetalleReserva)
    models.Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")
    
    seed_database()