from models import Creature, CreatureLanguages, CreatureFeats, CreatureSkills, CreatureSenses, CreatureAuras
import re

def _normalize_case(text: str) -> str:
    parts = [p.strip() for p in text.split(",")]
    return ", ".join(p[:1].upper() + p[1:] for p in parts)

def transition_skip(fsm_obj):
    pass

def transition_parse_formal_name(fsm_obj):
    fsm_obj.creature.formal_name = fsm_obj.current_line.strip()

def transition_parse_common_name(fsm_obj):
    name_match = re.match(r"^(.+)\sCR\s+([\d/]+)", fsm_obj.current_line)
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
        description += fsm_obj.current_line
    else:
        description = ''
    fsm_obj.creature.description = description
    pass

def transition_parse_experience_points(fsm_obj):
    xp_match = re.search(r"XP\s+([\d,]+)", fsm_obj.current_line, re.IGNORECASE)
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
            senses = _normalize_case(senses_match.group(1)).split(",")
            for sense in senses:
                creature_senses = CreatureSenses()
                creature_senses.sense = sense
                fsm_obj.creature.senses.append(creature_senses)

        transition_parse_auras(fsm_obj)

def transition_parse_auras(fsm_obj):
    aura_match = re.search(r"Aura\s+(.+)", fsm_obj.current_line)
    if aura_match:
        aura_details = re.findall(r"([, ]*(.+?)\s\((.+?),\s(.+?)\))+?", aura_match.group(1), re.IGNORECASE)
        if aura_details:
            print(len(aura_details), ' ', aura_details)
            for aura_detail in aura_details:
                creature_auras = CreatureAuras()
                creature_auras.aura = aura_detail[1].strip()
                creature_auras.radius = aura_detail[2].strip()
                creature_auras.save_role = aura_detail[3].strip()
                fsm_obj.creature.auras.append(creature_auras)

T_SKIP = transition_skip
T_PARSE_FORMAL_NAME = transition_parse_formal_name
T_PARSE_COMMON_NAME = transition_parse_common_name
T_PARSE_DESCRIPTION = transition_parse_description
T_PARSE_EXPERIENCE_POINTS = transition_parse_experience_points
T_PARSE_ALIGNMENT = transition_parse_alignment
T_PARSE_RACE = transition_parse_race
T_PARSE_INITIATIVE = transition_parse_initiative
T_PARSE_AURAS = transition_parse_auras

S_INITIAL_LOAD = "STATE: INITIAL FILE"
S_FOUND_FORMAL_NAME = "STATE: FOUND FORMAL NAME"
S_FOUND_COMMON_NAME = "STATE: FOUND COMMON NAME"
S_FOUND_DESCRIPTION = "STATE: FOUND DESCRIPTION"
S_FOUND_XP = "STATE: FOUND XP"
S_FOUND_RACE = "STATE: FOUND RACE"
S_FOUND_ALIGNMENT = "STATE: FOUND ALIGNMENT"
S_FOUND_INITIATIVE = "STATE: FOUND INITIATIVE"
S_FOUND_AURAS = "STATE: FOUND AURAS"
S_FOUND_DEFENSE = "STATE: FOUND DEFENSE"
S_FOUND_AC = "STATE: FOUND AC"
S_FOUND_HP = "STATE: FOUND HP"
S_FOUND_FORTITUDE = "STATE: FOUND FORTITUDE"
S_FOUND_DR = "STATE: FOUND DR"
S_FOUND_OFFENSE = "STATE: FOUND OFFENSE"
S_FOUND_SPEED = "STATE: FOUND SPEED"
S_FOUND_MELEE = "STATE: FOUND MELEE"
S_FOUND_SPACE = "STATE: FOUND SPACE"
S_FOUND_SPECIAL_ATTACKS = "STATE: FOUND SPECIAL ATTACKS"
S_FOUND_SPELL_LIKE_ABILITIES = "STATE: FOUND SPELL LIKE ABILITIES"
S_FOUND_SPELLS_KNOWN = "STATE: FOUND SPELLS KNOWN"
S_FOUND_SPELLS_PREPARED = "STATE: FOUND SPELLS PREPARED"
S_FOUND_TACTICS = "STATE: FOUND TACTICS"
S_FOUND_STATISTICS = "STATE: FOUND STATISTICS"
S_FOUND_STRENGTH = "STATE: FOUND STRENGTH"
S_FOUND_BASE_ATTACK = "STATE: FOUND BASE ATTACK"
S_FOUND_FEATS = "STATE: FOUND FEATS"
S_FOUND_SKILLS = "STATE: FOUND SKILLS"
S_FOUND_LANGUAGES = "STATE: FOUND LANGUAGES"
S_FOUND_SPECIAL_QUALITIES = "STATE: FOUND SPECIAL QUALITIES"
S_FOUND_GEAR_LINE = "STATE: FOUND GEAR LINE"
S_FOUND_SPECIAL_ABILITIES = "STATE: FOUND SPECIAL ABILITIES"
S_FOUND_ABILITY_NAME = "STATE: FOUND ABILITY NAME"
S_FOUND_ABILITY_DESCRIPTION = "STATE: FOUND ABILITY DESCRIPTION"
S_FOUND_GEAR_HEADER = "STATE: FOUND GEAR HEADER"
S_FOUND_GEAR_ITEM = "STATE: FOUND GEAR ITEM"
S_FOUND_GEAR_DESCRIPTION = "STATE: FOUND GEAR DESCRIPTION"
S_FOUND_ECOLOGY = "STATE: FOUND ECOLOGY"
S_FOUND_ENVIRONMENT = "STATE: FOUND ENVIRONMENT"
S_FOUND_ORGANIZATION = "STATE: FOUND ORGANIZATION"
S_FOUND_TREASURE = "STATE: FOUND TREASURE"
S_FOUND_COPYRIGHT = "STATE: FOUND COPYRIGHT"

