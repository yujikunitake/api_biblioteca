from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Livro


router = APIRouter()

@router.post("/")
def adicionar_livro(livro: Livro):
    dados_livro = livro.model_dump()
    db.livros.insert_one(dados_livro)
    
    return {"message": "Livro adicionado com sucesso"}

@router.get("/")
def listar_livros():
    livros = list(db.livros.find())
    for livro in livros:
        livro["_id"] = str(livro["_id"])

    return livros

@router.get("/{id_livro}")
def retornar_livro(id_livro: str):
    livro = db.livros.find_one({"_id": ObjectId(id_livro)})
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    livro["_id"] = str(livro["_id"])

    return livro
