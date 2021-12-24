from . import db
from .models import Territories, Adjacencies
import random

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


def init_territories_random(game_id):
    alaska = Territories(name="Alaska", territory_id=1, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="True", biome="Forest", region="")
    yukon = Territories(name="Yukon", territory_id=2, owner=0, color="gray", game=game_id,  gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="True", biome="Forest", region="")
    nunavut = Territories(name="Nunavut", territory_id=3, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False",coast="True", biome="Forest", region="")
    greenland = Territories(name="Greenland", territory_id=4, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="True", biome="Forest", region="")
    british_columbia = Territories(name="British Columbia", territory_id=5, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="True", biome="Forest", region="")
    alberta = Territories(name="Alberta", territory_id=6, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    saskatchewan = Territories(name="Saskatchewan", territory_id=7, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    ontario = Territories(name="Ontario", territory_id=8, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    quebec = Territories(name="Quebec", territory_id=9, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    newfoundland = Territories(name="Newfoundland", territory_id=10, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    new_england = Territories(name="New England", territory_id=11, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    cascadia = Territories(name="Cascadia", territory_id=12, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    rocky_mountains = Territories(name="Rocky Mountains", territory_id=13, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    nevada = Territories(name="Nevada", territory_id=14, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    alta_california = Territories(name="Alta California", territory_id=15, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    los_angeles = Territories(name="Los Angeles", territory_id=16, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    imperial_valley = Territories(name="Imperial Valley", territory_id=17, owner=0, color="gray", game=game_id, gdp=randomizer_gdp(), area=randomizer_area(), pop=randomizer_pop(), forts=randomizer_forts(), oil="False", uranium="False", gold="False", coast="False", biome="Forest", region="")
    

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

    adj_list = []
    adj_list.append(Adjacencies(territory_1 = alaska.id, territory_2 = yukon.id))
    adj_list.append(Adjacencies(territory_1 = alaska.id, territory_2 = british_columbia.id))
    adj_list.append(Adjacencies(territory_1 = yukon.id, territory_2 = nunavut.id))
    adj_list.append(Adjacencies(territory_1 = yukon.id, territory_2 = british_columbia.id))
    adj_list.append(Adjacencies(territory_1 = yukon.id, territory_2 = alberta.id))
    adj_list.append(Adjacencies(territory_1 = yukon.id, territory_2 = saskatchewan.id))
    adj_list.append(Adjacencies(territory_1 = nunavut.id, territory_2 = saskatchewan.id))
    adj_list.append(Adjacencies(territory_1 = british_columbia.id, territory_2 = alberta.id))
    adj_list.append(Adjacencies(territory_1 = british_columbia.id, territory_2 = cascadia.id))
    adj_list.append(Adjacencies(territory_1 = british_columbia.id, territory_2 = rocky_mountains.id))
    adj_list.append(Adjacencies(territory_1 = alberta.id, territory_2 = rocky_mountains.id))
    adj_list.append(Adjacencies(territory_1 = alberta.id, territory_2 = saskatchewan.id))
    adj_list.append(Adjacencies(territory_1 = saskatchewan.id, territory_2 = ontario.id))
    adj_list.append(Adjacencies(territory_1 = saskatchewan.id, territory_2 = rocky_mountains.id))
    adj_list.append(Adjacencies(territory_1 = ontario.id, territory_2 = quebec.id))
    adj_list.append(Adjacencies(territory_1 = ontario.id, territory_2 = newfoundland.id))
    adj_list.append(Adjacencies(territory_1 = quebec.id, territory_2 = newfoundland.id))
    adj_list.append(Adjacencies(territory_1 = quebec.id, territory_2 = new_england.id))
    adj_list.append(Adjacencies(territory_1 = newfoundland.id, territory_2 = new_england.id))
    adj_list.append(Adjacencies(territory_1 = cascadia.id, territory_2 = rocky_mountains.id))
    adj_list.append(Adjacencies(territory_1 = cascadia.id, territory_2 = nevada.id))
    adj_list.append(Adjacencies(territory_1 = rocky_mountains.id, territory_2 = nevada.id))
    adj_list.append(Adjacencies(territory_1 = alta_california.id, territory_2 = nevada.id))
    adj_list.append(Adjacencies(territory_1 = alta_california.id, territory_2 = los_angeles.id))
    adj_list.append(Adjacencies(territory_1 = los_angeles.id, territory_2 = imperial_valley.id))
    adj_list.append(Adjacencies(territory_1 = rocky_mountains.id, territory_2 = nevada.id))
    for item in adj_list:
        db.session.add(item)
    db.session.commit()
