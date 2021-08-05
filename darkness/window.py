import tkinter as tk
from functools import partial
import darkness.dark_functions as dark_fns
import darkness.create_card_func as dark_card
import darkness.create_deck_func as dark_deck
import darkness.review_func as dark_review
import darkness.settings_func as dark_settings
import darkness.find_func as dark_find

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        #self.create_widgets()


        
        self.load_display_decks()
        tk.Button(self, text="Create Card", command=partial(dark_card.create_card_button_window, self)).grid(column=2, row=0)
        tk.Button(self, text="Create Deck", command=partial(dark_deck.create_deck_button_window, self)).grid(column=2, row=1)
        tk.Button(self, text="Find/Edit/Delete Cards", command=partial(dark_find.find_window, self)).grid(column=2, row=2)
        tk.Button(self, text="Settings", command=partial(dark_settings.settings_window, self)).grid(column=2, row=3)
        

    def create_widgets(self):
        self.test = tk.Button(self)
        self.test["text"] = "Hello World\n(click me)"
        self.test["command"] = self.say_hi
        self.test.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")


    def say_hi(self):
        print("Hello World")

    def load_display_decks(self):
        testframe = tk.Frame(self)
        listbox = tk.Listbox(testframe)
        scrollbar = tk.Scrollbar(testframe, orient="vertical")

        decks = dark_fns.get_list_of_decks()
        tk.Label(self, text="List of All Decks:\tTotal Items\tFor Review").grid(column=0)

        for i in decks:
            num = dark_fns.get_card_id(i)
            num1 = dark_fns.determine_review(i)
            listbox.insert(tk.END, i + "    " + str(num) + "    " + str(len(num1)*2))

        listbox.bind("<Double-1>", partial(dark_review.review_window, self))
        listbox.pack(side="left")
        
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)
        scrollbar.pack(side="right", fill="y")
        testframe.grid(column=0)

#in order of easiest   
#               |
#              \ /
#            hardest    
#TODO: DONE[make it populate a list of decks], DONE[add deck] and DONE[card button], make it look not like crap.
#TODO: delete deck button
#TODO: [kinda already does it?]check review then [DONE]make the reviews
#TODO: [DONE]setting options: back to front review option and manual interval setup
#TODO: [DONE]find/[DONE]edit/[DONE]delete cards
#TODO: [DONE]ReOrganize and Tests


#ISSUES:
#[RESOLVED]review_deck in correct_or functions becomes complete garbage and not letting the index function work
#[RESOLVED]the entry and label entries wont delete and remake themselves
#[RESOLVED]the deck_name labels all open the same deck which is the last created deck. 