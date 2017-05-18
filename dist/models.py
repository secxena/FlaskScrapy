from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasktaskr.db'
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.


class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self,name=None, email = None,password=None):
        self.name = name
        self.password = password
        self.email = email



# Create tables.
Base.metadata.create_all(bind=engine)
