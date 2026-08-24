import sqlite3
from pathlib import Path
from utils.logger import logger

class DatabaseHelper:
    """
    DatabaseHelper wraps standard database connection and query execution patterns.
    It provides clean methods to execute DML commands (INSERT, UPDATE, DELETE) and 
    fetch query outputs formatted automatically as standard Python dictionaries.
    
    Defaults to SQLite for a lightweight, zero-dependency local setup.
    """
    def __init__(self, db_path: str = None):
        if not db_path:
            # Place the local sqlite file in the reports/ directory
            db_path = str(Path(__file__).resolve().parent.parent / "reports" / "test_database.db")
        self.db_path = db_path
        self._initialize_tables()

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes and returns a connection to the SQL database."""
        conn = sqlite3.connect(self.db_path)
        # Row factory allows row results to be accessed by field name (dict-like)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_tables(self):
        """Initializes testing tables if they do not already exist."""
        logger.info(f"Initializing local test database at: {self.db_path}")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    user_id INTEGER NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    category_name TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    pet_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    complete BOOLEAN NOT NULL
                )
            """)
            conn.commit()

    def execute(self, query: str, params: tuple = ()) -> int:
        """
        Executes a write/transactional query (INSERT, UPDATE, DELETE).
        Returns the count of modified rows.
        """
        logger.debug(f"DB Execute -> Query: {query} | Params: {params}")
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f"Database execution error: {e}")
            raise

    def fetch_one(self, query: str, params: tuple = ()) -> dict:
        """
        Executes a read query and returns a single row formatted as a dictionary.
        Returns None if no matching records are found.
        """
        logger.debug(f"DB Fetch One -> Query: {query} | Params: {params}")
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"Database query fetch_one error: {e}")
            raise

    def fetch_all(self, query: str, params: tuple = ()) -> list:
        """
        Executes a read query and returns all matching rows formatted as a list of dictionaries.
        """
        logger.debug(f"DB Fetch All -> Query: {query} | Params: {params}")
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Database query fetch_all error: {e}")
            raise
