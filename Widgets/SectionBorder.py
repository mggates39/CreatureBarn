import customtkinter


class SectionBorder(customtkinter.CTkFrame):
    def __init__(self, container, title, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text=title)
        self.label.configure(font=('Helvetica', 16, 'bold'))
        self.label.grid(row=0, column=0, sticky='ew')
