#imports
from map_assets import territories
import sqlite3
from military_setup import military

class Empires:

    #defines attributes of empire
    def __init__(self, name, user, capital, e_id):
        self.name = name
        self.user = user
        self.capital = capital
        self.is_puppet = False
        self.at_war = False
        self.e_id = e_id

    def empire_database_init():
        conn = sqlite3.connect('database.db')
        db = conn.cursor()
        db.execute('''
                    CREATE TABLE IF NOT EXISTS empires
                    ([empire_id] INTEGER PRIMARY KEY, [empire_name] TEXT, [user] TEXT)
                    ''')

    def get_territories(self):
        conn = sqlite3.connect('database.db')
        db = conn.cursor()
        db.execute(f'''
                    SELECT * FROM territories
                    ''')
        result = db.fetchall()
        
        

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