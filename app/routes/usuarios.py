from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Usuario
from bson import ObjectId


router = APIRouter()

@router.post("/")
def criar_usuario(usuario: Usuario):
    dados_usuario = usuario.model_dump()
    if db.usuarios.find_one({"email": dados_usuario["email"]}):
        raise HTTPException(status_code=400, detail="Já existe um usuário com esse e-mail cadastrado.")
    db.usuarios.insert_one(dados_usuario)
    
    return {"message", "Usuário criado com sucesso"}

@router.get("/")
def listar_usuarios():
    usuarios = list(db.usuarios.find())
    for usuario in usuarios:
        usuario["_id"] = str(usuario["_id"])
    
    return usuarios

@router.get("/{id_usuario}")
def retornar_usuario(id_usuario: str):
    usuario = db.usuarios.find_one({"_id": ObjectId(id_usuario)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario["_id"] = str(usuario["_id"])

    return usuario
