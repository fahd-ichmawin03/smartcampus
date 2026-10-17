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
    # Simulation d'une vérification en base de données
    if user.email == "admin@smartcampus.ma" and user.password == "password123":
        return {"status": "success", "message": "Connexion réussie"}
    
    raise HTTPException(status_code=401, detail="Mot de passe ou e-mail incorrect")