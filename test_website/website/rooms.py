from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Game, GamesJoined, User
import random
import string
from . import db

rooms = Blueprint('rooms', __name__)

@rooms.route('<int:game_id>')
@login_required
def room(game_id):
    players = []
    players_output = []
    for games in db.session.query(Game).filter_by(id = game_id):
        name = games.game_name
    for filtered in db.session.query(GamesJoined).filter_by(game = game_id):
        players.append(filtered.user)
    for player in players:
        for result in db.session.query(User).filter_by(id=player):
            players_output.append(result)
            print(result)
    return render_template("room.html", user=current_user, players = players_output, game = name)