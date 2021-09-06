# imports
import sqlite3
import os.path


class Territories:

    # sets up attributes of the territory
    def __init__(self, t_id:int, name:str, owner:str, stats:list):
        self.t_id = t_id
        self.name = name
        self.owner = owner
        self.stats = stats
        print(self.stats)
        conn = sqlite3.connect('territory_database')
        db = conn.cursor()
        db.execute(f'''
                    INSERT INTO territories (territory_id, territory_name, owner)

                        VALUES
                        ({self.t_id}, {self.name}, {self.owner})
                    ''')
        conn.commit
    
    def database_init():
        conn = sqlite3.connect('territory_database.db')
        db = conn.cursor()
        db.execute('''
                    CREATE TABLE IF NOT EXISTS territories
                    ([territory_id] INTEGER PRIMARY KEY, [territory_name] TEXT, [owner] TEXT)
                    ''')


    def database_edit(self):
        conn = sqlite3.connect('territory_database')
        db = conn.cursor()
        #unfinished
        db.execute(f'''
                    UPDATE territories
                    SET column_1 = 
                    WHERE
                    ORDER column_1

                    ''')

    # defines a function to change to owner of a said territory
    def change_owner(self, new_owner):
        self.owner = new_owner
        if not os.path.exists('territory_database.SQLITE3'): #checks to see if the database file exists 
            self.database_init()
        

    
