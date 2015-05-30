BACK_STAGE = "back"
FRONT_STAGE = "front"

FRONT_LEFT = 0
FRONT_CENTER = 1
FRONT_RIGHT = 2

BACK_LEFT = 0
BACK_RIGHT = 1

SCHWARZ_SIDE = "schwarz"
WEISS_SIDE = "weiss"
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

    def declarar_ataque(self, atacker, defender, another_side):
        """ """
        atacker_card = self.front_stage[atacker]
        defender_card = another_side.front_stage[defender]

        trigger_card = self.deck.draw_card()

        trigger_icon = trigger_card.get_trigger_icon()

        if not defender_card:
            soul_points = atacker_card.soul_points
            soul_points += trigger_icon + 1
            another_side.get_hit(soul_points)
            return trigger_card

        if atacker_card.power < defender_card.power:
            self.destroy(atacker)

        if atacker_card.power >= defender_card.power:
            another_side.destroy(defender)

        if atacker_card.power > defender_card.power:
            soul_points = atacker_card.soul_points
            soul_points += trigger_icon
            another_side.get_hit(soul_points)

        return trigger_card  # TODO: Ver

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

        if len(self.clock) >= 7:
            self.level_up()

    def destroy(self, card_number):
        pass

    def draw(self, amount):
        """ """
        cards = []
        while (not self.deck.is_empty()) and (amount > len(cards)):
            cards.append(self.deck.draw_card())

        if self.deck.is_empty():
            self.refill_deck()

        return cards

    def refill_deck(self):
        """ """
        self.deck.add_cards(self.waiting_room)
        self.deck.shuffle()
        self.waiting_room = []

    def get_clock_level(self):
        """ """
        return len(self.clock)

    def get_level(self):
        """ """
        return len(self.level)

    def clocking(self, card):
        self.clock.append(card)
        return self.draw(2)

    def get_clock_colors(self):
        colors = {}
        for card in self.clock:
            colors[card.get_color()] = 0
        return colors.keys()

    def get_level_colors(self):
        colors = {}
        for card in self.clock:
            colors[card.get_color()] = 0
        return colors.keys()

    def get_stock_colors(self):
        colors = {}
        for card in self.clock:
            colors[card.get_color()] = 0
        return colors.keys()

    def can_play_normal_card(self, card):
        if None not in self.front_stage + self.back_stage:
            return False

        if card.get_level() > self.get_level():
            return False

        if card.get_cost() > len(self.stock):
            return False

        playable_colors = self.get_clock_colors()
        playable_colors += self.get_level_colors()

        if card.get_color() not in playable_colors:
            if card.get_level() != 0:
                return False

        return True

    def play_character(self, card, stage, position):
        if not self.can_play_normal_card(card):
            raise ValueError, "Carta no jugable"

        if stage == FRONT_STAGE:
            if self.front_stage[position]:
                raise IndexError, "Posicion ocupada"
            self.front_stage[position] = card

        elif stage == BACK_STAGE:
            if self.front_stage[position]:
                raise IndexError, "Posicion ocupada"
            self.front_stage[position] = card

        else:
            raise ValueError, "No existe esa stage"


class GameBoard(object):
    """Simulates the gameboard"""

    def __init__(self, interface):
        """Creates an empty gameboard"""

        # White (Weiss)
        self.weiss = _PlayerSide()

        # Black (Schwarz)
        self.schwarz = _PlayerSide()

        self.interface_handler = interface

    def current(self, side):
        if side == WEISS_SIDE:
            return self.weiss
        return self.schwarz

    def declarar_ataque(self, side, posicion_atacante, posicion_defensor):
        """

        :param side:
        :param posicion_atacante:Posicion en el tablero del jugador de la carta que ataca Left Center Right (ctes)
        :param posicion_defensor:Posicion en el tablero del oponente de la carta a atacar: Left Center Right (ctes)
        :return:
        """
        if side == WEISS_SIDE:
            return self.weiss.declarar_ataque(posicion_atacante, posicion_defensor, self.schwarz)

        elif side == SCHWARZ_SIDE:
            return self.schwarz.declarar_ataque(posicion_atacante, posicion_defensor, self.weiss)

    def draw(self, side, amount=1):
        return self.current(side).draw(amount)

    def get_side_level(self, side):
        return self.current(side).get_level()

    def get_clock_level(self, side):
        return self.current(side).get_clock_level()

    def clocking(self, side, card):
        return self.current(side).clocking(card)

    def can_be_played(self, side, card):
        if isinstance(card, ClimaxCard):
            return self.current(side).can_play_climax(card)

        else:
            return self.current(side).can_play_card(card)

    def play_character(self, side, card, stage, position):
        self.current(side).play_character(card, stage, position)

    def get_winner(self):
        if self.weiss.get_level() == 4:
            return WEISS_SIDE
        if self.schwarz.get_level() == 4:
            return SCHWARZ_SIDE
        return ""
