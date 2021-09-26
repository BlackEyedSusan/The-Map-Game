from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from .models import Game, GamesJoined, User, Empires
from . import db
import sqlite3 as dbapi
import json

rooms = Blueprint('rooms', __name__)

@rooms.route('<int:game_id>', methods=["GET", "POST"])
@login_required
def room(game_id):
    if request.method == "POST":
        empire = request.form.get('empire')
        empire_query = Empires.query.filter_by(name=empire)
        if empire_query == empire:
            flash('That empire name is in use.', category='error')
        elif len(empire) < 1:
            flash('You cannot leave the empire name blank.', category='error')
        elif len(empire) > 200:
            flash('The max empire name length is 199 characters.', category='error')
        else:
            new_empire = Empires(name=empire, user=current_user.id, game=game_id)
            empire_query = Empires.query.filter_by(game=game_id, user=current_user.id).first()
            if empire_query:
                db.session.delete(Empires.query.get(empire_query.id))
                db.session.commit()
                db.session.add(new_empire)
                db.session.commit()
            else:
                db.session.add(new_empire)
                db.session.commit()
    colors = [['#000000', 'Black'], ['#000080', 'Navy'], ['#FFFF00', "Orange"], ['#FFFFFFF', "White"]]
    players = []
    players_output = []
    empires = {}
    empire_colors = []
    id = game_id
    for games in db.session.query(Game).filter_by(id = game_id):
        name = games.game_name
        if current_user.id == games.host:
            is_host = True
        else:
            is_host = False
    for filtered in db.session.query(GamesJoined).filter_by(game = game_id):
        players.append(filtered.user)
    for player in players:
        for result in db.session.query(User).filter_by(id=player):
            players_output.append([result, url_for('profiles.profile', user_id=result.id)])
    for empire in db.session.query(Empires).filter_by(game=id):
        empires[f"{empire.user}"]=empire.name
        empire_colors.append(empire.color)
    empire_key = [empires]
    return render_template("room.html", user=current_user, players = players_output, game = name, game_id = id, empire_key=empires, is_host=is_host, used_colors=empire_colors, colors=colors)

@rooms.route('<int:game_id>/<empire>', methods=['PUT'])
def update_empire(game_id, empire):
    pass


@rooms.route('<int:game_id>/map')
@login_required
def map(game_id):
    players = []
    players_output = []
    for games in db.session.query(Game).filter_by(id = game_id):
        name = games.game_name
    for filtered in db.session.query(GamesJoined).filter_by(game = game_id):
        players.append(filtered.user)
    for player in players:
        for result in db.session.query(User).filter_by(id=player):
            players_output.append(result)
    return render_template('map.html', user=current_user, game = name)
