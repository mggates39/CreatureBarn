from tkinter import *
from tkinter import ttk
from widgets.PairTupleCombobox import PairTupleCombobox
from widgets.SectionBorder import SectionBorder
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


def safe_copy(data):
    return data if data else ""


class CreatureForm:

    def __init__(self, root):
        self.root = root
        self.creature = None
        self.creature_id = 0

        root.title("Creature Details")
        root.geometry("1024x768")
        canvas = Canvas(root)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview, width=5)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        mainframe = ttk.Frame(root, padding=3, borderwidth=2, relief='raised')

        canvas.create_window((0, 0), window=mainframe, anchor="nw")
        mainframe.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # mainframe.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        row_count = 1
        ttk.Label(mainframe, text="Formal Name").grid(row=row_count, column=0, sticky=E)
        self.formal_name = StringVar()
        formal_name_entry = ttk.Entry(mainframe, width=50, textvariable=self.formal_name)
        formal_name_entry.grid(row=row_count, column=1, columnspan=3, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Common Name").grid(row=row_count, column=0, sticky=E)
        self.common_name = StringVar()
        common_name_entry = ttk.Entry(mainframe, width=50, textvariable=self.common_name)
        common_name_entry.grid(row=row_count, column=1, columnspan=3, sticky=W)

        ttk.Label(mainframe, text="CR").grid(row=row_count, column=4, sticky=E)
        self.challenge_rating = StringVar()
        challenge_rating_entry = ttk.Entry(mainframe, width=6, textvariable=self.challenge_rating)
        challenge_rating_entry.grid(row=row_count, column=5, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="XP").grid(row=row_count, column=0, sticky=E)
        self.experience_points = StringVar()
        experience_points_entry = ttk.Entry(mainframe, width=10, textvariable=self.experience_points)
        experience_points_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Alignment").grid(row=row_count, column=0, sticky=E)
        self.alignment_entry = PairTupleCombobox(mainframe, p_list_pair_tuple = alignment_tuples, p_default_key = 'N')
        self.alignment_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Size").grid(row=row_count, column=0, sticky=E)
        self.size = StringVar()
        size_entry = ttk.Combobox(mainframe, values=creature_sizes, textvariable=self.size)
        size_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Age").grid(row=row_count, column=0, sticky=E)
        self.age = StringVar()
        age_entry = ttk.Entry(mainframe, width=6, textvariable=self.age)
        age_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Type").grid(row=row_count, column=0, sticky=E)
        self.type = StringVar()
        type_entry = ttk.Entry(mainframe, width=16, textvariable=self.type)
        type_entry.grid(row=row_count, column=1, sticky=W)

        ttk.Label(mainframe, text=" / Sub-Type").grid(row=row_count, column=2, sticky=E)
        self.sub_type = StringVar()
        sub_type_entry = ttk.Entry(mainframe, width=16, textvariable=self.sub_type)
        sub_type_entry.grid(row=row_count, column=3, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Race").grid(row=row_count, column=0, sticky=E)
        self.race = StringVar()
        race_entry = ttk.Entry(mainframe, width=16, textvariable=self.race)
        race_entry.grid(row=row_count, column=1, sticky=W)

        ttk.Label(mainframe, text="Class").grid(row=row_count, column=2, sticky=E)
        self.char_class = StringVar()
        char_class_entry = ttk.Entry(mainframe, width=16, textvariable=self.char_class)
        char_class_entry.grid(row=row_count, column=3, sticky=W)

        ttk.Label(mainframe, text=" / Level").grid(row=row_count, column=4, sticky=E)
        self.level = StringVar()
        level_entry = ttk.Entry(mainframe, width=16, textvariable=self.level)
        level_entry.grid(row=row_count, column=5, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Init").grid(row=row_count, column=0, sticky=E)
        self.initiative = StringVar()
        initiative_entry = ttk.Entry(mainframe, width=16, textvariable=self.initiative)
        initiative_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="PM").grid(row=row_count, column=0, sticky=E)
        self.perception_modifier = StringVar()
        perception_modifier_entry = ttk.Entry(mainframe, width=16, textvariable=self.perception_modifier)
        perception_modifier_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Senses").grid(row=row_count, column=0, sticky=NE)
        self.senses_entry = Text(mainframe, width=30, height=1)
        self.senses_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Auras").grid(row=row_count, column=0, sticky=NE)
        self.auras_entry = Text(mainframe, width=40, height=1)
        self.auras_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        # defense_frame = SectionBorder(mainframe, title="Defense", borderwidth=3, relief="raised")
        defense_frame = SectionBorder(mainframe, title="Defense")
        defense_frame.grid(row=row_count, column=0, columnspan=12)

        row_count += 1
        ttk.Label(mainframe, text="AC").grid(row=row_count, column=0, sticky=E)
        self.base_ac = StringVar()
        base_ac_entry = ttk.Entry(mainframe, width=4, textvariable=self.base_ac)
        base_ac_entry.grid(row=row_count, column=1, sticky=W)

        ttk.Label(mainframe, text="Touch").grid(row=row_count, column=2, sticky=E)
        self.touch_ac = StringVar()
        touch_ac_entry = ttk.Entry(mainframe, width=4, textvariable=self.touch_ac)
        touch_ac_entry.grid(row=row_count, column=3, sticky=W)

        ttk.Label(mainframe, text="Flat-Footed").grid(row=row_count, column=4, sticky=E)
        self.flat_footed_ac = StringVar()
        flat_footed_ac_entry = ttk.Entry(mainframe, width=4, textvariable=self.flat_footed_ac)
        flat_footed_ac_entry.grid(row=row_count, column=5, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="AC Modifiers").grid(row=row_count, column=0, sticky=NE)
        self.ac_modifier_entry = Text(mainframe, width=30, height=1)
        self.ac_modifier_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="HP").grid(row=row_count, column=0, sticky=E)
        self.hit_points = StringVar()
        hit_points_entry = ttk.Entry(mainframe, width=20, textvariable=self.hit_points)
        hit_points_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Fort").grid(row=row_count, column=0, sticky=E)
        self.fortitude = StringVar()
        fortitude_entry = ttk.Entry(mainframe, width=16, textvariable=self.fortitude)
        fortitude_entry.grid(row=row_count, column=1, sticky=W)

        ttk.Label(mainframe, text="Ref").grid(row=row_count, column=2, sticky=E)
        self.reflex = StringVar()
        reflex_entry = ttk.Entry(mainframe, width=16, textvariable=self.reflex)
        reflex_entry.grid(row=row_count, column=3, sticky=W)

        ttk.Label(mainframe, text="Will").grid(row=row_count, column=4, sticky=E)
        self.will = StringVar()
        will_entry = ttk.Entry(mainframe, width=16, textvariable=self.will)
        will_entry.grid(row=row_count, column=5, sticky=W)

        self.will_modifier = StringVar()
        will_entry = ttk.Entry(mainframe, width=20, textvariable=self.will_modifier)
        will_entry.grid(row=row_count, column=6, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="DR").grid(row=row_count, column=0, sticky=E)
        self.damage_reduction = StringVar()
        damage_reduction_entry = ttk.Entry(mainframe, width=16, textvariable=self.damage_reduction)
        damage_reduction_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="SR").grid(row=row_count, column=0, sticky=E)
        self.spell_resistence = StringVar()
        spell_resistence_entry = ttk.Entry(mainframe, width=16, textvariable=self.spell_resistence)
        spell_resistence_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Immunities").grid(row=row_count, column=0, sticky=NE)
        self.immune_entry = Text(mainframe, width=40, height=1)
        self.immune_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Resistance").grid(row=row_count, column=0, sticky=NE)
        self.resist_entry = Text(mainframe, width=40, height=1)
        self.resist_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Weaknesses").grid(row=row_count, column=0, sticky=NE)
        self.weakness_entry = Text(mainframe, width=40, height=1)
        self.weakness_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Defensive Abilities").grid(row=row_count, column=0, sticky=NE)
        self.defense_action_entry = Text(mainframe, width=40, height=1)
        self.defense_action_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        offense_frame = SectionBorder(mainframe, title="Offense")
        offense_frame.grid(row=row_count, column=0, columnspan=12)

        row_count += 1
        ttk.Label(mainframe, text="Speed").grid(row=row_count, column=0, sticky=NE)
        self.speed = StringVar()
        speed_entry = ttk.Entry(mainframe, width=30, textvariable=self.speed)
        speed_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        self.speed_modifiers_entry = Text(mainframe, width=30, height=1)
        self.speed_modifiers_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Space").grid(row=row_count, column=0, sticky=E)
        self.space = StringVar()
        space_entry = ttk.Entry(mainframe, width=10, textvariable=self.space)
        space_entry.grid(row=row_count, column=1, sticky=W)

        ttk.Label(mainframe, text="Reach").grid(row=row_count, column=2, sticky=E)
        self.reach = StringVar()
        reach_entry = ttk.Entry(mainframe, width=20, textvariable=self.reach)
        reach_entry.grid(row=row_count, column=3, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Melee").grid(row=row_count, column=0, sticky=NE)
        self.melee_entry = Text(mainframe, width=40, height=1)
        self.melee_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Ranged").grid(row=row_count, column=0, sticky=NE)
        self.ranged_entry = Text(mainframe, width=40, height=1)
        self.ranged_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Special Attacks").grid(row=row_count, column=0, sticky=NE)
        self.special_attacks_entry = Text(mainframe, width=40, height=1)
        self.special_attacks_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        self.spell_like_label = StringVar()
        self.spell_like_label.set("Spell-Like Abilities")
        ttk.Label(mainframe, textvariable=self.spell_like_label).grid(row=row_count, column=0, sticky=NE)
        self.spell_like_caster_level = StringVar()
        casting_level_entry = ttk.Entry(mainframe, width=30, textvariable=self.spell_like_caster_level)
        casting_level_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        self.spell_like_abilities_entry = Text(mainframe, width=60, height=1)
        self.spell_like_abilities_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        self.known_spells_label = StringVar()
        self.known_spells_label.set("Known Spells")
        ttk.Label(mainframe, textvariable=self.known_spells_label).grid(row=row_count, column=0, sticky=NE)
        self.known_caster_level = StringVar()
        known_casting_level_entry = ttk.Entry(mainframe, width=30, textvariable=self.known_caster_level)
        known_casting_level_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        self.known_spells_entry = Text(mainframe, width=60, height=1)
        self.known_spells_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        self.prepared_spells_label = StringVar()
        self.prepared_spells_label.set("Prepared Spells")
        ttk.Label(mainframe, textvariable=self.prepared_spells_label).grid(row=row_count, column=0, sticky=NE)
        self.prepared_caster_level = StringVar()
        prepared_casting_level_entry = ttk.Entry(mainframe, width=30, textvariable=self.prepared_caster_level)
        prepared_casting_level_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        self.prepared_spells_entry = Text(mainframe, width=60, height=1)
        self.prepared_spells_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        offense_frame = SectionBorder(mainframe, title="Tactics")
        offense_frame.grid(row=row_count, column=0, columnspan=12)

        row_count += 1
        self.tactics_entry = Text(mainframe, wrap="word", width=90, height=1)
        self.tactics_entry.grid(row=row_count, column=1, columnspan=12, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Gear").grid(row=row_count, column=0, sticky=E)
        self.gear = StringVar()
        gear_entry = ttk.Entry(mainframe, width=60, textvariable=self.gear)
        gear_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        offense_frame = SectionBorder(mainframe, title="Statistics")
        offense_frame.grid(row=row_count, column=0, columnspan=12)

        row_count += 1
        ttk.Label(mainframe, text="STR").grid(row=row_count, column=0, sticky=E)
        self.strength = StringVar()
        strength_entry = ttk.Entry(mainframe, width=4, textvariable=self.strength)
        strength_entry.grid(row=row_count, column=1, sticky=W)

        ttk.Label(mainframe, text="DEX").grid(row=row_count, column=2, sticky=E)
        self.dexterity = StringVar()
        dexterity_entry = ttk.Entry(mainframe, width=4, textvariable=self.dexterity)
        dexterity_entry.grid(row=row_count, column=3, sticky=W)

        ttk.Label(mainframe, text="CON").grid(row=row_count, column=4, sticky=E)
        self.constitution = StringVar()
        constitution_entry = ttk.Entry(mainframe, width=4, textvariable=self.constitution)
        constitution_entry.grid(row=row_count, column=5, sticky=W)

        ttk.Label(mainframe, text="INT").grid(row=row_count, column=6, sticky=E)
        self.intelligence = StringVar()
        intelligence_entry = ttk.Entry(mainframe, width=4, textvariable=self.intelligence)
        intelligence_entry.grid(row=row_count, column=7, sticky=W)

        ttk.Label(mainframe, text="WIS").grid(row=row_count, column=8, sticky=E)
        self.wisdom = StringVar()
        wisdom_entry = ttk.Entry(mainframe, width=4, textvariable=self.wisdom)
        wisdom_entry.grid(row=row_count, column=9, sticky=W)

        ttk.Label(mainframe, text="CHA").grid(row=row_count, column=10, sticky=E)
        self.charisma = StringVar()
        charisma_entry = ttk.Entry(mainframe, width=4, textvariable=self.charisma)
        charisma_entry.grid(row=row_count, column=11, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="BAB").grid(row=row_count, column=0, sticky=E)
        self.base_attack = StringVar()
        base_attack_entry = ttk.Entry(mainframe, width=4, textvariable=self.base_attack)
        base_attack_entry.grid(row=row_count, column=1, sticky=W)

        ttk.Label(mainframe, text="CMB").grid(row=row_count, column=2, sticky=E)
        self.combat_maneuver_bonus = StringVar()
        combat_maneuver_bonus_entry = ttk.Entry(mainframe, width=4, textvariable=self.combat_maneuver_bonus)
        combat_maneuver_bonus_entry.grid(row=row_count, column=3, sticky=W)

        ttk.Label(mainframe, text="CMD").grid(row=row_count, column=4, sticky=E)
        self.combat_maneuver_defense = StringVar()
        combat_maneuver_defense_entry = ttk.Entry(mainframe, width=4, textvariable=self.combat_maneuver_defense)
        combat_maneuver_defense_entry.grid(row=row_count, column=5, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Feats").grid(row=row_count, column=0, sticky=NE)
        self.feats_entry = Text(mainframe, width=30, height=1)
        self.feats_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Skills").grid(row=row_count, column=0, sticky=NE)
        self.skills_entry = Text(mainframe, width=30, height=1)
        self.skills_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Racial Modifiers").grid(row=row_count, column=0, sticky=E)
        self.racial_modifiers = StringVar()
        racial_modifiers_entry = ttk.Entry(mainframe, width=32, textvariable=self.racial_modifiers)
        racial_modifiers_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Languages").grid(row=row_count, column=0, sticky=NE)
        self.language_entry = Text(mainframe, width=30, height=1)
        self.language_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Special Qualities").grid(row=row_count, column=0, sticky=NE)
        self.special_qualities_entry = Text(mainframe, width=30, height=1)
        self.special_qualities_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Languages").grid(row=row_count, column=0, sticky=NE)
        self.language_entry = Text(mainframe, width=30, height=1)
        self.language_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        special_ability_frame = SectionBorder(mainframe, title="Special Abilities")
        special_ability_frame.grid(row=row_count, column=0, columnspan=12)

        row_count += 1
        ttk.Label(mainframe, text="Special Abilities").grid(row=row_count, column=0, sticky=NE)
        self.special_abilities_entry = Text(mainframe, width=60, height=1)
        self.special_abilities_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        unique_gear_frame = SectionBorder(mainframe, title="Gear")
        unique_gear_frame.grid(row=row_count, column=0, columnspan=12)

        row_count += 1
        ttk.Label(mainframe, text="Unique Items").grid(row=row_count, column=0, sticky=NE)
        self.special_gear_entry = Text(mainframe, wrap="word", width=70, height=1)
        self.special_gear_entry.grid(row=row_count, column=1, columnspan=7, sticky=W)

        row_count += 1
        ecology_frame = SectionBorder(mainframe, title="Ecology")
        ecology_frame.grid(row=row_count, column=0, columnspan=12)

        row_count += 1
        ttk.Label(mainframe, text="Environment").grid(row=row_count, column=0, sticky=E)
        self.environment = StringVar()
        environment_entry = ttk.Entry(mainframe, width=30, textvariable=self.environment)
        environment_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Organization").grid(row=row_count, column=0, sticky=E)
        self.organization = StringVar()
        organization_entry = ttk.Entry(mainframe, width=30, textvariable=self.organization)
        organization_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        ttk.Label(mainframe, text="Treasure").grid(row=row_count, column=0, sticky=E)
        self.treasure = StringVar()
        treasure_entry = ttk.Entry(mainframe, width=30, textvariable=self.treasure)
        treasure_entry.grid(row=row_count, column=1, sticky=W)

        row_count += 1
        offense_frame = SectionBorder(mainframe, title="About")
        offense_frame.grid(row=row_count, column=0, columnspan=12)

        row_count += 1
        self.description_entry = Text(mainframe, wrap="word", width=90, height=1)
        self.description_entry.grid(row=row_count, column=1, columnspan=12, sticky=W)

        row_count += 1
        ttk.Button(mainframe, text='save', command=self.on_save).grid(row=0, column=0)
        ttk.Button(mainframe, text='export', command=self.on_export).grid(row=0, column=1)

        # root.columnconfigure(0, weight=1)
        # root.rowconfigure(0, weight=1)
        # mainframe.columnconfigure(2, weight=1)
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
            self.base_ac.set(getattr(self.creature, 'base_armor_class'))
            self.touch_ac.set(getattr(self.creature, 'touch_armor_class'))
            self.flat_footed_ac.set(getattr(self.creature, 'flat_footed_armor_class'))
            self.space.set(getattr(self.creature, 'space'))
            self.reach.set(getattr(self.creature, 'reach'))

            self.ac_modifier_entry.delete("1.0", END)
            self.ac_modifier_entry['height'] = len(self.creature.ac_modifiers)
            for ac_modifier in self.creature.ac_modifiers:
                self.ac_modifier_entry.insert(END, getattr(ac_modifier, 'modifier_amount') + " " + getattr(ac_modifier, 'modifier_type') + "\n")

            self.hit_points.set(getattr(self.creature, 'hit_points') + " (" + getattr(self.creature, 'hit_dice') + ")")
            self.fortitude.set(getattr(self.creature, 'fortitude'))
            self.reflex.set(getattr(self.creature, 'reflex'))
            self.will.set(getattr(self.creature, 'will'))
            self.will_modifier.set(getattr(self.creature, 'will_modifiers'))
            self.damage_reduction.set(getattr(self.creature, 'damage_reduction'))

            self.immune_entry.delete("1.0", END)
            self.immune_entry['height'] = len(self.creature.immune_modifiers)
            for immunity in self.creature.immune_modifiers:
                self.immune_entry.insert(END, getattr(immunity, 'immune_to') + "\n")

            self.defense_action_entry.delete("1.0", END)
            self.defense_action_entry['height'] = len(self.creature.immune_modifiers)
            for defense_action in self.creature.defensive_abilities:
                self.defense_action_entry.insert(END, getattr(defense_action, 'ability') + "\n")

            self.resist_entry.delete("1.0", END)
            self.resist_entry['height'] = len(self.creature.immune_modifiers)
            for resist in self.creature.sr_modifiers:
                self.resist_entry.insert(END, getattr(resist, 'resists') + " " + getattr(resist, 'resist_amount') + "\n")

            self.spell_resistence.set(getattr(self.creature, 'spell_resistence'))

            prefix = self.creature.spell_like_type if self.creature.spell_like_type else ""
            self.spell_like_label.set(prefix + " Spell Like Abilities")
            self.spell_like_caster_level.set(getattr(self.creature, 'spell_like_caster_level'))

            self.spell_like_abilities_entry.delete("1.0", END)
            self.spell_like_abilities_entry['height'] = len(self.creature.spell_like_abilities)
            for spell_like in self.creature.spell_like_abilities:
                if getattr(spell_like, 'modifiers'):
                    spell_modifiers = " (" + getattr(spell_like, 'modifiers') + ")"
                else:
                    spell_modifiers = ""
                self.spell_like_abilities_entry.insert(END, getattr(spell_like, 'rate') + " - " + getattr(spell_like, 'name') + spell_modifiers + "\n")

            prefix = self.creature.spell_known_type if self.creature.spell_known_type else ""
            self.known_spells_label.set(prefix + " Known Spells")
            self.known_caster_level.set(getattr(self.creature, 'spell_known_caster_level'))

            self.known_spells_entry.delete("1.0", END)
            self.known_spells_entry['height'] = len(self.creature.known_spells)
            for spell_like in self.creature.known_spells:
                if getattr(spell_like, 'modifiers'):
                    spell_modifiers = " (" + getattr(spell_like, 'modifiers') + ")"
                else:
                    spell_modifiers = ""
                self.known_spells_entry.insert(END, getattr(spell_like, 'spell_level') + " - " + getattr(spell_like, 'rate') + " - " + getattr(spell_like, 'name') + spell_modifiers + "\n")

            prefix = self.creature.spell_prepared_type if self.creature.spell_prepared_type else ""
            self.prepared_spells_label.set(prefix + " Prepared Spells")
            self.prepared_caster_level.set(getattr(self.creature, 'spell_prepared_caster_level'))

            self.prepared_spells_entry.delete("1.0", END)
            self.prepared_spells_entry['height'] = len(self.creature.prepared_spells)
            for prepared_spell in self.creature.prepared_spells:
                if getattr(prepared_spell, 'modifiers'):
                    spell_modifiers = " (" + getattr(prepared_spell, 'modifiers') + ")"
                else:
                    spell_modifiers = ""
                self.prepared_spells_entry.insert(END, getattr(prepared_spell, 'spell_level') + " - " + getattr(prepared_spell, 'name') + spell_modifiers + "\n")

            self.gear.set(getattr(self.creature, 'gear'))

            self.tactics_entry.delete("1.0", END)
            if self.creature.tactics:
                tactic_lines = self.creature.tactics.split("\n")
                for tactic_line in tactic_lines:
                    self.tactics_entry.insert(END, tactic_line + "\n")
                # self.tactics_entry['height'] = self.tactics_entry.count("1.0", END, "displaylines")[0]
                self.tactics_entry['height'] = 5

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
            self.environment.set(getattr(self.creature, 'environment'))
            self.organization.set(getattr(self.creature, 'organization'))
            self.treasure.set(getattr(self.creature, 'treasure'))

            self.weakness_entry.delete("1.0", END)
            self.weakness_entry['height'] = len(self.creature.weaknesses)
            for weakness in self.creature.weaknesses:
                self.weakness_entry.insert(END, getattr(weakness, 'weakness') + "\n")

            self.speed.set(getattr(self.creature, 'speed'))

            self.speed_modifiers_entry.delete("1.0", END)
            self.speed_modifiers_entry['height'] = len(self.creature.speed_modifiers)
            for speed_modifier in self.creature.speed_modifiers:
                self.speed_modifiers_entry.insert(END, getattr(speed_modifier, 'speed_modifier') + "\n")

            self.melee_entry.delete("1.0", END)
            self.melee_entry['height'] = len(self.creature.melee_attacks)
            for melee in self.creature.melee_attacks:
                self.melee_entry.insert(END, getattr(melee, 'attack') + "\n")

            self.ranged_entry.delete("1.0", END)
            self.ranged_entry['height'] = len(self.creature.ranged_attacks)
            for ranged in self.creature.ranged_attacks:
                self.ranged_entry.insert(END, getattr(ranged, 'attack') + "\n")

            self.special_attacks_entry.delete("1.0", END)
            self.special_attacks_entry['height'] = len(self.creature.special_attacks)
            for attack in self.creature.special_attacks:
                self.special_attacks_entry.insert(END, getattr(attack, 'attack') + "\n")

            self.language_entry.delete("1.0", END)
            self.language_entry['height'] = len(self.creature.languages)
            for language in self.creature.languages:
                self.language_entry.insert(END, getattr(language, 'language') + "\n")

            self.auras_entry.delete("1.0", END)
            self.auras_entry['height'] = len(self.creature.auras)
            for aura in self.creature.auras:
                self.auras_entry.insert(END, getattr(aura, 'aura') + " (" + getattr(aura, 'radius') + ", " + getattr(aura, 'save_role') + ")\n")

            self.special_qualities_entry.delete("1.0", END)
            self.special_qualities_entry['height'] = len(self.creature.special_qualities)
            for special_quality in self.creature.special_qualities:
                self.special_qualities_entry.insert(END, getattr(special_quality, 'special_quality') + "\n")

            self.special_abilities_entry.delete("1.0", END)
            self.special_abilities_entry['height'] = len(self.creature.special_abilities) * 3
            for special_ability in self.creature.special_abilities:
                self.special_abilities_entry.insert(END, getattr(special_ability, 'ability') + " " + getattr(special_ability, 'type') + "\n")
                self.special_abilities_entry.insert(END, getattr(special_ability, 'description') + "\n\n")


            self.special_gear_entry.delete("1.0", END)
            self.special_gear_entry['height'] = len(self.creature.gear_items) * 3
            for gear_item in self.creature.gear_items:
                self.special_gear_entry.insert(END, getattr(gear_item, 'name') + "\n")
                self.special_gear_entry.insert(END, getattr(gear_item, 'description') + "\n\n")

            self.senses_entry.delete("1.0", END)
            self.senses_entry['height'] = len(self.creature.senses)
            for sense in self.creature.senses:
                self.senses_entry.insert(END, getattr(sense, 'sense') + "\n")

            self.feats_entry.delete("1.0", END)
            self.feats_entry['height'] = len(self.creature.feats)
            for feat in self.creature.feats:
                self.feats_entry.insert(END, getattr(feat, 'feat') + "\n")

            self.skills_entry.delete("1.0", END)
            self.skills_entry['height'] = len(self.creature.skills)
            for skill in self.creature.skills:
                self.skills_entry.insert(END, getattr(skill, 'skill') + " " + getattr(skill, 'modifier') + "\n")

            self.description_entry.delete("1.0", END)
            if self.creature.description:
                description_lines = self.creature.description.split("\n")
                for description_line in description_lines:
                    self.description_entry.insert(END, description_line + "\n")
                # self.description_entry['height'] = self.description_entry.count("1.0", END, "displaylines")[0]
                self.description_entry['height'] = 5

            # print(self.creature)

        except ValueError:
            pass

    def on_save(self):
        db = SessionLocal()
        if not self.creature_id:
            db.add(self.creature)
        db.commit()
        db.refresh(self.creature)  # Refresh to get generated values (id, created_at)
        self.creature_id = self.creature.id

    def on_export(self):
        if self.creature.senses:
            senses_list = []
            for sense in self.creature.senses:
                senses_list.append(sense.sense)
            senses = ", ".join(senses_list) + "; Perception " + self.creature.perception_modifier
        else:
            senses = "Perception " + self.creature.perception_modifier

        if self.creature.auras:
            auras_list = []
            for aura in self.creature.auras:
                auras_list.append(aura.aura + " (" + aura.radius + ", " + aura.save_role + ")")
            auras = ", ".join(auras_list)
        else:
            auras = ""

        if self.creature.ac_modifiers:
            ac_mod_list = []
            for ac_mod in self.creature.ac_modifiers:
                ac_mod_list.append(ac_mod.modifier_amount + " " + ac_mod.modifier_type)
            ac_modifiers = " (" + ", ".join(ac_mod_list) + ")"
        else:
            ac_modifiers = ""

        if self.creature.immune_modifiers:
            immune_list = []
            for immune in self.creature.immune_modifiers:
                immune_list.append(immune.immune_to)
            immunity = ", ".join(immune_list)
        else:
            immunity = ""

        if self.creature.weaknesses:
            weakness_list = []
            for weakness in self.creature.weaknesses:
                weakness_list.append(weakness.weakness)
            weaknesses = ", ".join(weakness_list)
        else:
            weaknesses = ""

        if self.creature.defensive_abilities:
            defense_ability_list = []
            for defense_ability in self.creature.defensive_abilities:
                defense_ability_list.append(defense_ability.ability)
            defense_abilities = ", ".join(defense_ability_list)
        else:
            defense_abilities = ""

        if self.creature.sr_modifiers:
            resistance_list = []
            for resist in self.creature.sr_modifiers:
                resistance_list.append(resist.resists + " " + resist.resist_amount)
            resistance = ", ".join(resistance_list)
        else:
            resistance = ""

        if self.creature.languages:
            languages_list = []
            for language in self.creature.languages:
                languages_list.append(language.language)
            languages = ", ".join(languages_list)
        else:
            languages = ""

        if self.creature.skills:
            skill_list = []
            for skill in self.creature.skills:
                skill_list.append(skill.skill + " " + skill.modifier)
            skills = ", ".join(skill_list)
        else:
            skills = ""

        if self.creature.speed:
            speed_list = [self.creature.speed]
            for speed in self.creature.speed_modifiers:
                speed_list.append(speed.speed_modifier )
            speeds = ", ".join(speed_list)
        else:
            speeds = ""

        if self.creature.feats:
            feat_list = []
            for feat in self.creature.feats:
                feat_list.append(feat.feat)
            feats = ", ".join(feat_list)
        else:
            feats = ""

        if self.creature.melee_attacks:
            melee_list = []
            for melee in self.creature.melee_attacks:
                melee_list.append(melee.attack)
            melees = ", ".join(melee_list)
        else:
            melees = ""

        if self.creature.ranged_attacks:
            ranged_list = []
            for range in self.creature.ranged_attacks:
                ranged_list.append(range.attack)
            ranged = ", ".join(ranged_list)
        else:
            ranged = ""

        if self.creature.special_attacks:
            special_attack_list = []
            for special_attack in self.creature.special_attacks:
                special_attack_list.append(special_attack.attack)
            special_attacks = ", ".join(special_attack_list)
        else:
            special_attacks = ""

        if self.creature.spell_like_abilities:
            spell_dictionary = {}
            spell_list = [self.creature.spell_like_caster_level]
            for spell in self.creature.spell_like_abilities:
                key = spell.rate + "— "
                value = spell.name
                value += (" (" + spell.modifiers + ")") if spell.modifiers else ""
                if key in spell_dictionary:
                    spell_dictionary[key].append(value)
                else:
                    spell_dictionary[key] = [value]
            for rate, spells in spell_dictionary.items():
                spell_list.append(rate + ", ".join(spells))

            spell_like_abilities = "{#ENTER}".join(spell_list)
        else:
            spell_like_abilities = ""

        if self.creature.known_spells:
            spell_dictionary = {}
            spell_list = [self.creature.spell_known_caster_level]
            for spell in self.creature.known_spells:
                key = spell.spell_level + " " + spell.rate + "— "
                value = spell.name
                value += (" (" + spell.modifiers + ")") if spell.modifiers else ""
                if key in spell_dictionary:
                    spell_dictionary[key].append(value)
                else:
                    spell_dictionary[key] = [value]
            for rate, spells in spell_dictionary.items():
                spell_list.append(rate + ", ".join(spells))

            known_spells = "{#ENTER}".join(spell_list)

        else:
            known_spells = ""

        if self.creature.description:
            description = re.sub(r"\n", " ", self.creature.description)
        else:
            description = ""

        if self.creature.special_qualities:
            special_quality_list = []
            for special_quality in self.creature.special_qualities:
                special_quality_list.append(special_quality.special_quality)
            special_qualities = ", ".join(special_quality_list)
        else:
            special_qualities = ""

        if self.creature.prepared_spells:
            spell_dictionary = {}
            spell_list = [self.creature.spell_prepared_caster_level]
            for spell in self.creature.prepared_spells:
                key = spell.spell_level + "— "
                value = spell.name
                value += (" (" + spell.modifiers + ")") if spell.modifiers else ""
                if key in spell_dictionary:
                    spell_dictionary[key].append(value)
                else:
                    spell_dictionary[key] = [value]
            for rate, spells in spell_dictionary.items():
                spell_list.append(rate + ", ".join(spells))

            prepared_spells = "{#ENTER}".join(spell_list)
        else:
            prepared_spells = ""

        creature_type = self.creature.type
        creature_type += (" (" + self.creature.sub_type + ")") if self.creature.sub_type else ""

        special_abilities_and_content = ""
        if self.creature.special_abilities:
            special_abilities_list = ["Special Abilities"]
            for ability in self.creature.special_abilities:
                special_abilities_list.append(ability.ability + " (" + ability.type + ") " + ability.description)
            special_abilities_and_content = "{#ENTER}".join(special_abilities_list)
            special_abilities_and_content += "{#ENTER}" + description
        else:
            special_abilities_and_content += description

        creature_class = ""
        if self.creature.race:
            creature_class = self.creature.race + " "
            if self.creature.char_class:
                creature_class += self.creature.char_class
        elif self.creature.char_class:
            creature_class = self.creature.char_class
        if self.creature.level:
            creature_class += " " + self.creature.level

        output_fields = [
            self.creature.common_name,
            "CR " + self.creature.challenge_rating,
            self.creature.experience_points,
            self.creature.alignment,
            self.creature.size,
            creature_type,
            creature_class,
            safe_copy(self.creature.alignment) + " " + safe_copy(self.creature.size) + " " + safe_copy(creature_type) + " " + safe_copy(self.creature.initiative),
            senses,
            auras,
            safe_copy(self.creature.base_armor_class) + ", touch " + safe_copy(self.creature.touch_armor_class) + ", flat-footed " + safe_copy(self.creature.flat_footed_armor_class) + ac_modifiers,
            self.creature.hit_points + " (" + self.creature.hit_dice + ")",
            safe_copy(self.creature.fortitude),
            safe_copy(self.creature.reflex),
            safe_copy(self.creature.will),
            safe_copy(self.creature.damage_reduction),
            safe_copy(self.creature.spell_resistence),
            immunity,
            resistance,
            weaknesses,
            defense_abilities,
            speeds,
            safe_copy(self.creature.space),
            safe_copy(self.creature.reach),
            melees,
            ranged,
            special_attacks,
            spell_like_abilities,
            known_spells,
            prepared_spells,
            self.creature.strength,
            self.creature.dexterity,
            self.creature.constitution,
            self.creature.intelligence,
            self.creature.wisdom,
            self.creature.charisma,
            safe_copy( self.creature.base_attack),
            safe_copy( self.creature.combat_maneuver_bonus),
            safe_copy(self.creature.combat_maneuver_defense),
            feats,
            skills,
            safe_copy(self.creature.racial_modifiers),
            languages,
            special_qualities,
            safe_copy(self.creature.environment),
            safe_copy(self.creature.organization),
            safe_copy(self.creature.gear),
            special_abilities_and_content
        ]

        print("{#TAB}".join(output_fields))

        try:
            file_path = "output/" + self.creature.common_name + '.txt'
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("{#TAB}".join(output_fields)+"\n")
            print(f"File '{file_path}' written successfully in write mode.")
        except IOError as e:
            print(f"Error writing to file: {e}")

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
        self.newWindow = None

        root.title("Creature List")

        mainframe = ttk.Frame(root, padding=3, borderwidth=2, relief='raised')
        mainframe.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
        self.creature_choices_var = StringVar()
        self.creature_list = Listbox(mainframe, height=10, width=60, listvariable=self.creature_choices_var)
        self.creature_list.grid(row=0, column=0, columnspan=2, sticky="nsew")

        load_button = ttk.Button(mainframe, text="load", command=self.show_creature)
        load_button.grid(row=1, column=0, sticky="w")
        new_button = ttk.Button(mainframe, text="New")
        new_button.grid(row=1, column=2, sticky="e")

        self.creature_list.bind('<Double-Button-1>', lambda: self.show_creature)

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
            self.newWindow = Toplevel(self.root)
            creature_form = CreatureForm(self.newWindow)
            creature_form.on_load(self.creature)
        else:
            print("No item selected")



