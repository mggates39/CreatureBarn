from tkinter import *
from tkinter import ttk
from widgets.PairTupleCombobox import PairTupleCombobox
from database import SessionLocal
from models import Creature

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
        formal_name_entry.grid(row=1, column=1, columnspan=4, sticky=W)

        ttk.Label(mainframe, text="Common Name").grid(row=2, column=0, sticky=W)
        self.common_name = StringVar()
        common_name_entry = ttk.Entry(mainframe, width=50, textvariable=self.common_name)
        common_name_entry.grid(row=2, column=1, columnspan=4, sticky=W)

        ttk.Label(mainframe, text="CR").grid(row=2, column=5, sticky=W)
        self.challenge_rating = StringVar()
        challenge_rating_entry = ttk.Entry(mainframe, width=6, textvariable=self.challenge_rating)
        challenge_rating_entry.grid(row=2, column=6, sticky=W)

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
        spell_resistence_entry.grid(row=7, column=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(row=20, column=0, sticky=W)
        ttk.Label(mainframe, text="feet").grid(row=21, column=0, sticky=W)
        ttk.Label(mainframe, text="feet").grid(row=22, column=0, sticky=W)
        ttk.Label(mainframe, text="feet").grid(row=23, column=0, sticky=W)
        ttk.Label(mainframe, text="feet").grid(row=24, column=0, sticky=W)
        ttk.Label(mainframe, text="feet").grid(row=25, column=0, sticky=W)
        ttk.Label(mainframe, text="feet").grid(row=26, column=0, sticky=W)

        ttk.Button(mainframe, text='load', command=lambda: self.on_load(2)).grid(row=27, column=0, sticky=W)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def on_load(self, creature_id):
        try:
            db = SessionLocal()
            self.creature_id = creature_id
            self.creature = db.query(Creature).filter(Creature.id == creature_id).first()
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
            self.challenge_rating.set(getattr(self.creature, 'level'))
            self.initiative.set(getattr(self.creature, 'initiative'))
            self.challenge_rating.set(getattr(self.creature, 'perception_modifier'))

        except ValueError:
            pass
