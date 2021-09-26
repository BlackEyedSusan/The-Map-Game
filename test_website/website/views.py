from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Game, GamesJoined, User
import random
import string
from . import db

letters = string.ascii_letters

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    game = []
    for games in db.session.query(GamesJoined).filter_by(user = current_user.id):
        id = games.game
        for filtered in db.session.query(Game).filter_by(id = id):
            links = (filtered, url_for('rooms.room', game_id=id))
            game.append(links)
        
    return render_template("home.html", user=current_user, games_joined = game)

@views.route('/deceit')
@login_required
def deceit():
    return render_template("deceit.html", user=current_user)

@views.route('/join-game', methods=["GET", "POST"])
@login_required
def join_game():
    if request.method == "POST":
        code = request.form.get("code")
        print(code)
        check = db.session.query(Game).filter_by(code=code).first()
        if check:
            db.session.add(GamesJoined(user=current_user.id, game=check.id))
            db.session.commit()
            flash('Game Joined!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect Code.', category='error')
    return render_template("join_game.html", user=current_user)

@views.route('/create-game', methods=["GET", "POST"])
@login_required
def create_game():
    if request.method == "POST":
        code = (''.join(random.choice(letters) for i in range(6)))
        username = current_user.username
        name = request.form.get('game_name')
        if len(name) < 4:
            flash('The game room\'s name must be at least 4 characters.', category='error')
        else:
            game = Game.query.filter_by(code=code).first()
            new_game = Game(game_name=name, code=code, host=current_user.id)
            db.session.add(new_game)
            db.session.commit()
            game = Game.query.filter_by(code=code).first()
            db.session.add(GamesJoined(user=current_user.id, game=game.id))
            db.session.commit()
            flash('Game Created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("create_game.html", user=current_user)