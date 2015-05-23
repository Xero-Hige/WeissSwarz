__author__ = 'hige'


class _Board_Side(object):
    """Simulates a player field"""

    def __init__(self):
        self.clock = []
        self.stock = []
        self.level = []

        self.climax = None

        self.waiting_room = []

        self.front_stage = [None, None, None]
        self.back_stage = [None, None]


class GameBoard(object):
    """Simulates the gameboard"""

    def __init__(self):
        """Creates an empty gameboard"""

        # White (Weiss)
        self.weiss = _Board_Side()

        self.schwarz = _Board_Side()


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


class Card(object):
    """ Simulates a card  """

    def __init__(self, name, color, trigger_icon, hability):
        self.name = name
        self.color = color
        self.trigger_icon = trigger_icon
        self.hability = hability


class CharacterCard(Card):
    """Simulates a character card"""

    def __init__(self, name, color, trigger_icon, hability, level, cost, power, soul_points, trait):
        """ Creates a card with the info  """
        super(self.__class__, self).__init__(name, color, trigger_icon, hability)
        self.level = level
        self.cost = cost
        self.power = power
        self.soul_points = soul_points
        self.trait = trait


board = GameBoard()
deck = Deck("swartz")
card = deck.draw_card()
