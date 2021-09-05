#imports
from map_assets import Territories
import sqlite3

class Empires:

    #defines attributes of empire
    def __init__(self, name, user, capital):
        self.name = name
        self.user = user
        self.capital = capital
        self.is_puppet = False
        self.at_war = False

    def get_territories(self, territories):
        pass

    def declare_war(self, opponent):
        self.at_war = True
        pass

    def get_military_units(self):
        pass

    def make_peace(self, opponent):
        self.at_war = False
        pass

    def inf_production(self, territories):
        pass

    def acquire_territory(self, territory):
        pass