import tkinter as tk
import darkness.dark_functions as dark_fns

def create_card_button_window(self):
        #you dont need to put self on literally everything but if you dont that label wont work.
        self.createdialog = tk.Toplevel(self)
        self.createdialog.geometry("350x100")
        self.createdialog.title("Create Card")
        self.clicked = tk.StringVar(self.createdialog)
        self.clicked.set("Select a Deck")
        self.dropdown = tk.OptionMenu(self.createdialog, self.clicked, *dark_fns.get_list_of_decks())
        self.dropdown.pack(side="top")

        self.frontside = tk.Entry(self.createdialog)
        self.frontside.pack(side="top")

        self.backside = tk.Entry(self.createdialog)
        self.backside.pack(side="top")

        self.add_button = tk.Button(self.createdialog, text="Add", command=lambda: self.create_card_button_add(self.clicked.get(), self.frontside.get(), self.backside.get()))
        self.add_button.pack(side="top")

def create_card_button_add(self, deck_name, frontside, backside):
        dark_fns.create_card(deck_name, frontside, backside)
        tk.Label(self.createdialog, text="Card Added").pack()