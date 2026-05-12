from Backend.Database_API import *
from Backend import *

def new_entry(web: str | None, user: str | None, passwrd: str | None):
    data = {}

    if web is not None:
        data["websites"] = web
    if user is not None:
        data["users"] = user
    if passwrd is not None:
        data["passwrds"] = passwrd

    DB_OBJ.run(query(table_name).insert(**data))

def delete_entry(index: int):
    DB_OBJ.run(query(table_name).delete().where("index = ?", index))

def change_entry(index: int, web: str | None, user: str | None, passwrd: str | None):
    data = {}

    if web is not None:
        data["websites"] = web
    if user is not None:
        data["users"] = user
    if passwrd is not None:
        data["passwrds"] = passwrd

    DB_OBJ.run(query(table_name).update(**data).where("index = ?", index))