import tkinter as tk
from tkinter import ttk


class SectionBorder(ttk.Frame):
    def __init__(self, container, title, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.label = ttk.Label(self, text=title)
        self.label.configure(font=('Helvetica', 16, 'bold'))
        self.label.grid(row=0, column=0)
