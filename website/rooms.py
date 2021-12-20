from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm.session import sessionmaker
from werkzeug.local import F
from .models import Alliances, Diplo_Reqs, Game, GamesJoined, Puppets, Territories, User, Empires, Wars
from . import db
from flask_sqlalchemy import event
from PIL import Image
import os
import random
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
            ['#FF0080', 'Salmon', 'salmon'],
            ['#40DD40', 'Dark Green', 'dark-green']]

governments = [['Thalassocracy', 'thalassocracy'],
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

country_flags = [['Austria Hungary', '/static/flags/country/austria_hungary.png'],
                ['Brazil', '/static/flags/country/brazil.png'],
                ['China', '/static/flags/country/china.png'],
                ['Dutch East India Company', '/static/flags/country/dutch_east_india_company.png'],
                ['France', '/static/flags/country/france.png'],
                ['Germany', '/static/flags/country/germany.png'],
                ['Great Britain', '/static/flags/country/great_britain.png'],
                ['India', '/static/flags/country/india.png'],
                ['Iran', '/static/flags/country/iran.png'],
                ['Japan', '/static/flags/country/japan.png'],
                ['Mexico', '/static/flags/country/mexico.png'],
                ['The Netherlands', '/static/flags/country/netherlands.png'],
                ['Ottoman Empire', '/static/flags/country/ottoman_empire.png'],
                ['Poland', '/static/flags/country/poland.png'],
                ['Saudi Arabia', '/static/flags/country/saudi_arabia.png'],
                ['Soviet Union', '/static/flags/country/soviet_union.png'],
                ['United States', '/static/flags/country/united_states.png'],
                ['Venice', '/static/flags/country/venice.png'],
                ['Portugal', '/static/flags/country/portugal.png'],
                ['Imperial Germany', '/static/flags/country/imperial_germany.png'],
                ['Ethiopia', '/static/flags/country/ethiopia.png'],
                ['Iraq', '/static/flags/country/iraq.png'],
                ['Nepal', '/static/flags/country/nepal.png'],
                ['Chad', '/static/flags/country/chad.png']]

@rooms.route('<int:game_id>', methods=["GET", "POST"])
@login_required
def room(game_id):
    current_game = db.session.query(Game).filter_by(id=game_id).first()

    if str(current_game.is_started) == "True":
        return redirect(url_for('rooms.draft', game_id=game_id))

    if request.method == "POST":
        
        if str(request.form.get("update_empire")) == "update_empire":
            empire = request.form.get('empire')
            color = request.form.get('color_input')
            gov = request.form.get('gov')
            flag1 = request.files['flag']
            print(flag1.filename)
            flag2 = request.form.get('flag2')
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
                if flag1.filename != '':
                    new_empire = Empires(name=empire, user=current_user.id, game=game_id, color=color, gov=gov, flag=flag1, oil_stockpiles=0, global_trade_power=0, capital=0)
                    filename = str(current_user.id) + str(game_id) + ".png"
                    flag1.save(os.path.join('website/static/flags/uploaded/', filename))
                    image = Image.open(f'website/static/flags/uploaded/{filename}')
                    image = image.resize((150,100))
                    image.save(f'website/static/flags/uploaded/{filename}')
                    new_empire.flag = f'/static/flags/uploaded/{filename}'
                else:
                    new_empire = Empires(name=empire, user=current_user.id, game=game_id, color=color, gov=gov, flag=flag2, oil_stockpiles=0, global_trade_power=0, capital=0)
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
                current_game.is_started = "True"
                db.session.commit()
                init_territories_random(current_game.id)
                return redirect(url_for('rooms.draft', game_id=game_id))
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
    avail_flags = []
    id = game_id
    current_gov = None
    current_color = None
    current_tag = None
    current_empire = "None"
    name_color = "None"
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
    for banner in country_flags:
        search = db.session.query(Empires).filter_by(game=game_id, flag=banner[1]).first()
        if search == None:
            avail_flags.append(banner)
    avail_colors.append([current_tag, str(current_color).title().replace('-', ' '), current_color])
    for color in colors:
        if color[0] == current_empire.color:
            name_color= color[1]
    return render_template("room.html", user=current_user, players = players_output, game = games, game_id = id, empire_key=empires, is_host=is_host, avail_flags=avail_flags,
                            used_colors=empire_colors, colors=colors, id=id, current_empire=current_empire, avail_colors=avail_colors, current_color=current_color, name_color = name_color,
                            govs=governments, current_gov=current_gov)

@event.listens_for(Session, 'after_commit')
def receive_after_commit(session):
    print('commit done.')




@rooms.route('<int:game_id>/draft', methods=['POST', "GET"])
@login_required
def draft(game_id):
    current_empire = None
    is_turn = False
    empire_list = []
    current_game = db.session.query(Game).filter_by(id=game_id).first()
    val = current_game.ticker
    if val > 3:
        return redirect(url_for('rooms.map', game_id=game_id))
    
    for empire in db.session.query(Empires).filter_by(game=game_id):
        if empire.user == current_user.id:
            current_empire = empire
        empire_list.append(empire)
    turn = empire_list[current_game.draft_pos]

    if current_empire == turn:
        is_turn = True

    

    if request.method == "POST":
        input = request.form.get("draft")
        print(input)
        for territory in db.session.query(Territories).filter_by(game=game_id):
            print(territory.name)
            if str(territory.name).lower() == input.lower().strip():
                territory.owner = current_empire.id
                territory.color = current_empire.color
                db.session.commit()
                if len(empire_list) == current_game.draft_pos + 1:
                    current_game.draft_pos = 0
                    current_game.ticker += 1
                else:
                    current_game.draft_pos += 1
                db.session.commit()
        return redirect(url_for('rooms.draft', game_id=game_id))
        
    return render_template("draft.html", user=current_user, current_empire=current_empire, is_turn=is_turn, game = current_game )
    




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
    for territory in db.session.query(Territories).filter_by(game=game_id):
        territory_list.append(territory)
    total_area = 0
    total_pop = 0
    total_gdp = 0
    total_forts = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=current_empire.id):
        total_area += territory.area
        total_pop += territory.pop
        total_gdp += territory.gdp
        total_forts += territory.forts
    infantry = infantry_calc(total_area, total_pop, total_gdp, total_forts)
    return render_template("map.html", user=current_user, territory_list=territory_list, players = players_output, game = games, game_id = id, empire_key=empires, is_host=is_host,
                            used_colors=empire_colors, colors=colors, id=id, current_empire=current_empire, avail_colors=avail_colors, current_color=current_color, govs=governments,
                            current_gov=current_gov, infantry=infantry)




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
        diplomacy_requests.append([diplo_request.type, sender.name, url_for('rooms.request_accept', game_id=game_id, request_id=diplo_request.id, sender=sender.id), url_for('rooms.request_decline', game_id=game_id, request_id=diplo_request.id, sender=sender.id)])
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
    current_empire = db.session.query(Empires).filter_by(game=game_id, user=current_user.id).first()
    diplo_action = db.session.query(Diplo_Reqs).filter_by(id=request_id).first()
    if diplo_action.type == 'peace':
        war1 = db.session.query(Wars).filter_by(attacker=current_empire.id, defender=sender).first()
        war2 = db.session.query(Wars).filter_by(attacker=sender, defender=current_empire.id).first()
        if war1 != None:
            db.session.delete(war1)
        if war2 != None:
            db.session.delete(war2)
        db.session.commit()
        flash('You have accepted the request for peace.', category='success')
    if diplo_action.type == 'ally':
        alliance = Alliances(empire1 = current_empire.id, empire2 = sender)
        db.session.add(alliance)
        db.session.commit()
        flash('You have accepted the request for an alliance.', category='success')
    db.session.delete(diplo_action)
    db.session.commit()
    return redirect(url_for('rooms.diplomacy', game_id=game_id))




