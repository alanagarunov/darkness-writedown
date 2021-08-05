import tkinter as tk
import darkness.dark_functions as dark_fns


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