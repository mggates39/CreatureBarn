"""
CreatureStatBlockParser – version 1.00
Robust Pathfinder stat-block parser.
"""
import argparse
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from pathlib import Path
from ttkthemes import ThemedTk
from Forms.creatures import CreatureForm, CreatureList
from Forms.AboutBox import AboutBox
from Parsers.CreatureParser import CreatureTextParser
from Parsers.JsonParser import CreatureJsonParser
from Parsers.XmlParser import CreatureXmlParser
from Database.database import DATABASE_VERSION, Database
from Database.create_tables import initialize_repository
from Application.Options import APPLICATION_VERSION, SystemOptions

def initialize_database():
    if messagebox.askyesno("Initialize Database", message="Do you really want to initialize the database?",
                           detail="This will remove all information currently in the database", icon='question',):
        initialize_repository(True)
        messagebox.showinfo("Database", "Database Initialized")


class CreatureBarn:
    def __init__(self, root, options):
        self.options = options
        self.root = root
        self.newWindow = None
        self.app = None
        if self.options.is_hero():
            self.root.title("Creature Hero Lab Stat Block Parser")
        else:
            self.root.title("Creature R20 Stat Block Parser")
        self.text = tk.Text(root, wrap="word", width=120, height=45)
        self.text.pack(expand=True, fill="both")

        self.menu = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Open and Parse", command=self.load)
        self.file_menu.add_command(label="Open and Parse JSON", command=self.load_json)
        self.file_menu.add_command(label="Open and Parse XML", command=self.load_xml)
        self.file_menu.add_command(label="Parse", command=self.parse_screen)
        self.file_menu.add_command(label="Exit", command=root.quit)
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

        root.config(menu=self.menu)
        self.database = Database()

        # Ensure the database is valid and the structure is up to date
        # Ensure the database is valid and the structure is up to date
        if not self.database.is_database_valid():
            self.database_menu.entryconfig("Initialize Database", state="normal")
        else:
            self.database.verify_database_version()

        if self.options.is_batch():
            self.process_batch()
            self.root.destroy()
        elif self.options.has_file():
            self.process_single_file()
            self.root.destroy()

    # Function to display the "About" dialog box
    def show_about_dialog(self):
        """Creates and displays a custom about dialog with specified dimensions."""
        about_box = AboutBox(self.root)

    def show_creature_list(self):
        self.newWindow = tk.Toplevel(self.root)
        self.app = CreatureList(self.newWindow, "Creature")

    def show_npc_list(self):
        self.newWindow = tk.Toplevel(self.root)
        self.app = CreatureList(self.newWindow, "NPC")

    def show_parsed_creature(self, creature):
        self.newWindow = tk.Toplevel(self.root)
        self.app = CreatureForm(self.newWindow)
        self.app.on_load(creature)

    def load_json(self):
        file_list = filedialog.askopenfilenames(filetypes=[("JSON Files", "*.json")], initialdir="./samples")
        if not file_list:
            return
        if len(file_list) == 1:
            raw = Path(file_list[0]).read_text(encoding="utf-8")
            parser = CreatureJsonParser(raw, self.options)
            parser.run()

            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, raw)
            self.show_parsed_creature(parser.creature)

    def load_xml(self):
        file_list = filedialog.askopenfilenames(filetypes=[("XML Files", "*.xml")], initialdir="./samples")
        if not file_list:
            return
        if len(file_list) == 1:
            raw = Path(file_list[0]).read_text(encoding="utf-8")
            parser = CreatureXmlParser(raw, self.options)
            parser.run()

            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, raw)
            self.show_parsed_creature(parser.creature)

    def load(self):
        file_list = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")], initialdir="./samples")
        if not file_list:
            return
        if len(file_list) == 1:
            raw = Path(file_list[0]).read_text(encoding="utf-8")
            parser = CreatureTextParser(raw, self.options.is_hero())
            parser.run()

            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, raw)
            self.show_parsed_creature(parser.creature)
        else:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, "Processing selected files:\n")
            for file in file_list:
                self.parse_and_process_file(file, True)

    def parse_screen(self):
        text = self.text.get("1.0", tk.END)
        if len(text) > 5:
            parser = CreatureTextParser(text, self.options.is_hero())
            parser.run()
            self.show_parsed_creature(parser.creature)
        else:
            messagebox.showwarning("No Data", "No text to parse!")

    def process_batch(self):
        print( "Processing files in {}".format(self.options.get_path()))
        for file in Path(self.options.get_path()).glob("*.txt"):
            self.parse_and_process_file(file, False)

    def process_single_file(self):
        print("Processing file {}".format(self.options.get_file()))
        self.parse_and_process_file(self.options.get_file(), False)

    def parse_and_process_file(self, file, log_to_screen=False):
        if log_to_screen:
            self.text.insert(tk.END, file + "\n")
        else:
            print(file)

        raw = Path(file).read_text(encoding="utf-8")
        creature_parser = CreatureTextParser(raw, self.options.is_Hero())
        creature_parser.run()
        creature_parser.creature.barn_type = self.options.get_type()
        self.show_parsed_creature(creature_parser.creature)

        if self.options.do_export():
            self.app.on_export()

        if self.options.is_save():
            self.app.on_save()

        self.app.root.destroy()
        self.app = None


def init_argparse() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser(
        description="Simple Creature and NPC Stat Parser and Storage System"
    )
    arg_parser.add_argument(
        "-v", "--version", action="version",
        version = f"{arg_parser.prog} version {APPLICATION_VERSION} Database {DATABASE_VERSION}"
    )
    arg_parser.add_argument(
        "-p", "--path", default='./source', type=str,
        help="Directory to batch process, defaults to ./source"
    )
    arg_parser.add_argument(
        "-b", "--batch", action='store_true',
        help="Batch process all files in path"
    )
    arg_parser.add_argument(
        "-i", "--input",  choices=['R20', 'Hero', 'XML', 'JSON'],  default='R20',
        help="Input file format, default R20"
    )
    arg_parser.add_argument(
        "-o", "--output",  choices=['V1', 'V2'], default='V2',
        help="Output format R20 V1 or V2, default V2"
    )
    arg_parser.add_argument(
        "-f", "--file", type=str,
        help="file to process"
    )
    arg_parser.add_argument(
        "-t", "--type", choices=['NPC', 'Creature'], default='NPC',
        help="Type of the file or files in the path, default is NPC"
    )
    arg_parser.add_argument(
        "-a", "--action", choices=['export', 'save', 'both'], default='export',
        help="Action to perform on the batch or file, defaults to export"
    )
    return arg_parser


def main() -> None:
    arg_parser = init_argparse()
    args = arg_parser.parse_args()
    root_widget = ThemedTk(theme='Black')
    options = SystemOptions()
    options.load_from_args(args)
    app = CreatureBarn(root_widget, options)
    root_widget.mainloop()

if __name__ == "__main__":
    main()
