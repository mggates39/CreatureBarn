"""
CreatureStatBlockParser – version 1.00
Robust Pathfinder stat-block parser.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from Forms.creatures import CreatureForm, CreatureList
from Parsers.CreatureParser import ParseCreature
from Database.create_tables import create_tables, drop_tables


def initialize_database():
    if messagebox.askyesno("Confirm Database Init", message="Do you really want to initialize the database?",
                           detail="This will remove all information currently in the database", icon='question',):
        drop_tables()
        create_tables()
        messagebox.showinfo("Database", "Database Initialized")


class CreatureBarn:
    def __init__(self, root):
        self.root = root
        self.newWindow = None
        self.app = None
        self.root.title("Creature Stat Block Parser")
        self.text = tk.Text(root, wrap="word", width=120, height=45)
        self.text.pack(expand=True, fill="both")

        menu = tk.Menu(root)
        fm = tk.Menu(menu, tearoff=0)
        fm.add_command(label="Open and Parse", command=self.load)
        fm.add_command(label="Parse", command=self.parse_screen)
        fm.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=fm)

        dbm = tk.Menu(menu, tearoff=0)
        dbm.add_command(label="Manage Spells")
        dbm.add_command(label="Manage Creatures", command=self.show_creature_list)
        dbm.add_command(label="Manage NPCs")
        dbm.add_separator()
        dbm.add_command(label="Init Database", command=initialize_database)
        menu.add_cascade(label="Database", menu=dbm)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        menu.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menu)

    # Function to display the "About" dialog box
    def show_about_dialog(self):
        """Creates and displays a custom about dialog with specified dimensions."""

        # Create the Toplevel window
        about_box = tk.Toplevel(self.root)
        about_box.title("About Creature Barn")

        # Specify the width and height (e.g., 300x200 pixels)
        about_box.geometry("500x360")

        # Make the window non-resizable
        about_box.resizable(False, False)

        # Center the dialog over the parent window (optional, but good practice)
        about_box.transient(self.root) # Makes the dialog box a transient window of the root window
        about_box.grab_set()     # Makes the dialog modal (forces user interaction)

        # Add content (e.g., Labels, Buttons)
        # Use a Message widget for multi-line text that wraps properly
        message_text = "This is simple creature barn to manage creature and NPC definitions.\n\nVersion 1.0"
        about_message = tk.Message(about_box, text=message_text, justify=tk.CENTER,
                                   width=400)  # width in character units
        about_message.pack(pady=20, padx=10)

        # Add an OK button to close the dialog
        ok_button = tk.Button(about_box, text="OK", command=about_box.destroy)
        ok_button.pack(pady=10)

    def show_creature_list(self):
        self.newWindow = tk.Toplevel(self.root)
        self.app = CreatureList(self.newWindow)

    def show_parsed_creature(self, creature):
        self.newWindow = tk.Toplevel(self.root)
        self.app = CreatureForm(self.newWindow)
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
    rootWidget = tk.Tk()
    app = CreatureBarn(rootWidget)
    rootWidget.mainloop()
