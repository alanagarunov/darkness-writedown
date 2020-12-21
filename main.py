import sqlite3
import time

def create_deck(name):
    conn = sqlite3.connect(name+'.db')
    cursor = conn.cursor()
    sql = '''CREATE TABLE ''' + name + '''(DECK_NAME CHAR(20) NOT NULL, CARD_ID CHAR(20) NOT NULL, CARD_FRONT CHAR(20) NOT NULL, CARD_BACK CHAR(20) NOT NULL, LAST_REVIEW CHAR(20), CARD_LEVEL CHAR(1))'''
    cursor.execute(sql)
    print("Table Created")
    conn.commit()
    conn.close()
    f = open("config.txt", "a")
    f.write(name + " " + str(0) + "\n")
    f.close()

def update_id(deck_name, id):
    templst = []
    f = open("config.txt", "r")
    templst = f.readlines()
    for i in range(0,len(templst)):
        if deck_name in templst[i]:
            templst[i] = deck_name + " " + str(id+1) + "\n"
    
    f = open("config.txt", "w")
    f.writelines(templst)
    f.close()

def get_card_id(deck_name):
    templst = []
    templst1 = []
    f = open("config.txt", "r")
    for x in f:
        if deck_name in x:
            templst.append(str(x))
    for i in range(0,len(templst)):
        return templst[i].split()[1]
        #return templst1[1]

#perhaps deckname needs to be apart of cards, otherwise how do i update.
def create_card(deck_name, card_front, card_back):
    current_id = int(get_card_id(deck_name))
    conn = sqlite3.connect(deck_name+'.db')
    cursor = conn.cursor()
    sql = '''INSERT INTO ''' + deck_name + '''(DECK_NAME, CARD_ID, CARD_FRONT, CARD_BACK, LAST_REVIEW, CARD_LEVEL) VALUES (' ''' + deck_name + ''' ',' ''' + str(current_id+1) + ''' ',' ''' + card_front + ''' ',' ''' + card_back + ''' ',' ''' + str(int(time.time())) + ''' ',' ''' + str(0) + ''' ')'''
    cursor.execute(sql)
    print("Card added")
    update_id(deck_name, current_id)
    conn.commit()
    conn.close()

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

def determine_review(deck_name):
    review_deck = []
    current_time = int(time.time())
    conn = sqlite3.connect(deck_name+'.db')
    cursor = conn.cursor()
    sql = '''SELECT * from ''' + deck_name + ''' '''
    result = cursor.execute(sql).fetchall()
    conn.commit()
    conn.close()

    temparr = []
    for x in result:
        #print(x)
        temparr = list(x)
        if int(temparr[5]) == 0:
            review_deck.append(x)
        if (int(temparr[5]) == 1 or int(temparr[5]) == 2) and (current_time - int(temparr[4]) >= 14400):
            review_deck.append(x)
        if (int(temparr[5]) == 3 or int(temparr[5]) == 4) and (current_time - int(temparr[4]) >= 28800):
            review_deck.append(x)
        if (int(temparr[5]) == 5 or int(temparr[5]) == 6) and (current_time - int(temparr[4]) >= 86400):
            review_deck.append(x)
        if (int(temparr[5]) == 7 or int(temparr[5]) == 8) and (current_time - int(temparr[4]) >= 172800):
            review_deck.append(x)
        if (int(temparr[5]) == 9 or int(temparr[5]) == 10) and (current_time - int(temparr[4]) >= 604800):
            review_deck.append(x)
        if (int(temparr[5]) == 11 or int(temparr[5]) == 12) and (current_time - int(temparr[4]) >= 1209600):
            review_deck.append(x)
        if (int(temparr[5]) == 13 or int(temparr[5]) == 14) and (current_time - int(temparr[4]) >= 2419200):
            review_deck.append(x)
        if (int(temparr[5]) == 15 or int(temparr[5]) == 16) and (current_time - int(temparr[4]) >= 9676800):
            review_deck.append(x)
        temparr = []
    return review_deck


#create_deck('deck1')
#create_card('deck1', 'testfront', 'testback')
testdeck = determine_review('deck1')
update_card('deck1', testdeck[0], True)
