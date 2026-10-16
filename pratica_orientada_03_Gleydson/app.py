from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import Base, SessionLocal, engine
from models import Livro, Usuario

app = Flask(__name__)
Base.metadata.create_all(engine)


@app.route('/')
def index():
    with SessionLocal() as session:
        usuarios = session.scalars(select(Usuario)).all()
        livros = session.scalars(
            select(Livro).options(joinedload(Livro.usuario))
        ).all()

    return render_template(
        'index.html',
        usuarios=usuarios,
        livros=livros
    )

@app.route('/usuario/novo', methods=['POST', 'GET'])
def form_usuario():
    if request.method == 'POST':
        usuario = Usuario(
            nome=request.form.get('nome'),
            email=request.form.get('email')
        )
        with SessionLocal() as session:
            session.add(usuario)
            session.commit()
        return redirect(url_for('index'))
    return render_template('form_usuario.html')


@app.route('/livros/novo', methods=['GET', 'POST'])
def form_livro():
    with SessionLocal() as session:
        usuarios = session.scalars(select(Usuario).order_by(Usuario.nome)).all()
        if request.method == 'POST':
            livro = Livro(
                titulo=request.form.get('titulo'),
                id_usuario=int(request.form.get('usuario_id'))
)
            session.add(livro)
            session.commit()
            return redirect(url_for('index'))
    return render_template('form_livro.html', usuarios=usuarios)

@app.route('/livros/listar', methods=['GET'])
def listar_livros():
    with SessionLocal() as session:
        livros = session.scalars(
            select(Livro).order_by(Livro.titulo)
        ).all()

        usuarios = session.scalars(
            select(Usuario).order_by(Usuario.nome)
        ).all()

    return render_template(
        'index.html',
        usuarios=usuarios,
        livros=livros
    )

@app.route('/usuarios/listar', methods=['GET'])
def listar_usuarios():
    with SessionLocal() as session:
        usuarios = session.scalars(
            select(Usuario).order_by(Usuario.nome)
        ).all()

        livros = session.scalars(
            select(Livro).order_by(Livro.titulo)
        ).all()

    return render_template(
        'index.html',
        usuarios=usuarios,
        livros=livros
    )
        
if __name__ == "__main__":
    app.run(debug=True)