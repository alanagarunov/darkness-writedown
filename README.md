# Darkness-Writedown

A flashcard application based off a popular open-source flashcard software called Anki, which primarily uses a scientifically proven method of memorization known as SRS (Spaced Repition System). Such software is popular among language learners and academics.  
The name darkness-writedown is a literal translation of the Japanese word 暗記 (anki) which means memorization.  

# Use
Darkness-Writedown or just Darkness, lets you create a deck and add cards with a front and back to it.  
You can use the find button to edit or delete cards you have already made. 
![add](https://i.imgur.com/hUzrSQs.gif)
You can then review the card by double clicking the name of the deck you want to review and answering the questions, front or back.  
If you do not wish to answer cards back to front, you can change that option in the settings. You can also change the review intervals in the settings to better suit yourself.

### Review intervals
SRS works by increasing the amount of time you wait between reviews as you keep answering the cards correctly. This can include waiting a week or more between reviews after answering the card correctly more than five times in a row, for example. The card becomes "burned" after the maximum interval is reached.  
The default interval (in seconds) is ```7200,14400,43200,86400,302400,604800,1209600,4838400```  
Typically, to move on the next interval, you should get the card correct two times in one interval. For example, if you answer a card correctly every two hours two times then your next interval will be four hours.  
You can change the review intervals in settings.

### Find/Edit/Delete Cards
You can also use the find/edit/delete button to see a list of cards in each deck. Double left-click a card to edit it, and double right-click a card to delete it.

# Setup and Installation
Install and setup by cloning the repository, creating a virtual environment, and installing dependencies.
```
python -m venv env
source env/scripts/activate
pip install -r requirements.txt
```
Exit the virtual environment with ```deactivate``` in the commandline.  
Run the application in the commandline with ```python main.py```

# Testing
Test that creating a deck, inserting a card into it, and creating a review deck from it, all work properly. In the main directory of the repository, Run
```python -m unittest tests/test_create_all.py```  
You should get an "OK" from 3 tests.