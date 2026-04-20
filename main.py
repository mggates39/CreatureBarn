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
from Parsers.CreatureParser import ParseCreature
from Database.database import DATABASE_VERSION, Database
from Database.create_tables import initialize_repository

APPLICATION_VERSION = '1.1.0'

def initialize_database():
    if messagebox.askyesno("Initialize Database", message="Do you really want to initialize the database?",
                           detail="This will remove all information currently in the database", icon='question',):
        initialize_repository(True)
        messagebox.showinfo("Database", "Database Initialized")


class CreatureBarn:
    def __init__(self, root, args):
        self.args = args
        self.root = root
        self.newWindow = None
        self.app = None
        self.root.title("Creature Stat Block Parser")
        self.text = tk.Text(root, wrap="word", width=120, height=45)
        self.text.pack(expand=True, fill="both")

        self.menu = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Open and Parse", command=self.load)
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

        if args.batch:
            self.process_batch()
            self.root.destroy()

    # Function to display the "About" dialog box
    def show_about_dialog(self):
        """Creates and displays a custom about dialog with specified dimensions."""

        # Create the Toplevel window
        about_box = tk.Toplevel(self.root)
        about_box.title("About")

        # Specify the width and height (e.g., 300x200 pixels)
        about_box.geometry("450x360")

        # Make the window non-resizable
        about_box.resizable(False, False)

        # Center the dialog over the parent window (optional, but good practice)
        about_box.transient(self.root) # Makes the dialog box a transient window of the root window
        about_box.grab_set()     # Makes the dialog modal (forces user interaction)

        # Add content (e.g., Labels, Buttons)
        # Use a Message widget for multi-line text that wraps properly
        message_text = "This is a simple creature barn to manage creature and NPC definitions.\n\nVersion {}, Database {}".format(APPLICATION_VERSION, DATABASE_VERSION)
        about_message = tk.Message(about_box, text=message_text, justify=tk.CENTER,
                                   width=400)  # width in character units
        about_message.pack(pady=20, padx=10)

        # Add an OK button to close the dialog
        ok_button = ttk.Button(about_box, text="OK", command=about_box.destroy)
        ok_button.pack(pady=10)

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

    def load(self):
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
                self.parse_and_export_file(file, True)

    def parse_screen(self):
        text = self.text.get("1.0", tk.END)
        if len(text) > 5:
            parser = ParseCreature(text)
            parser.run()
            self.show_parsed_creature(parser.creature)
        else:
            messagebox.showwarning("No Data", "No text to parse!")

    def process_batch(self):
        print( "Processing files in {}".format(self.args.path))
        for file in Path(self.args.path).glob("*.txt"):
            self.parse_and_export_file(file, False)

    def parse_and_export_file(self, file, log_to_screen=False):
        if log_to_screen:
            self.text.insert(tk.END, file + "\n")
        else:
            print(file)

        raw = Path(file).read_text(encoding="utf-8")
        parser = ParseCreature(raw)
        parser.run()
        parser.creature.barn_type = "NPC"
        self.show_parsed_creature(parser.creature)
        self.app.on_export()
        self.app.root.destroy()
        self.app = None


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
    root_widget = ThemedTk(theme='winxpblue')
    app = CreatureBarn(root_widget, args)
    root_widget.mainloop()

if __name__ == "__main__":
    main()
