# A test to see the db_manager.py actually works
from Backend.Database_API import column, query, db_manager

if __name__ == "__main__":
    # Initialize DB (unencrypted at this moment)
    user_data = db_manager(
        "./Backend/Database_API/tempData",
        "logins",
        "users",
        (
            column("id").int().primary_key().autoincrement(),
            column("name").text().not_null(),
            column("age").numeric().not_null(),
        )
    ).encrypt("password")  # Enable full SQLCipher encryption

    # Create the encrypted .db file + table
    user_data.create_db()

    # INSERT (via QueryBuilder)
    user_data.run(query("users").insert(name="some guy", age=17))
    user_data.run(query("users").insert(name="Alice", age=22))
    user_data.run(query("users").insert(name="Bob", age=30))

    # SELECTING
    q_specified = query("users").select("id", "name", "age")
    print("Specified select:", user_data.run(q_specified))

    q_all = query("users").select("*")
    print("select all:", user_data.run(q_all))

    # SELECT with WHERE (strict mode requires placeholders)
    q_adults = query("users").select("id", "name", "age").where("age >= ?", 18)
    print("ADULTS:", user_data.run(q_adults))

    # UPDATE (strict mode requires placeholders)
    q_update = query("users").update(name="Umar Y").where("name = ?", "some guy")
    user_data.run(q_update)

    print("AFTER UPDATE:", user_data.run(q_all))

    # DELETE (strict mode requires placeholders)
    q_delete = query("users").delete().where("name = ?", "Alice")
    user_data.run(q_delete)

    print("AFTER DELETE:", user_data.run(q_all))
