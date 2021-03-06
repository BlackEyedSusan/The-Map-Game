from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Empires, Friends, Game, GamesJoined, User
import random
import string
from . import db

letters = string.ascii_letters

views = Blueprint('views', __name__)


#the command decorators declare where the path is in relation to the default path for 
#this type of route, and it also declares what methods it can use. (default is only GET)
#You can also set it so you can only access the page if you are logged in.
@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    game = []
    friends = []
    for games in db.session.query(GamesJoined).filter_by(user = current_user.id):
        id = games.game
        for filtered in db.session.query(Game).filter_by(id = id):
            links = (filtered, url_for('rooms.room', game_id=id))
            game.append(links)
    friends1 = db.session.query(Friends).filter_by(user1=current_user.id)
    friends2 = db.session.query(Friends).filter_by(user2=current_user.id)
    for friend in friends1:
        print('worked')
        add = db.session.query(User).filter_by(id=friend.user2).first()
        friends.append(add)
    for friend in friends2:
        add = db.session.query(User).filter_by(id=friend.user1).first()
        friends.append(add)

    #the render template function can take in as many keyword arguments as variables to be used 
    #in the jinja of the html file
    return render_template("home.html", friends=friends, user=current_user, games_joined = game)

@views.route('/deceit')
@login_required
def deceit():
    return render_template("deceit.html", user=current_user)

@views.route('/join-game', methods=["GET", "POST"])
@login_required
def join_game():
    if request.method == "POST":
        code = request.form.get("code")
        #you can query the database with this syntax, and if you don't use first(), you
        #get a list of objects inside the database
        check = db.session.query(Game).filter_by(code=code).first()
        if check:
            amt_players = db.session.query(GamesJoined).filter_by(game=check.id)
            counter = 0
            for player in amt_players:
                counter += 1
            if counter >= 13:
                flash('Game is full.', category='error')
            elif check.is_started == "True":
                flash('Game has already started.', category='error')
            else:
                db.session.add(GamesJoined(user=current_user.id, game=check.id))
                db.session.commit()
                db.session.add(Empires(user=current_user.id, game=check.id))
                db.session.commit()
                flash('Game Joined!', category='success')
                #use url_for() instead of writing the direct url because if the other urls
                #change for whatever reason, it won't break the code.
                return redirect(url_for('views.home'))
        else:
            flash('Incorrect Code.', category='error')
    return render_template("join_game.html", user=current_user)

@views.route('/help')
def rick_roll():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@views.route('/create-game', methods=["GET", "POST"])
@login_required
def create_game():
    if request.method == "POST":
        worked = False
        while worked == False:
            code = (''.join(random.choice(letters) for i in range(6)))
            check = db.session.query(Game).filter_by(code=code).first()
            if check == None:
                worked = True
            elif code != check.code:
                worked = True
        username = current_user.username
        name = request.form.get('game_name')
        if len(name) < 4:
            flash('The game room\'s name must be at least 4 characters.', category='error')
        else:
            game = Game.query.filter_by(code=code).first()
            new_game = Game(game_name=name, code=code, host=current_user.id, is_started="False", draft_pos = 0, ticker = 1)
            db.session.add(new_game)
            db.session.commit()
            game = Game.query.filter_by(code=code).first()
            db.session.add(GamesJoined(user=current_user.id, game=game.id))
            db.session.commit()
            db.session.add(Empires(user=current_user.id, game=game.id))
            db.session.commit()
            flash('Game Created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("create_game.html", user=current_user)