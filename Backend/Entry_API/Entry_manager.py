from Backend.Database_API import *
from Backend import DB_OBJ

def new_entry(web: str | None, user: str | None, passwrd: str | None):
    data = {}

    if web is not None:
        data["websites"] = web
    if user is not None:
        data["users"] = user
    if passwrd is not None:
        data["passwrds"] = passwrd

    DB_OBJ.run(query("Info").insert(**data))