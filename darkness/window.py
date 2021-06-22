import tkinter as tk
import darkness.dark_functions as dark_fns

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        #self.create_widgets()
        self.load_display_decks()
        tk.Button(self, text="Create Card", command=self.create_card_button_window).grid(column=2, row=0)
        tk.Button(self, text="Create Deck", command=self.create_deck_button_window).grid(column=2, row=1)
        tk.Button(self, text="Find/Edit/Delete Cards", command=self.find_window).grid(column=2, row=2)
        

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
        decks = dark_fns.get_list_of_decks()
        tk.Label(self, text="List of All Decks:\tTotal Items\tFor Review").grid(column=0)
        labels = []
        for i in decks:
            num = dark_fns.get_card_id(i)
            num1 = dark_fns.determine_review(i)
            labels.append(tk.Label(self, text=i+"\t"+str(num)+"\t"+str(len(num1)*2)))
            # label.grid(column=0)
            # label.bind("<Button-1>", lambda e: self.review_window(i))

        for x in range(0, len(labels)):
            labels[x].grid(column=0)
            labels[x].bind("<Button-1>", lambda event, bound_x=x: self.review_window(decks[bound_x]))



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

    def create_deck_button_window(self):
        self.deckcreate = tk.Toplevel(self)
        self.deckcreate.geometry("350x50")
        self.deckcreate.title("Create Deck")
        
        self.name = tk.Entry(self.deckcreate)
        self.name.pack(side="top")

        self.add_button = tk.Button(self.deckcreate, text="Add", command=lambda: self.create_deck_button_add(self.name.get()))
        self.add_button.pack(side="top")

    def review_window(self, name):
        self.reviewwindow = tk.Toplevel(self)
        self.reviewwindow.geometry("350x50")
        review_deck = dark_fns.determine_review(name)
        back_front = review_deck.copy()
        self.var = tk.IntVar(self)

        self.labl = tk.Label(self.reviewwindow, text=review_deck[0][2])
        self.labl.pack(side="top")
        self.ans = tk.Entry(self.reviewwindow)
        self.ans.pack(side="top")
        self.ans.config(state="normal")

        print(review_deck)
        for i in review_deck:
            # self.labl = tk.Label(self.reviewwindow, text=i[2])
            # self.labl.pack(side="top")
            # self.ans = tk.Entry(self.reviewwindow)
            # self.ans.pack(side="top")
            self.ans.config(state="normal")
            self.ans.bind('<Return>', lambda x: self.correct_or_not(i, review_deck))
            self.ans.wait_variable(self.var)
        for i in back_front:
            # self.labl = tk.Label(self.reviewwindow, text=i[3])
            # self.labl.pack(side="top")
            # self.ans = tk.Entry(self.reviewwindow)
            # self.ans.pack(side="top")
            self.ans.config(state="normal")
            self.ans.bind('<Return>', lambda x: self.not_or_correct(i, back_front))
            self.ans.wait_variable(self.var)

    def find_window(self):
        self.findwindow = tk.Toplevel(self)
        self.findwindow.geometry("400x500")
        self.clicked = tk.StringVar(self.findwindow)
        self.clicked.set("Select a Deck")
        self.dropdown = tk.OptionMenu(self.findwindow, self.clicked, *dark_fns.get_list_of_decks())
        self.dropdown.pack(side="top")

        self.clickonce = 0
        self.labels = []

        self.list_button = tk.Button(self.findwindow, text="List", command=lambda: self.find_window_populate(self.clicked.get(), self.clickonce, self.labels))
        self.list_button.pack(side="left")

    def find_window_populate(self, name, clickonce, labels):
        tempdeck = dark_fns.get_cards(name)
        if self.clickonce <= 0:
            for x in tempdeck:
                self.labels.append(tk.Label(self.findwindow, text=x))

            for b in range(0, len(labels)):
                labels[b].bind("<Button-3>", lambda event, bound_b=b: dark_fns.delete_card(self, name, labels[bound_b].cget("text")))

            self.clickonce = clickonce + 1
        else:
            for a in range(len(labels)):
                self.labels[a].config(text="")
            for y,z in zip(tempdeck, range(len(labels))):
                self.labels[z].config(text=y)

            for c in range(0, len(labels)):  
                labels[c].bind("<Button-3>", lambda event, bound_c=c: dark_fns.delete_card(self, name, labels[bound_c].cget("text")))
                #self.labels = list(map(lambda a: labels.config(text=y), range(0, len(labels)))) 
        
        for i in range(0, len(labels)):
            self.labels[i].pack(side="top")
        
        #minor problem, when you re-list a deck, it only shows as many cards as the previous.

    def correct_or_not(self, i, review_deck):
        #print(i)
        if self.ans.get() == i[3]:
            dark_fns.update_card(i[0], i, True)
            #print(review_deck)
            try:
                self.labl.config(text=review_deck[review_deck.index(i)+1][2])
            except:
                self.labl.config(text="You've reached the end of the review! You can close the window now.")
            review_deck.pop(review_deck.index(i))
        else:
            dark_fns.update_card(i[0], i, False)
            self.labl.config(text=review_deck[review_deck.index(i)+1][2])
        self.ans.delete(0, 'end')
        self.var.set(1)

    def not_or_correct(self, i, back_front):
        if self.ans.get() == i[2]:
            dark_fns.update_card(i[0], i, True)
            try:
                self.labl.config(text=back_front[back_front.index(i)+1][3])
            except:
                self.labl.config(text="You've reached the end of the review! You can close the window now.")
            back_front.pop(back_front.index(i))
        else:
            dark_fns.update_card(i[0], i, False)
            self.labl.config(text=back_front[back_front.index(i)+1][3])
        self.ans.delete(0, 'end')
        self.var.set(1)

    def create_card_button_add(self, deck_name, frontside, backside):
        dark_fns.create_card(deck_name, frontside, backside)
        tk.Label(self.createdialog, text="Card Added").pack()

    def create_deck_button_add(self, name):
        dark_fns.create_deck(name)
        tk.Label(self.deckcreate, text="Deck Added").pack()

#in order of easiest   
#               |
#              \ /
#            hardest    
#TODO: DONE[make it populate a list of decks], DONE[add deck] and DONE[card button], make it look not like crap.
#TODO: check review then [DONE]make the reviews
#TODO: setting options: back to front review option and manual interval setup
#TODO: [DONE]find/edit/[DONE]delete cards


#ISSUES:
#[RESOLVED]review_deck in correct_or functions becomes complete garbage and not letting the index function work
#[RESOLVED]the entry and label entries wont delete and remake themselves
#[RESOLVED]the deck_name labels all open the same deck which is the last created deck. 