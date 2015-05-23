__author__ = 'hige'

from deck import Deck
from cards import ClimaxCard

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

        if atacker_card.power > defender_card.power:
            soul_points = atacker_card.soul_points
            soul_points += trigger_icon;
            another_side.get_hit(soul_points)
            another_side.destroy(defender)

        elif atacker_card.power < defender_card.power:
            self.destroy(atacker)

    def level_up(self):

        # Choice
        selected_card = self.clock.pop(-1)
        # Choice

        self.level.append(selected_card)

        self.back_stage += self.clock
        self.clock = []

    def get_hit(self, soul_points):
        damage = []
        for x in xrange(soul_points):
            damage.append(self.deck.draw_card())
            if isinstance(damage[-1], ClimaxCard):
                for card in damage:
                    self.waiting_room.append(card)
                return

        self.clock += damage

        if len(self.clock >= 7):
            self.level_up()

    def destroy(card_number):
        pass

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