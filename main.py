"""
CreatureStatBlockParser – version 1.00
Robust Pathfinder stat-block parser.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
from pathlib import Path
import platform
from Forms.CreatureForm import CreatureForm
from Forms.CreatureList import CreatureList
from Widgets.AboutBox import AboutBox
from Parsers.CreatureParser import ParseCreature
from Database.database import DATABASE_VERSION, Database
from Database.create_tables import initialize_repository

APPLICATION_VERSION = '1.0.0'

def initialize_database():
    if messagebox.askyesno("Initialize Database", message="Do you really want to initialize the database?",
                           detail="This will remove all information currently in the database", icon='question',):
        initialize_repository(True)
        messagebox.showinfo("Database", "Database Initialized")


class CreatureBarn(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.newWindow = None
        self.app = None
        customtkinter.set_default_color_theme("dark-blue")
        if "Linux" == platform.system():
            customtkinter.set_widget_scaling(2.0)  # widget dimensions and text size
            customtkinter.set_window_scaling(2.0)  # window geometry dimensions

        self.title("Creature Stat Block Parser")
        self.text = tk.Text(self, wrap="word", width=120, height=45)
        self.text.pack(expand=True, fill="both")

        self.menu = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Open and Parse", command=self.load)
        self.file_menu.add_command(label="Parse", command=self.parse_screen)
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.database_menu = tk.Menu(self.menu, tearoff=0)
        self.database_menu.add_command(label="Manage Spells", state="disabled")
        self.database_menu.add_command(label="Manage Creatures", command=self.show_creature_list)
        self.database_menu.add_command(label="Manage NPCs", command=self.show_npc_list)
        self.database_menu.add_separator()
        self.database_menu.add_command(label="Initialize Database", command=initialize_database, state="disabled")
        self.menu.add_cascade(label="Database", menu=self.database_menu)

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about_dialog)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menu)
        self.database = Database()

        # Ensure the database is valid and the structure is up to date
        # Ensure the database is valid and the structure is up to date
        if not self.database.is_database_valid():
            self.database_menu.entryconfig("Initialize Database", state="normal")
        else:
            self.database.verify_database_version()

    # Function to display the "About" dialog box
    def show_about_dialog(self):
        about = AboutBox(self, 'About', APPLICATION_VERSION, DATABASE_VERSION)

    def show_creature_list(self):
        self.app = CreatureList(self, "Creature")

    def show_npc_list(self):
        self.app = CreatureList(self, "NPC")

    def show_parsed_creature(self, creature):
        self.app = CreatureForm(self)
        self.app.on_load(creature)

    def load(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        raw = Path(path).read_text(encoding="utf-8")
        parser = ParseCreature(raw)
        parser.run()

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, raw)
        self.show_parsed_creature(parser.creature)

    def parse_screen(self):
        text = self.text.get("1.0", tk.END)
        if len(text) > 5:
            parser = ParseCreature(text)
            parser.run()
            self.show_parsed_creature(parser.creature)
        else:
            messagebox.showwarning("No Data", "No text to parse!")


if __name__ == "__main__":
    app = CreatureBarn()
    app.mainloop()
