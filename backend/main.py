from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle de données attendu depuis Angular
class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/api/login")
def login(user: UserLogin):
    if user.email == "admin@smartcampus.ma" and user.password == "password123":
        return {"status": "success", "message": "Connexion réussie"}
    
    # Ajout du log de sécurité demandé lors de la revue
    print(f"[ALERTE SÉCURITÉ] Tentative de connexion échouée pour l'e-mail : {user.email}")
    
    raise HTTPException(status_code=401, detail="Mot de passe ou e-mail incorrect")
import os
import psycopg

@app.get("/api/database-check")
def database_check():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise HTTPException(
            status_code=503,
            detail="La variable DATABASE_URL n'est pas définie"
        )

    try:
        with psycopg.connect(database_url, connect_timeout=5) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database()")
                database_name = cursor.fetchone()[0]

        return {
            "status": "success",
            "message": "Connexion à PostgreSQL réussie",
            "database": database_name
        }
    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Connexion à PostgreSQL impossible"
        )