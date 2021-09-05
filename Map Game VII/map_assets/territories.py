# imports
import sqlite3
import os.path
from main import database_init

class Territories:

    # sets up attributes of the territory
    def __init__(self, t_id, name, owner, stats):
        self.t_id = t_id
        self.name = name
        self.owner = owner
        self.stats = stats
        conn = sqlite3.connect('territory_database')
        db = conn.cursor()
        db.execute(f'''
                    INSERT INTO territories (territory_id, territory_name, owner)

                        VALUES
                        ({self.t_id}, {self.name}, {self.owner})
                    ''')
        conn.commit

    def database_edit(self):
        table_to_edit = 'territories'
        conn = sqlite3.connect('territory_database')
        db = conn.cursor()
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
            database_init()
        

    
