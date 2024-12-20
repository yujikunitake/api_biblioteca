from fastapi import FastAPI
from app.routes import livros, usuarios, emprestimos


app = FastAPI()

app.include_router(livros.router, prefix="/livros", tags=["Livros"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(emprestimos.router, prefix="/emprestimos", tags=["Emprestimos"])

@app.get("/")
def home():
    return {"message": "Bem-vindo à Biblioteca Digital"}


