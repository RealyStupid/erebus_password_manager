from Backend.Database_API import *
from Backend import DB_OBJ, table_name, ind, websites, users, passwrds
from datetime import datetime

# ============================================================
# INTERNAL HELPERS
# ============================================================

def _timestamp():
    return datetime.utcnow().isoformat()

def _strength(pw: str):
    score = 0
    if len(pw) >= 12: score += 1
    if any(c.isdigit() for c in pw): score += 1
    if any(c.isupper() for c in pw): score += 1
    if any(c in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|" for c in pw): score += 1
    return score

def validate_entry(**kwargs):
    if passwrds in kwargs and not kwargs[passwrds]:
        raise ValueError("Password cannot be empty")

# ============================================================
# CREATE ENTRY
# ============================================================

def new_entry(**kwargs):
    validate_entry(**kwargs)

    data = {}

    for col in DB_OBJ.columns:
        if col in kwargs and kwargs[col] is not None and col != ind:
            data[col] = kwargs[col]

    # timestamps
    data["created_at"] = _timestamp()
    data["updated_at"] = _timestamp()

    # password strength
    if passwrds in data:
        data["strength"] = _strength(data[passwrds])

    DB_OBJ.run(query(table_name).insert(**data))

# ============================================================
# UPDATE ENTRY
# ============================================================

def change_entry(index: int, **kwargs):
    validate_entry(**kwargs)

    data = {}

    for col in DB_OBJ.columns:
        if col in kwargs and kwargs[col] is not None and col != ind:
            data[col] = kwargs[col]

    # update timestamp
    data["updated_at"] = _timestamp()

    # update strength if password changed
    if passwrds in data:
        data["strength"] = _strength(data[passwrds])

    DB_OBJ.run(query(table_name).update(**data).where(f"{ind} = ?", index))

# ============================================================
# SOFT DELETE
# ============================================================

def soft_delete(index: int):
    change_entry(index, deleted=1)

# ============================================================
# HARD DELETE + NORMALIZE
# ============================================================

def delete_entry(index: int):
    DB_OBJ.run(query(table_name).delete().where(f"{ind} = ?", index))
    normalize_indices()

def normalize_indices():
    rows = DB_OBJ.run(query(table_name).select(ind))

    new_index = 1
    for (old_index,) in rows:
        DB_OBJ.run(
            query(table_name)
            .update(**{ind: new_index})
            .where(f"{ind} = ?", old_index)
        )
        new_index += 1

# ============================================================
# FETCHING
# ============================================================

def get_entry(index: int):
    return DB_OBJ.run(
        query(table_name).select("*").where(f"{ind} = ?", index)
    )

def get_all_entries():
    return DB_OBJ.run(query(table_name).select("*"))

# ============================================================
# SEARCH
# ============================================================

def search_entries(**filters):
    conditions = []
    params = []

    for col, value in filters.items():
        if col in DB_OBJ.columns:
            conditions.append(f"{col} LIKE ?")
            params.append(f"%{value}%")

    where_clause = " AND ".join(conditions) if conditions else "1"

    return DB_OBJ.run(
        query(table_name).select("*").where(where_clause, *params)
    )

# ============================================================
# DUPLICATE DETECTION
# ============================================================

def find_duplicates():
    return DB_OBJ.run(
        query(table_name)
        .select(users, websites, "COUNT(*) as count")
        .group_by(users, websites)
        .having("count > 1")
    )

# ============================================================
# SORTING
# ============================================================

def get_sorted(by: str, descending=False):
    if by not in DB_OBJ.columns:
        raise ValueError("Invalid column")

    order = "DESC" if descending else "ASC"
    return DB_OBJ.run(
        query(table_name).select("*").order_by(f"{by} {order}")
    )

# ============================================================
# EXPORT / IMPORT
# ============================================================

def export_all():
    rows = DB_OBJ.run(query(table_name).select("*"))
    return [dict(zip(DB_OBJ.columns, row)) for row in rows]

def import_entries(entries: list[dict]):
    for entry in entries:
        new_entry(**entry)

# ============================================================
# AUDIT LOGGING (optional future expansion)
# ============================================================

def log_change(action: str, index: int, before: dict, after: dict):
    """
    Placeholder for future audit logging table.
    """
    pass
