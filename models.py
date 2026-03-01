from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Creature(Base):
    """ Creature record"""
    __tablename__ = 'creatures'
    id = Column(Integer, primary_key=True)
    formal_name = Column(String)
    common_name = Column(String)
    challenge_rating = Column(String)
    description = Column(String)
    experience_points = Column(String)
    alignment = Column(String)
    size = Column(String)
    age = Column(Integer)
    type = Column(String)
    sub_type = Column(String)
    race = Column(String)
    char_class = Column(String)
    level = Column(String)
    initiative = Column(String)
    perception_modifier = Column(String)
    base_armor_class = Column(String)
    touch_armor_class = Column(String)
    flat_footed_armor_class = Column(String)
    hit_points = Column(Integer)
    hit_dice = Column(String)
    fortitude = Column(Integer)
    reflex = Column(Integer)
    will = Column(Integer)
    will_modifiers = Column(String)
    damage_reduction = Column(String)
    spell_resistence = Column(String)
    speed = Column(String)
    space = Column(String)
    reach = Column(String)
    reach_modifier = Column(String)
    spell_like_caster_level = Column(String)
    spell_known_caster_level = Column(String)
    spell_prepared_caster_level = Column(String)
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)
    base_attack = Column(Integer)
    base_attack_modifier = Column(String)
    combat_maneuver_bonus = Column(Integer)
    combat_maneuver_bonus_modifier = Column(String)
    combat_maneuver_defense = Column(Integer)
    combat_maneuver_defense_modifier = Column(String)
    gear = Column(String)
    tactics = Column(String)
    racial_modifiers = Column(String)
    environment = Column(String)
    organization = Column(String)
    treasure = Column(String)
    content = Column(String)

    # Relationships (one-to-many)
    senses = relationship("CreatureSenses", back_populates="creature", cascade="all, delete-orphan")
    auras = relationship("CreatureAuras", back_populates="creature", cascade="all, delete-orphan")
    ac_modifiers = relationship("CreatureACModifiers", back_populates="creature", cascade="all, delete-orphan")
    dr_modifiers = relationship("CreatureDamageReductionModifiers", back_populates="creature", cascade="all, delete-orphan")
    sr_modifiers = relationship("CreatureSpellResistenceModifiers", back_populates="creature", cascade="all, delete-orphan")
    weaknesses = relationship("CreatureWeaknesses", back_populates="creature", cascade="all, delete-orphan")
    immune_modifiers = relationship("CreatureImmuneModifiers", back_populates="creature", cascade="all, delete-orphan")
    defensive_abilities = relationship("CreatureDefenseAbilities", back_populates="creature", cascade="all, delete-orphan")
    speed_modifiers = relationship("CreatureSpeedModifiers", back_populates="creature", cascade="all, delete-orphan")
    melee_attacks = relationship("CreatureMeleeAttacks", back_populates="creature", cascade="all, delete-orphan")
    ranged_attacks = relationship("CreatureRangedAttacks", back_populates="creature", cascade="all, delete-orphan")
    special_attacks = relationship("CreatureSpecialAttacks", back_populates="creature", cascade="all, delete-orphan")
    spell_like_abilities = relationship("CreatureSpellLikeAbilities", back_populates="creature", cascade="all, delete-orphan")
    known_spells = relationship("CreatureKnownSpells", back_populates="creature", cascade="all, delete-orphan")
    prepared_spells = relationship("CreaturePreparedSpells", back_populates="creature", cascade="all, delete-orphan")
    feats = relationship("CreatureFeats", back_populates="creature", cascade="all, delete-orphan")
    skills = relationship("CreatureSkills", back_populates="creature", cascade="all, delete-orphan")
    languages = relationship("CreatureLanguages", back_populates="creature", cascade="all, delete-orphan")
    special_qualities = relationship("CreatureSpecialQualities", back_populates="creature", cascade="all, delete-orphan")
    special_abilities = relationship("CreatureSpecialAbilities", back_populates="creature", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Creature: {}>".format(self.__dict__)


class CreatureSenses(Base):
    __tablename__ = 'creature_senses'
    id = Column(Integer, primary_key=True)
    sense = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='senses')

    def __repr__(self):
        return "<CreatureSenses: {}>".format(self.__dict__)


class CreatureAuras(Base):
    __tablename__ = 'creature_auras'
    id = Column(Integer, primary_key=True)
    aura = Column(String)
    radius = Column(String)
    save_role = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='auras')

    def __repr__(self):
        return "<CreatureAuras: {}>".format(self.__dict__)


class CreatureACModifiers(Base):
    __tablename__ = 'creature_ac_modifiers'
    id = Column(Integer, primary_key=True)
    modifier_amount = Column(String)
    modifier_type = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='ac_modifiers')

    def __repr__(self):
        return "<CreatureACModifiers: {}>".format(self.__dict__)

