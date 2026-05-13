# this is a test client to make sure the backend api actually works
# This will also be a refrence for me when creating the codebase

from Backend import *
from Backend.Initializer_API import initialize
from Backend.Entry_API import *

if __name__ == "__main__":
    # initialize and print the content of the table
    password = input("Password for database: ")
    DB_OBJ.encrypt(password)
    initialize()

    DB_OBJ.print_table(table_name)

    # create a few entries and then print the table result
    new_entry(web=None, user="user1", passwrd="123456789")
    new_entry(web=None, user="user2", passwrd="aaaaaaaaa")
    new_entry(web=None, user="user3", passwrd="qwertyuiopwrdydrydrrd")

    DB_OBJ.print_table(table_name)

    # change a entry
    change_entry(index=1, web="youtube.com", user=None, passwrd=None)

    DB_OBJ.print_table(table_name)

    # delete a entry
    delete_entry(index=3)

    DB_OBJ.print_table(table_name)