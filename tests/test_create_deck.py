import unittest
from configparser import ConfigParser
from darkness.dark_functions import create_deck
from darkness.dark_functions import create_card
from darkness.dark_functions import get_cards
from darkness.dark_functions import determine_review

class Test1CreateDeck(unittest.TestCase):
    def test1_create_deck(self):
        #creates a deck with specific name and looks for it in the config file
        name = "testnamedeck"
        create_deck(name)

        config = ConfigParser()
        config.read("settings.ini")
        test_deck_name_str_lst = dict(config.items("deck_settings"))
        for i in test_deck_name_str_lst:
            if i == name:
                test_deck_name_str = i
            
        self.assertEqual(test_deck_name_str, name)

class Test2CreateCard(unittest.TestCase):
    def test2_create_card(self):
        create_card("testnamedeck", 'testfront', 'testback')
        create_card('testnamedeck', '1testfront', '1testback')

        lst = get_cards("testnamedeck")
        for i in lst:
            #print(i)
            front2 = i[2]

        self.assertEqual(front2, "1testfront")

class Test3DetermineReview(unittest.TestCase):
    def test3_determine_review(self):
        review = determine_review("testnamedeck")
        self.assertEqual(review[0][3], "testback")

if __name__ == '__main__':
    unittest.main()