FSM_MAP = [
    #  {'src':, 'dst':, 'condition':, 'callback': },
    {'src': S_INITIAL_LOAD, 'dst': S_FOUND_FORMAL_NAME, 'cond': r"(.+)", 'callback': T_PARSE_FORMAL_NAME},  # 1
    {'src': S_INITIAL_LOAD, 'dst': S_FOUND_COMMON_NAME, 'cond': r"^(.+)\sCR\s+([\d/]+)", 'callback': T_PARSE_COMMON_NAME},  # 2
    {'src': S_FOUND_FORMAL_NAME, 'dst': S_FOUND_COMMON_NAME, 'cond': r"^(.+)\sCR\s+([\d/]+)", 'callback': T_PARSE_COMMON_NAME},  # 3
    {'src': S_FOUND_FORMAL_NAME, 'dst': S_FOUND_DESCRIPTION, 'cond': r"^(.+)", 'callback': T_PARSE_DESCRIPTION},  # 4
    {'src': S_FOUND_DESCRIPTION, 'dst': S_FOUND_COMMON_NAME, 'cond': r"^(.+)\sCR\s+([\d/]+)", 'callback': T_PARSE_COMMON_NAME},  # 5
    {'src': S_FOUND_DESCRIPTION, 'dst': S_FOUND_XP, 'cond': r"XP\s+([\d,]+)", 'callback': T_PARSE_EXPERIENCE_POINTS}, #6
    {'src': S_FOUND_DESCRIPTION, 'dst': S_FOUND_DESCRIPTION, 'cond': r"^(.+)", 'callback': T_PARSE_DESCRIPTION},  #7
    {'src': S_FOUND_COMMON_NAME, 'dst': S_FOUND_XP, 'cond': r"XP\s+([\d,]+)", 'callback': T_PARSE_EXPERIENCE_POINTS}, #8
    {'src': S_FOUND_COMMON_NAME, 'dst': S_FOUND_DESCRIPTION, 'cond': r"^(.+)", 'callback': T_PARSE_EXPERIENCE_POINTS}, #9
    {'src': S_FOUND_XP, 'dst': S_FOUND_ALIGNMENT, 'cond': r"^([LNCEG]{1,2})\s", 'callback': T_PARSE_ALIGNMENT}, #10
    {'src': S_FOUND_XP, 'dst': S_FOUND_RACE, 'cond': r"^(.+)", 'callback': T_PARSE_RACE}, #11
    {'src': S_FOUND_RACE, 'dst': S_FOUND_ALIGNMENT, 'cond': r"^([LNCEG]{1,2})\s", 'callback': T_PARSE_ALIGNMENT},  # 12
    {'src': S_FOUND_ALIGNMENT, 'dst': S_FOUND_INITIATIVE, 'cond': r"^Init\s+([^\n;]+)", 'callback': T_PARSE_INITIATIVE},  # 13
    {'src': S_FOUND_INITIATIVE, 'dst': S_FOUND_AURAS, 'cond': r"^Aura\s+([^\n;]+)", 'callback': T_PARSE_AURAS}, # 14
    {'src': S_FOUND_INITIATIVE, 'dst': S_FOUND_DEFENSE, 'cond': r"^DEFENSE", 'callback': T_SKIP}, # 15
    {'src': S_FOUND_AURAS, 'dst': S_FOUND_DEFENSE, 'cond': r"^DEFENSE", 'callback': T_SKIP},  # 16

]

for map_item in FSM_MAP:
    map_item['condition_re_compiled'] = re.compile(map_item['cond'])

class ParseCreature:
    def __init__(self, raw_input):
        self.creature = Creature()
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
        print("{} -> {} : {}".format(self.current_line,
                                     self.current_state,
                                     new_state))
        self.current_state = new_state
        callback(self)
