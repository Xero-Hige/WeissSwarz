import random

from cards import CharacterCard

__author__ = 'hige'


class Deck(object):
    """Simulates a deck"""

    def __init__(self, deckname):
        # TODO: open file

        self.cards = []

        while True:
            self.cards.append(CharacterCard("Dovahkiin", "Red", 0, None, 0, 0, 2000, 1, ("Warrior", "Dragon")))
            break

    def draw_card(self):
        """ Draws a card from the deck """
        return self.cards.pop()

    def add_cards(self, card_list):
        """ """
        self.card += card_list

    def shuffle(self):
        """ """
        random.shuffle(self.cards)
