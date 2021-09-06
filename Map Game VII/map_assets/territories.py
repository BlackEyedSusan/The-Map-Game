# imports
import sqlite3
import os.path

def territory_database_init():
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    #need to update to include stats
    db.execute('''
                CREATE TABLE IF NOT EXISTS territories
                ([territory_id] INTEGER PRIMARY KEY, [territory_name] TEXT, [owner] TEXT)
                ''')


class Territories:

    # sets up attributes of the territory
    def __init__(self, t_id:int, name:str, owner:str, stats:list):
        self.t_id = t_id
        self.name = name
        self.owner = owner
        self.stats = stats
        conn = sqlite3.connect('database.db')
        gdp, pop, area, coast, gdp_per_capita, pop_density, iron, aluminum, silver, gold, oil, num_ports, num_forts = self.stats
        db = conn.cursor()
        db.execute(f'''
                    INSERT INTO territories (territory_id, territory_name, owner)
                        VALUES({self.t_id}, '{str(self.name)}', '{str(self.owner)}')
                    ''')
        conn.commit()
    
    def database_edit(self):
        conn = sqlite3.connect('database.db')
        db = conn.cursor()
        #unfinished
        db.execute(f'''
                    UPDATE territories
                    SET owner = 
                    WHERE
                    ORDER column_1

                    ''')
        conn.commit()

    # defines a function to change to owner of a said territory
    def change_owner(self, new_owner):
        self.owner = new_owner
        if not os.path.exists('database.db'): #checks to see if the database file exists 
            self.database_init()
        conn = sqlite3.connect('database.db')
        db = conn.cursor()
        db.execute(f'''
                    UPDATE territories
                    SET owner = '{new_owner}'
                    WHERE territory_name = '{self.name}'
                    ''')
        conn.commit()

    
