import tkinter as tk
from tkinter import ttk
from Application.Options import APPLICATION_VERSION
from Database.database import DATABASE_VERSION

class AboutBox:
    def __init__(self, parent):
        self.parent = parent

        # Create the Toplevel window
        about_box = tk.Toplevel(self.parent)
        about_box.title("About")

        # Specify the width and height (e.g., 300x200 pixels)
        about_box.geometry("450x360")

        # Make the window non-resizable
        about_box.resizable(False, False)

        # Center the dialog over the parent window (optional, but good practice)
        about_box.transient(self.parent)  # Makes the dialog box a transient window of the parent window
        about_box.grab_set()  # Makes the dialog modal (forces user interaction)

        # Add content (e.g., Labels, Buttons)
        # Use a Message widget for multi-line text that wraps properly
        message_text = "This is a simple creature barn to manage creature and NPC definitions.\n\nVersion {}, Database {}".format(
            APPLICATION_VERSION, DATABASE_VERSION)
        about_message = tk.Message(about_box, text=message_text, justify=tk.CENTER,
                                   width=400)  # width in character units
        about_message.pack(pady=20, padx=10)

        # Add an OK button to close the dialog
        ok_button = ttk.Button(about_box, text="OK", command=about_box.destroy)
        ok_button.pack(pady=10)
