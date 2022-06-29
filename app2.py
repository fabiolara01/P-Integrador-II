from flask import Flask, render_template, request, url_for, flash, redirect
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app2 = Flask(__name__)
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app2.config['SECRET_KEY'] = 'your secret key'
app2.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app2)

class Cadastros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    nome = db.Column(db.String(80), nullable=True)
    contato = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(150), nullable=False)
    cidade = db.Column(db.String(150), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    servico = db.Column(db.String(30), nullable=False)
    conteudo = db.Column(db.String(500), nullable=True)
    numero = db.Column(db.Integer, nullable=True)
    tipo = db.Column(db.CHAR, nullable=False, default='A')
    nota = db.Column(db.Integer, nullable=False, default='0')

@app2.route('/')
@app2.route('/index')
def index():
    return render_template('index.html')

@app2.route('/dashboard')
def dashboard():
    reg = Cadastros.query.all()
    return render_template('dashboard.html', cadastro=reg)

@app2.route('/localizar', methods=('GET', 'POST'))
def localizar():
    reg = Cadastros.query.all()
    if request.method == 'POST':
        filtro = request.form['servico']
        cad = Cadastros.query.filter_by(servico=filtro).all()
        return render_template('localizei.html', cadastro=cad)
    return render_template('localizar.html', cadastro=reg)

@app2.route('/localizei')
def localizei():
    return render_template('localizei.html')

@app2.route('/<int:id>')
def exibir(id):
    reg = get_cad(id)
    return render_template('exibe.html', cadastro=reg)

@app2.route('/exibe', methods=('GET', 'POST'))
def exibe():
    return render_template('exibe.html')

@app2.route('/<int:id>/score', methods=('GET', 'POST'))
def score(id):
    reg = get_cad(id)
    if request.method == 'POST':
        n_nota = float(reg.nota)
        n_numero = (reg.numero)
        new_nota = float(request.form['nota'])
        if not new_nota:
            flash('Nome é obrigatório')
        else:
            if n_numero is None:
                n_numero = float(0)
                numero = (n_numero + 1)
                nota = ((n_nota * n_numero) + new_nota) / numero
            else:
                numero = (n_numero + 1)
                nota = ((n_nota * n_numero) + new_nota) / numero
            reg.nota = nota
            reg.numero = numero
            db.session.commit()
        return redirect(url_for('exibir', id=id))
    return render_template('score.html', edicao=reg)

@app2.route('/busca', methods=('GET', 'POST'))
def busca():
    if request.method == 'POST':
        n_id = request.form['id']
        n_email = request.form['email']
        padrao = Cadastros.query.filter_by(id=n_id).first()
        reg = Cadastros.query.filter_by(email=n_email).first()
        if not n_email:
            flash('Campo de preenchimento obrigatório')
        else:
            if padrao is None and reg is None:
                return redirect(url_for('create', id=n_id, email=n_email))
            else:
                return render_template('buscar.html')
    return render_template('busca.html')

@app2.route('/create/<int:id>/<string:email>', methods=('GET', 'POST'))
def create(id, email):
    if request.method == 'POST':
        new_id = id
        new_nome = request.form['nome']
        new_contato = request.form['contato']
        new_email = email
        new_cidade = request.form['cidade']
        new_estado = request.form['estado']
        new_servico = request.form['servico']
        new_conteudo = request.form['conteudo']
        if not new_email or not new_servico:
            flash('Campo de preenchimento obrigatório')
        else:
            new_cadastro = Cadastros(id=new_id, nome=new_nome, contato=new_contato, email=new_email, cidade=new_cidade, estado=new_estado, servico=new_servico, conteudo=new_conteudo)
            db.session.add(new_cadastro)
            db.session.commit()
            return render_template('confirmacao.html')
    return render_template('create.html')

def get_cad(cad_id):
    cad = Cadastros.query.filter_by(id=cad_id).first()
    if cad is None:
        abort(404)
    return cad

@app2.route('/buscar', methods=('GET', 'POST'))
def buscar():
    if request.method == 'POST':
        n_id = request.form['id']
        n_email = request.form['email']
        padrao = Cadastros.query.filter_by(id=n_id).first()
        if not n_email:
            flash('Campo de preenchimento obrigatório')
        else:
            if padrao is None:
                flash('Usuário não cadastrado')
                return render_template('busca.html')
            else:
                if n_email == padrao.email:
                    return redirect(url_for('consultar', id=n_id))
    return render_template('buscar.html')

@app2.route('/consultar/<int:id>')
def consultar(id):
    reg = get_cad(id)
    return render_template('consulta.html', cadastro=reg)

@app2.route('/editar/<int:id>', methods=('GET', 'POST'))
def edit(id):
    padrao = get_cad(id)
    if request.method == 'POST':
        n_id = id
        n_nome = request.form['nome']
        n_contato = request.form['contato']
        n_email = request.form['email']
        n_cidade = request.form['cidade']
        n_estado = request.form['estado']
        n_servico = request.form['servico']
        n_conteudo = request.form['conteudo']

        if not n_email:
            flash('E-mail é obrigatório')
        else:
            padrao.nome = n_nome
            padrao.contato = n_contato
            padrao.email = n_email
            padrao.cidade = n_cidade
            padrao.estado = n_estado
            padrao.servico = n_servico
            padrao.conteudo = n_conteudo
            db.session.commit()
            return redirect(url_for('consultar', id=n_id))
    return render_template('edit.html', edicao=padrao)

@app2.route('/editar/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    cad = get_cad(id)
    db.session.delete(cad)
    db.session.commit()
    return render_template('confirmacao.html')

@app2.route('/confirmacao')
def confirmacao():
    return render_template('confirmacao.html')