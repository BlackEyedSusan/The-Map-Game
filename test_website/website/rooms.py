import sqlite3
from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm.session import sessionmaker
from .models import Alliances, Diplo_Reqs, Game, GamesJoined, Puppets, Territories, User, Empires, Wars
from . import db
from flask_sqlalchemy import event

Session = sessionmaker()


rooms = Blueprint('rooms', __name__)

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
                ['Anocracy', 'anocracy']
                ]

@rooms.route('<int:game_id>', methods=["GET", "POST"])
@login_required
def room(game_id):
    current_game = db.session.query(Game).filter_by(id=game_id).first()

    if str(current_game.is_started) == "True":
        return redirect(url_for('rooms.map', game_id=game_id))

    if request.method == "POST":
        
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
        elif str(request.form.get("start_game")) == "start_game":
            print('worked')
            all_ready = True
            for empire in db.session.query(Empires).filter_by(game=game_id):
                if empire.user == current_user.id:
                    current_empire = empire
                if empire.color == None:
                    all_ready = False
                if empire.gov == None:
                    all_ready == False
                if empire.name == None:
                    all_ready = False
            if all_ready:
                db.session.delete(current_game)
                db.session.commit()
                new_game = Game(code=current_game.code, game_name=current_game.game_name, host=current_game.host, is_started="True")
                db.session.add(new_game)
                db.session.commit()
                init_territories_default(current_game.id)
                return redirect(url_for('rooms.map', game_id=game_id))
            else:
                flash('A user has not finished setting up their empire yet.', category='error')
                return redirect(url_for('rooms.room', game_id=game_id))

        #this is where all of the colors that can be used for the 
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

@event.listens_for(Session, 'after_commit')
def receive_after_commit(session):
    print('commit done.')

@rooms.route('<int:game_id>/map', methods=['POST', 'GET'])
@login_required
def map(game_id):
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
    territory_list = []
    for territory in db.session.query(Territories):
        territory_list.append(territory)
    return render_template("map.html", user=current_user, territory_list=territory_list, players = players_output, game = games, game_id = id, empire_key=empires, is_host=is_host, used_colors=empire_colors, colors=colors, id=id, current_empire=current_empire, avail_colors=avail_colors, current_color=current_color, govs=governments, current_gov=current_gov)

@login_required
@rooms.route('<int:game_id>/diplomacy', methods=['GET', 'POST'])
def diplomacy(game_id):
    players = []
    players_output = []
    empires = []
    id = game_id
    current_gov = None
    diplomacy_requests = []
    sent_diplomacy = []
    current_empire = db.session.query(Empires).filter_by(game=game_id, user=current_user.id).first()
    diplo_requests = db.session.query(Diplo_Reqs).filter_by(receiver=current_empire.id)
    
    for diplo_request in diplo_requests:
        sender = db.session.query(Empires).filter_by(id=diplo_request.sender).first()
        diplomacy_requests.append([diplo_request.type, sender.name, url_for('rooms.request_accept', game_id=game_id, request_id=diplo_request.id, sender=sender.id)])
    sent_diplos = db.session.query(Diplo_Reqs).filter_by(sender=current_empire.id)

    for sent_diplo in sent_diplos:
        receiver = db.session.query(Empires).filter_by(id=sent_diplo.receiver).first()
        sent_diplomacy.append([sent_diplo.type, receiver.name])

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
        if empire.user != current_user.id:
            empires.append([empire.name, url_for('rooms.diplomacyplayer', game_id=game_id, empire_id=empire.id)])
        if empire.user == current_user.id:
            current_gov = current_empire.gov
    territory_list = []
    for territory in db.session.query(Territories):
        territory_list.append(territory)
    return render_template("diplomacy.html", user=current_user, sent_diplos=sent_diplomacy, diplomacy_requests = diplomacy_requests, territory_list=territory_list, players = players_output, game = games, game_id = id, empire_key=empires, is_host=is_host, current_empire=current_empire, govs=governments, current_gov=current_gov)

@login_required
@rooms.route('<int:game_id>/diplomacy/<int:request_id>/<int:sender>/accept')
def request_accept(game_id, request_id, sender):
    diplo_action = db.session.query(Diplo_Reqs).filter_by(id=request_id).first()
    if diplo_action.type == 'peace':
        war1 = db.session.query(Wars).filter_by(attacker=current_user.id, defender=sender).first()
        war2 = db.session.query(Wars).filter_by(attacker=sender, defender=current_user.id).first()
        if war1 != None:
            db.session.delete(war1)
        if war2 != None:
            db.session.delete(war2)
        db.session.commit()
        flash('You have accepted the request for peace.', category='success')
    if diplo_action.type == 'ally':
        alliance = Alliances(empire1 = current_user.id, empire2 = sender)
        db.session.add(alliance)
        db.session.commit()
        flash('You have accepted the request for an alliance.', category='success')
    db.session.delete(diplo_action)
    db.session.commit()
    return redirect(url_for('rooms.diplomacy', game_id=game_id))

