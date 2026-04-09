from tkinter import *
import customtkinter
import re

from Database.database import my_db
from Database.models import Creature
from Forms.CreatureForm import CreatureForm


class CreatureList(customtkinter.CTkToplevel):

    def __init__(self, master, barn_type='Creature'):
        super().__init__(master)
        self.creature = None
        self.creature_id = 0
        self.newWindow = None

        self.title(barn_type + " List")

        mainframe = customtkinter.CTkFrame(self, border_width=2)
        mainframe.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
        self.creature_choices_var = StringVar()
        self.creature_list = Listbox(mainframe, height=10, width=70, listvariable=self.creature_choices_var)
        self.creature_list.grid(row=0, column=0, columnspan=2, sticky="nsew")

        load_button = customtkinter.CTkButton(mainframe, text="load", command=self.show_creature)
        load_button.grid(row=1, column=0, sticky="w")
        new_button = customtkinter.CTkButton(mainframe, text="New")
        new_button.grid(row=1, column=1, sticky="e")

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.creature_list.bind('<Double-Button-1>', self.show_creature_binding)

        try:
            creatures = my_db.query(Creature).order_by(Creature.formal_name).where(Creature.barn_type == barn_type)
            creature_choices = []
            for creature in creatures:
                creature_choices.append("{} CR {}".format(creature.formal_name, creature.challenge_rating))

            self.creature_choices_var.set(creature_choices)

        except ValueError:
            pass

    def show_creature_binding(self,event):
        self.show_creature()

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
            real_name = re.match(r'(.+) CR .*', formal_name)
            true_name = real_name.group(1)
            self.creature = my_db.query(Creature).filter(Creature.formal_name == true_name).first()
            print(self.creature)
            self.creature_id = self.creature.id
            creature_form = CreatureForm(self)
            creature_form.on_load(self.creature)
        else:
            print("No item selected")

