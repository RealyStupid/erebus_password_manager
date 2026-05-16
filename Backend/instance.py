# This creates an instance of the .db file and the object its connected to.
from Backend.Database_API import *

db_name = "credidentials" # will change to a randomly generated base64 
table_name = "info" # will change to a randomly generated base64 

# Some values to instance
ind = "ind"
websites = "websites"
users = "users"
passwrds = "passwrds"
DB_OBJ = db_manager(
    "tempData",     # will change in the future
    db_name,
    table_name,
    (
        column(ind).int().primary_key().autoincrement(),
        column(websites).text().default("EMPTY"),
        column(users).text().default("EMPTY"),
        column(passwrds).text().default("EMPTY"),
        column("created_at").text().default(""),
        column("updated_at").text().default(""),
        column("strength").int().default(0),
        column("deleted").int().default(0)
    )
)

def initialize():
    # at startup, this will be called to call DB_OBJ.create_db()
    DB_OBJ.create_db()