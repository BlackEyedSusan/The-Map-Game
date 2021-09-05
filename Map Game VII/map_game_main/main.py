#imports
import sqlite3
from empires import Empires
from map_assets import Territories

CALIFORNIA = Empires('California', 'Swordlord', 'Irvine')



def database_init():
        conn = sqlite3.connect('territory_database.db')
        db = conn.cursor()
        db.execute('''
                    CREATE TABLE IF NOT EXISTS territories
                    ([territory_id] INTEGER PRIMARY KEY, [territory_name] TEXT, [owner] TEXT)
                    ''')


database_init()