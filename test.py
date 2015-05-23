__author__ = 'hige'

from cards import Card, CharacterCard, ClimaxCard

class Player(object):
    """ Encapsulates the player behavior """
    pass


board = GameBoard()
deck = Deck("swartz")
card = deck.draw_card()
