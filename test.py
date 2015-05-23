__author__ = 'hige'


class GameBoard(object):
    """Simulates the gameboard"""

    def __init__(self):
        """Creates an empty gameboard"""
        self.clock = []
        self.stock = []
        self.level = []

        self.climax = None

        self.waiting_room = []

        self.front_stage = [None, None, None]
        self.back_stage = [None, None]


class Deck(object):
    """Simulates a deck"""

    def __init__(self, deckname):
        # TODO: open file

        self.cards = []

    def draw_card(self):
        """ Draws a card from the deck """
        return self.cards.pop()


class Card(object):
    """ Simulates a card  """
    pass


class CharacterCard(Card):
    """Simulates a character card"""

    def __init__(self, attack):
        """ Creates a card with the info  """
        self.atk = attack


board = GameBoard()
deck = Deck("swartz")