from tkinter import *
from tkinter import ttk
from widgets.PairTupleCombobox import PairTupleCombobox
from database import SessionLocal
from models import Creature, CreatureLanguages, CreatureFeats, CreatureSkills
import re

alignment_tuples = [ ('LG', 'Lawful Good'), ('NG', 'Neutral Good'), ('CG', 'Chaotic Good'),
                     ('LN', 'Lawful Neutral'), ('N', 'Neutral'), ('CN', 'Chaotic Neutral'),
                     ('LE', 'Lawful Evil'), ('NE', 'Neutral Evil'), ('CE', 'Chaotic Evil')]

creature_sizes = [
    "Fine",
    "Diminutive",
    "Tiny",
    "Small",
    "Medium",
    "Large",
    "Huge",
    "Gargantuan",
    "Colossal",
]

class CreatureForm:

    def __init__(self, root):
        self.root = root
        self.creature = None
        self.creature_id = 0

        root.title("Creature Details")

        mainframe = ttk.Frame(root, padding=3, borderwidth=2, relief='raised')
        mainframe.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(mainframe, text="Formal Name").grid(row=1, column=0, sticky=W)
        self.formal_name = StringVar()
        formal_name_entry = ttk.Entry(mainframe, width=50, textvariable=self.formal_name)
        formal_name_entry.grid(row=1, column=1, columnspan=3, sticky=W)

        ttk.Label(mainframe, text="Common Name").grid(row=2, column=0, sticky=W)
        self.common_name = StringVar()
        common_name_entry = ttk.Entry(mainframe, width=50, textvariable=self.common_name)
        common_name_entry.grid(row=2, column=1, columnspan=3, sticky=W)

        ttk.Label(mainframe, text="CR").grid(row=2, column=4, sticky=W)
        self.challenge_rating = StringVar()
        challenge_rating_entry = ttk.Entry(mainframe, width=6, textvariable=self.challenge_rating)
        challenge_rating_entry.grid(row=2, column=5, sticky=W)

        ttk.Label(mainframe, text="XP").grid(row=3, column=0, sticky=W)
        self.experience_points = StringVar()
        experience_points_entry = ttk.Entry(mainframe, width=10, textvariable=self.experience_points)
        experience_points_entry.grid(row=3, column=1, sticky=W)

        ttk.Label(mainframe, text="Alignment").grid(row=4, column=0, sticky=W)
        self.alignment_entry = PairTupleCombobox(mainframe, p_list_pair_tuple = alignment_tuples, p_default_key = 'N')
        self.alignment_entry.grid(row=4, column=1, sticky=W)

        ttk.Label(mainframe, text="Size").grid(row=5, column=0, sticky=W)
        self.size = StringVar()
        size_entry = ttk.Combobox(mainframe, values=creature_sizes, textvariable=self.size)
        size_entry.grid(row=5, column=1, sticky=W)

        ttk.Label(mainframe, text="Age").grid(row=6, column=0, sticky=W)
        self.age = StringVar()
        age_entry = ttk.Entry(mainframe, width=6, textvariable=self.age)
        age_entry.grid(row=6, column=1, sticky=W)

        ttk.Label(mainframe, text="Type").grid(row=7, column=0, sticky=W)
        self.type = StringVar()
        type_entry = ttk.Entry(mainframe, width=16, textvariable=self.type)
        type_entry.grid(row=7, column=1, sticky=W)

        ttk.Label(mainframe, text=" / Sub-Type").grid(row=7, column=2, sticky=W)
        self.sub_type = StringVar()
        sub_type_entry = ttk.Entry(mainframe, width=16, textvariable=self.sub_type)
        sub_type_entry.grid(row=7, column=3, sticky=W)

        ttk.Label(mainframe, text="Race").grid(row=8, column=0, sticky=W)
        self.race = StringVar()
        race_entry = ttk.Entry(mainframe, width=16, textvariable=self.race)
        race_entry.grid(row=8, column=1, sticky=W)

        ttk.Label(mainframe, text="Class").grid(row=8, column=2, sticky=W)
        self.char_class = StringVar()
        char_class_entry = ttk.Entry(mainframe, width=16, textvariable=self.char_class)
        char_class_entry.grid(row=8, column=3, sticky=W)

        ttk.Label(mainframe, text=" / Level").grid(row=8, column=4, sticky=W)
        self.level = StringVar()
        level_entry = ttk.Entry(mainframe, width=16, textvariable=self.level)
        level_entry.grid(row=8, column=5, sticky=W)

        ttk.Label(mainframe, text="Init").grid(row=9, column=0, sticky=W)
        self.initiative = StringVar()
        initiative_entry = ttk.Entry(mainframe, width=16, textvariable=self.initiative)
        initiative_entry.grid(row=9, column=1, sticky=W)

        ttk.Label(mainframe, text="PM").grid(row=10, column=0, sticky=W)
        self.perception_modifier = StringVar()
        perception_modifier_entry = ttk.Entry(mainframe, width=16, textvariable=self.perception_modifier)
        perception_modifier_entry.grid(row=9, column=1, sticky=W)

        ttk.Label(mainframe, text="Senses").grid(row=11, column=0, sticky=W)
        ttk.Label(mainframe, text="Auras").grid(row=12, column=0, sticky=W)
        ttk.Label(mainframe, text="AC").grid(row=13, column=0, sticky=W)
        ttk.Label(mainframe, text="HP").grid(row=14, column=0, sticky=W)

        ttk.Label(mainframe, text="Fort").grid(row=15, column=0, sticky=W)
        self.fortitude = StringVar()
        fortitude_entry = ttk.Entry(mainframe, width=16, textvariable=self.fortitude)
        fortitude_entry.grid(row=15, column=1, sticky=W)

        ttk.Label(mainframe, text="Ref").grid(row=15, column=2, sticky=W)
        self.reflex = StringVar()
        reflex_entry = ttk.Entry(mainframe, width=16, textvariable=self.reflex)
        reflex_entry.grid(row=15, column=3, sticky=W)

        ttk.Label(mainframe, text="Will").grid(row=15, column=4, sticky=W)
        self.will = StringVar()
        will_entry = ttk.Entry(mainframe, width=16, textvariable=self.will)
        will_entry.grid(row=15, column=5, sticky=W)

        ttk.Label(mainframe, text="DR").grid(row=18, column=0, sticky=W)
        self.damage_reduction = StringVar()
        damage_reduction_entry = ttk.Entry(mainframe, width=16, textvariable=self.damage_reduction)
        damage_reduction_entry.grid(row=18, column=1, sticky=W)

        ttk.Label(mainframe, text="SR").grid(row=19, column=0, sticky=W)
        self.spell_resistence = StringVar()
        spell_resistence_entry = ttk.Entry(mainframe, width=16, textvariable=self.spell_resistence)
        spell_resistence_entry.grid(row=19, column=1, sticky=W)

        ttk.Label(mainframe, text="STR").grid(row=20, column=0, sticky=W)
        self.strength = StringVar()
        strength_entry = ttk.Entry(mainframe, width=4, textvariable=self.strength)
        strength_entry.grid(row=20, column=1, sticky=W)

        ttk.Label(mainframe, text="DEX").grid(row=20, column=2, sticky=W)
        self.dexterity = StringVar()
        dexterity_entry = ttk.Entry(mainframe, width=4, textvariable=self.dexterity)
        dexterity_entry.grid(row=20, column=3, sticky=W)

        ttk.Label(mainframe, text="CON").grid(row=20, column=4, sticky=W)
        self.constitution = StringVar()
        constitution_entry = ttk.Entry(mainframe, width=4, textvariable=self.constitution)
        constitution_entry.grid(row=20, column=5, sticky=W)

        ttk.Label(mainframe, text="INT").grid(row=20, column=6, sticky=W)
        self.intelligence = StringVar()
        intelligence_entry = ttk.Entry(mainframe, width=4, textvariable=self.intelligence)
        intelligence_entry.grid(row=20, column=7, sticky=W)

        ttk.Label(mainframe, text="WIS").grid(row=20, column=8, sticky=W)
        self.wisdom = StringVar()
        wisdom_entry = ttk.Entry(mainframe, width=4, textvariable=self.wisdom)
        wisdom_entry.grid(row=20, column=9, sticky=W)

        ttk.Label(mainframe, text="CHA").grid(row=20, column=10, sticky=W)
        self.charisma = StringVar()
        charisma_entry = ttk.Entry(mainframe, width=4, textvariable=self.charisma)
        charisma_entry.grid(row=20, column=11, sticky=W)

        ttk.Label(mainframe, text="BAB").grid(row=21, column=0, sticky=W)
        self.base_attack = StringVar()
        base_attack_entry = ttk.Entry(mainframe, width=4, textvariable=self.base_attack)
        base_attack_entry.grid(row=21, column=1, sticky=W)

        ttk.Label(mainframe, text="CMB").grid(row=21, column=2, sticky=W)
        self.combat_maneuver_bonus = StringVar()
        combat_maneuver_bonus_entry = ttk.Entry(mainframe, width=4, textvariable=self.combat_maneuver_bonus)
        combat_maneuver_bonus_entry.grid(row=21, column=3, sticky=W)

        ttk.Label(mainframe, text="CMD").grid(row=21, column=4, sticky=W)
        self.combat_maneuver_defense = StringVar()
        combat_maneuver_defense_entry = ttk.Entry(mainframe, width=4, textvariable=self.combat_maneuver_defense)
        combat_maneuver_defense_entry.grid(row=21, column=5, sticky=W)

        ttk.Label(mainframe, text="Feats").grid(row=22, column=0, sticky=NW)
        self.feats_entry = Text(mainframe, width=30, height=1)
        self.feats_entry.grid(row=22, column=1, sticky=W)

        ttk.Label(mainframe, text="Skills").grid(row=23, column=0, sticky=NW)
        self.skills_entry = Text(mainframe, width=30, height=1)
        self.skills_entry.grid(row=23, column=1, sticky=W)

        ttk.Label(mainframe, text="Racial Modifiers").grid(row=24, column=0, sticky=W)
        self.racial_modifiers = StringVar()
        racial_modifiers_entry = ttk.Entry(mainframe, width=4, textvariable=self.racial_modifiers)
        racial_modifiers_entry.grid(row=24, column=1, sticky=W)

        ttk.Label(mainframe, text="Languages").grid(row=26, column=0, sticky=NW)
        self.language_entry = Text(mainframe, width=30, height=1)
        self.language_entry.grid(row=26, column=1, columnspan=3, sticky=W)


        ttk.Button(mainframe, text='load').grid(row=27, column=0, sticky=W)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def on_load(self, creature):
        try:
            self.creature = creature
            self.formal_name.set(getattr(self.creature, 'formal_name'))
            self.common_name.set(getattr(self.creature, 'common_name'))
            self.challenge_rating.set(getattr(self.creature, 'challenge_rating'))
            self.experience_points.set(getattr(self.creature, 'experience_points'))
            self.alignment_entry.set_selected_key(getattr(self.creature, 'alignment'))
            self.size.set(getattr(self.creature, 'size'))
            self.age.set(getattr(self.creature, 'age'))
            self.type.set(getattr(self.creature, 'type'))
            self.sub_type.set(getattr(self.creature, 'sub_type'))
            self.race.set(getattr(self.creature, 'race'))
            self.char_class.set(getattr(self.creature, 'char_class'))
            self.level.set(getattr(self.creature, 'level'))
            self.initiative.set(getattr(self.creature, 'initiative'))
            self.perception_modifier.set(getattr(self.creature, 'perception_modifier'))
            self.fortitude.set(getattr(self.creature, 'fortitude'))
            self.reflex.set(getattr(self.creature, 'reflex'))
            self.will.set(getattr(self.creature, 'will'))
            self.damage_reduction.set(getattr(self.creature, 'damage_reduction'))
            self.spell_resistence.set(getattr(self.creature, 'spell_resistence'))
            self.strength.set(getattr(self.creature, 'strength'))
            self.dexterity.set(getattr(self.creature, 'dexterity'))
            self.constitution.set(getattr(self.creature, 'constitution'))
            self.intelligence.set(getattr(self.creature, 'intelligence'))
            self.wisdom.set(getattr(self.creature, 'wisdom'))
            self.charisma.set(getattr(self.creature, 'charisma'))
            self.base_attack.set(getattr(self.creature, 'base_attack'))
            self.combat_maneuver_bonus.set(getattr(self.creature, 'combat_maneuver_bonus'))
            self.combat_maneuver_defense.set(getattr(self.creature, 'combat_maneuver_defense'))
            self.racial_modifiers.set(getattr(self.creature, 'racial_modifiers'))

            self.language_entry.delete("1.0", END)
            self.language_entry['height'] = len(self.creature.languages)
            for language in self.creature.languages:
                self.language_entry.insert(END, getattr(language, 'language') + "\n")

            self.feats_entry.delete("1.0", END)
            self.feats_entry['height'] = len(self.creature.feats)
            for feat in self.creature.feats:
                self.feats_entry.insert(END, getattr(feat, 'feat') + "\n")

            self.skills_entry.delete("1.0", END)
            self.skills_entry['height'] = len(self.creature.skills)
            for skill in self.creature.skills:
                self.skills_entry.insert(END, getattr(skill, 'skill') + " " + getattr(skill, 'modifier') + "\n")


        except ValueError:
            pass

    def populate_creature(self, parsed_data):
        creature = Creature()
        creature.formal_name = parsed_data.get('Formal Name','')
        creature.common_name = parsed_data.get('Name','')
        creature.challenge_rating = parsed_data.get('CR','')
        creature.experience_points = parsed_data.get('XP','')
        creature.alignment = parsed_data.get('Alignment','')
        creature.size = parsed_data.get('Size','')
        type_sub_type = parsed_data.get('Type/(sub-type)','')
        matches = re.match("(.+) (\\((.+)\\))", type_sub_type)
        if matches:
            creature.type = matches.group(1)
            if matches.group(3):
                creature.sub_type = matches.group(3)
        else:
            matches = re.match("(.+)", type_sub_type)
            if matches:
                creature.type = matches.group(1)

        creature.fortitude = parsed_data.get('Fort','')
        creature.reflex = parsed_data.get('Ref','')
        creature.will = parsed_data.get('Will','')
        creature.strength = parsed_data.get('STR','')
        creature.dexterity = parsed_data.get('DEX','')
        creature.constitution = parsed_data.get('CON','')
        creature.intelligence = parsed_data.get('INT','')
        creature.wisdom = parsed_data.get('WIS','')
        creature.charisma = parsed_data.get('CHA','')
        creature.base_attack = parsed_data.get('BAB','')
        creature.combat_maneuver_bonus = parsed_data.get('CMB','')
        creature.combat_maneuver_defense = parsed_data.get('CMD','')

        languages = [p.strip() for p in parsed_data['Languages'].split(",") if p.strip()]
        for language in languages:
            creature_language = CreatureLanguages()
            creature_language.language = language
            creature.languages.append(creature_language)

        feats = [p.strip() for p in parsed_data['Feats'].split(",") if p.strip()]
        for feat in feats:
            creature_feat = CreatureFeats()
            creature_feat.feat = feat
            creature.feats.append(creature_feat)

        skills = [p.strip() for p in parsed_data['Skills'].split(",") if p.strip()]
        for skill in skills:
            creature_skill = CreatureSkills()
            parts = skill.split("+")
            creature_skill.skill = parts[0].strip()
            creature_skill.modifier = "+" + parts[1].strip()
            creature.skills.append(creature_skill)

        self.on_load(creature)

