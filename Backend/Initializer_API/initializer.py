# This File makes sure the .db file has been created before or (is its missing) create one
from Backend import DB_OBJ

def initialize():
    # at startup, this will be called to call DB_OBJ.create_db()
    DB_OBJ.create_db()