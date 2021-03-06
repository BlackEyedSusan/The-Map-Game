from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm.session import sessionmaker
from werkzeug.local import F
from .models import Achievements, Adjacencies, Alliances, Diplo_Reqs, Game, GamesJoined, Military, Puppets, SeaZoneAdj, SeaZones, StatsAllTime, Territories, User, Empires, Wars
from . import db
from flask_sqlalchemy import event
from PIL import Image
import os
import schedule
Session = sessionmaker()
from .territory_setup import init_territories_random
from threading import Thread, Timer
import time
import sys



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
                    new_empire = Empires(name=empire, user=current_user.id, game=game_id, color=color, gov=gov, flag=flag1, oil_stockpiles=0, global_trade_power=0, uranium = 0, enriched_uranium=0, capital=0, cash=0)
                    filename = str(current_user.id) + str(game_id) + ".png"
                    flag1.save(os.path.join('website/static/flags/uploaded/', filename))
                    image = Image.open(f'website/static/flags/uploaded/{filename}')
                    image = image.resize((150,100))
                    image.save(f'website/static/flags/uploaded/{filename}')
                    new_empire.flag = f'/static/flags/uploaded/{filename}'
                else:
                    new_empire = Empires(name=empire, user=current_user.id, game=game_id, color=color, gov=gov, flag=flag2, oil_stockpiles=0, global_trade_power=0, uranium = 0, enriched_uranium=0, capital=0, cash=0)
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
    territory_list = []
    claimed = []
    valid_claims = []
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
    for territory in db.session.query(Territories).filter_by(game=game_id):
        territory_list.append(territory)
        if territory.owner == current_empire.id:
            claimed.append(territory)
     
    for territory in db.session.query(Territories).filter_by(game=game_id):
        if current_game.ticker > 1: 
            for claim in claimed:
                if is_adjacent(territory, claim) and territory.owner == 0:
                    valid_claims.append(territory)
        if current_game.ticker == 1:
            if territory.owner == 0:
                valid_claims.append(territory)
    temp_list = []        
    for item in valid_claims:
        if item not in temp_list:
            temp_list.append(item)
    valid_claims = temp_list
    if request.method == "POST":
        input = request.form.get("draft")
        object_input = None
        for territory in db.session.query(Territories).filter_by(game=game_id):
            if str(territory.name).lower() == input.lower().strip():
                valid = False
                object_input = territory
                if current_game.ticker > 1:
                    for claim in claimed:
                        if is_adjacent(territory, claim):
                            valid = True
                if current_game.ticker == 1:
                    current_empire.capital = territory.id
                    valid = True
                if valid:
                    territory.owner = current_empire.id
                    territory.color = current_empire.color
                    db.session.commit()
                    if len(empire_list) == current_game.draft_pos + 1:
                        current_game.draft_pos = 0
                        current_game.ticker += 1
                    else:
                        current_game.draft_pos += 1
                    db.session.commit()
                else:
                    flash("You are not adjacent to that territory, try again", category="error")
        if object_input not in db.session.query(Territories).filter_by(game=game_id):
            flash("That territory does not exist, try again", category="error")
        return redirect(url_for('rooms.draft', game_id=game_id))
        
    return render_template("draft.html", user=current_user, current_empire=current_empire, is_turn=is_turn, game = current_game, territory_list = territory_list, valid_claims=valid_claims)
    




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
    infantry = infantry_calc(current_empire.id, game_id)
    transport = transport_calc(current_empire.id, game_id)
    sub = sub_calc(current_empire.id, game_id)
    tanks = tank_calc(current_empire.id, game_id)
    bomber = bomber_calc(current_empire.id, game_id)
    fighter = fighter_calc(current_empire.id, game_id)
    destroyer = destroyer_calc(current_empire.id, game_id)
    return render_template("map.html", user=current_user, territory_list=territory_list, players = players_output, game = games, game_id = id, empire_key=empires, is_host=is_host,
                            used_colors=empire_colors, colors=colors, id=id, current_empire=current_empire, avail_colors=avail_colors, current_color=current_color, govs=governments,
                            current_gov=current_gov, infantry=infantry, transport=transport, sub=sub, tanks=tanks, bomber=bomber, destroyer=destroyer, fighter=fighter)




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
    stat = db.session.query(StatsAllTime).filter_by(user=current_empire.user).first()
    sender_empire = db.session.query(Empires).filter_by(game=game_id, id=sender).first()
    stat_sender = db.session.query(StatsAllTime).filter_by(user=sender_empire.user).first()
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
        stat.total_ally += 1
        stat_sender.total_ally += 1
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
    curr_stat = db.session.query(StatsAllTime).filter_by(user=current_empire.user).first()
    receiver_stat = db.session.query(StatsAllTime).filter_by(user=target_empire.user).first()
    curr_achieve = db.session.query(Achievements).filter_by(user=target_empire.user).first()
    if request.method == "POST":
        if str(request.form.get("declare_war")) == "declare_war":
            new_war = Wars(attacker=current_empire.id, defender=target_empire.id)
            db.session.add(new_war)
            curr_stat.total_war += 1
            receiver_stat.total_war += 1
            if curr_stat.total_war >= 5:
                curr_achieve._5_wars = "True"
                flash("Achievement Unlocked! Take part in five wars.", category="neutral")
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
            curr_stat.total_betray += 1
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




