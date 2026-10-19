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