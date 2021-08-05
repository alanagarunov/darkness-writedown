import tkinter as tk
import darkness.dark_functions as dark_fns

def create_deck_button_window(self):
        self.deckcreate = tk.Toplevel(self)
        self.deckcreate.geometry("350x100")
        self.deckcreate.title("Create Deck")
        
        self.name = tk.Entry(self.deckcreate)
        self.name.pack(side="top")

        self.add_button = tk.Button(self.deckcreate, text="Add", command=lambda: create_deck_button_add(self, self.name.get()))
        self.add_button.pack(side="top")

def create_deck_button_add(self, name):
        dark_fns.create_deck(name)
        tk.Label(self.deckcreate, text="Deck Added").pack()