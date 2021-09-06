#imports
import sqlite3
from map_assets import territories
from empire_setup import empires

territories.Territories.database_init()
california = empires.Empires('California', 'Swordlord', 'Irvine')
print(california.name + ' rules from ' + california.capital + f' and their user is {california.user}')