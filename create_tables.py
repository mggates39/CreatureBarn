# create_tables.py
# Create all tables in the database
from database import engine, Base
from models import (Creature, CreatureSenses, CreatureAuras, CreatureACModifiers, CreatureDamageReductionModifiers,
                    CreatureSpellResistenceModifiers, CreatureWeaknesses, CreatureImmuneModifiers,
                    CreatureDefenseAbilities, CreatureSpeedModifiers, CreatureMeleeAttacks,
                    CreatureRangedAttacks, CreatureSpecialAttacks, CreatureSpellLikeAbilities,
                    CreatureKnownSpells, CreaturePreparedSpells, CreatureFeats, CreatureSkills,
                    CreatureLanguages, CreatureSpecialQualities, CreatureSpecialAbilities)  # Import models to register them

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