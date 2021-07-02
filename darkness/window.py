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
        tk.Button(self, text="Settings", command=self.settings_window).grid(column=2, row=3)
        

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

        listbox.bind("<Double-1>", self.review_window)
        listbox.pack(side="left")
        
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)
        scrollbar.pack(side="right", fill="y")
        testframe.grid(column=0)


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

    def review_window(self, event):
        widget = event.widget
        cs = widget.curselection()
        name = ""
        decks = dark_fns.get_list_of_decks()
        for i in cs:
            name = decks[i]

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
        if dark_fns.get_backfront():
            for i in back_front:
                # self.labl = tk.Label(self.reviewwindow, text=i[3])
                # self.labl.pack(side="top")
                # self.ans = tk.Entry(self.reviewwindow)
                # self.ans.pack(side="top")
                self.ans.config(state="normal")
                self.ans.bind('<Return>', lambda x: self.not_or_correct(i, back_front))
                self.ans.wait_variable(self.var)

    def settings_window(self):
        self.settingswindow = tk.Toplevel(self)
        self.settingswindow.geometry("400x200")
        lapseentry = tk.Entry(self.settingswindow)
        lapseentry.insert(0, dark_fns.get_current_lapses())
        lapseentry.pack(side="top")

        check1var = tk.IntVar()
        check1 = tk.Checkbutton(self.settingswindow, text="Include back-to-front reviews?", variable=check1var, onvalue=1, offvalue=0)
        check1.pack(side="top")

        print(lapseentry.get())
        save_button = tk.Button(self.settingswindow, text="Save", command=lambda: self.change_settings(lapseentry.get(), check1var.get()))
        save_button.pack(side="bottom")

        self.congrats = tk.Label(self.settingswindow, text="")
        self.congrats.pack(side="bottom")

    def change_settings(self, new_lapse, backfront_option):
        dark_fns.update_lapses(str(new_lapse))
        dark_fns.update_backfront(str(backfront_option))
        self.congrats.config(text="Settings successfully changed.")


    def find_window(self):
        self.findwindow = tk.Toplevel(self)
        self.findwindow.geometry("400x200")
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
            testframe = tk.Frame(self.findwindow)
            self.listbox = tk.Listbox(testframe)
            #self.listbox.config(width=250, height=0)
            scrollbar = tk.Scrollbar(testframe, orient="vertical")

            for x in tempdeck:
                self.listbox.insert(tk.END, x)
                self.labels.append(tk.Label(self.findwindow, text=x))

            a = 0
            b = 0
            self.listbox.bind("<Double-3>", lambda event, arg=a: self.find_window_populate_delete(event, name, labels))
            self.listbox.bind("<Double-1>", lambda event, arg=b: self.find_window_populate_edit(event, name, labels))
            self.listbox.pack(side="left")
            
            self.listbox.config(yscrollcommand = scrollbar.set)
            scrollbar.config(command = self.listbox.yview)
            scrollbar.pack(side="right", fill="y")
            testframe.pack(side="bottom")

            self.clickonce = clickonce + 1
        else:
            self.listbox.delete(0, tk.END)

            for x in tempdeck:
                self.listbox.insert(tk.END, x)
            for a in range(len(labels)):
                 self.labels[a].config(text="")
            for y,z in zip(tempdeck, range(len(labels))):
                 self.labels[z].config(text=y)


    def find_window_populate_delete(self, event, name, labels):
        widget = event.widget
        cs = widget.curselection()
        for i in cs:
            #print(labels[i].cget("text").split())
            if name == labels[i].cget("text").split()[0]:
                dark_fns.delete_card(name, labels[i].cget("text"))
                self.listbox.delete(i)

    def find_window_populate_edit(self, event, name, labels):
        self.editwindow = tk.Toplevel(self.findwindow)
        self.editwindow.geometry("350x50")
        widget = event.widget
        cs = widget.curselection()
        sentcard = ""

        self.frontside = tk.Entry(self.editwindow)
        for i in cs:
            self.frontside.insert(0, labels[i].cget("text").split()[2])
            sentcard = labels[i].cget("text")
        self.frontside.pack(side="top")
        self.backside = tk.Entry(self.editwindow)
        for i in cs:
            self.backside.insert(0, labels[i].cget("text").split()[3])
            sentcard = labels[i].cget("text")
        self.backside.pack(side="top")

        self.update_button = tk.Button(self.editwindow, text="Update", command= lambda: self.find_window_populate_edit_exec(name, sentcard, self.frontside.get(), self.backside.get()))
        self.update_button.pack(side="right", fill="y")

        self.congrats = tk.Label(self.editwindow, text="")
        self.congrats.pack(side="bottom")

    def find_window_populate_edit_exec(self, name, card, frontside, backside):
        dark_fns.update_card_contents(name, card, frontside, backside)
        self.congrats.config(text="Card successfully updated.")


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
#TODO: delete deck button
#TODO: [kinda already does it?]check review then [DONE]make the reviews
#TODO: [DONE]setting options: back to front review option and manual interval setup
#TODO: [DONE]find/[DONE]edit/[DONE]delete cards


#ISSUES:
#[RESOLVED]review_deck in correct_or functions becomes complete garbage and not letting the index function work
#[RESOLVED]the entry and label entries wont delete and remake themselves
#[RESOLVED]the deck_name labels all open the same deck which is the last created deck. 