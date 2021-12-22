from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from . import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(25))
    is_started = db.Column(db.String(5))
    code = db.Column(db.String(10), unique=True)
    host = db.Column(db.Integer, db.ForeignKey('user.id'))
    draft_pos = db.Column(db.Integer)
    ticker = db.Column(db.Integer)


class GamesJoined(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.Column(db.Integer, db.ForeignKey('user.id'))


class Empires(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    color = db.Column(db.String(7))
    gov = db.Column(db.String(50))
    flag = db.Column(db.String(50))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
    oil_stockpiles = db.Column(db.Integer)
    gold_stockpiles = db.Column(db.Integer)
    global_trade_power = db.Column(db.Integer)
    uranium = db.Column(db.Integer)
    enriched_uranium = db.Column(db.Integer)
    capital = db.Column(db.Integer, db.ForeignKey('territories.id'))
    cash = db.Column(db.Integer)
    total_inf = db.Column(db.Integer)
    total_tank = db.Column(db.Integer)
    total_transport = db.Column(db.Integer)
    total_sub = db.Column(db.Integer)
    total_bombers = db.Column(db.Integer)
    total_fighters = db.Column(db.Integer)


class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_1 = db.Column(db.Integer, db.ForeignKey('empires.id'))
    party_2 = db.Column(db.Integer, db.ForeignKey('empires.id'))
    category = db.Column(db.String(50))
    amount =  db.Column(db.Integer)


class Territories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    territory_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    owner = db.Column(db.Integer)
    color = db.Column(db.String(15))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
    pop = db.Column(db.Integer)
    gdp = db.Column(db.Integer)
    area = db.Column(db.Integer)
    oil = db.Column(db.String(5))
    forts = db.Column(db.Integer)
    uranium = db.Column(db.String(5))
    gold = db.Column(db.String(5))
    coast = db.Column(db.String(5))
    biome = db.Column(db.String(20))
    region = db.Column(db.String(25))


class Adjacencies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    territory_1 = db.Column(db.Integer, db.ForeignKey('territories.id'))
    territory_2 = db.Column(db.Integer, db.ForeignKey('territories.id'))


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


class StatsAllTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    wins = db.Column(db.Integer)
    total_ally = db.Column(db.Integer)
    total_betray = db.Column(db.Integer)
    total_war = db.Column(db.Integer)
    wars_won = db.Column(db.Integer)
    games_finished = db.Column(db.Integer)
    battles_won = db.Column(db.Integer)
    battles_done = db.Column(db.Integer)
    nukes_dropped = db.Column(db.Integer)
    gov_changes = db.Column(db.Integer)
    worst_defeat_lower = db.Column(db.Integer)
    worst_defeat_higher = db.Column(db.Integer)
    amt_spent_mil = db.Column(db.Integer)
    total_inf_produce = db.Column(db.Integer)


class StatsInGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empire = db.Column(db.Integer, db.ForeignKey('empires.id'))
    trade_agree_total = db.Column(db.Integer)


class SeaZones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)


class SeaZoneAdj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sea_zone1 = db.Column(db.Integer, db.ForeignKey('sea_zones.id'))
    sea_zone2 = db.Column(db.Integer, db.ForeignKey('sea_zones.id'))


class Ports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    territory = db.Column(db.Integer, db.ForeignKey('territories.id'))
    sea_zone = db.Column(db.Integer, db.ForeignKey('sea_zones.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    pfp = db.Column(db.String(50))
    admin = db.Column(db.String(50))