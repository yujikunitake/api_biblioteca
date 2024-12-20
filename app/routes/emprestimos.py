from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Emprestimo
from bson import ObjectId
from datetime import datetime, timedelta


router = APIRouter()

@router.post("/emprestar")
def emprestar_livro(emprestimo: Emprestimo):
    usuario = db.usuarios.find_one({"_id": ObjectId(emprestimo.id_usuario)})
    livro = db.livros.find_one({"_id": ObjectId(emprestimo.id_livro)})

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not livro or livro["copias_disponiveis"] < 1:
        raise HTTPException(status_code=404, detail="Livro não disponível")
    
    db.livros.update_one(
        {"_id": ObjectId(emprestimo.id_livro)}, 
        {"$inc": {"copias_disponiveis": -1}}
        )

    db.usuarios.update_one(
        {"_id": ObjectId(emprestimo.id_usuario)},
        {"$push": {"livros_emprestados": {"id_livro": emprestimo.id_livro, "data_emprestimo": emprestimo.data_emprestimo, "data_devolucao": emprestimo.data_devolucao}}}
        )
    
    return {"message", "Empréstimo registrado com sucesso"}

@router.post("/devolver")
def devolver_livro(emprestimo: Emprestimo):
    usuario = db.usuarios.find_one({"_id": ObjectId(emprestimo.id_usuario)})
    livro = db.livros.find_one({"_id": ObjectId(emprestimo.id_livro)})

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    db.livros.update_one(
        {"_id": ObjectId(emprestimo.id_livro)}, 
        {"$inc": {"copias_disponiveis": 1}}
        )

    db.usuarios.update_one(
        {"_id": ObjectId(emprestimo.id_usuario)},
        {"$pull", {"livros_emprestados": {"id_livro": emprestimo.id_livro}}}
    )

    return {"message", "Livro devolvido com sucesso"}
