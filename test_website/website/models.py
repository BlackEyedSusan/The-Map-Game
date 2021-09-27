from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import random


from . import db

#this is where the databases get the values that they will hold. All of them have to
#have a primary key, which is how it tells the entries apart. This is why all of them
#have an id column (its only ok to overwrite a keyword here because its in a class that
#doesn't need it. its still not the best practice)
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(25))
    #The number is to tell it the max length of the string.
    code = db.Column(db.String(10))
    host = db.Column(db.Integer, db.ForeignKey('user.id'))


class GamesJoined(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.Column(db.Integer, db.ForeignKey('user.id'))


class Empires(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    color = db.Column(db.String(7))
    #You can use foreign keys to relate tables together
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))