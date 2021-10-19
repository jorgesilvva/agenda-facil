import os
import sqlite3
from flask import Flask, render_template, url_for, request, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

cors = CORS(app, resouce={r'/*':{'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Cadastro(db.Model):

    __tablename__= 'agendamentos'

    _id = db.Column(db.Integer , primary_key=True, autoincrement=True)
    cliente = db.Column(db.String)
    datahora = db.Column(db.String)
    email = db.Column(db.String)
    contato = db.Column(db.String)
    servico = db.Column(db.String)

    def __init__(self, cliente, datahora, email, contato, servico):
        self.cliente = cliente
        self.datahora = datahora
        self.email = email
        self.contato = contato
        self.servico = servico

db.create_all()

@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/botaogendar', methods=['GET','POST'])
def botaoagendar():
        global servico
        if request.method == 'POST':
            servico = request.form.get('contact')
        return render_template('agenda.html')

@app.route('/botaoenviar', methods=['GET','POST'])
def botaoenviar():
    if request.method == 'POST':
        cliente = request.form.get('cliente')
        datahora = request.form.get('datahora')
        email = request.form.get('email')
        contato = request.form.get('contato')
                
        if cliente and datahora and email and contato and servico:
            temp = Cadastro(cliente, datahora, email, contato, servico)
            db.session.add(temp)
            db.session.commit()

    return render_template('final.html')

@app.route('/relatorio')
def relatorio():
    cadastrados = Cadastro.query.all()
    return render_template('relatorio.html', cadastrados=cadastrados)

@app.route('/excluir/<int:id>')
def excluir(id):
    cadastrado = Cadastro.query.filter_by(_id=id).first()

    db.session.delete(cadastrado)
    db.session.commit()

    cadastrados = Cadastro.query.all()
    return render_template('relatorio.html', cadastrados=cadastrados)

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    cadastrado = Cadastro.query.filter_by(_id=id).first()
    
    if request.method == 'POST':
            cliente = request.form.get('cliente')
            datahora = request.form.get('datahora')
            email = request.form.get('email')
            contato = request.form.get('contato')
                
            if cliente and datahora and email and contato:
                cadastrado.cliente = cliente
                cadastrado.datahora = datahora
                cadastrado.email = email
                cadastrado.contato = contato

                db.session.commit()

                return redirect(url_for('relatorio'))

    return render_template('editar.html', cadastrado=cadastrado)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=port, debug=True)
