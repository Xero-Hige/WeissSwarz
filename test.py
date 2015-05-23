__author__ = 'hige'


class _PlayerSide(object):
    """Simulates a player field"""

    def __init__(self):
        self.clock = []
        self.stock = []
        self.level = []

        self.climax = None

        self.waiting_room = []

        self.front_stage = [None, None, None]
        self.back_stage = [None, None]

        self.deck = Deck("swartz")

    def atack(self, atacker, defender, another_side):
        """ """
        atacker_card = self.front_stage[atacker]
        defender_card = another_side.front_stage[defender]

        trigger_card = self.deck.draw_card();

        trigger_icon = trigger_card.triger_icon;

        if (atacker_card.power > defender_card.power):
            soul_points = atacker_card.soul_points
            soul_points += trigger_icon;
            another_side.get_hit(soul_points)
            another_side.destroy(defender)

        elif (atacker_card.power < defender_card.power):
            self.destroy(atacker)

    def level_up(self):

        # Choice
        selected_card = self.clock.pop(-1)
        #Choice

        self.level.append(selected_card)

        self.back_stage += self.clock
        self.clock = []

    def get_hit(self,soul_points):
        damage = []
        for x in xrange(soul_points):
            damage.append(self.deck.draw_card())
            if isinstance(damage[-1],Climax_Card):
                for card in damage:
                    self.waiting_room.append(card)
                return

        self.clock += damage

        if len(self.clock >= 7):
            self.level_up()


    def destroy(card_number):


class GameBoard(object):
    """Simulates the gameboard"""

    def __init__(self):
        """Creates an empty gameboard"""

        # White (Weiss)
        self.weiss = _PlayerSide()

        self.schwarz = _PlayerSide()

    def atack(self, side, atacker, defender):
        """ TODO:
        :param side:
        :param atacker:
        :param defender:
        :return:
        """
        if side == "weiss":
            self.weiss.atack(atacker, defender, self.schwarz)
        else:
            self.schwarz.atack(atacker, defender, self.weiss)


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

class ClimaxCard(Card):
    """ """
    pass


class Player(object):
    """ Encapsulates the player behavior """
    pass


board = GameBoard()
deck = Deck("swartz")
card = deck.draw_card()