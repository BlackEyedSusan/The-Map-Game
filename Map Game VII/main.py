#imports
import sqlite3
from map_assets import territories
import os
if not os.path.exists('database.db'): #checks to see if the database file exists 
    territories.territory_database_init()
    from map_assets import defaultmapstats
from empire_setup import empires
empires.Empires.empire_database_init()
from military_setup import military



california = empires.Empires('California', 'Swordlord', 'Irvine', 1)
running = True
california.get_territories()
while running:
    command = input("What is your next command? ")

    if command == 'create empire':
        name = input("What will its name be? ")
        user = input("Who is the user? ")
        capital = input("Where is the capital city? ")
        new_empire = empires.Empires(name, user, capital)
        print(name + ' rules from ' + capital + f' and their user is {user}')

    if command == 'create unit':
        unit_type = input("What type of unit shall it be? ")
        location = input("What is the id of the province you are spawning the unit in? ")
        owner = input("Who is the owner of this unit? ")
        new_unit = military.Military(unit_type, location, owner)
        print(f"New {unit_type} unit created for {owner}")

    if command == 'change owner':
        territory = input('Which territory? ')
        new_owner = input('Who is the new owner? ')
        conn = sqlite3.connect('database.db')
        db = conn.cursor()
        db.execute(f'''
                    UPDATE territories
                    SET owner = '{new_owner}'
                    WHERE territory_name = '{territory}'
                    ''')
        conn.commit()

    if command == 'territory list':
        conn = sqlite3.connect('database.db')
        db = conn.cursor()
        db.execute(f'''
                    SELECT * FROM territories
                    ''')
        result = db.fetchall()
        print(result)

    if command == 'get territory':
        territory = input('What territory would you like to see? ')
        conn = sqlite3.connect('database.db')
        db = conn.cursor()
        db.execute(f'''
                    SELECT * FROM territories
                    ''')
        result = db.fetchall()
        found = False
        for row in result:
            if str(row[1]).lower() == territory.lower():
                output = row
                found = True
        if not found:
            print('Territory doesn\'t exist.')
        else:
            print(output)

    if command == 'quit':
        running = False