# database.py
# Database connection and session setup
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL format: dialect+driver://user:password@host:port/database
# DATABASE_URL = "postgresql://user:password@localhost/mydb"

# For SQLite (file-based)
DATABASE_NAME = 'creature_barn.db'
DATABASE_URL = "sqlite:///./"+DATABASE_NAME
DATABASE_VERSION = '1'

# Create the engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL statements (disable in production)
    pool_size=5,  # Connection pool size
    max_overflow=10  # Extra connections when pool is full
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

my_db = SessionLocal()

# Base class for models
Base = declarative_base()


# Dependency for getting database sessions
def get_db():
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def upgrade():
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE creatures ADD COLUMN barn_type VARCHAR(16)"))
        conn.execute(text("UPDATE creatures set barn_type = 'Creature'"))
        conn.execute(text("UPDATE creatures set barn_type = 'NPC' WHERE `race` is not null"))
        conn.commit()


class Database:
    version = DATABASE_VERSION
    con = None
    cur = None

    def connect(self):
        if self.con is None:
            self.con = sqlite3.connect(DATABASE_NAME)
            self.con.row_factory = sqlite3.Row

    def is_database_valid(self) -> bool:
        self.create_cursor()
        try:
            self.fetch_all("select version from db_version", {})
            return True
        except sqlite3.DatabaseError:
            self.init_database_version()
            return False

    def get_expected_version(self):
        return self.version

    def get_actual_version(self):
        self.create_cursor()
        version = self.fetch_all("select version from db_version", {})
        if version:
            return version[0][0]
        else:
            self.cur.execute("insert into db_version (version) values(:ver)",
                             {"ver": '0'})
            self.commit()
            return '0'

    def update_database_version(self, new_database_version):
        self.cur.execute("update db_version set version = :ver",
                         {"ver": new_database_version})
        self.commit()

    def create_cursor(self):
        self.connect()
        if self.cur is None:
            self.cur = self.con.cursor()

    def init_database_version(self):
        self.create_cursor()
        self.cur.execute("create table db_version ( version )")
        self.cur.execute("insert into db_version (version) values(:ver)",
                         {"ver": self.version})
        self.commit()

    def execute_query(self, query, parameters):
        self.create_cursor()
        self.cur.execute(query, parameters)

    def execute_many_query(self, query, parameters):
        self.create_cursor()
        self.cur.executemany(query, parameters)

    def commit(self):
        self.con.commit()

    def rollback(self):
        self.con.rollback()

    def fetch_all(self, query, parameters):
        self.create_cursor()
        self.cur.execute(query, parameters)
        return self.cur.fetchall()

    def close_cursor(self, commit=True):
        if self.cur is not None:
            if self.con.in_transaction:
                if commit:
                    self.con.commit()
                else:
                    self.con.rollback()
            self.cur.close()
            self.cur = None

    def disconnect(self):
        if self.con is not None:
            self.close_cursor()
            self.con.close()
            self.con = None

    def verify_database_version(self):
        actual_version = self.get_actual_version()
        expected_version = self.get_expected_version()
        if actual_version < expected_version:
            print("Updating from version {} to version {}".format(actual_version, expected_version))
            # @TODO: Update the data structures
            # Then update version number in the database
            self.update_database_version(expected_version)
        elif actual_version > expected_version:
            print("Error Database version {} is newer than the code {}!".format(actual_version, expected_version))
            exit(-1)
        else:
            print("Database version {} is current.".format(actual_version))
