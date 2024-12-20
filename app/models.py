from pydantic import BaseModel
from typing import List, Optional


class Livro(BaseModel):
    titulo: str
    autores: List[str]
    ano_publicacao: int
    generos: List[str]
    copias_disponiveis: int
    copias_totais: int


class Usuario(BaseModel):
    nome: str
    email: str
    livros_emprestados: Optional[List[dict]] = []


class Emprestimo(BaseModel):
    id_usuario: str
    id_livro: str
    data_emprestimo: str
    data_devolucao: str
