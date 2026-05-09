from db_manager import db_manager, column, query

if __name__ == "__main__":
    # Initialize DB (unencrypted at this moment)
    user_data = db_manager(
        "./data",
        "logins",
        "users",
        (
            column("id").int().primary_key().autoincrement(),
            column("name").text().not_null(),
            column("age").numeric().not_null(),
        )
    ).encrypt("password") # Enable full SQLCipher encryption

    # Create the encrypted .db file + table
    user_data.create_db()

    # INSERT (via QueryBuilder)
    q_insert1 = query("users").insert(name="some guy", age=17)
    q_insert2 = query("users").insert(name="Alice", age=22)
    q_insert3 = query("users").insert(name="Bob", age=30)

    user_data.run(q_insert1)
    user_data.run(q_insert2)
    user_data.run(q_insert3)

    # SELECTING
    q_specified = query("users").select("id", "name", "age")
    print("Specified select:", user_data.run(q_specified))

    q_all = query("users").select("*")
    print("select all:", user_data.run(q_all))

    # SELECT with WHERE
    q_adults = query("users").select("id", "name", "age").where("age >= 18")
    print("ADULTS:", user_data.run(q_adults))

    # UPDATE
    q_update = query("users").update(name="Umar Y").where("name = 'some guy'")
    user_data.run(q_update)

    print("AFTER UPDATE:", user_data.run(q_all))

    # DELETE
    q_delete = query("users").delete().where("name = 'Alice'")
    user_data.run(q_delete)

    print("AFTER DELETE:", user_data.run(q_all))