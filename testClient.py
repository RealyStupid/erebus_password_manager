# this is a test client to make sure the backend api actually works
# This will also be a reference for me when creating the codebase

from Backend import *
from Backend.Entry_API import *

if __name__ == "__main__":
    # initialize and print the content of the table
    password = input("Password for database: ")
    DB_OBJ.encrypt(password)
    initialize()

    DB_OBJ.print_table(table_name)

    # create a few entries and then print the table result
    new_entry(users="user1", passwrds="123456789")
    new_entry(websites="roblox.com", users="user2", passwrds="aaaaaaaaa")
    new_entry(users="user3", passwrds="qwertyuiopwrdydrydrrd")
    new_entry(users="user1", passwrds="123456789")
    new_entry(websites="roblox.com", users="user2", passwrds="aaaaaaaaa")
    new_entry(users="user3", passwrds="qwertyuiopwrdydrydrrd")
    new_entry(users="user1", passwrds="123456789")
    new_entry(websites="roblox.com", users="user2", passwrds="aaaaaaaaa")
    new_entry(users="user3", passwrds="qwertyuiopwrdydrydrrd")

    DB_OBJ.print_table(table_name)

    # change an entry (index 1)
    change_entry(1, websites="youtube.com")

    DB_OBJ.print_table(table_name)

    # delete entry with index 3
    delete_entry(3)

    DB_OBJ.print_table(table_name)

    print(get_all_entries())
