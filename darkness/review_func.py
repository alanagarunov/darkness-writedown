import tkinter as tk
from functools import partial
import darkness.dark_functions as dark_fns


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
            self.ans.bind('<Return>',  lambda x: correct_or_not(self, i, review_deck))
            self.ans.wait_variable(self.var)
        if dark_fns.get_backfront():
            for i in back_front:
                # self.labl = tk.Label(self.reviewwindow, text=i[3])
                # self.labl.pack(side="top")
                # self.ans = tk.Entry(self.reviewwindow)
                # self.ans.pack(side="top")
                self.ans.config(state="normal")
                self.ans.bind('<Return>',  lambda x: not_or_correct(self, i, review_deck))
                self.ans.wait_variable(self.var)


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