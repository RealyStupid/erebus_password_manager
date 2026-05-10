import sqlcipher3
from typing import Iterable

class _ColumnBuilder:
    def __init__(self, name: str):
        self.name = name
        self.type = None
        self.constraints = []
        self._type_set = False
        self._finalized = False

    def __repr__(self):
        return f"<RowBuilder {self.to_sql()}>"

    # datatypes
    def int(self):
        if self._type_set:
            raise ValueError("[Invalid Chaining] Type already set for this column")
        self._type_set = True
        self.type = "INTEGER"
        return self

    def text(self):
        if self._type_set:
            raise ValueError("[Invalid Chaining] Type already set for this column")
        self._type_set = True
        self.type = "TEXT"
        return self

    def real(self):
        if self._type_set:
            raise ValueError("[Invalid Chaining] Type already set for this column")
        self._type_set = True
        self.type = "REAL"
        return self
    
    def blob(self):
        if self._type_set:
            raise ValueError("[Invalid Chaining] Type already set for this column")
        self._type_set = True
        self.type = "BLOB"
        return self
    
    def numeric(self):
        if self._type_set:
            raise ValueError("[Invalid Chaining] Type already set for this column")
        self._type_set = True
        self.type = "NUMARIC"
        return self
    
    # aliases
    def boolean(self): return self.numeric()
    def float(self): return self.real()
    def double(self): return self.real()
    def date(self): return self.text()
    def datetime(self): return self.text()

    # constraints
    def primary_key(self):
        if not self._type_set:
            raise ValueError("Set a type before adding constraints")
        if "PRIMARY KEY" in self.constraints:
            raise ValueError("PRIMARY KEY already applied")
        self.constraints.append("PRIMARY KEY")
        return self

    def not_null(self):
        if not self._type_set:
            raise ValueError("Set a type before NOT NULL")
        if "NOT NULL" in self.constraints:
            raise ValueError("NOT NULL already applied")
        self.constraints.append("NOT NULL")
        return self

    def unique(self):
        if "UNIQUE" in self.constraints:
            raise ValueError("UNIQUE already applied")
        self.constraints.append("UNIQUE")
        return self

    def default(self, value):
        if isinstance(value, str):
            value = f"'{value}'"
        self.constraints.append(f"DEFAULT {value}")
        return self

    def check(self, expression: str):
        self.constraints.append(f"CHECK ({expression})")
        return self

    def collate(self, collation: str):
        self.constraints.append(f"COLLATE {collation}")
        return self

    def autoincrement(self):
        if self.type != "INTEGER":
            raise ValueError("AUTOINCREMENT requires INTEGER type")
        if "PRIMARY KEY" not in self.constraints:
            raise ValueError("AUTOINCREMENT requires PRIMARY KEY")
        self.constraints.append("AUTOINCREMENT")
        return self
    
    def foreign_key(self, reference: str):
        self.constraints.append(f"REFERENCES {reference}")
        return self

    def on_conflict(self, rule: str):
        rule = rule.upper()
        if rule not in ("ROLLBACK", "ABORT", "FAIL", "IGNORE", "REPLACE"):
            raise ValueError("Invalid ON CONFLICT rule")
        self.constraints.append(f"ON CONFLICT {rule}")
        return self

    def to_sql(self):
        if not self._type_set:
            raise ValueError("Column type not set")
        return " ".join([self.name, self.type] + self.constraints)

class _QueryBuilder:
    def __init__(self, table: str):
        self.table = table

        self._mode = None  # SELECT / INSERT / UPDATE / DELETE

        # SELECT state
        self._select_cols = []
        self._joins = []
        self._where = []
        self._group_by = []
        self._having = []
        self._order_by = None
        self._limit = None
        self._offset = None

        # INSERT state
        self._insert_cols = []
        self._insert_vals = []

        # UPDATE state
        self._update_pairs = {}

    # SELECT
    def select(self, *cols):
        self._mode = "SELECT"
        self._select_cols.extend(cols)
        return self

    def join(self, table, on):
        self._joins.append(f"JOIN {table} ON {on}")
        return self

    def left_join(self, table, on):
        self._joins.append(f"LEFT JOIN {table} ON {on}")
        return self

    def where(self, condition):
        self._where.append(condition)
        return self

    def group_by(self, *cols):
        self._group_by.extend(cols)
        return self

    def having(self, condition):
        self._having.append(condition)
        return self

    def order_by(self, col, direction="ASC"):
        direction = direction.upper()
        self._order_by = f"{col} {direction}"
        return self

    def limit(self, n):
        self._limit = n
        return self

    def offset(self, n):
        self._offset = n
        return self

    # INSERT
    def insert(self, **kwargs):
        self._mode = "INSERT"
        for col, val in kwargs.items():
            self._insert_cols.append(col)
            self._insert_vals.append(val)
        return self

    # UPDATE
    def update(self, **kwargs):
        self._mode = "UPDATE"
        for col, val in kwargs.items():
            self._update_pairs[col] = val
        return self

    # DELETE
    def delete(self):
        self._mode = "DELETE"
        return self

    def to_sql(self):
        if self._mode == "SELECT":
            return self._build_select()
        if self._mode == "INSERT":
            return self._build_insert()
        if self._mode == "UPDATE":
            return self._build_update()
        if self._mode == "DELETE":
            return self._build_delete()
        raise ValueError("No query mode selected")

    def _build_select(self):
        cols = ", ".join(self._select_cols) if self._select_cols else "*"
        sql = f"SELECT {cols} FROM {self.table}"

        if self._joins:
            sql += " " + " ".join(self._joins)
        if self._where:
            sql += " WHERE " + " AND ".join(self._where)
        if self._group_by:
            sql += " GROUP BY " + ", ".join(self._group_by)
        if self._having:
            sql += " HAVING " + " AND ".join(self._having)
        if self._order_by:
            sql += f" ORDER BY {self._order_by}"
        if self._limit is not None:
            sql += f" LIMIT {self._limit}"
        if self._offset is not None:
            sql += f" OFFSET {self._offset}"

        return sql + ";"

    def _build_insert(self):
        cols = ", ".join(self._insert_cols)
        placeholders = ", ".join([repr(v) for v in self._insert_vals])
        return f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders});"

    def _build_update(self):
        pairs = ", ".join([f"{col} = {repr(val)}" for col, val in self._update_pairs.items()])
        sql = f"UPDATE {self.table} SET {pairs}"
        if self._where:
            sql += " WHERE " + " AND ".join(self._where)
        return sql + ";"

    def _build_delete(self):
        sql = f"DELETE FROM {self.table}"
        if self._where:
            sql += " WHERE " + " AND ".join(self._where)
        return sql + ";"

