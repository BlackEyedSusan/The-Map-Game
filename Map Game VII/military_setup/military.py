from empire_setup import empires
import sqlite3

def military_database_init():
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    db.execute('''
                CREATE TABLE IF NOT EXISTS military
                ([unit_id] INTEGER PRIMARY KEY, [unit_type] TEXT, [owner] TEXT, [location_id] INTEGER)
                ''')


class Military:

    def __init__(self, unit_type, unit_id, location_id, owner):
        self.unit_type = unit_type
        self.location_id = location_id
        self.owner = owner
        self.unit_id = unit_id
        if self.unit_type != 'infantry' and self.unit_type != 'destroyer':
            self.amount_units_loaded = 0

    def move(self, new_location_id, distance):
        self.location_id = new_location_id

    def load(self, amount_units):
        if self.unit_type == 'airforce':
            if self.amount_units_loaded + amount_units <= 5:
                self.amount_units_loaded += amount_units
            else:
                return
        if self.unit_type == 'transport':
            if self.amount_units_loaded + amount_units <= 10:
                self.amount_units_loaded += amount_units

    def unload(self, amount_units):
        if self.amount_units_loaded - amount_units < 0:
            return
        self.amount_units_loaded -= amount_units