@login_required
@rooms.route('<int:game_id>/diplomacy/<int:request_id>/<int:sender>/decline')
def request_decline(game_id, request_id, sender):
    diplo_action = db.session.query(Diplo_Reqs).filter_by(id=request_id).first()
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


def infantry_calc(area, pop, gdp, forts):
    infantry = round(area/100000+pop/4000000+gdp/1000000000000) + round(forts/2)
    print("You have " + str(infantry) + " additional infantry")
    return infantry


def randomizer_pop():
    return round(random.uniform(0.6, 1.4)*5072021)

def randomizer_area():
    return round(random.uniform(0.6, 1.4)*38103)

def randomizer_gdp():
    return round(random.uniform(0.6, 1.4)*89827668129)

def randomizer_forts():
    randomInt = random.randint(1, 20)
    if randomInt == 1:
        return 1
    else:
        return 0


def init_territories_default(game_id, DEFAULT_OWNER=0, DEFAULT_COLOR="gray"):
    alaska = Territories(name="Alaska", territory_id=1, owner=DEFAULT_OWNER, color=DEFAULT_COLOR, game=game_id, pop=731545, gdp=49120000000, area=1717939, oil="True", uranium="False", gold="True", biome="Forest", region="Arctic")
    yukon = Territories(name="Yukon", territory_id=2, owner=DEFAULT_OWNER, color=DEFAULT_COLOR, game=game_id, pop=86878, gdp=6920000000, area=1828458, oil="True", uranium="True", gold="True", biome="Tundra", region="Arcitc")
    nunavut = Territories(name="Nunavut", territory_id=3, owner=DEFAULT_OWNER, color=DEFAULT_COLOR, game=game_id, pop=38780, gdp=3160000000, area=1611677, oil="False", uranium="False", gold="True", biome="Tundra", region="Arctic")
    db.session.add(alaska)
    db.session.add(yukon)
    db.session.add(nunavut)
    db.session.commit()



