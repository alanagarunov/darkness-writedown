import darkness.dark_functions as dark_fns
import darkness.window as dark_window

print("Hello World")
# dark_fns.create_deck('deck1')
# dark_fns.create_card('deck1', 'testfront', 'testback')
# dark_fns.create_card('deck1', '1testfront', '1testback')

# testdeck = dark_fns.determine_review('deck1')
# dark_fns.review(testdeck)
# print(dark_fns.get_list_of_decks())

root = dark_window.tk.Tk()
app = dark_window.Application(master=root)
app.master.geometry("400x400")
app.mainloop()
