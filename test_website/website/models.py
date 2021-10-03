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
    is_started = db.Column(db.String(5))
    code = db.Column(db.String(10), unique=True)
    host = db.Column(db.Integer, db.ForeignKey('user.id'))


class GamesJoined(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.Column(db.Integer, db.ForeignKey('user.id'))


class Empires(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    color = db.Column(db.String(7))
    gov = db.Column(db.String(50))
    #You can use foreign keys to relate tables together
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))


class Territories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    owner = db.Column(db.Integer)
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
    pop = db.Column(db.Integer)
    gdp = db.Column(db.Integer)
    area = db.Column(db.Integer)
    oil = db.Column(db.String(5))
    uranium = db.Column(db.String(5))
    gold = db.Column(db.String(5))
    biome = db.Column(db.String(20))


class Military(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('empires.id'))
    location = db.Column(db.Integer, db.ForeignKey('territories.id'))
    category = db.Column(db.String(9))
    type = db.Column(db.String(15))
    amount = db.Column(db.Integer)


class Wars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attacker = db.Column(db.Integer, db.ForeignKey('empires.id'))
    defender = db.Column(db.Integer, db.ForeignKey('empires.id'))


class Alliances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empire1 = db.Column(db.Integer, db.ForeignKey('empires.id'))
    empire2 = db.Column(db.Integer, db.ForeignKey('empires.id'))


class Puppets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    controller = db.Column(db.Integer, db.ForeignKey('empires.id'))
    puppet = db.Column(db.Integer, db.ForeignKey('empires.id'))


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'))


class Diplo_Reqs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('empires.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('empires.id'))
    type = db.Column(db.String(10))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))