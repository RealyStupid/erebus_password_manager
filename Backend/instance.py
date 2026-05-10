# This creates an instance of the .db file and the object its connected to.
from Backend.Database_API import *

DB_OBJ = db_manager(
    "tempData",     # Will be changed in the future
    "credidentials",
    "Info",
    (
        column("index").int().primary_key().autoincrement(),
        column("websites").text().default("EMPTY"),
        column("users").text().default("EMPTY"),
        column("passwrds").text().default("EMPTY")
    )
).encrypt("password")