class CreatureDamageReductionModifiers(Base):
    __tablename__ = 'creature_damage_modifiers'
    id = Column(Integer, primary_key=True)
    reduction_against = Column(String)
    reduction_amount = Column(Integer)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='dr_modifiers')

    def __repr__(self):
        return "<CreatureDamageReductionModifiers: {}>".format(self.__dict__)


class CreatureSpellResistenceModifiers(Base):
    __tablename__ = 'creature_spell_resistence_modifiers'
    id = Column(Integer, primary_key=True)
    resists = Column(String)
    resist_amount = Column(Integer)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='sr_modifiers')

    def __repr__(self):
        return "<CreatureSpellResistenceModifiers: {}>".format(self.__dict__)


class CreatureWeaknesses(Base):
    __tablename__ = 'creature_weaknesses'
    id = Column(Integer, primary_key=True)
    weakness = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='weaknesses')

    def __repr__(self):
        return "<CreatureWeaknesses: {}>".format(self.__dict__)


class CreatureImmuneModifiers(Base):
    __tablename__ = 'creature_immune_modifiers'
    id = Column(Integer, primary_key=True)
    immune_to = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='immune_modifiers')

    def __repr__(self):
        return "<CreatureImmuneModifiers: {}>".format(self.__dict__)


class CreatureDefenseAbilities(Base):
    __tablename__ = 'creature_defensive_abilities'
    id = Column(Integer, primary_key=True)
    ability = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='defensive_abilities')

    def __repr__(self):
        return "<CreatureDefenseAbilities: {}>".format(self.__dict__)


class CreatureSpeedModifiers(Base):
    __tablename__ = 'creature_speed_modifiers'
    id = Column(Integer, primary_key=True)
    speed_modifier = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='speed_modifiers')

    def __repr__(self):
        return "<CreatureSpeedModifiers: {}>".format(self.__dict__)


class CreatureMeleeAttacks(Base):
    __tablename__ = 'creature_melee_attacks'
    id = Column(Integer, primary_key=True)
    attack = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='melee_attacks')

    def __repr__(self):
        return "<CreatureMeleeAttacks: {}>".format(self.__dict__)


class CreatureRangedAttacks(Base):
    __tablename__ = 'creature_ranged_attacks'
    id = Column(Integer, primary_key=True)
    attack = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='ranged_attacks')

    def __repr__(self):
        return "<CreatureRangedAttacks: {}>".format(self.__dict__)


class CreatureSpecialAttacks(Base):
    __tablename__ = 'creature_special_attacks'
    id = Column(Integer, primary_key=True)
    attack = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='special_attacks')

    def __repr__(self):
        return "<CreatureSpecialAttacks: {}>".format(self.__dict__)


class CreatureSpellLikeAbilities(Base):
    __tablename__ = 'creature_spell_like_abilities'
    id = Column(Integer, primary_key=True)
    rate =  Column(String)
    name = Column(String)
    modifiers = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='spell_like_abilities')

    def __repr__(self):
        return "<CreatureSpellLikeAbilities: {}>".format(self.__dict__)


class CreatureKnownSpells(Base):
    __tablename__ = 'creature_known_spells'
    id = Column(Integer, primary_key=True)
    spell_level =  Column(String)
    rate = Column(String)
    name = Column(String)
    modifiers = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='known_spells')

    def __repr__(self):
        return "<CreatureKnownSpells: {}>".format(self.__dict__)


class CreaturePreparedSpells(Base):
    __tablename__ = 'creature_prepared_spells'
    id = Column(Integer, primary_key=True)
    spell_level =  Column(Integer)
    name = Column(String)
    modifier = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='prepared_spells')

    def __repr__(self):
        return "<CreaturePreparedSpells: {}>".format(self.__dict__)


class CreatureFeats(Base):
    __tablename__ = 'creature_feats'
    id = Column(Integer, primary_key=True)
    feat = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='feats')

    def __repr__(self):
        return "<CreatureFeats: {}>".format(self.__dict__)


class CreatureSkills(Base):
    __tablename__ = 'creature_skills'
    id = Column(Integer, primary_key=True)
    skill = Column(String)
    modifier = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='skills')

    def __repr__(self):
        return "<CreatureSkills: {}>".format(self.__dict__)


class CreatureLanguages(Base):
    __tablename__ = 'creature_languages'
    id = Column(Integer, primary_key=True)
    language = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='languages')

    def __repr__(self):
        return "<CreatureLanguages: {}>".format(self.__dict__)


class CreatureSpecialQualities(Base):
    __tablename__ = 'creature_special_qualities'
    id = Column(Integer, primary_key=True)
    special_quality = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='special_qualities')

    def __repr__(self):
        return "<CreatureSpecialQualities: {}>".format(self.__dict__)


class CreatureSpecialAbilities(Base):
    __tablename__ = 'creature_special_abilities'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    ability = Column(String)
    description = Column(String)

    # Foreign key to Creatures
    creature_id = Column(Integer, ForeignKey('creatures.id'))

    # Relationships
    creature = relationship('Creature', back_populates='special_abilities')

    def __repr__(self):
        return "<CreatureSpecialAbilities: {}>".format(self.__dict__)
