"""
CreatureStatBlockParser – version 1.00
Robust Pathfinder stat-block parser.
"""
import argparse
import glob
from pathlib import Path
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

APPLICATION_VERSION = '1.1.0'

def initialize_database():
    if messagebox.askyesno("Initialize Database", message="Do you really want to initialize the database?",
                           detail="This will remove all information currently in the database", icon='question',):
        initialize_repository(True)
        messagebox.showinfo("Database", "Database Initialized")


class CreatureBarn(customtkinter.CTk):
    def __init__(self, my_args, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = my_args
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
        self.file_menu.add_command(label="Open and Parse", command=self.load_and_parse)
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

        if self.args.batch:
            self.process_batch()

    # Function to display the "About" dialog box
    def show_about_dialog(self):
        AboutBox(self, 'About Creature Barn', APPLICATION_VERSION, DATABASE_VERSION)

    def show_creature_list(self):
        self.app = CreatureList(self, "Creature")

    def show_npc_list(self):
        self.app = CreatureList(self, "NPC")

    def show_parsed_creature(self, creature):
        self.app = CreatureForm(self)
        self.app.on_load(creature)

    def load_and_parse(self):
        file_list = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")], initialdir="./samples")
        if not file_list:
            return
        if len(file_list) == 1:
            raw = Path(file_list[0]).read_text(encoding="utf-8")
            parser = ParseCreature(raw)
            parser.run()

            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, raw)
            self.show_parsed_creature(parser.creature)
        else:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, "Processing selected files:\n")
            for file in file_list:
                self.parse_and_export_file(file)

    def parse_screen(self):
        text = self.text.get("1.0", tk.END)
        if len(text) > 5:
            parser = ParseCreature(text)
            parser.run()
            self.show_parsed_creature(parser.creature)
        else:
            messagebox.showwarning("No Data", "No text to parse!")

    def process_batch(self):
        self.text.insert(tk.END, "Processing files in {}\n".format(self.args.path))
        for file_path in sorted(glob.glob("{}/*.txt".format(self.args.path))):
            self.parse_and_export_file(file_path)

    def parse_and_export_file(self, file):
        self.text.insert(tk.END, "{}\n".format(file))
        raw = Path(file).read_text(encoding="utf-8")
        parser = ParseCreature(raw)
        parser.run()
        # parser.creature.barn_type = "NPC"
        # self.show_parsed_creature(parser.creature)
        # self.app.on_export()
        # self.app.destroy()
        # self.app = None


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simple Creature and NPC Stat Parser and Storage"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version {APPLICATION_VERSION}"
    )
    parser.add_argument(
        "-p", "--path", default='./source', type=str,
        help="Directory to batch process, defaults to ./source"
    )
    parser.add_argument(
        "-b", "--batch", action='store_true',
        help="Batch process all files in path"
    )
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    app = CreatureBarn(args)
    app.mainloop()

if __name__ == "__main__":
    main()
