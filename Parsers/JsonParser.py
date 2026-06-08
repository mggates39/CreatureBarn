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

        if  character["classes"]["@summary"]:
            class_info = character["classes"]["class"]
            self.creature.char_class = class_info["@name"]
            self.creature.level = class_info["@level"]

        self.creature.type = character["types"]["type"]["@name"]
        if character["subtypes"]:
            self.creature.sub_type = character["subtypes"]["subtype"]["@name"]

        personal = character["personal"]
        self.creature.age = personal["@age"]

        if character["languages"]:
            if type(character["languages"]["language"]) is list:
                for language in character["languages"]["language"]:
                    creature_language = CreatureLanguages()
                    creature_language.language = language["@name"].strip()
                    self.creature.languages.append(creature_language)
            else:
                language = character["languages"]["language"]
                creature_language = CreatureLanguages()
                creature_language.language = language["@name"].strip()
                self.creature.languages.append(creature_language)

        for attribute in character["attributes"]["attribute"]:
            stat_name = attribute["@name"]
            if stat_name == "Strength":
                self.creature.strength = attribute["attrvalue"]["@text"]
            elif stat_name == "Dexterity":
                self.creature.dexterity = attribute["attrvalue"]["@text"]
            elif stat_name == "Constitution":
                self.creature.constitution = attribute["attrvalue"]["@text"]
            elif stat_name == "Intelligence":
                self.creature.intelligence = attribute["attrvalue"]["@text"]
            elif stat_name == "Wisdom":
                self.creature.wisdom = attribute["attrvalue"]["@text"]
            elif stat_name == "Charisma":
                self.creature.charisma = attribute["attrvalue"]["@text"]

        for save in character["saves"]["save"]:
            save_name = save["@name"]
            if save_name == "Fortitude Save":
                self.creature.fortitude = save["@save"]
            elif save_name == "Reflex Save":
                self.creature.reflex = save["@save"]
            elif save_name == "Will Save":
                self.creature.will = save["@save"]

        self.creature.hit_points = character["health"]["@hitpoints"]
        self.creature.hit_dice = character["health"]["@hitdice"]

        if character["senses"]:
            if type(character["senses"]["special"]) is list:
                for sense in character["senses"]["special"]:
                    creature_senses = CreatureSenses()
                    creature_senses.sense = sense["@name"].strip()
                    self.creature.senses.append(creature_senses)
            else:
                sense = character["senses"]["special"]
                creature_senses = CreatureSenses()
                creature_senses.sense = sense["@name"].strip()
                self.creature.senses.append(creature_senses)

        armor_class = character["armorclass"]
        self.creature.base_armor_class = armor_class["@ac"]
        self.creature.touch_armor_class = armor_class["@touch"]
        self.creature.flat_footed_armor_class = armor_class["@flatfooted"]

        for name, value in armor_class.items():
            if value and "from" in name:
                creature_ac_modifiers = CreatureACModifiers()
                creature_ac_modifiers.modifier_amount = value.strip()
                creature_ac_modifiers.modifier_type = name.replace('@from','').strip()
                self.creature.ac_modifiers.append(creature_ac_modifiers)

        skills = character["skills"]
        for skill in skills["skill"]:
            if skill["@name"] == "Perception":
                self.creature.perception_modifier = skill["@value"]

        maneuvers = character["maneuvers"]
        self.creature.combat_maneuver_bonus = maneuvers["@cmb"]
        self.creature.combat_maneuver_defense = maneuvers["@cmd"]

        self.creature.base_attack = character["attack"]["@baseattack"]

        self.creature.initiative = character["initiative"]["@total"]

        self.creature.speed = "{} ft.".format(character["movement"]["speed"]["@value"])

        if character["melee"]:
            if type(character["melee"]["weapon"]) is list:
                for melee in character["melee"]["weapon"]:
                    creature_melee = CreatureMeleeAttacks()
                    creature_melee.attack = "{} {} ({}/{})".format(
                        melee["@name"].strip(),
                        melee["@attack"].strip(),
                        melee["@damage"].strip(),
                        melee["@crit"].strip())
                    self.creature.melee_attacks.append(creature_melee)
            else:
                melee = character["melee"]["weapon"]
                creature_melee = CreatureMeleeAttacks()
                creature_melee.attack = "{} {} ({}/{})".format(
                    melee["@name"].strip(),
                    melee["@attack"].strip(),
                    melee["@damage"].strip(),
                    melee["@crit"].strip())
                self.creature.melee_attacks.append(creature_melee)

        if character["ranged"]:
            if type(character["ranged"]["weapon"]) is list:
                for ranged in character["ranged"]["weapon"]:
                    creature_ranged = CreatureRangedAttacks()
                    creature_ranged.attack = "{} {} ({}/{})".format(
                        ranged["@name"].strip(),
                        ranged["@attack"].strip(),
                        ranged["@damage"].strip(),
                        ranged["@crit"].strip())
                    self.creature.ranged_attacks.append(creature_ranged)
            else:
                ranged = character["ranged"]["weapon"]
                creature_ranged = CreatureRangedAttacks()
                creature_ranged.attack = "{} {} ({}/{})".format(
                    ranged["@name"].strip(),
                    ranged["@attack"].strip(),
                    ranged["@damage"].strip(),
                    ranged["@crit"].strip())
                self.creature.ranged_attacks.append(creature_ranged)

        if "special" in character["attack"]:
            if type(character["attack"]["special"]) is list:
                for attack in character["attack"]["special"]:
                    creature_sp_attack = CreatureSpecialAttacks()
                    creature_sp_attack.attack = attack["@name"].strip()
                    self.creature.special_attacks.append(creature_sp_attack)
            else:
                attack = character["attack"]["special"]
                creature_sp_attack = CreatureSpecialAttacks()
                creature_sp_attack.attack = attack["@name"].strip()
                self.creature.special_attacks.append(creature_sp_attack)


        if character["skills"]:
            if type(character["skills"]["skill"]) is list:
                for skill in character["skills"]["skill"]:
                    if skill["@value"] != '0':
                        valid = True
                        if "@usable" in skill:
                            valid = False if skill["@usable"] == "no" else True
                        if valid:
                            creature_skill = CreatureSkills()
                            creature_skill.skill = skill["@name"].strip()
                            creature_skill.modifier = skill["@value"].strip()
                            self.creature.skills.append(creature_skill)
            else:
                skill = character["skills"]["skill"]
                if skill["@value"] != '0':
                    creature_skill = CreatureSkills()
                    creature_skill.skill = skill["@name"].strip()
                    creature_skill.modifier = skill["@value"].strip()
                    self.creature.skills.append(creature_skill)

        if character["feats"]["feat"]:
            if type(character["feats"]["feat"]) is list:
                for feat in character["feats"]["feat"]:
                    creature_feat = CreatureFeats()
                    creature_feat.feat = feat["@name"].strip()
                    self.creature.feats.append(creature_feat)
            else:
                feat = character["feats"]["feat"]
                creature_feat = CreatureFeats()
                creature_feat.feat = feat["@name"].strip()
                self.creature.feats.append(creature_feat)

        if character["gear"]:
            gear_list = ""
            gear_seperator = ""
            if type(character["gear"]["item"]) is list:
                for gear in character["gear"]["item"]:
                    gear_list += gear_seperator + gear["@name"].strip()
                    gear_seperator = "; "
            else:
                gear = character["gear"]["item"]
                gear_list += gear_seperator + gear["@name"].strip()

            self.creature.gear = gear_list

        if character["magicitems"]:
            if type(character["magicitems"]["item"]) is list:
                for gear in character["magicitems"]["item"]:
                    gear_item = CreatureGearItems()
                    gear_item.name = gear["@name"].strip()
                    gear_item.description = gear["description"].strip()
                    self.creature.gear_items.append(gear_item)
            else:
                gear = character["magicitems"]["item"]
                gear_item = CreatureGearItems()
                gear_item.name = gear["@name"].strip()
                gear_item.description = gear["description"].strip()
                self.creature.gear_items.append(gear_item)

        if character["otherspecials"]:
            if type(character["otherspecials"]["special"]) is list:
                for special_ability in character["otherspecials"]["special"]:
                    creature_special_ability = CreatureSpecialAbilities()
                    special_ability_match = re.search(r"(.+) (\(.+\))", special_ability["@name"].strip(), re.IGNORECASE)
                    if special_ability_match:
                        creature_special_ability.ability = special_ability_match.group(1).strip()
                        creature_special_ability.type = special_ability_match.group(2).strip()
                    else:
                        creature_special_ability.ability = special_ability["@name"].strip()
                    creature_special_ability.description = special_ability["description"].strip()
                    self.creature.special_abilities.append(creature_special_ability)
            else:
                special_ability = character["otherspecials"]["special"]
                creature_special_ability = CreatureSpecialAbilities()
                special_ability_match = re.search(r"(.+) (\(.+\))", special_ability["@name"].strip(), re.IGNORECASE)
                if special_ability_match:
                    creature_special_ability.ability = special_ability_match.group(1).strip()
                    creature_special_ability.type = special_ability_match.group(2).strip()
                else:
                    creature_special_ability.ability = special_ability["@name"].strip()
                creature_special_ability.description = special_ability["description"].strip()
                self.creature.special_abilities.append(creature_special_ability)

        if character["spellsknown"]:
            if "class" in character["classes"]:
                 self.creature.spell_known_type = character["classes"]["class"]["@castersource"].strip()
                 self.creature.spell_known_caster_level = "(CL {}; Concentration {})".format(
                     character["classes"]["class"]["@casterlevel"].strip(),
                     character["classes"]["class"]["@concentrationcheck"].strip())

            if type(character["spellsknown"]["spell"]) is list:
                for spell in character["spellsknown"]["spell"]:
                    spell_item = CreatureKnownSpells()
                    spell_item.spell_level = spell["@level"].strip()
                    if spell_item.spell_level == "0":
                        spell_item.rate = "(at will)"
                    else:
                        spell_item.rate = ""
                    spell_item.name = spell["@name"].strip()
                    if spell["@resisttext"].strip() == "Yes":
                        spell_item.modifiers = spell["@save"].strip()
                    self.creature.known_spells.append(spell_item)
            else:
                spell = character["spellsknown"]["spell"]
                spell_item = CreatureKnownSpells()
                spell_item.spell_level = spell["@level"].strip()
                if spell_item.spell_level == "0":
                    spell_item.rate = "(at will)"
                else:
                    spell_item.rate = ""
                spell_item.name = spell["@name"].strip()
                if spell["@resisttext"].strip() == "Yes":
                    spell_item.modifiers = spell["@save"].strip()
                self.creature.known_spells.append(spell_item)


        print(self.creature)