@login_required
@rooms.route('<int:game_id>/military', methods=['GET', 'POST'])
def military(game_id):
    current_empire = db.session.query(Empires).filter_by(game=game_id, user=current_user.id).first()
    infantry = db.session.query(Military).filter_by(game=game_id, owner=current_empire.id)
    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")
        flash("That would take " + str(calc_naval_movement(game_id, start, end)) + " minutes", category="neutral")
        

    return render_template("military.html", user=current_user, infantry=infantry)

#Dijkstra's Algorithm
def calc_naval_movement(game_id, start, end):
    start_z = db.session.query(SeaZones).filter_by(game=game_id, name=start).first()
    end_z = db.session.query(SeaZones).filter_by(game=game_id, name=end).first()
    zones = db.session.query(SeaZones).filter_by(game=game_id)
    short_way = {}
    prev_zones = {}
    unchecked = [] 
    for zone in zones:
        unchecked.append(zone)
    max = sys.maxsize
    for zone in unchecked:
        short_way[zone] = max
    short_way[start_z] = 0

    while unchecked:
        min_zone = None
        for zone in unchecked:
            if min_zone == None:
                min_zone = zone
            elif short_way[zone] < short_way[min_zone]:
                min_zone = zone
        print("Min Zone " + str(min_zone.name) + " " + str(short_way[min_zone]))
        unchecked.remove(min_zone)
        adjs = get_neighbor_sea_zones(game_id, min_zone)
        for adj in adjs:
            val = short_way[min_zone] + adj.time
            if val < short_way[adj]:
                short_way[adj] = val
                prev_zones[adj] = min_zone
    return short_way[end_z]


   

def get_neighbor_sea_zones(game_id, sea_zone):
    zone_list = []
    zone = db.session.query(SeaZones).filter_by(id=sea_zone.id).first()
    for zone in db.session.query(SeaZoneAdj).filter_by(sea_zone1 = zone.id).all():
        zone_list.append(db.session.query(SeaZones).filter_by(game=game_id, id=zone.sea_zone2).first())
    for zone in db.session.query(SeaZoneAdj).filter_by(game=game_id, sea_zone2 = sea_zone.id).all():
        zone_list.append(db.session.query(SeaZones).filter_by(game=game_id, id=zone.sea_zone1).first())
    return zone_list


def is_adjacent(territory_1, territory_2):
    check1 = db.session.query(Adjacencies).filter_by(territory_1=territory_1.id, territory_2=territory_2.id).first()
    check2 = db.session.query(Adjacencies).filter_by(territory_1=territory_2.id, territory_2=territory_1.id).first()
    if check1 != None or check2 != None:
        return True
    else:
        return False

def get_valid_claims(game_id):
    current_game = db.session.query(Game).filter_by(id=game_id['data']).first()
    current_empire = db.session.query(Empires).filter_by(game=game_id['data'], user=current_user.id).first()
    valid_claims = []
    claimed = []
    for territory in db.session.query(Territories).filter_by(game=game_id['data']):
        if territory.owner == current_empire.id:
            claimed.append(territory)
    
    for territory in db.session.query(Territories).filter_by(game=game_id['data']):
        if current_game.ticker > 1: 
            for claim in claimed:
                if is_adjacent(territory, claim) and territory.owner == 0:
                    valid_claims.append(territory.name)
        if current_game.ticker == 1:
            if territory.owner == 0:
                valid_claims.append(territory.name)
    temp_list = []        
    for item in valid_claims:
        if item not in temp_list:
            temp_list.append(item)
    valid_claims = temp_list
    return valid_claims

def get_empire_list(game_id):
    empire_list = []
    for empire in db.session.query(Empires).filter_by(game=game_id['data']):
        user = db.session.query(User).filter_by(id=empire.user).first()
        fixed_empire_color = str(empire.color).lower().replace(' ', '-')
        empire_list.append([empire.name, fixed_empire_color, user.username, url_for('profiles.profile', user_id=user.id)])
    return empire_list

def is_turn(game_id):
    current_empire = None
    is_turn = False
    empire_list = []
    current_game = db.session.query(Game).filter_by(id=game_id['data']).first()
    
    for empire in db.session.query(Empires).filter_by(game=game_id['data']):
        if empire.user == current_user.id:
            current_empire = empire
        empire_list.append(empire)
    turn = empire_list[current_game.draft_pos]

    if current_empire == turn:
        is_turn = True
    return is_turn


def infantry_calc(owner, game_id):
    args = [owner, game_id]
    infantry = round(get_total_pop(*args)/25000000 + get_total_pop(*args)/25000000 * get_total_gdp(*args)/20000000000000) + 2
    return infantry


