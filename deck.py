import random

from cards import CharacterCard, EventCard, ClimaxCard

__author__ = 'hige'


class Deck(object):
    """Simulates a deck"""

    def __init__(self, deckname):
        # TODO: open file

        self.cards = []

        for x in range(4):
            self.cards.append(
                CharacterCard("Illya", "blue", 0, None, "\"Good night\"", 1, 1, 5500, 1, ("Mage", "Loli")))
            self.cards.append(CharacterCard("Archer", "red", 1, None,
                                            "\"But it's all a fake. Such hypocrisy cannot save anything.\nNo, first of all, I did not know what I wanted to save!\"",
                                            2, 0, 8000, 1, ("Archer", "Heroic")))
            self.cards.append(CharacterCard("Elegant Lily", "yellow", 2, None,
                                            "\"Even if he is not a Master, our contract will not go away.\nI have sworn to protect him and to be his sword.\"",
                                            2, 2, 11000, 2, ("Warrior", "Heroic")))
            self.cards.append(
                CharacterCard("Bride Saber", "green", 2, None, "\"Answer me:\n   Are you my Praetor?.\"", 3, 1, 15000,
                              2,
                              ("Warrior", "Heroic")))
            self.cards.append(
                CharacterCard("Shiro", "green", 1, None, "\"People die when they are killed\"", 0, 0, 1000, 1,
                              ("Warrior", "Mage")))
            self.cards.append(EventCard("Wounded charge", "blue", 0, None,
                                        "Believe it till the end, i won't go away\nAnd won't say never", 1, 2))

            self.cards.append(ClimaxCard("A fated encounter", "red", 1, None,
                                         "\"I'm not scared anymore even though it's dark.\n You're strong, Berserker.\n I'm safe if you're there like that.\""))

        self.shuffle()

    def draw_card(self):
        """ Draws a card from the deck """
        return self.cards.pop()

    def add_cards(self, card_list):
        """ """
        self.cards += card_list

    def shuffle(self):
        """ """
        random.shuffle(self.cards)

    def is_empty(self):
        return len(self.cards) == 0
