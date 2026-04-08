import customtkinter

class AboutBox(customtkinter.CTkToplevel):
    def __init__(self, master, title, app_version, db_version):
        super().__init__(master)
        # Create the Toplevel window
        self.title(title)

        # Specify the width and height (e.g., 300x200 pixels)
        self.geometry("400x250")

        # Make the window non-resizable
        self.resizable(False, False)

        # Center the dialog over the parent window (optional, but good practice)
        self.transient(master) # Makes the dialog box a transient window of the root window
        self.grab_set()     # Makes the dialog modal (forces user interaction)

        # Add content (e.g., Labels, Buttons)
        message_text = "This is a simple creature barn to manage creature and NPC definitions.\n\nVersion {}, Database {}".format(app_version, db_version)
        about_message = customtkinter.CTkLabel(self, text=message_text, justify="center", wraplength=300, width=300)  # width in character units
        about_message.pack(pady=20, padx=10)

        # Add an OK button to close the dialog
        ok_button = customtkinter.CTkButton(self, text="OK", command=self.destroy)
        ok_button.pack(pady=10)
