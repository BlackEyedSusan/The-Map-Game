from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import random

from . import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(25))
    code = db.Column(db.String(10))


class GamesJoined(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.Column(db.Integer, db.ForeignKey('user.id'))


class Empires(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    empire = db.relationship('Empires')