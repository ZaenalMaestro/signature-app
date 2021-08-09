from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.secret_key = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:''@localhost/digital_signature'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from core import routes