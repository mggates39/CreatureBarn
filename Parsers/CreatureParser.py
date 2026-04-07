from Database.models import Creature, CreatureLanguages, CreatureFeats, CreatureSkills, CreatureSenses, CreatureAuras, \
    CreatureACModifiers, CreatureWeaknesses, CreatureImmuneModifiers, CreatureSpellResistenceModifiers, \
    CreatureSpellLikeAbilities, CreatureKnownSpells, CreaturePreparedSpells, CreatureSpeedModifiers, \
    CreatureMeleeAttacks, CreatureRangedAttacks, CreatureSpecialQualities, CreatureSpecialAttacks, \
    CreatureDefenseAbilities, CreatureSpecialAbilities, CreatureGearItems
import re


def _normalize_mixed_case(text: str) -> str:
    parts = [p.strip() for p in text.split(",")]
    return ", ".join(p[:1].upper() + p[1:] for p in parts)

def _normalize_lower_case(text: str) -> str:
    parts = [p.strip() for p in text.split(",")]
    return ", ".join(p.lower() for p in parts)

def transition_skip(fsm_obj):
    pass

def transition_parse_formal_name(fsm_obj):
    fsm_obj.creature.formal_name = fsm_obj.current_line.strip()

def transition_parse_common_name(fsm_obj):
    name_match = re.match(R_COMMON_NAME, fsm_obj.current_line)
    if name_match:
        fsm_obj.creature.common_name = name_match.group(1).strip()
        if fsm_obj.creature.formal_name == '':
            fsm_obj.creature.formal_name = fsm_obj.creature.common_name

    cr_match = re.search(r"CR\s+([\d/]+)", fsm_obj.current_line, re.IGNORECASE)
    if cr_match:
        fsm_obj.creature.challenge_rating = cr_match.group(1)

    transition_parse_experience_points(fsm_obj)

def transition_parse_description(fsm_obj):
    description = fsm_obj.creature.description
    if description:
        description += fsm_obj.current_line + "\n"
    else:
        description = fsm_obj.current_line + "\n"
    fsm_obj.creature.description = description

def transition_parse_experience_points(fsm_obj):
    xp_match = re.search(R_EXPERIENCE, fsm_obj.current_line, re.IGNORECASE)
    if xp_match:
        fsm_obj.creature.experience_points = xp_match.group(1)

def transition_parse_alignment(fsm_obj):
    type_match = re.match(
        r"(?P<alignment>[LNCEG]{1,2})\s+(?P<size>\w+)?\s+(?P<type>[^\n]+)",
        fsm_obj.current_line,
        re.IGNORECASE,
    )
    if type_match:
        fsm_obj.creature.alignment = type_match.group("alignment").upper()
        fsm_obj.creature.size = type_match.group("size") or ""
        type_sub_type = type_match.group("type").strip().title()
        matches = re.match("(.+) (\\((.+)\\))", type_sub_type)
        if matches:
            fsm_obj.creature.type = matches.group(1)
            if matches.group(3):
                fsm_obj.creature.sub_type = matches.group(3)
        else:
            matches = re.match("(.+)", type_sub_type)
            if matches:
                fsm_obj.creature.type = matches.group(1)

def transition_parse_race(fsm_obj):
    parts = fsm_obj.current_line.split(' ')
    fsm_obj.creature.level = parts[-1]
    fsm_obj.creature.char_class = parts[-2]
    fsm_obj.creature.race = " ".join(parts[:-2])

def transition_parse_initiative(fsm_obj):
    parts = fsm_obj.current_line.split(';')
    for part in parts:
        init_match = re.search(r"Init\s+([^\n;]+)", part, re.IGNORECASE)
        if init_match:
            fsm_obj.creature.initiative = init_match.group(1).strip()

        perceptions_match = re.search(r"Perception ([+\d]+)", part, re.IGNORECASE)
        if perceptions_match:
            fsm_obj.creature.perception_modifier = perceptions_match.group(1).strip()

        senses_match = re.search(r"Senses\s+(.*)", part, re.IGNORECASE)
        if senses_match:
            senses = _normalize_mixed_case(senses_match.group(1)).split(",")
            for sense in senses:
                perceptions_match = re.search(r"Perception ([+\d]+)", sense, re.IGNORECASE)
                if perceptions_match:
                    fsm_obj.creature.perception_modifier = perceptions_match.group(1).strip()
                else:
                    creature_senses = CreatureSenses()
                    creature_senses.sense = sense.strip()
                    fsm_obj.creature.senses.append(creature_senses)

        aura_match = re.search(r"Aura\s+(.+)", part, re.IGNORECASE)
        if aura_match:
            fsm_obj.current_line = part
            transition_parse_auras(fsm_obj)

def transition_parse_auras(fsm_obj):
    aura_match = re.search(r"Aura\s+(.+)", fsm_obj.current_line)
    if aura_match:
        aura_details = re.findall(r"([, ]*(.+?)\s\((.+?),\s(.+?)\))+?", aura_match.group(1), re.IGNORECASE)
        if aura_details:
            for aura_detail in aura_details:
                creature_auras = CreatureAuras()
                creature_auras.aura = aura_detail[1].strip()
                creature_auras.radius = aura_detail[2].strip()
                creature_auras.save_role = aura_detail[3].strip()
                fsm_obj.creature.auras.append(creature_auras)

def transition_parse_armor_class(fsm_obj):
    ac_match = re.search(r"AC\s([+\d]+), touch\s([+\d]+), flat-footed\s([+\d]+) \((.+)\)", fsm_obj.current_line, re.IGNORECASE)
    if not ac_match:
        ac_match = re.search(r"AC\s([+\d]+), touch\s([+\d]+), flat-footed\s([+\d]+)", fsm_obj.current_line,
                             re.IGNORECASE)
    if ac_match:
        fsm_obj.creature.base_armor_class = ac_match.group(1)
        fsm_obj.creature.touch_armor_class = ac_match.group(2)
        fsm_obj.creature.flat_footed_armor_class = ac_match.group(3)
        if len(ac_match.groups()) > 3:
            modifiers = ac_match.group(4).split(",")
            for modifier in modifiers:
                mod_match = re.search(r"(.\d+)\s(.+)", modifier)
                if mod_match:
                    creature_ac_modifiers = CreatureACModifiers()
                    creature_ac_modifiers.modifier_amount = mod_match.group(1).strip()
                    creature_ac_modifiers.modifier_type = mod_match.group(2).strip()
                    fsm_obj.creature.ac_modifiers.append(creature_ac_modifiers)

def transition_parse_hit_points(fsm_obj):
    hp_match = re.search(r"HP\s(\d+)\s\((.+)\)", fsm_obj.current_line, re.IGNORECASE)
    if hp_match:
        fsm_obj.creature.hit_points = hp_match.group(1).strip()
        if hp_match.group(2):
            fsm_obj.creature.hit_dice = hp_match.group(2).strip()