class CreatureList:

    def __init__(self, root):
        self.root = root
        self.creature = None
        self.creature_id = 0

        root.title("Creature List")

        mainframe = ttk.Frame(root, padding=3, borderwidth=2, relief='raised')
        mainframe.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
        self.creature_choices_var = StringVar()
        self.creature_list = Listbox(mainframe, height=10, listvariable=self.creature_choices_var)
        self.creature_list.grid(row=0, column=0, sticky="nsew")

        load_button = ttk.Button(mainframe, text="load", command=lambda: self.show_creature())
        load_button.grid(row=1, column=0, sticky="w")
        new_button = ttk.Button(mainframe, text="New")
        new_button.grid(row=1, column=2, sticky="e")


        try:
            db = SessionLocal()
            creatures = db.query(Creature).order_by(Creature.formal_name).all()
            creature_choices = []
            for creature in creatures:
                creature_choices.append(creature.formal_name)

            self.creature_choices_var.set(creature_choices)



        except ValueError:
            pass

    def show_creature(self):
        selection_indices = self.creature_list.curselection()
        if selection_indices:
            # Get the first (and only) index from the tuple
            index = selection_indices[0]
            # Get the value at that index
            selected_item = self.creature_list.get(index)
            print(f"Selected item: {selected_item}")
            formal_name = selected_item
            print(formal_name)
            db = SessionLocal()
            self.creature = db.query(Creature).filter(Creature.formal_name == formal_name).first()
            self.creature_id = self.creature.id
            creature_form = CreatureForm(self.root)
            creature_form.on_load(self.creature)
        else:
            print("No item selected")



