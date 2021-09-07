# imports
import sqlite3
import os.path

def territory_database_init():
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    #need to update to include stats
    db.execute('''
                CREATE TABLE IF NOT EXISTS territories
                ([territory_id] INTEGER PRIMARY KEY, [territory_name] TEXT, [owner] TEXT, [gdp] INTEGER, [pop] INTEGER, [area] INTEGER, [coast] TEXT, [gdp_per_capita] INTEGER, [pop_density] INTEGER, [iron] TEXT, [aluminum] TEXT, [silver] TEXT, [gold] TEXT, [oil] TEXT, [num_ports] INTEGER, [num_forts] INTEGER)
                ''')


class Territories:

    # sets up attributes of the territory
    def __init__(self, t_id:int, name:str, owner:str, stats:list, borders=None):
        self.t_id = t_id
        self.name = name
        self.owner = owner
        self.stats = stats
        conn = sqlite3.connect('database.db')
        gdp, pop, area, coast, gdp_per_capita, pop_density, iron, aluminum, silver, gold, oil, num_ports, num_forts = self.stats
        db = conn.cursor()
        db.execute(f'''
                    INSERT INTO territories (territory_id, territory_name, owner, gdp, pop, area, coast, gdp_per_capita, pop_density, iron, aluminum, silver, gold, oil, num_ports, num_forts)
                        VALUES({self.t_id}, '{str(self.name)}', '{str(self.owner)}', {int(gdp)}, {int(pop)}, {int(area)}, '{str(coast)}', {int(gdp_per_capita)}, {int(pop_density)}, '{str(iron)}', '{str(aluminum)}', '{str(silver)}', '{str(gold)}', '{str(oil)}', {int(num_ports)}, {int(num_forts)})
                    ''')
        conn.commit()
        print(f"Initialized {self.name}")

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

    