def get_oil_count(owner, game_id):
    count = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=owner):
        if territory.oil == "True":
            count += 1
    return count


def get_coast_total(owner, game_id):
    coast = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=owner):
        if territory.coast == "True":
            coast += 1
    return coast


def get_gold_count(owner, game_id):
    count = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=owner):
        if territory.gold == "True":
            count += 1
    return count


def get_uranium_count(owner, game_id):
    count = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=owner):
        if territory.uranium == "True":
            count += 1
    return count


def get_total_area(owner, game_id):
    count = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=owner):
        count += territory.area
    return count


def get_total_gdp(owner, game_id):
    count = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=owner):
        count += territory.gdp
    return count


def get_total_pop(owner, game_id):
    count = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=owner):
        count += territory.pop
    return count


def get_total_forts(owner, game_id):
    count = 0
    for territory in db.session.query(Territories).filter_by(game=game_id, owner=owner):
        count += territory.forts
    return count


def get_trade_power(owner, game_id):
    current_empire = db.session.query(Empires).filter_by(id=owner, game=game_id).first()
    args = [owner, game_id]
    trade_power = (get_total_gdp(*args)/1000000000000)+(get_gold_count(*args)/3)+(get_oil_count(*args))
    print("Trade power is at: " + str(trade_power))
    return trade_power


def tank_calc(owner, game_id):
    args = [owner, game_id]
    tank = round(get_total_pop(*args)/40000000 + get_total_pop(*args)/40000000 * get_total_gdp(*args)/4000000000000 + (get_oil_count(*args)/5))
    return tank

def sub_calc(owner, game_id):
    args = [owner, game_id]
    if get_coast_total(*args) == 0:
        return 0
    sub = round((get_total_pop(*args)/75000000 + (get_total_pop(*args)/75000000 * get_total_gdp(*args)/30000000000000)*get_coast_total(*args)/3)/4 + get_oil_count(*args)/5 + get_uranium_count(*args))
    return sub

def transport_calc(owner, game_id):
    args = [owner, game_id]
    if get_coast_total(*args) == 0:
        return 0
    transport = round(get_coast_total(*args)*(get_trade_power(*args)+get_oil_count(*args))*0.0001)+round(get_total_forts(*args)/4)+round(get_total_pop(*args)/10000000)
    return transport


def destroyer_calc(owner, game_id):
    args = [owner, game_id]
    if get_coast_total(*args) == 0:
        return 0
    destroyer = round(((get_total_pop(*args)/75000000 + get_total_pop(*args)/75000000 * get_total_gdp(*args)/30000000000000)*get_coast_total(*args)/3)/5 + get_oil_count(*args)/3)
    return destroyer


def bomber_calc(owner, game_id):
    args = [owner, game_id]
    bomber = round(((get_total_pop(*args)/120000000 * get_total_gdp(*args)/300000000000000 + get_total_area(*args)/600000)/5)+get_oil_count(*args)/15)
    return bomber


def fighter_calc(owner,game_id):
    args = [owner, game_id]
    fighter = round(get_total_pop(*args)/120000000 * get_total_gdp(*args)/30000000000000 + get_total_area(*args)/600000 + get_oil_count(*args)/5)
    return fighter


def init_territories_default(game_id, DEFAULT_OWNER=0, DEFAULT_COLOR="gray"):
    alaska = Territories(name="Alaska", territory_id=1, owner=DEFAULT_OWNER, color=DEFAULT_COLOR, game=game_id, pop=731545, gdp=49120000000, area=1717939, oil="True", uranium="False", gold="True", biome="Forest", region="Arctic")
    yukon = Territories(name="Yukon", territory_id=2, owner=DEFAULT_OWNER, color=DEFAULT_COLOR, game=game_id, pop=86878, gdp=6920000000, area=1828458, oil="True", uranium="True", gold="True", biome="Tundra", region="Arcitc")
    nunavut = Territories(name="Nunavut", territory_id=3, owner=DEFAULT_OWNER, color=DEFAULT_COLOR, game=game_id, pop=38780, gdp=3160000000, area=1611677, oil="False", uranium="False", gold="True", biome="Tundra", region="Arctic")
    db.session.add(alaska)
    db.session.add(yukon)
    db.session.add(nunavut)
    db.session.commit()

def daily_events():
    from main import create_app
    app = create_app()
    print("5 minutes passed!")
    with app.app_context():
        for empire in db.session.query(Empires):
            inf_prod = infantry_calc(empire.id, empire.game)
            game = db.session.query(Game).filter_by(id=empire.game).first()
            if empire.total_inf == None:
                if game.is_started == "True":
                    empire.total_inf = inf_prod
                else:
                    continue
            else:
                empire.total_inf += inf_prod
            new_inf = Military(owner=empire.id, location=empire.capital, game=empire.game, category="ground", type="infantry", amount=inf_prod)
            db.session.add(new_inf)
            db.session.commit()
        for territory in db.session.query(Territories):
            territory.pop = round(1.015*territory.pop)
            db.session.commit()