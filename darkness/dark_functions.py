import sqlite3
import time
from configparser import ConfigParser

def create_deck(name):
    name = name.replace(" ", "_")
    conn = sqlite3.connect(name+'.db')
    cursor = conn.cursor()
    sql = '''CREATE TABLE ''' + name + '''(DECK_NAME CHAR(20) NOT NULL, CARD_ID CHAR(20) NOT NULL, CARD_FRONT CHAR(20) NOT NULL, CARD_BACK CHAR(20) NOT NULL, LAST_REVIEW CHAR(20), CARD_LEVEL CHAR(1))'''
    cursor.execute(sql)
    print("Table Created")
    conn.commit()
    conn.close()

    config = ConfigParser()
    config.read("settings.ini")

    #!!! UNCOMMENT IF RUNNING FOR FIRST TIME
    #config.add_section("deck_settings")
    #config.add_section("Lapses")
    #config.add_section("Back-Front")
    #config.set("Lapses", "user_lapse", "7200,14400,43200,86400,302400,604800,1209600,4838400")
    #config.set("Back-Front", "user-set", str(1))

    config.set("deck_settings", name, '0')
    with open("settings.ini", "w") as f:
        config.write(f)

def update_id(deck_name, id):
    config = ConfigParser()
    config.read("settings.ini")
    current_id = config.getint("deck_settings", deck_name)
    current_id = current_id + 1
    config.set("deck_settings", deck_name, str(current_id))
    with open("settings.ini", "w") as f:
        config.write(f)

def get_card_id(deck_name):
    config = ConfigParser()
    config.read("settings.ini")
    current_id = config.getint("deck_settings", deck_name)
    return current_id
    

def get_list_of_decks():
    templst = []
    templst1 = []

    config = ConfigParser()
    config.read("settings.ini")
    templst = config.items("deck_settings")
    for i in templst:
        templst1.append(i[0])
    return templst1
    

#perhaps deckname needs to be apart of cards, otherwise how do i update.
def create_card(deck_name, card_front, card_back):
    current_id = int(get_card_id(deck_name))
    conn = sqlite3.connect(deck_name+'.db')
    cursor = conn.cursor()
    sql = '''INSERT INTO ''' + deck_name + '''(DECK_NAME, CARD_ID, CARD_FRONT, CARD_BACK, LAST_REVIEW, CARD_LEVEL) VALUES (\'''' + deck_name + '''\',\'''' + str(current_id+1) + '''\',\''''+ card_front +'''\',\''''+ card_back +'''\',\'''' + str(int(time.time())) + '''\',\'''' + str(0) + ''' ')'''
    cursor.execute(sql)
    print("Card added")
    update_id(deck_name, current_id)
    conn.commit()
    conn.close()

def get_cards(name):
    conn = sqlite3.connect(name+'.db')
    cursor = conn.cursor()
    sql = '''SELECT * from ''' + name + ''' '''
    result = cursor.execute(sql).fetchall()
    conn.commit()
    conn.close()
    return result

def update_card(deck_name, card, correctness):
    if correctness is True:
        try:
            card_items = list(card)
            print(card_items)
            conn = sqlite3.connect(deck_name+'.db')
            cursor = conn.cursor()
            sql = '''UPDATE ''' + deck_name + ''' SET LAST_REVIEW = \'''' + str(int(time.time())) + '''\', CARD_LEVEL = \'''' + str(int(card_items[5])+1) + '''\' WHERE CARD_ID = \'''' + str(card_items[1]) + '''\''''
            print(str(card_items[1]) + " ID Card Updated")
            print(sql)
            cursor.execute(sql)
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print("There was a failure. Error: ", error)
    if correctness is False:
        try:
            card_items = list(card)
            print(card_items)
            conn = sqlite3.connect(deck_name+'.db')
            cursor = conn.cursor()
            sql = '''UPDATE ''' + deck_name + ''' SET LAST_REVIEW = \'''' + str(int(time.time())) + '''\', CARD_LEVEL = \'''' + str(int(card_items[5])-1) + '''\' WHERE CARD_ID = \'''' + str(card_items[1]) + '''\''''
            print(str(card_items[1]) + " ID Card Updated")
            print(sql)
            cursor.execute(sql)
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print("There was a failure. Error: ", error)

def delete_card(deck_name, card):
    tempdeck = get_cards(deck_name)
    card = card.split(" ")
    print(card)
    conn = sqlite3.connect(deck_name+'.db')
    cursor = conn.cursor()
    sql = '''DELETE FROM ''' + deck_name + ''' WHERE CARD_ID = ''' + card[1] + ''' '''
    cursor.execute(sql)
    print("Deleted card")
    conn.commit()
    conn.close()
    #self.list_button.invoke()

