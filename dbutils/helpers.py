from psycopg import sql, connect
from pathlib import Path
from typing import Iterable, List
import os


def upsert(
    table_name: str, columns: list[str], values: list[str], conflict_columns: list[str]
):
    with open(Path(__file__).parent / "routines" / "upsert.sql", "r") as f:
        query_template = sql.SQL(f.read())
    query = query_template.format(
        table_name=sql.Identifier(table_name),
        columns=sql.SQL(", ").join(map(sql.Identifier, columns)),
        values=sql.SQL(", ").join(map(sql.Literal, values)),
        conflict_columns=sql.SQL(", ").join(map(sql.Identifier, conflict_columns)),
        updates=sql.SQL(", ").join(
            map(
                lambda col: sql.SQL("{} = EXCLUDED.{}".format(col, col)),
                columns,
            )
        ),
    )
    execute_query(query)


def batch_upsert(
    table_name: str,
    columns: List[str],
    values: Iterable[Iterable[str]],
    conflict_columns: List[str],
):
    with open(Path(__file__).parent / "routines" / "upsert.sql", "r") as f:
        query_template = sql.SQL(f.read())
    query = query_template.format(
        table_name=sql.Identifier(table_name),
        columns=sql.SQL(", ").join(map(sql.Identifier, columns)),
        values=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
        conflict_columns=sql.SQL(", ").join(map(sql.Identifier, conflict_columns)),
        updates=sql.SQL(", ").join(
            map(
                lambda col: sql.SQL("{} = EXCLUDED.{}".format(col, col)),
                columns,
            )
        ),
    )
    batch_execute_query(query, values)


def drop(table_name: str):
    with open(Path(__file__).parent / "routines" / "drop.sql", "r") as f:
        query_template = sql.SQL(f.read())
    query = query_template.format(
        table_name=sql.Identifier(table_name),
    )
    execute_query(query)


def init_database():
    """Initialize the database with all schema files."""

    # Get all SQL files in order (identification must be first due to foreign keys)
    table_names = [
        "identification",  # Must be first for foreign key references
        "status",
        "conditions",
        "collaborators",
        "oversight",
        "design",
        "phases",
        "eligibility",
        "groups",
        "interventions",
        "outcome",
        "facility",
        "contact",
        "officials",
    ]

    try:
        # Execute each SQL file
        for table_name in table_names:
            drop(table_name)

        for table_name in table_names:
            file_path = Path(__file__).parent / "ddl" / f"{table_name}.sql"
            with open(file_path, "r") as f:
                sql = f.read()
                execute_query(sql)

        print("Database schema initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")


def get_connection():
    """Get a connection to the PostgreSQL database."""
    return connect(
        dbname=os.getenv("DBNAME", "argon_db"),
        user=os.getenv("DBUSER", "argon_user"),
        password=os.getenv("DBPASSWORD", "somepassword"),
        host=os.getenv("DBHOST", "localhost"),
        port=os.getenv("DBPORT", "5432"),
    )


def batch_execute_query(query, params, batch_size=100):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for i in range(0, len(params), batch_size):
                batch = params[i : (i + batch_size)]
                cur.executemany(query, batch)
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def execute_query(query, params=None):
    """Execute a query and return results."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                return cur.fetchall()
            conn.commit()
            return None
    except Exception as e:
        conn.rollback()
        print(query.as_string())
        raise e
    finally:
        conn.close()