def init_territories_random(game_id):
    alaska = Territories(name="Alaska", territory_id=1, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    yukon = Territories(name="Yukon", territory_id=2, owner=0, color="gray", game=game_id,  gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    nunavut = Territories(name="Nunavut", territory_id=3, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    greenland = Territories(name="Greenland", territory_id=4, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    british_columbia = Territories(name="British Columbia", territory_id=5, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    alberta = Territories(name="Alberta", territory_id=5, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    saskatchewan = Territories(name="Saskatchewan", territory_id=6, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    ontario = Territories(name="Ontario", territory_id=7, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    quebec = Territories(name="Quebec", territory_id=8, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    newfoundland = Territories(name="Newfoundland", territory_id=9, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    new_england = Territories(name="New England", territory_id=10, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    cascadia = Territories(name="Cascadia", territory_id=11, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    rocky_mountains = Territories(name="Rocky Mountains", territory_id=12, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    nevada = Territories(name="Nevada", territory_id=13, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    alta_california = Territories(name="Alta California", territory_id=14, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    los_angeles = Territories(name="Los Angeles", territory_id=15, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    imperial_valley = Territories(name="Imperial Valley", territory_id=16, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", biome="Forest", region="")
    
    db.session.add(alaska)
    db.session.add(yukon)
    db.session.add(nunavut)
    db.session.add(greenland)
    db.session.add(british_columbia)
    db.session.add(alberta)
    db.session.add(saskatchewan)
    db.session.add(ontario)
    db.session.add(quebec)
    db.session.add(newfoundland)
    db.session.add(new_england)
    db.session.add(cascadia)
    db.session.add(rocky_mountains)
    db.session.add(nevada)
    db.session.add(alta_california)
    db.session.add(los_angeles)
    db.session.add(imperial_valley)
    db.session.commit()