def update_card_contents(deck_name, card, new_frontside, new_backside):
    try:
        tempdeck = get_cards(deck_name)
        card = card.split(" ")
        print(card)
        conn = sqlite3.connect(deck_name+'.db')
        cursor = conn.cursor()
        sql = '''UPDATE ''' + deck_name + ''' SET CARD_FRONT = \'''' + str(new_frontside) + '''\', CARD_BACK = \'''' + str(new_backside)+ '''\' WHERE CARD_ID = \'''' + str(card[1]) + '''\''''
        print(str(card[1]) + "ID Card Updated")
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
            print("There was a failure. Error: ", error)

def update_lapses(new_lapses):
    config = ConfigParser()
    config.read("settings.ini")
    #updated_lapse = ','.join(new_lapses)
    config.set("Lapses", "user_lapse", new_lapses)
    with open("settings.ini", "w") as f:
        config.write(f)

def get_current_lapses():
    config = ConfigParser()
    config.read("settings.ini")
    review_lapse_str = config.get("Lapses", "user_lapse")
    return review_lapse_str

def update_backfront(setting):
    config = ConfigParser()
    config.read("settings.ini")
    config.set("Back-Front", "user-set", str(setting))
    with open("settings.ini", "w") as f:
        config.write(f)

def get_backfront():
    config = ConfigParser()
    config.read("settings.ini")
    setting = config.get("Back-Front", "user-set")
    return setting


def determine_review(deck_name):
    review_deck = []
    current_time = int(time.time())
    #print(deck_name)
    conn = sqlite3.connect(deck_name+'.db')
    cursor = conn.cursor()
    sql = '''SELECT * from ''' + deck_name + ''' '''
    result = cursor.execute(sql).fetchall()
    conn.commit()
    conn.close()

    config = ConfigParser()
    config.read("settings.ini")
    review_lapse_str = config.get("Lapses", "user_lapse")
    review_lapse_list = review_lapse_str.split(',')
    print(review_lapse_list)

    temparr = []
    for x in result:
        #print(x)
        temparr = list(x)
        if int(temparr[5]) == 0:
            review_deck.append(x)
        elif (int(temparr[5]) == 1 or int(temparr[5]) == 2) and (current_time - int(temparr[4]) >= int(review_lapse_list[0])):
            review_deck.append(x)
        elif (int(temparr[5]) == 3 or int(temparr[5]) == 4) and (current_time - int(temparr[4]) >= int(review_lapse_list[1])):
            review_deck.append(x)
        elif (int(temparr[5]) == 5 or int(temparr[5]) == 6) and (current_time - int(temparr[4]) >= int(review_lapse_list[2])):
            review_deck.append(x)
        elif (int(temparr[5]) == 7 or int(temparr[5]) == 8) and (current_time - int(temparr[4]) >= int(review_lapse_list[3])):
            review_deck.append(x)
        elif (int(temparr[5]) == 9 or int(temparr[5]) == 10) and (current_time - int(temparr[4]) >= int(review_lapse_list[4])):
            review_deck.append(x)
        elif (int(temparr[5]) == 11 or int(temparr[5]) == 12) and (current_time - int(temparr[4]) >= int(review_lapse_list[5])):
            review_deck.append(x)
        elif (int(temparr[5]) == 13 or int(temparr[5]) == 14) and (current_time - int(temparr[4]) >= int(review_lapse_list[6])):
            review_deck.append(x)
        elif (int(temparr[5]) == 15 or int(temparr[5]) == 16) and (current_time - int(temparr[4]) >= int(review_lapse_list[7])):
            review_deck.append(x)
        temparr = []
    return review_deck

def review(review_deck):
    back_front = review_deck.copy()
    print("Studying " + str(len(review_deck)*2) + " items.")
    while len(review_deck) > 0:
        for i in review_deck:
            print(i[2])
            ans = input("?: ")
            print("ans: " + ans + ". actual: " + i[3] )
            if ans == i[3]:
                update_card(i[0], i, True)
                review_deck.pop(review_deck.index(i))
            else:
                update_card(i[0], i, False)
    while len(back_front) > 0:
        for i in back_front:
            print(i[3])
            ans = input("?: ")
            if ans == i[2]:
                update_card(i[0], i, True)
                back_front.pop(back_front.index(i))
            else:
                update_card(i[0], i, False)


# create_deck('deck1')
# create_card('deck1', 'testfront', 'testback')
# create_card('deck1', '1testfront', '1testback')

#testdeck = determine_review('deck1')
#review(testdeck)