def column(name: str) -> _ColumnBuilder:
    """Set columns for your database."""
    return _ColumnBuilder(name)

def query(table: str) -> _QueryBuilder:
    """Create a query for your Database."""
    return _QueryBuilder(table)

class db_manager:
    def __init__(self, directory: str, db_name: str, table_name: str, schema: Iterable):
        """
        Creates a database object linked to the desired .db file.
        `schema` is an iterable of _ColumnBuilder instances.
        """
        self.table_name = table_name
        self.directory = directory
        self.db_name = db_name

        # Build schema SQL
        self.schema = ", ".join(col.to_sql() for col in schema)

        # Encryption
        self._encryption_key = None  # Set by .encrypt()

        print("Database Initialized with:")
        print(f"Name: {db_name}.db")
        print(f"Directory: {directory}")
        print(f"Table Name: {table_name}")
        print(f"Schema: {self.schema}")

    # INTERNAL CONNECTION HANDLER (SQLCipher)
    def _connect(self):
        """
        Always uses SQLCipher. If encryption key is set, apply it.
        """
        # ensure directory exists
        _os = __import__("os")
        _os.makedirs(self.directory, exist_ok=True)

        path = f"{self.directory}/{self.db_name}.db"
        conn = sqlcipher3.connect(path)

        if self._encryption_key is not None:
            # Apply key FIRST
            conn.execute(f"PRAGMA key = '{self._encryption_key}';")

            # Force SQLCipher 4.x format parameters for new DBs and ensure strong KDF/HMAC
            # These must be set immediately after the key and before creating any schema.
            try:
                conn.execute("PRAGMA cipher_page_size = 4096;")
                conn.execute("PRAGMA kdf_iter = 256000;")
                conn.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA512;")
                conn.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA512;")
                # Set compatibility to 4 to ensure SQLCipher4 format is used
                conn.execute("PRAGMA cipher_compatibility = 4;")
            except Exception:
                # Some sqlcipher3 builds may not expose all PRAGMAs; ignore and continue,
                # but surface a warning via an exception later if the DB is unreadable.
                pass

            # If the file already existed and used an older format, attempt migration.
            # This will succeed only if the key is correct and the runtime supports migration.
            try:
                conn.execute("PRAGMA cipher_migrate;")
            except Exception:
                # If migration fails, we don't automatically overwrite; caller should handle.
                pass

        return conn

    # DATABASE CREATION
    def create_db(self):
        """
        Create the main table defined in __init__.
        """
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({self.schema})")
        conn.commit()
        conn.close()

    def create_table(self, table_name: str, schema: Iterable):
        """
        Create an additional table with the given schema.
        """
        schema_sql = ", ".join(col.to_sql() for col in schema)
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema_sql})")
        conn.commit()
        conn.close()

    # INTERNAL RAW SQL HELPERS
    def _execute_sql(self, sql: str):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()

    def _fetchall_sql(self, sql: str):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows

    def _fetchone_sql(self, sql: str):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        conn.close()
        return row

    # ENABLE FULL-DATABASE ENCRYPTION
    def encrypt(self, key: str):
        """
        Enable full-database encryption using SQLCipher.
        Must be called BEFORE writing any data.
        """
        self._encryption_key = key
        print("Full database encryption enabled (SQLCipher).")
        return self  # allow chaining

    # PUBLIC QUERY EXECUTION (QueryBuilder only)
    def run(self, builder):
        sql = builder.to_sql()
        mode = builder._mode

        if mode == "SELECT":
            return self._fetchall_sql(sql)

        self._execute_sql(sql)
        return None
