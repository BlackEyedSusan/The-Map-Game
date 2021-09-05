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
