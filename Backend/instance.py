# This creates an instance of the .db file and the object its connected to.
from Backend.Database_API import *

db_name = "credidentials" # will change to a randomly generated base64 
table_name = "info" # will change to a randomly generated base64 
DB_OBJ = db_manager(
    "tempData",     # Will be changed in the future
    db_name,
    table_name,
    (
        column("ind").int().primary_key().autoincrement(),
        column("websites").text().default("EMPTY"),
        column("users").text().default("EMPTY"),
        column("passwrds").text().default("EMPTY")
    )
)