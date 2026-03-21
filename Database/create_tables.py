# create_tables.py
# Create all tables in the database
from Database.database import engine, Base


def create_tables():
    """Create all tables defined in models."""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

def drop_tables():
    """Drop all tables (use with caution!)."""
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped")

if __name__ == "__main__":
    drop_tables()
    create_tables()