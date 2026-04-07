# create_tables.py
# Create all tables in the database
from Database.database import engine, Base, Database
from Database.models import Creature, CreatureLanguages, CreatureFeats, CreatureSkills, CreatureSenses, CreatureAuras, \
    CreatureACModifiers, CreatureWeaknesses, CreatureImmuneModifiers, CreatureSpellResistenceModifiers, \
    CreatureSpellLikeAbilities, CreatureKnownSpells, CreaturePreparedSpells, CreatureSpeedModifiers, \
    CreatureMeleeAttacks, CreatureRangedAttacks, CreatureSpecialQualities, CreatureSpecialAttacks, \
    CreatureDefenseAbilities, CreatureSpecialAbilities, CreatureGearItems

def create_tables():
    """Create all tables defined in models."""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

def drop_tables():
    """Drop all tables (use with caution!)."""
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped")

def initialize_repository(force_init):
    database = Database()
    database.connect()
    if not database.is_database_valid() or force_init:
        drop_tables()
        create_tables()
    database.verify_database_version()

if __name__ == "__main__":
    initialize_repository(True)