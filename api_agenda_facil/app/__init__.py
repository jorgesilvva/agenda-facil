#Modulos do Flask
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

@app.template_filter('cadastrado.data')
def format_datetime(value):
    return value.strptime('%d/%m/%Y')
