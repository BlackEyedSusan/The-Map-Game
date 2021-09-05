#imports
from map_assets import Territories
import sqlite3

class Empires:

    #defines attributes of empire
    def __init__(self, name, user, capital):
        self.name = name
        self.user = user
        self.capital = capital

    def get_territories(self, territories):
        pass