@login_required
@rooms.route('<int:game_id>/diplomacy/<empire_id>', methods=['GET', 'POST'])
def diplomacyplayer(game_id, empire_id):
    target_empire = db.session.query(Empires).filter_by(id=empire_id).first()
    current_empire = db.session.query(Empires).filter_by(game=game_id, user=current_user.id).first()
    if request.method == "POST":
        if str(request.form.get("declare_war")) == "declare_war":
            new_war = Wars(attacker=current_empire.id, defender=target_empire.id)
            db.session.add(new_war)
            db.session.commit()
        if str(request.form.get("ally")) == "ally":
            new_ally_request = Diplo_Reqs(sender=current_empire.id, receiver=target_empire.id, type="ally")
            if db.session.query(Diplo_Reqs).filter_by(sender=target_empire.id, receiver=current_empire.id, type="ally").first() != None or db.session.query(Diplo_Reqs).filter_by(sender=current_empire.id, receiver=target_empire.id, type="ally").first() != None:
                flash('A request for that already exists.', category='error')
                return redirect(url_for('rooms.diplomacyplayer', game_id=game_id, empire_id=empire_id))
            else:
                db.session.add(new_ally_request)
                db.session.commit()
                flash(f'Request for an alliance sent to the {target_empire.name}', category='success')
                return redirect(url_for('rooms.diplomacyplayer', game_id=game_id, empire_id=empire_id))
        if str(request.form.get('make_peace')) == 'make_peace':
            new_peace_request = Diplo_Reqs(sender=current_empire.id, receiver=target_empire.id, type="peace")
            if db.session.query(Diplo_Reqs).filter_by(sender=target_empire.id, receiver=current_empire.id, type="peace").first() != None or db.session.query(Diplo_Reqs).filter_by(sender=current_empire.id, receiver=target_empire.id, type="peace").first() != None:
                flash("A request for that already exists.", category='error')
                return redirect(url_for('rooms.diplomacyplayer', game_id=game_id, empire_id=empire_id))
            else:
                db.session.add(new_peace_request)
                db.session.commit()
                flash("Request for peace sent.", category='success')
                return redirect(url_for('rooms.diplomacyplayer', game_id=game_id, empire_id=empire_id))
        if str(request.form.get('betray')) == 'betray':
            betrayal1 = db.session.query(Alliances).filter_by(empire1=empire_id, empire2=current_empire.id).first()
            betrayal2 = db.session.query(Alliances).filter_by(empire1=current_empire.id, empire2=empire_id).first()
            if betrayal1 != None:
                db.session.delete(betrayal1)
            if betrayal2 != None:
                db.session.delete(betrayal2)
            db.session.commit()
            flash(f'You have betrayed the {target_empire.name}...', category='success')
            return redirect(url_for('rooms.diplomacyplayer', game_id=game_id, empire_id=empire_id))

    at_war = False
    allied = False
    is_puppet = False
    is_controller = False
    at_war1 = db.session.query(Wars).filter_by(attacker=current_empire.id, defender=target_empire.id).first()
    at_war2 = db.session.query(Wars).filter_by(attacker=target_empire.id, defender=current_empire.id).first()
    if at_war1 != None or at_war2 != None:
        at_war = True
    allied1 = db.session.query(Alliances).filter_by(empire1=current_empire.id, empire2=target_empire.id).first()
    allied2 = db.session.query(Alliances).filter_by(empire1=target_empire.id, empire2=current_empire.id).first()
    if allied1 != None or allied2 != None:
        allied = True
    puppet1 = db.session.query(Puppets).filter_by(controller=current_empire.id, puppet=target_empire.id).first()
    puppet2 = db.session.query(Puppets).filter_by(controller=target_empire.id, puppet=current_empire.id).first()
    if puppet1 == "True":
        is_puppet = True
    if puppet2 == "True":
        is_controller = True
    return render_template("diplomacyplayer.html", user=current_user, target_empire=target_empire, current_empire=current_empire, at_war=at_war, allied=allied, is_puppet=is_puppet, is_controller=is_controller)


def init_territories_default(game_id, DEFAULT_OWNER=0):
    alaska = Territories(name="Alaska", owner=DEFAULT_OWNER, game=game_id, pop=731545, gdp=49120000000, area=1717939, oil="True", uranium="False", gold="True", biome="Forest")
    db.session.add(alaska)
    db.session.commit()