def transition_parse_fortitude(fsm_obj):
    fortitude = fsm_obj.current_line.split(';')
    match_fortitude = re.findall(r"(Fort|Ref|Will)\s*([+\-]?\d+)", fortitude[0], re.IGNORECASE)
    for stat, val in match_fortitude:
        stat_name = stat.capitalize()
        if stat_name == "Fort":
            fsm_obj.creature.fortitude = val
        elif stat_name == "Ref":
            fsm_obj.creature.reflex = val
        elif stat_name == "Will":
            fsm_obj.creature.will = val

    if len(fortitude) > 1:
        fsm_obj.creature.will_modifiers = fortitude[1].strip()

def transition_parse_weakness(fsm_obj):
    weakness_match = re.search(r"Weaknesses\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if weakness_match:
        for weakness in _normalize_mixed_case(weakness_match.group(1)).split(","):
            creature_weakness = CreatureWeaknesses()
            creature_weakness.weakness = weakness.strip()
            fsm_obj.creature.weaknesses.append(creature_weakness)

def transition_parse_damage_resistance(fsm_obj):
    parts = fsm_obj.current_line.split(';')
    for part in parts:
        damage_reduction_match = re.search(r"DR\s+(.+)", part, re.IGNORECASE)
        if damage_reduction_match:
            fsm_obj.creature.damage_reduction = damage_reduction_match.group(1).strip()

        spell_reduction_match = re.search(r"SR\s+(.+)", part, re.IGNORECASE)
        if spell_reduction_match:
            fsm_obj.creature.spell_resistence = spell_reduction_match.group(1).strip()

        defence_ability_match = re.search(r"Defensive Abilities\s+(.+)", part, re.IGNORECASE)
        if defence_ability_match:
            abilities = _normalize_mixed_case(defence_ability_match.group(1)).split(",")
            for ability in abilities:
                creature_defense_ability = CreatureDefenseAbilities()
                creature_defense_ability.ability = ability.strip()
                fsm_obj.creature.defensive_abilities.append(creature_defense_ability)

        immunity_match = re.search(r"Immune\s+(.+)", part, re.IGNORECASE)
        if immunity_match:
            immunities = _normalize_mixed_case(immunity_match.group(1)).split(",")
            for immunity in immunities:
                creature_immunity = CreatureImmuneModifiers()
                creature_immunity.immune_to = immunity.strip()
                fsm_obj.creature.immune_modifiers.append(creature_immunity)

        resist_match = re.search(r"Resist\s+(.+)", part, re.IGNORECASE)
        if resist_match:
            resists = _normalize_mixed_case(resist_match.group(1)).split(",")
            for resist in resists:
                resistance_match = re.search(r"(.+)\s(\d+)", resist)
                if resistance_match:
                    creature_resists = CreatureSpellResistenceModifiers()
                    creature_resists.resists = resistance_match.group(1).strip()
                    creature_resists.resist_amount = resistance_match.group(2).strip()
                    fsm_obj.creature.sr_modifiers.append(creature_resists)

def transition_parse_speed(fsm_obj):
    speed_match = re.search(R_SPEED, fsm_obj.current_line, re.IGNORECASE)
    if speed_match:
        speeds = re.split(R_SPLIT_COMMA_OUTSIDE_PARENS, speed_match.group(1))
        base_speed = speeds[0]
        fsm_obj.creature.speed = base_speed.strip()
        for speed in speeds:
            if speed != base_speed:
                creature_speed_modifier = CreatureSpeedModifiers()
                creature_speed_modifier.speed_modifier = speed.strip()
                fsm_obj.creature.speed_modifiers.append(creature_speed_modifier)

def transition_parse_melee(fsm_obj):
    melee_match = re.search(R_MELEE, fsm_obj.current_line, re.IGNORECASE)
    if melee_match:
        if " or " in melee_match.group(1):
            melee_attacks = melee_match.group(1).split(" or ")
        else:
            melee_attacks = re.split(R_SPLIT_COMMA_OUTSIDE_PARENS, melee_match.group(1))
        for melee_attack in melee_attacks:
            creature_melee = CreatureMeleeAttacks()
            creature_melee.attack = melee_attack.strip()
            fsm_obj.creature.melee_attacks.append(creature_melee)

def transition_parse_ranged(fsm_obj):
    ranged_match = re.search(R_RANGED, fsm_obj.current_line, re.IGNORECASE)
    if ranged_match:
        if " or " in ranged_match.group(1):
            ranged_attacks = ranged_match.group(1).split(" or ")
        else:
            ranged_attacks = re.split(R_SPLIT_COMMA_OUTSIDE_PARENS, ranged_match.group(1))
        for ranged_attack in ranged_attacks:
            creature_ranged = CreatureRangedAttacks()
            creature_ranged.attack = ranged_attack.strip()
            fsm_obj.creature.ranged_attacks.append(creature_ranged)

def transition_parse_space(fsm_obj):
    space_match = re.search(R_SPACE, fsm_obj.current_line, re.IGNORECASE)
    if space_match:
        parts = space_match.group(1).split("; ")
        for part in parts:
            reach_match = re.search(R_REACH, part, re.IGNORECASE)
            if reach_match:
                fsm_obj.creature.reach = reach_match.group(1).strip()
            else:
                fsm_obj.creature.space = part.strip()

def transition_parse_special_attacks(fsm_obj):
    special_attack_match = re.search(r"Special Attacks\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if special_attack_match:
        for special_attack in re.split(R_SPLIT_COMMA_OUTSIDE_PARENS, special_attack_match.group(1)):
            creature_special_attack = CreatureSpecialAttacks()
            creature_special_attack.attack = special_attack.strip()
            fsm_obj.creature.special_attacks.append(creature_special_attack)


def transition_parse_spell_like_abilities(fsm_obj):
    spell_like_match = re.search(r"(.*)Spell-Like Abilities\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if spell_like_match:
        fsm_obj.creature.spell_like_type = spell_like_match.group(1).strip()
        fsm_obj.creature.spell_like_caster_level = spell_like_match.group(2).strip()

def transition_parse_sla_spells(fsm_obj):
    spell_like_match = re.search(r"(.+)—(.+)", fsm_obj.current_line, re.IGNORECASE)
    if spell_like_match:
        spell_rate = spell_like_match.group(1).strip()

        for spell_like in re.split(R_SPLIT_COMMA_OUTSIDE_PARENS, spell_like_match.group(2)):
            spells_match = re.search(r"(.+)\((.+)\)", spell_like)
            if spells_match:
                name = spells_match.group(1).strip()
                modifiers = spells_match.group(2).strip()
            else:
                name = spell_like.strip()
                modifiers = ""
            creature_spell_like_ability = CreatureSpellLikeAbilities()
            creature_spell_like_ability.rate = spell_rate
            creature_spell_like_ability.name = name
            creature_spell_like_ability.modifiers = modifiers
            fsm_obj.creature.spell_like_abilities.append(creature_spell_like_ability)

def transition_parse_spells_known(fsm_obj):
    spell_known_match = re.search(r"(.*)Spells Known\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if spell_known_match:
        fsm_obj.creature.spell_known_type = spell_known_match.group(1).strip()
        fsm_obj.creature.spell_known_caster_level = spell_known_match.group(2).strip()

def transition_parse_sk_spells(fsm_obj):
    spell_known_match = re.search(r"(.+) (\(.+\))?—(.+)", fsm_obj.current_line, re.IGNORECASE)
    if spell_known_match:
        spell_level = spell_known_match.group(1).strip()
        spell_rate = spell_known_match.group(2).strip()

        for spells in re.split(R_SPLIT_COMMA_OUTSIDE_PARENS, spell_known_match.group(3)):
            spells_match = re.search(r"(.+)\((.+)\)", spells)
            if spells_match:
                name = spells_match.group(1).strip().lower()
                modifiers = spells_match.group(2).strip()
            else:
                name = spells.strip().lower()
                modifiers = ""
            creature_known_spell = CreatureKnownSpells()
            creature_known_spell.spell_level = spell_level
            creature_known_spell.rate = spell_rate
            creature_known_spell.name = name
            creature_known_spell.modifiers = modifiers
            fsm_obj.creature.known_spells.append(creature_known_spell)

def transition_parse_spells_prepared(fsm_obj):
    spell_prepared_match = re.search(r"(.*)Spells Prepared\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if spell_prepared_match:
        fsm_obj.creature.spell_prepared_type = spell_prepared_match.group(1).strip()
        fsm_obj.creature.spell_prepared_caster_level = spell_prepared_match.group(2).strip()

def transition_parse_sp_spells(fsm_obj):
    spell_prepared_match = re.search(r"(.+)—(.+)", fsm_obj.current_line, re.IGNORECASE)
    if spell_prepared_match:
        spell_level = spell_prepared_match.group(1).strip()

        for spells in re.split(R_SPLIT_COMMA_OUTSIDE_PARENS, spell_prepared_match.group(2)):
            spells_match = re.search(r"(.+)\((.+)\)", spells)
            if spells_match:
                name = spells_match.group(1).strip().lower()
                modifiers = spells_match.group(2).strip()
            else:
                name = spells.strip().lower()
                modifiers = ""
            creature_prepared_spell = CreaturePreparedSpells()
            creature_prepared_spell.spell_level = spell_level
            creature_prepared_spell.name = name
            creature_prepared_spell.modifiers = modifiers
            fsm_obj.creature.prepared_spells.append(creature_prepared_spell)

def transition_parse_tactics(fsm_obj):
    tactics = fsm_obj.creature.tactics
    if tactics:
        tactics += fsm_obj.current_line + "\n"
    else:
        tactics = fsm_obj.current_line + "\n"
    fsm_obj.creature.tactics = tactics

def transition_parse_strength(fsm_obj):
    match_strength = re.findall(r"(Str|Dex|Con|Int|Wis|Cha)\s*([+\-]?\d+)", fsm_obj.current_line, re.IGNORECASE)
    for stat, val in match_strength:
        stat_name = stat.capitalize()
        if stat_name == "Str":
            fsm_obj.creature.strength = val
        elif stat_name == "Dex":
            fsm_obj.creature.dexterity = val
        elif stat_name == "Con":
            fsm_obj.creature.constitution = val
        elif stat_name == "Int":
            fsm_obj.creature.intelligence = val
        elif stat_name == "Wis":
            fsm_obj.creature.wisdom = val
        elif stat_name == "Cha":
            fsm_obj.creature.charisma = val

def transition_parse_base_attack(fsm_obj):
    match_attack = re.findall(r"(Base Atk|CMB|CMD)\s*([+\-]?\d+)", fsm_obj.current_line, re.IGNORECASE)
    for stat, val in match_attack:
        stat_name = stat.capitalize()
        if stat_name == "Base atk":
            fsm_obj.creature.base_attack = val
        elif stat_name == "Cmb":
            fsm_obj.creature.combat_maneuver_bonus = val
        elif stat_name == "Cmd":
            fsm_obj.creature.combat_maneuver_defense = val

def transition_parse_feats(fsm_obj):
    feat_match = re.search(r"Feats\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if feat_match:
        for feat in _normalize_mixed_case(feat_match.group(1)).split(","):
            creature_feat = CreatureFeats()
            creature_feat.feat = feat.strip()
            fsm_obj.creature.feats.append(creature_feat)

def transition_parse_skills(fsm_obj):
    skills_match = re.search(r"Skills\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if skills_match:
        parts = skills_match.group(1).split(";")
        for part in parts:
            racial_match = re.search(r"Racial Modifiers\s(.+)", part, re.IGNORECASE)
            if racial_match:
                fsm_obj.creature.racial_modifiers = racial_match.group(1).strip()
            else:
                skills = _normalize_mixed_case(part).split(",")
                for skill in skills:
                    skill_match = re.search(r"(.+)\s([+\-]?\d+)", skill, re.IGNORECASE)
                    if skill_match:
                        creature_skill = CreatureSkills()
                        creature_skill.skill = skill_match.group(1).strip()
                        creature_skill.modifier = skill_match.group(2).strip()
                        fsm_obj.creature.skills.append(creature_skill)

def transition_parse_languages(fsm_obj):
    language_match = re.search(r"Languages\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if language_match:
        for language in _normalize_mixed_case(language_match.group(1)).split(","):
            creature_language = CreatureLanguages()
            creature_language.language = language.strip()
            fsm_obj.creature.languages.append(creature_language)

def transition_parse_special_qualities(fsm_obj):
    special_qualities_match = re.search(r"SQ\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if special_qualities_match:
        for special_quality in _normalize_mixed_case(special_qualities_match.group(1)).split(","):
            creature_special_quality = CreatureSpecialQualities()
            creature_special_quality.special_quality = special_quality.strip()
            fsm_obj.creature.special_qualities.append(creature_special_quality)



def transition_parse_gear_list(fsm_obj):
    gear = fsm_obj.creature.gear
    if gear:
        gear += "; " + fsm_obj.current_line
    else:
        gear = fsm_obj.current_line
    fsm_obj.creature.gear = gear


def transition_parse_gear_item(fsm_obj):
    gear_item_match = re.search(r"Unique Item: (.+)", fsm_obj.current_line, re.IGNORECASE)
    if gear_item_match:
        if fsm_obj.gear_item:
            fsm_obj.creature.gear_items.append(fsm_obj.gear_item)
        fsm_obj.gear_item = CreatureGearItems()
        fsm_obj.gear_item.name = gear_item_match.group(1).strip()

def transition_parse_gear_description(fsm_obj):
    gear_item_match = re.search(R_ANYTHING, fsm_obj.current_line, re.IGNORECASE)
    if gear_item_match:
        description = fsm_obj.gear_item.description
        if description:
            description += gear_item_match.group(1).strip() + "\n"
        else:
            description = gear_item_match.group(1).strip() + "\n"
        fsm_obj.gear_item.description = description


def transition_parse_save_gear_item(fsm_obj):
    if fsm_obj.gear_item:
        fsm_obj.creature.gear_items.append(fsm_obj.gear_item)
        fsm_obj.gear_item = None

def transition_parse_special_ability_name(fsm_obj):
    special_ability_match = re.search(r"(.+) (\(.+\))", fsm_obj.current_line, re.IGNORECASE)
    if special_ability_match:
        if fsm_obj.special_ability:
            fsm_obj.creature.special_abilities.append(fsm_obj.special_ability)
        fsm_obj.special_ability = CreatureSpecialAbilities()
        fsm_obj.special_ability.ability = special_ability_match.group(1).strip()
        fsm_obj.special_ability.type = special_ability_match.group(2).strip()

def transition_parse_special_ability_description(fsm_obj):
    special_ability_match = re.search(R_ANYTHING,fsm_obj.current_line, re.IGNORECASE)
    if special_ability_match:
        fsm_obj.special_ability.description = special_ability_match.group(1).strip()

def transition_parse_save_special_ability(fsm_obj):
    if fsm_obj.special_ability:
        fsm_obj.creature.special_abilities.append(fsm_obj.special_ability)
        fsm_obj.special_ability = None

def transition_parse_environment(fsm_obj):
    environment_match = re.search(r"Environment\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if environment_match:
        fsm_obj.creature.environment = _normalize_mixed_case(environment_match.group(1)).strip()

def transition_parse_organization(fsm_obj):
    organization_match = re.search(r"Organization\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if organization_match:
        fsm_obj.creature.organization = _normalize_mixed_case(organization_match.group(1)).strip()

def transition_parse_treasure(fsm_obj):
    treasure_match = re.search(r"Treasure\s+(.+)", fsm_obj.current_line, re.IGNORECASE)
    if treasure_match:
        fsm_obj.creature.treasure = _normalize_mixed_case(treasure_match.group(1)).strip()


T_SKIP = transition_skip
T_PARSE_FORMAL_NAME = transition_parse_formal_name
T_PARSE_COMMON_NAME = transition_parse_common_name
T_PARSE_DESCRIPTION = transition_parse_description
T_PARSE_EXPERIENCE_POINTS = transition_parse_experience_points
T_PARSE_ALIGNMENT = transition_parse_alignment
T_PARSE_RACE = transition_parse_race
T_PARSE_INITIATIVE = transition_parse_initiative
T_PARSE_AURAS = transition_parse_auras
T_PARSE_AC = transition_parse_armor_class
T_PARSE_HP= transition_parse_hit_points
T_PARSE_FORTITUDE = transition_parse_fortitude
T_PARSE_WEAKNESS = transition_parse_weakness
T_PARSE_DAMAGE_RESISTANCE = transition_parse_damage_resistance
T_PARSE_SPEED = transition_parse_speed
T_PARSE_MELEE = transition_parse_melee
T_PARSE_SPACE = transition_parse_space
T_PARSE_RANGED = transition_parse_ranged
T_PARSE_SPECIAL_ATTACKS = transition_parse_special_attacks
T_PARSE_SPELL_LIKE_ABILITIES = transition_parse_spell_like_abilities
T_PARSE_SPELLS_KNOWN = transition_parse_spells_known
T_PARSE_SPELLS_PREPARED = transition_parse_spells_prepared
T_PARSE_SLA_SPELLS = transition_parse_sla_spells
T_PARSE_SK_SPELLS = transition_parse_sk_spells
T_PARSE_SP_SPELLS = transition_parse_sp_spells
T_PARSE_TACTICS = transition_parse_tactics
T_PARSE_STRENGTH = transition_parse_strength
T_PARSE_BASE_ATTACK = transition_parse_base_attack
T_PARSE_FEATS = transition_parse_feats
T_PARSE_SKILLS = transition_parse_skills
T_PARSE_LANGUAGES = transition_parse_languages
T_PARSE_SPECIAL_QUALITIES = transition_parse_special_qualities
T_PARSE_GEAR_LIST = transition_parse_gear_list
T_PARSE_GEAR_ITEM = transition_parse_gear_item
T_PARSE_GEAR_DESCRIPTION = transition_parse_gear_description
T_PARSE_SAVE_GEAR_ITEM = transition_parse_save_gear_item
T_PARSE_SPECIAL_ABILITY_NAME = transition_parse_special_ability_name
T_PARSE_SPECIAL_ABILITY_DESCRIPTION = transition_parse_special_ability_description
T_PARSE_SAVE_SPECIAL_ABILITY = transition_parse_save_special_ability
T_PARSE_ENVIRONMENT = transition_parse_environment
T_PARSE_ORGANIZATION = transition_parse_organization
T_PARSE_TREASURE = transition_parse_treasure

S_INITIAL_LOAD = "STATE: INITIAL FILE"
S_FOUND_FORMAL_NAME = "STATE: FOUND FORMAL NAME"
S_FOUND_COMMON_NAME = "STATE: FOUND COMMON NAME"
S_FOUND_DESCRIPTION = "STATE: FOUND DESCRIPTION"
S_FOUND_XP = "STATE: FOUND XP"
S_FOUND_RACE = "STATE: FOUND RACE"
S_FOUND_ALIGNMENT = "STATE: FOUND ALIGNMENT"
S_FOUND_INITIATIVE = "STATE: FOUND INITIATIVE"
S_FOUND_AURAS = "STATE: FOUND AURAS"
S_FOUND_DEFENSE_HEADER = "STATE: FOUND DEFENSE HEADER"
S_FOUND_AC = "STATE: FOUND AC"
S_FOUND_HP = "STATE: FOUND HP"
S_FOUND_FORTITUDE = "STATE: FOUND FORTITUDE"
S_FOUND_DR = "STATE: FOUND DR"
S_FOUND_WEAKNESS = "STATE: FOUND WEAKNESS"
S_FOUND_OFFENSE_HEADER = "STATE: FOUND OFFENSE HEADER"
S_FOUND_SPEED = "STATE: FOUND SPEED"
S_FOUND_MELEE = "STATE: FOUND MELEE"
S_FOUND_RANGED = "STATE: FOUND RANGED"
S_FOUND_SPACE = "STATE: FOUND SPACE"
S_FOUND_SPECIAL_ATTACKS = "STATE: FOUND SPECIAL ATTACKS"
S_FOUND_SPELL_LIKE_ABILITIES = "STATE: FOUND SPELL LIKE ABILITIES"
S_FOUND_SLA_SPELLS = "STATE: FOUND SPELL LIKE ABILITIES SPELLS"
S_FOUND_SPELLS_KNOWN = "STATE: FOUND SPELLS KNOWN"
S_FOUND_SK_SPELLS = "STATE: FOUND SPELLS KNOWN SPELLS"
S_FOUND_SPELLS_PREPARED = "STATE: FOUND SPELLS PREPARED"
S_FOUND_SP_SPELLS = "STATE: FOUND SPELLS PREPARED SPELLS"
S_FOUND_TACTICS_HEADER = "STATE: FOUND TACTICS HEADER"
S_FOUND_TACTICS_DETAIL = "STATE: FOUND TACTICS DETAIL"
S_FOUND_STATISTICS_HEADER = "STATE: FOUND STATISTICS HEADER"
S_FOUND_STRENGTH = "STATE: FOUND STRENGTH"
S_FOUND_BASE_ATTACK = "STATE: FOUND BASE ATTACK"
S_FOUND_FEATS = "STATE: FOUND FEATS"
S_FOUND_SKILLS = "STATE: FOUND SKILLS"
S_FOUND_LANGUAGES = "STATE: FOUND LANGUAGES"
S_FOUND_SPECIAL_QUALITIES = "STATE: FOUND SPECIAL QUALITIES"
S_FOUND_GEAR_LINE = "STATE: FOUND GEAR LINE"
S_FOUND_SPECIAL_ABILITIES_HEADER = "STATE: FOUND SPECIAL ABILITIES HEADER"
S_FOUND_SPECIAL_ABILITY_NAME = "STATE: FOUND SPECIAL ABILITY NAME"
S_FOUND_SPECIAL_ABILITY_DESCRIPTION = "STATE: FOUND SPECIAL ABILITY DESCRIPTION"
S_FOUND_GEAR_HEADER = "STATE: FOUND GEAR HEADER"
S_FOUND_GEAR_ITEM = "STATE: FOUND GEAR ITEM"
S_FOUND_GEAR_DESCRIPTION = "STATE: FOUND GEAR DESCRIPTION"
S_FOUND_ECOLOGY_HEADER = "STATE: FOUND ECOLOGY HEADER"
S_FOUND_ENVIRONMENT = "STATE: FOUND ENVIRONMENT"
S_FOUND_ORGANIZATION = "STATE: FOUND ORGANIZATION"
S_FOUND_TREASURE = "STATE: FOUND TREASURE"
S_FOUND_ABOUT_HEADER = "STATE: FOUND ABOUT HEADER"
S_FOUND_ABOUT_DETAILS = "STATE: FOUND ABOUT DETAILS"
S_FOUND_COPYRIGHT = "STATE: FOUND COPYRIGHT"

R_ANYTHING = r"^(.+)"
R_COMMON_NAME = r"^(.+)CR\s+([\d/]+)"
R_ALIGNMENT = r"^([LNCEG]{1,2})\s"
R_EXPERIENCE = r"XP\s+([\d,]+)"
R_INITIATIVE = r"^Init\s+([^\n;]+)"
R_AURA = r"^Aura\s+([^\n;]+)"
R_DEFENCE_HEADER = r"^DEFENSE"
R_KNOWN_SPELLS = r".*Spells\sKnown\s"
R_SPEED = r"^Speed\s+(.+)"
R_MELEE = r"^Melee\s+(.+)"
R_RANGED = r"^Ranged\s+(.+)"
R_SPACE = r"^Space\s+(.+)"
R_REACH = r"Reach\s+(.+)"
R_GEAR_LIST =  r"(.* )*Gear (.+)"
R_SPLIT_COMMA_OUTSIDE_PARENS = r',\s*(?![^()]*\))'

FSM_MAP = [
    #  {'src':, 'dst':, 'condition':, 'callback': },
    {'src': S_INITIAL_LOAD, 'dst': S_FOUND_FORMAL_NAME, 'cond': R_ANYTHING, 'callback': T_PARSE_FORMAL_NAME},  # 1
    {'src': S_INITIAL_LOAD, 'dst': S_FOUND_COMMON_NAME, 'cond': R_COMMON_NAME, 'callback': T_PARSE_COMMON_NAME},  # 2
    {'src': S_FOUND_FORMAL_NAME, 'dst': S_FOUND_COMMON_NAME, 'cond': R_COMMON_NAME, 'callback': T_PARSE_COMMON_NAME},  # 3
    {'src': S_FOUND_FORMAL_NAME, 'dst': S_FOUND_DESCRIPTION, 'cond': R_ANYTHING, 'callback': T_PARSE_DESCRIPTION},  # 4
    {'src': S_FOUND_DESCRIPTION, 'dst': S_FOUND_COMMON_NAME, 'cond': R_COMMON_NAME, 'callback': T_PARSE_COMMON_NAME},  # 5
    {'src': S_FOUND_DESCRIPTION, 'dst': S_FOUND_XP, 'cond': R_EXPERIENCE, 'callback': T_PARSE_EXPERIENCE_POINTS}, #6
    {'src': S_FOUND_DESCRIPTION, 'dst': S_FOUND_DESCRIPTION, 'cond': R_ANYTHING, 'callback': T_PARSE_DESCRIPTION},  #7
    {'src': S_FOUND_COMMON_NAME, 'dst': S_FOUND_XP, 'cond': R_EXPERIENCE, 'callback': T_PARSE_EXPERIENCE_POINTS}, #8
    {'src': S_FOUND_COMMON_NAME, 'dst': S_FOUND_DESCRIPTION, 'cond': R_ANYTHING, 'callback': T_PARSE_DESCRIPTION}, #9
    {'src': S_FOUND_XP, 'dst': S_FOUND_ALIGNMENT, 'cond': R_ALIGNMENT, 'callback': T_PARSE_ALIGNMENT}, #10
    {'src': S_FOUND_XP, 'dst': S_FOUND_RACE, 'cond': R_ANYTHING, 'callback': T_PARSE_RACE}, #11
    {'src': S_FOUND_RACE, 'dst': S_FOUND_ALIGNMENT, 'cond': R_ALIGNMENT, 'callback': T_PARSE_ALIGNMENT},  # 12
    {'src': S_FOUND_ALIGNMENT, 'dst': S_FOUND_INITIATIVE, 'cond': R_INITIATIVE, 'callback': T_PARSE_INITIATIVE},  # 13
    {'src': S_FOUND_INITIATIVE, 'dst': S_FOUND_AURAS, 'cond': R_AURA, 'callback': T_PARSE_AURAS}, # 14
    {'src': S_FOUND_INITIATIVE, 'dst': S_FOUND_DEFENSE_HEADER, 'cond':R_DEFENCE_HEADER, 'callback': T_SKIP}, # 15
    {'src': S_FOUND_AURAS, 'dst': S_FOUND_DEFENSE_HEADER, 'cond':R_DEFENCE_HEADER, 'callback': T_SKIP},  # 16
    {'src': S_FOUND_DEFENSE_HEADER, 'dst': S_FOUND_AC, 'cond': r"^AC\s(\d+)", 'callback': T_PARSE_AC},  # 17
    {'src': S_FOUND_AC, 'dst': S_FOUND_HP, 'cond': r"^[HPhp]{2}\s(\d+)", 'callback': T_PARSE_HP},  # 18
    {'src': S_FOUND_HP, 'dst': S_FOUND_FORTITUDE, 'cond': r"^Fort\s", 'callback': T_PARSE_FORTITUDE},  # 19
    {'src': S_FOUND_FORTITUDE, 'dst': S_FOUND_DR, 'cond': r"^DR\s(\d+)", 'callback': T_PARSE_DAMAGE_RESISTANCE},  # 20
    {'src': S_FOUND_FORTITUDE, 'dst': S_FOUND_OFFENSE_HEADER, 'cond': r"^OFFENSE", 'callback': T_PARSE_DAMAGE_RESISTANCE},  # 20
    {'src': S_FOUND_DR, 'dst': S_FOUND_WEAKNESS, 'cond': r"^Weaknesses\s", 'callback': T_PARSE_WEAKNESS},  # 21
    {'src': S_FOUND_DR, 'dst': S_FOUND_OFFENSE_HEADER, 'cond': r"^OFFENSE", 'callback': T_SKIP},  # 22
    {'src': S_FOUND_WEAKNESS, 'dst': S_FOUND_OFFENSE_HEADER, 'cond': r"^OFFENSE", 'callback': T_SKIP},  # 23
    {'src': S_FOUND_OFFENSE_HEADER, 'dst': S_FOUND_SPEED, 'cond': R_SPEED, 'callback': T_PARSE_SPEED},  # 24
    {'src': S_FOUND_SPEED, 'dst': S_FOUND_MELEE, 'cond': R_MELEE, 'callback': T_PARSE_MELEE},  # 25
    {'src': S_FOUND_MELEE, 'dst': S_FOUND_RANGED, 'cond': R_RANGED, 'callback': T_PARSE_RANGED},  # 26
    {'src': S_FOUND_MELEE, 'dst': S_FOUND_SPACE, 'cond': R_SPACE, 'callback': T_PARSE_SPACE},  # 26
    {'src': S_FOUND_MELEE, 'dst': S_FOUND_SPECIAL_ATTACKS, 'cond': r"^Special Attacks\s", 'callback': T_PARSE_SPECIAL_ATTACKS},  # 27
    {'src': S_FOUND_MELEE, 'dst': S_FOUND_SPELLS_KNOWN, 'cond': R_KNOWN_SPELLS, 'callback': T_PARSE_SPELLS_KNOWN},  # 29
    {'src': S_FOUND_MELEE, 'dst': S_FOUND_SPELLS_PREPARED, 'cond': r".*Spells\sPrepared\s", 'callback': T_PARSE_SPELLS_PREPARED},  # 29
    {'src': S_FOUND_MELEE, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},  # 28
    {'src': S_FOUND_MELEE, 'dst': S_FOUND_TACTICS_HEADER, 'cond': r"^TACTICS", 'callback': T_SKIP},  # 28
    {'src': S_FOUND_RANGED, 'dst': S_FOUND_SPECIAL_ATTACKS, 'cond': r"^Special Attacks\s", 'callback': T_PARSE_SPECIAL_ATTACKS},  # 27
    {'src': S_FOUND_RANGED, 'dst': S_FOUND_SPACE, 'cond': R_SPACE, 'callback': T_PARSE_SPACE},  # 26
    {'src': S_FOUND_RANGED, 'dst': S_FOUND_SPELLS_KNOWN, 'cond': R_KNOWN_SPELLS, 'callback': T_PARSE_SPELLS_KNOWN},  # 29
    {'src': S_FOUND_RANGED, 'dst': S_FOUND_SPELLS_PREPARED, 'cond': r".*Spells\sPrepared\s", 'callback': T_PARSE_SPELLS_PREPARED},  # 29
    {'src': S_FOUND_RANGED, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},  # 28
    {'src': S_FOUND_RANGED, 'dst': S_FOUND_TACTICS_HEADER, 'cond': r"^TACTICS", 'callback': T_SKIP},  # 28
    {'src': S_FOUND_SPACE, 'dst': S_FOUND_SPECIAL_ATTACKS, 'cond': r"^Special Attacks\s", 'callback': T_PARSE_SPECIAL_ATTACKS},  # 27
    {'src': S_FOUND_SPACE, 'dst': S_FOUND_SPELLS_KNOWN, 'cond': R_KNOWN_SPELLS, 'callback': T_PARSE_SPELLS_KNOWN},  # 29
    {'src': S_FOUND_SPACE, 'dst': S_FOUND_SPELLS_PREPARED, 'cond': r".*Spells\sPrepared\s", 'callback': T_PARSE_SPELLS_PREPARED},  # 29
    {'src': S_FOUND_SPACE, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},  # 28
    {'src': S_FOUND_SPACE, 'dst': S_FOUND_TACTICS_HEADER, 'cond': r"^TACTICS", 'callback': T_SKIP},  # 28
    {'src': S_FOUND_SPECIAL_ATTACKS, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},  # 29
    {'src': S_FOUND_SPECIAL_ATTACKS, 'dst': S_FOUND_TACTICS_HEADER, 'cond': r"^TACTICS", 'callback': T_SKIP},  # 29
    {'src': S_FOUND_SPECIAL_ATTACKS, 'dst': S_FOUND_SPELL_LIKE_ABILITIES, 'cond': r".*Spell\-Like\sAbilities\s", 'callback': T_PARSE_SPELL_LIKE_ABILITIES},  # 29
    {'src': S_FOUND_SPECIAL_ATTACKS, 'dst': S_FOUND_SPELLS_KNOWN, 'cond': R_KNOWN_SPELLS, 'callback': T_PARSE_SPELLS_KNOWN},  # 29
    {'src': S_FOUND_SPECIAL_ATTACKS, 'dst': S_FOUND_SPELLS_PREPARED, 'cond': r".*Spells\sPrepared\s", 'callback': T_PARSE_SPELLS_PREPARED},  # 29
    {'src': S_FOUND_SPELL_LIKE_ABILITIES, 'dst': S_FOUND_SLA_SPELLS, 'cond': r"(.+)—(.+)", 'callback': T_PARSE_SLA_SPELLS},
    {'src': S_FOUND_SLA_SPELLS, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},
    {'src': S_FOUND_SLA_SPELLS, 'dst': S_FOUND_TACTICS_HEADER, 'cond': r"^TACTICS", 'callback': T_SKIP},  # 29
    {'src': S_FOUND_SLA_SPELLS, 'dst': S_FOUND_SPELLS_KNOWN, 'cond': R_KNOWN_SPELLS, 'callback': T_PARSE_SPELLS_KNOWN},  # 29
    {'src': S_FOUND_SLA_SPELLS, 'dst': S_FOUND_SPELLS_PREPARED, 'cond': r".*Spells\sPrepared\s", 'callback': T_PARSE_SPELLS_PREPARED},  # 29
    {'src': S_FOUND_SLA_SPELLS, 'dst': S_FOUND_SLA_SPELLS, 'cond': r"(.+)—(.+)", 'callback': T_PARSE_SLA_SPELLS},
    {'src': S_FOUND_SPELLS_KNOWN, 'dst': S_FOUND_SK_SPELLS, 'cond': r"(.+) (\(.+\))?—(.+)", 'callback': T_PARSE_SK_SPELLS},
    {'src': S_FOUND_SK_SPELLS, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},
    {'src': S_FOUND_SK_SPELLS, 'dst': S_FOUND_TACTICS_HEADER, 'cond': r"^TACTICS", 'callback': T_SKIP},  # 29
    {'src': S_FOUND_SK_SPELLS, 'dst': S_FOUND_SPELLS_PREPARED, 'cond': r".*Spells\sPrepared\s", 'callback': T_PARSE_SPELLS_PREPARED},  # 29
    {'src': S_FOUND_SK_SPELLS, 'dst': S_FOUND_SK_SPELLS, 'cond': r"(.+) (\(.+\))?—(.+)", 'callback': T_PARSE_SK_SPELLS},
    {'src': S_FOUND_SPELLS_PREPARED, 'dst': S_FOUND_SP_SPELLS, 'cond': r"(.+)—(.+)", 'callback': T_PARSE_SP_SPELLS},
    {'src': S_FOUND_SP_SPELLS, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},
    {'src': S_FOUND_SP_SPELLS, 'dst': S_FOUND_TACTICS_HEADER, 'cond': r"^TACTICS", 'callback': T_SKIP},
    {'src': S_FOUND_SP_SPELLS, 'dst': S_FOUND_SP_SPELLS, 'cond': r"(.+)—(.+)", 'callback': T_PARSE_SP_SPELLS},
    {'src': S_FOUND_TACTICS_HEADER, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},
    {'src': S_FOUND_TACTICS_HEADER, 'dst': S_FOUND_TACTICS_DETAIL, 'cond': R_ANYTHING, 'callback': T_PARSE_TACTICS},
    {'src': S_FOUND_TACTICS_DETAIL, 'dst': S_FOUND_STATISTICS_HEADER, 'cond': r"^STATISTICS", 'callback': T_SKIP},
    {'src': S_FOUND_TACTICS_DETAIL, 'dst': S_FOUND_TACTICS_DETAIL, 'cond': R_ANYTHING, 'callback': T_PARSE_TACTICS},
    {'src': S_FOUND_STATISTICS_HEADER, 'dst': S_FOUND_STRENGTH, 'cond': r"^Str\s(\d+)", 'callback': T_PARSE_STRENGTH},
    {'src': S_FOUND_STRENGTH, 'dst': S_FOUND_BASE_ATTACK, 'cond': r"^Base Atk\s", 'callback': T_PARSE_BASE_ATTACK},
    {'src': S_FOUND_BASE_ATTACK, 'dst': S_FOUND_FEATS, 'cond': r"^Feats\s", 'callback': T_PARSE_FEATS},
    {'src': S_FOUND_BASE_ATTACK, 'dst': S_FOUND_SKILLS, 'cond': r"^Skills\s", 'callback': T_PARSE_SKILLS},
    {'src': S_FOUND_BASE_ATTACK, 'dst': S_FOUND_LANGUAGES, 'cond': r"^Languages\s", 'callback': T_PARSE_LANGUAGES},
    {'src': S_FOUND_BASE_ATTACK, 'dst': S_FOUND_SPECIAL_QUALITIES, 'cond': r"^SQ\s", 'callback': T_PARSE_SPECIAL_QUALITIES},
    {'src': S_FOUND_BASE_ATTACK, 'dst': S_FOUND_GEAR_LINE, 'cond': R_GEAR_LIST, 'callback': T_PARSE_GEAR_LIST},
    {'src': S_FOUND_BASE_ATTACK, 'dst': S_FOUND_SPECIAL_ABILITIES_HEADER, 'cond': r"^SPECIAL ABILITIES",  'callback': T_SKIP},
    {'src': S_FOUND_FEATS, 'dst': S_FOUND_SKILLS, 'cond': r"^Skills\s", 'callback': T_PARSE_SKILLS},
    {'src': S_FOUND_FEATS, 'dst': S_FOUND_LANGUAGES, 'cond': r"^Languages\s", 'callback': T_PARSE_LANGUAGES},
    {'src': S_FOUND_FEATS, 'dst': S_FOUND_SPECIAL_QUALITIES, 'cond': r"^SQ\s", 'callback': T_PARSE_SPECIAL_QUALITIES},
    {'src': S_FOUND_FEATS, 'dst': S_FOUND_GEAR_LINE, 'cond': R_GEAR_LIST, 'callback': T_PARSE_GEAR_LIST},
    {'src': S_FOUND_FEATS, 'dst': S_FOUND_SPECIAL_ABILITIES_HEADER, 'cond': r"^SPECIAL ABILITIES",  'callback': T_SKIP},
    {'src': S_FOUND_SKILLS, 'dst': S_FOUND_LANGUAGES, 'cond': r"^Languages\s", 'callback': T_PARSE_LANGUAGES},
    {'src': S_FOUND_SKILLS, 'dst': S_FOUND_SPECIAL_QUALITIES, 'cond': r"^SQ\s", 'callback': T_PARSE_SPECIAL_QUALITIES},
    {'src': S_FOUND_SKILLS, 'dst': S_FOUND_GEAR_LINE, 'cond': R_GEAR_LIST, 'callback': T_PARSE_GEAR_LIST},
    {'src': S_FOUND_SKILLS, 'dst': S_FOUND_SPECIAL_ABILITIES_HEADER, 'cond': r"^SPECIAL ABILITIES",  'callback': T_SKIP},
    {'src': S_FOUND_LANGUAGES, 'dst': S_FOUND_SPECIAL_QUALITIES, 'cond': r"^SQ\s", 'callback': T_PARSE_SPECIAL_QUALITIES},
    {'src': S_FOUND_LANGUAGES, 'dst': S_FOUND_GEAR_LINE, 'cond': R_GEAR_LIST, 'callback': T_PARSE_GEAR_LIST},
    {'src': S_FOUND_LANGUAGES, 'dst': S_FOUND_SPECIAL_ABILITIES_HEADER, 'cond': r"^SPECIAL ABILITIES",  'callback': T_SKIP},
    {'src': S_FOUND_LANGUAGES, 'dst': S_FOUND_ECOLOGY_HEADER, 'cond': r"^ECOLOGY",  'callback': T_SKIP},
    {'src': S_FOUND_SPECIAL_QUALITIES, 'dst': S_FOUND_GEAR_LINE, 'cond': R_GEAR_LIST, 'callback': T_PARSE_GEAR_LIST},
    {'src': S_FOUND_SPECIAL_QUALITIES, 'dst': S_FOUND_SPECIAL_ABILITIES_HEADER, 'cond': r"^SPECIAL ABILITIES", 'callback': T_SKIP},
    {'src': S_FOUND_GEAR_LINE, 'dst': S_FOUND_SPECIAL_ABILITIES_HEADER, 'cond': r"^SPECIAL ABILITIES",  'callback': T_SKIP},
    {'src': S_FOUND_GEAR_LINE, 'dst': S_FOUND_GEAR_LINE, 'cond': R_GEAR_LIST, 'callback': T_PARSE_GEAR_LIST},
    {'src': S_FOUND_GEAR_LINE, 'dst': S_FOUND_ECOLOGY_HEADER, 'cond': r"^ECOLOGY", 'callback': T_SKIP},
    {'src': S_FOUND_GEAR_LINE, 'dst': S_FOUND_ABOUT_HEADER, 'cond': r"^(ABOUT|DESCRIPTION)", 'callback': T_SKIP},
    {'src': S_FOUND_SPECIAL_ABILITIES_HEADER, 'dst': S_FOUND_SPECIAL_ABILITY_NAME, 'cond': r"^(.+) \((.+)\)", 'callback': T_PARSE_SPECIAL_ABILITY_NAME},
    {'src': S_FOUND_SPECIAL_ABILITY_NAME, 'dst': S_FOUND_SPECIAL_ABILITY_DESCRIPTION, 'cond': R_ANYTHING, 'callback': T_PARSE_SPECIAL_ABILITY_DESCRIPTION},
    {'src': S_FOUND_SPECIAL_ABILITY_DESCRIPTION, 'dst': S_FOUND_ECOLOGY_HEADER, 'cond': r"^ECOLOGY", 'callback': T_PARSE_SAVE_SPECIAL_ABILITY},
    {'src': S_FOUND_SPECIAL_ABILITY_DESCRIPTION, 'dst': S_FOUND_ECOLOGY_HEADER, 'cond': r"^Ecology", 'callback': T_PARSE_SAVE_SPECIAL_ABILITY},
    {'src': S_FOUND_SPECIAL_ABILITY_DESCRIPTION, 'dst': S_FOUND_GEAR_HEADER, 'cond': r"^GEAR", 'callback': T_PARSE_SAVE_SPECIAL_ABILITY},
    {'src': S_FOUND_SPECIAL_ABILITY_DESCRIPTION, 'dst': S_FOUND_ABOUT_HEADER, 'cond': r"^(ABOUT|DESCRIPTION)", 'callback': T_PARSE_SAVE_SPECIAL_ABILITY},
    {'src': S_FOUND_SPECIAL_ABILITY_DESCRIPTION, 'dst': S_FOUND_SPECIAL_ABILITY_NAME, 'cond': r"^(.+) \((.+)\)", 'callback': T_PARSE_SPECIAL_ABILITY_NAME},
    {'src': S_FOUND_SPECIAL_ABILITY_DESCRIPTION, 'dst': S_FOUND_SPECIAL_ABILITY_DESCRIPTION, 'cond': R_ANYTHING, 'callback': T_PARSE_SPECIAL_ABILITY_DESCRIPTION},
    {'src': S_FOUND_GEAR_HEADER, 'dst': S_FOUND_GEAR_ITEM, 'cond': r"^(.* )Item: (.+)", 'callback': T_PARSE_GEAR_ITEM},
    {'src': S_FOUND_GEAR_ITEM, 'dst': S_FOUND_GEAR_DESCRIPTION, 'cond': R_ANYTHING, 'callback': T_PARSE_GEAR_DESCRIPTION},
    {'src': S_FOUND_GEAR_DESCRIPTION, 'dst': S_FOUND_ECOLOGY_HEADER, 'cond': r"^ECOLOGY", 'callback': T_PARSE_SAVE_GEAR_ITEM},
    {'src': S_FOUND_GEAR_DESCRIPTION, 'dst': S_FOUND_ABOUT_HEADER, 'cond': r"^(ABOUT|DESCRIPTION)", 'callback': T_PARSE_SAVE_GEAR_ITEM},
    {'src': S_FOUND_GEAR_DESCRIPTION, 'dst': S_FOUND_GEAR_DESCRIPTION, 'cond': R_ANYTHING, 'callback': T_PARSE_GEAR_DESCRIPTION},
    {'src': S_FOUND_ECOLOGY_HEADER, 'dst': S_FOUND_ENVIRONMENT, 'cond': r"^Environment\s+(.+)", 'callback': T_PARSE_ENVIRONMENT},
    {'src': S_FOUND_ECOLOGY_HEADER, 'dst': S_FOUND_ORGANIZATION, 'cond': r"^Organization\s+(.+)", 'callback': T_PARSE_ORGANIZATION},
    {'src': S_FOUND_ECOLOGY_HEADER, 'dst': S_FOUND_TREASURE, 'cond': r"^Treasure\s+(.+)", 'callback': T_PARSE_TREASURE},
    {'src': S_FOUND_ECOLOGY_HEADER, 'dst': S_FOUND_GEAR_HEADER, 'cond': r"^GEAR", 'callback': T_SKIP},
    {'src': S_FOUND_ENVIRONMENT, 'dst': S_FOUND_ORGANIZATION, 'cond': r"^Organization\s+(.+)", 'callback': T_PARSE_ORGANIZATION},
    {'src': S_FOUND_ENVIRONMENT, 'dst': S_FOUND_TREASURE, 'cond': r"^Treasure\s+(.+)", 'callback': T_PARSE_TREASURE},
    {'src': S_FOUND_ENVIRONMENT, 'dst': S_FOUND_GEAR_HEADER, 'cond': r"^GEAR", 'callback': T_SKIP},
    {'src': S_FOUND_ORGANIZATION, 'dst': S_FOUND_TREASURE, 'cond': r"^Treasure\s+(.+)", 'callback': T_PARSE_TREASURE},
    {'src': S_FOUND_ORGANIZATION, 'dst': S_FOUND_GEAR_HEADER, 'cond': r"^GEAR", 'callback': T_SKIP},
    {'src': S_FOUND_TREASURE, 'dst': S_FOUND_GEAR_HEADER, 'cond': r"^GEAR", 'callback': T_SKIP},
    {'src': S_FOUND_TREASURE, 'dst': S_FOUND_ABOUT_HEADER, 'cond': r"^(ABOUT|DESCRIPTION)", 'callback': T_SKIP},
    {'src': S_FOUND_TREASURE, 'dst': S_FOUND_ABOUT_DETAILS, 'cond': R_ANYTHING, 'callback': T_PARSE_DESCRIPTION},
    {'src': S_FOUND_ABOUT_HEADER, 'dst': S_FOUND_ABOUT_DETAILS, 'cond': R_ANYTHING, 'callback': T_PARSE_DESCRIPTION},
    {'src': S_FOUND_ABOUT_DETAILS, 'dst': S_FOUND_COPYRIGHT, 'cond': r"Copyright", 'callback': T_SKIP},
    {'src': S_FOUND_ABOUT_DETAILS, 'dst': S_FOUND_ABOUT_DETAILS, 'cond': R_ANYTHING, 'callback': T_PARSE_DESCRIPTION}
]

for map_item in FSM_MAP:
    map_item['condition_re_compiled'] = re.compile(map_item['cond'])

class ParseCreature:
    def __init__(self, raw_input):
        self.creature = Creature()
        self.creature.space = '5 ft.'
        self.creature.reach = '5 ft.'
        self.gear_item = None
        self.special_ability = None
        self.input_str = raw_input
        self.current_state = S_INITIAL_LOAD
        self.current_line = ""

    def run(self):
        text = self.input_str
        text = re.sub(r"\r\n", "\n", text)
        text = re.sub(r"\n+", "\n", text)

        for line in text.split("\n"):
            if not self.process_next(line):
                print("skip '{}' in {}".format(line, self.current_state))

        # Clean up any unsaved compound objects
        transition_parse_save_special_ability(self)
        transition_parse_save_gear_item(self)

        print(self.creature)

    def process_next(self, line):
        self.current_line = line
        frozen_state = self.current_state
        for transition in FSM_MAP:
            if transition['src'] == frozen_state:
                if self.iterate_re_evaluators(line, transition):
                    return True
        return False

    def iterate_re_evaluators(self, line, transition):
        condition = transition['condition_re_compiled']
        if condition.match(line):
            self.update_state(
                transition['dst'], transition['callback'])
            return True
        return False

    def update_state(self, new_state, callback):
        print("{} -> {} : {}".format(self.current_state,
                                     new_state,
                                     self.current_line))
        self.current_state = new_state
        callback(self)
