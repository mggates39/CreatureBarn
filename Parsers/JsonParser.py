import json
import re
from Parsers.CreatureParser import _normalize_mixed_case
from Database.models import Creature, CreatureLanguages, CreatureFeats, CreatureSkills, CreatureSenses, CreatureAuras, \
    CreatureACModifiers, CreatureWeaknesses, CreatureImmuneModifiers, CreatureSpellResistenceModifiers, \
    CreatureSpellLikeAbilities, CreatureKnownSpells, CreaturePreparedSpells, CreatureSpeedModifiers, \
    CreatureMeleeAttacks, CreatureRangedAttacks, CreatureSpecialQualities, CreatureSpecialAttacks, \
    CreatureDefenseAbilities, CreatureSpecialAbilities, CreatureGearItems


class CreatureJsonParser:
    def __init__(self, json_string, options):
        self.creature = Creature()
        self.creature.formal_name = ''
        self.creature.space = '5 ft.'
        self.creature.reach = '5 ft.'
        self.gear_item = None
        self.special_ability = None
        self.options = options
        self.input_json = json.loads(json_string)

    def run(self):
        character = self.input_json["document"]["public"]["character"]
        self.creature.formal_name = character["@name"]
        self.creature.common_name = character["@name"]
        challenge_rating = character["challengerating"]["@text"]
        cr_match = re.search(r"CR\s+([\d/]+)", challenge_rating, re.IGNORECASE)
        if cr_match:
            self.creature.challenge_rating = cr_match.group(1)
        self.creature.experience_points = character["xpaward"]["@value"]
        self.creature.race = _normalize_mixed_case(character["race"]["@name"])
        alignment = character["alignment"]["@name"]
        if alignment == "True Neutral":
            alignment = "Neutral"
        self.creature.alignment =  "".join(word[0] for word in alignment.split(' '))

        size = character["size"]
        self.creature.size = size["@name"]
        self.creature.space = size["space"]["@value"] + " ft"
        self.creature.reach = size["reach"]["@value"] + " ft"

        class_info = character["classes"]["class"]
        self.creature.char_class = class_info["@name"]
        self.creature.level = class_info["@level"]

        self.creature.type = character["types"]["type"]["@name"]
        self.creature.sub_type = character["subtypes"]["subtype"]["@name"]

        for language in character["languages"]["language"]:
            creature_language = CreatureLanguages()
            creature_language.language = language["@name"].strip()
            self.creature.languages.append(creature_language)



        print(self.creature)