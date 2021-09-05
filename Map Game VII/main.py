#imports
import sqlite3
from map_assets import territories
from empires import Empires

CALIFORNIA = Empires('California', 'Swordlord', 'Irvine')
RIVERSIDE = territories.Territories(0, 'Riverside', CALIFORNIA.name, [1, 2, 3, 4, 5])


def database_init():
        conn = sqlite3.connect('territory_database.db')
        db = conn.cursor()
        db.execute('''
                    CREATE TABLE IF NOT EXISTS territories
                    ([territory_id] INTEGER PRIMARY KEY, [territory_name] TEXT, [owner] TEXT)
                    ''')


database_init()