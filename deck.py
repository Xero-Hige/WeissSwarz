import random

from cards import CharacterCard

__author__ = 'hige'


class Deck(object):
    """Simulates a deck"""

    def __init__(self, deckname):
        # TODO: open file

        self.cards = []

        for x in range(4):
            self.cards.append(CharacterCard("Archer", "Red", 0, None,"", 0, 0, 2000, 1, ("Warrior", "Heroic")))
            self.cards.append(CharacterCard("Shiro", "Blue", 0, None,"", 0, 0, 2000, 1, ("Warrior", "Mage")))
            self.cards.append(CharacterCard("Saber", "Yellow", 0, None,"", 0, 0, 2000, 1, ("Warrior", "Heroic")))
            self.cards.append(CharacterCard("Caster", "Blue", 0, None,"", 0, 0, 2000, 1, ("Mage", "Heroic")))
            self.cards.append(CharacterCard("Rider", "Green", 0, None,"", 0, 0, 2000, 1, ("Warrior", "Heroic")))

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
