# database.py
# Database connection and session setup
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL format: dialect+driver://user:password@host:port/database
# DATABASE_URL = "postgresql://user:password@localhost/mydb"

# For SQLite (file-based)
DATABASE_URL = "sqlite:///./creature_barn.db"

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