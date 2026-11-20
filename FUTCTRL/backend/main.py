from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import database
import models

# Crea automáticamente las tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="MatchMind API", version="1.0")

# Permitir conexiones desde cualquier origen para que tus páginas HTML funcionen sin problemas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo o nombre de usuario ya está registrado.")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password + "_secure_hash"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario registrado con éxito", "username": new_user.username}

@app.post("/api/auth/login")
def login(credentials: UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos.")
    
    return {"message": "Inicio de sesión exitoso", "username": db_user.username, "role": db_user.role}

@app.get("/api/matches")
def get_matches(db: Session = Depends(database.get_db)):
    matches = db.query(models.Match).all()
    if not matches:
        # Crear datos de demostración iniciales si la tabla está vacía
        t1 = models.Team(name="Real Demo CF", is_demo=True)
        t2 = models.Team(name="Atlético Ficticio", is_demo=True)
        db.add_all([t1, t2])
        db.commit()
        
        m = models.Match(
            home_team_id=t1.id,
            away_team_id=t2.id,
            competition="Liga Demo MatchMind",
            status="upcoming"
        )
        db.add(m)
        db.commit()
        matches = [m]
    return matches