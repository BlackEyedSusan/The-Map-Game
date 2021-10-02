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
    current_game = db.session.query(Game).filter_by(id=game_id).first()
    if str(current_game.is_started) == "True":
        return redirect(url_for('rooms.map', game_id=game_id))
    if request.method == "POST":
        if str(request.form.get("start_game")) == "start_game":
            db.session.delete(current_game)
            db.session.commit()
            new_game = Game(code=current_game.code, game_name=current_game.game_name, host=current_game.host, is_started="True")
            db.session.add(new_game)
            db.session.commit()
            return redirect(url_for('rooms.map', game_id=game_id))
        
        if str(request.form.get("update_empire")) == "update_empire":
            empire = request.form.get('empire')
            color = request.form.get('color_input')
            gov = request.form.get('gov')
            empire_query = Empires.query.filter_by(name=empire).first()
            color_query = Empires.query.filter_by(color=color, game=game_id)
            if empire_query != None and (empire_query.name == empire and empire_query.user != current_user.id and empire_query.game == game_id):
                    flash('That empire name is in use.', category='error')
            elif len(empire) < 1:
                flash('You cannot leave the empire name blank.', category='error')
            elif len(empire) > 200:
                flash('The max empire name length is 199 characters.', category='error')
            elif color_query == color:
                flash('That color is in use.', category='error')
            else:
                new_empire = Empires(name=empire, user=current_user.id, game=game_id, color=color, gov=gov)
                empire_query = db.session.query(Empires).filter_by(game=game_id, user=current_user.id).first()
                if empire_query:
                    if empire_query.game == game_id:
                        db.session.delete(Empires.query.get(empire_query.id))
                        db.session.commit()
                        db.session.add(new_empire)
                        db.session.commit()
                else:
                    db.session.add(new_empire)
                    db.session.commit()
                return redirect(url_for('rooms.room', game_id=game_id))
        #this is where all of the colors that can be used for the 
    colors = [['#FF0000', 'Red', 'red'],
             ['#FF4400', 'Neon Orange', 'neon-orange'], 
             ['#FF80000', 'Orange', 'orange'], 
             ['#FFBF00', 'Mustard Yellow', 'mustard-yellow'], 
             ["#FFFF00", 'Yellow', 'yellow'], 
             ['#80FF00', 'Lime Green', 'lime-green'],
             ['#00FF40', 'Neon Green', 'neon-green'],
             ['#00FFBF', 'Aquamarine', 'aquamarine'],
             ['#0080FF', 'Blue', 'blue'],
             ['#0000FF', 'Dark Blue', 'dark-blue'],
             ['#8000FF', 'Purple', 'purple'],
             ['#FF00FF', 'Pink', 'pink'],
             ['#FF0080', 'Salmon', 'salmon']]
    governments = [['Thassalocracy', 'thassalocracy'],
                    ['Monarchy', 'monarchy'],
                    ['Aristocracy', 'aristocracy'],
                    ['Authoritarian Communism', 'authoritarian-communism'],
                    ['Anarchy', 'anarchy'],
                    ['Democracy', 'democracy'],
                    ['Fascism', 'fascism'],
                    ['Theocracy', 'theocracy'],
                    ['Corporate Republic', 'corporate-republic'],
                    ['Military Dictatorship', 'military-dictatorship'],
                    ['Fuedalist Kingdom', 'fuedalist-kingdom'],
                    ['Kleptocracy', 'kleptocracy'],
                    ['Chiefdom', 'chiefdom'],
                    ['Anocracy', 'anocracy'],
                    ]
    players = []
    players_output = []
    #it was just easier to use a dictionary specifically for this one
    empires = {}
    empire_colors = []
    avail_colors = []
    id = game_id
    current_gov = None
    current_color = None
    current_tag = None
    current_empire = "None"
    games = db.session.query(Game).filter_by(id = game_id).first()
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
        if empire.user == current_user.id:
            current_empire = empire
            current_gov = current_empire.gov
            current_color = current_empire.color
        if empire.color != "None":
            fixed_empire_color = str(empire.color).lower().replace(' ', '-')
            empire_colors.append(fixed_empire_color)
        else:
            empire_colors.append('white')
    for color in colors:
        if color[2] == current_color:
            current_tag = color[0]
        if color[2] not in empire_colors:
            avail_colors.append(color)
    avail_colors.append([current_tag, str(current_color).title().replace('-', ' '), current_color])
    return render_template("room.html", user=current_user, players = players_output, game = games, game_id = id, empire_key=empires, is_host=is_host, used_colors=empire_colors, colors=colors, id=id, current_empire=current_empire, avail_colors=avail_colors, current_color=current_color, govs=governments, current_gov=current_gov)


@rooms.route('<int:game_id>/map', methods=['POST', 'GET'])
@login_required
def map(game_id):
    colors = [['#FF0000', 'Red', 'red'],
             ['#FF4400', 'Neon Orange', 'neon-orange'], 
             ['#FF80000', 'Orange', 'orange'], 
             ['#FFBF00', 'Mustard Yellow', 'mustard-yellow'], 
             ["#FFFF00", 'Yellow', 'yellow'], 
             ['#80FF00', 'Lime Green', 'lime-green'],
             ['#00FF40', 'Neon Green', 'neon-green'],
             ['#00FFBF', 'Aquamarine', 'aquamarine'],
             ['#0080FF', 'Blue', 'blue'],
             ['#0000FF', 'Dark Blue', 'dark-blue'],
             ['#8000FF', 'Purple', 'purple'],
             ['#FF00FF', 'Pink', 'pink'],
             ['#FF0080', 'Salmon', 'salmon']]
    players = []
    players_output = []
    empires = {}
    empire_colors = []
    avail_colors = []
    id = game_id
    games = db.session.query(Game).filter_by(id = game_id).first()
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
        if empire.user == current_user.id:
            current_empire = empire
        else:
            current_empire = None
        if empire.color != None:
            fixed_empire_color = str(empire.color).lower().replace(' ', '-')
            empire_colors.append(fixed_empire_color)
        else:
            print('white')
            empire_colors.append('white')
    empire_key = [empires]
    for color in colors:
        if color not in empire_colors:
            avail_colors.append(color)

    return render_template("map.html", user=current_user, players = players_output, game = games, game_id = id, empire_key=empires, is_host=is_host, used_colors=empire_colors, colors=colors, id=id, current_empire=current_empire)