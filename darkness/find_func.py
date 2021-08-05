import tkinter as tk
import darkness.dark_functions as dark_fns

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