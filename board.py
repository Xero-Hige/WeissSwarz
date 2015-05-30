import random

CLOCKING_AMOUNT = 2

MAX_LEVEL = 4

MAX_CLOCK_LEVEL = 7

BACK_STAGE = "back"
FRONT_STAGE = "front"

FRONT_LEFT = 0
FRONT_CENTER = 1
FRONT_RIGHT = 2

BACK_LEFT = 0
BACK_RIGHT = 1

SCHWARZ_SIDE = "schwarz"
WEISS_SIDE = "weiss"
NONE_SIDE = ""

__author__ = 'hige'

from deck import Deck
from cards import ClimaxCard


class _PlayerSide(object):
    """Simulates a player field"""

    def __init__(self):
        self.area_clock = []
        self.area_stock = []
        self.area_nivel = []

        self.area_climax = None

        self.area_espera = []

        self.escena_principal = [None, None, None]
        self.backstage = [None, None]

        self.deck = Deck("swartz")

    def declarar_ataque(self, posicion_atacante, posicion_defensor, lado_oponente, interface):
        """

        :param posicion_atacante:
        :param posicion_defensor:
        :param lado_oponente:
        :return: None
        """
        atacker_card = self.escena_principal[posicion_atacante]
        defender_card = lado_oponente.front_stage[posicion_defensor]

        # Empate o perdida
        if defender_card and atacker_card.power <= defender_card.power:  # Si es menor o igual se destruye el atacante
            self.destroy(posicion_atacante)
            if atacker_card.power == defender_card.power:  # Si son iguales se destruyen ambas
                lado_oponente.destroy(posicion_defensor)
            return

        trigger_card = self.deck.draw_card()
        trigger_icon = trigger_card.get_trigger_icon()
        soul_points = atacker_card.soul_points + trigger_icon

        if not defender_card:  # Ataque directo
            soul_points += 1

        elif atacker_card.power > defender_card.power:
            lado_oponente.destroy(posicion_defensor)

        interface.show_card(trigger_card, "Trigered card: +" + str(trigger_icon) + " soul points")
        lado_oponente.get_hit(soul_points, interface)

        self.area_stock.append(trigger_card)


    def level_up(self):

        # Choice
        selected_card = random.choice(self.area_clock)
        self.area_clock.remove(selected_card)
        # Choice

        self.area_nivel.append(selected_card)

        self.area_espera += self.area_clock
        self.area_clock = []

    def get_hit(self, soul_points):
        damage = []
        for x in xrange(soul_points):
            damage.append(self.deck.draw_card())
            if isinstance(damage[-1], ClimaxCard):
                for card in damage:
                    self.area_espera.append(card)
                return

        self.area_clock += damage

        if len(self.area_clock) >= MAX_CLOCK_LEVEL:
            self.level_up()

    def destroy(self, card_number):
        """Remueve una carta de caracter del campo"""
        card = self.escena_principal[card_number]
        self.escena_principal[card_number] = None
        self.area_espera.append(card)


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
        self.deck.add_cards(self.area_espera)
        self.deck.shuffle()
        self.area_espera = []

    def get_clock_level(self):
        """ """
        return len(self.area_clock)

    def get_level(self):
        """ """
        return len(self.area_nivel)

    def clocking(self, card):
        """Agrega la carta pasada por parametro al clock y devuelve las CLOCKING_AMOUNT cartas sacadas del mazo"""
        self.area_clock.append(card)
        return self.draw(CLOCKING_AMOUNT)

    def get_clock_colors(self):
        """ Devuelve una lista con todos los colores de cartas que hay en la zona de clock

        :return:
        """
        colors = {}
        for card in self.area_clock:
            colors[card.get_color()] = 0
        return colors.keys()

    def get_level_colors(self):
        """ Devuelve una lista con todos los colores de cartas que hay en la zona de nivel"""

        colors = {}
        for card in self.area_clock:
            colors[card.get_color()] = 0
        return colors.keys()

    def get_stock_colors(self):
        colors = {}
        for card in self.area_clock:
            colors[card.get_color()] = 0
        return colors.keys()

    def can_play_normal_card(self, card):
        if None not in self.escena_principal + self.backstage:
            return False

        if card.get_level() > self.get_level():
            return False

        if card.get_cost() > len(self.area_stock):
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
            if self.escena_principal[position]:
                raise IndexError, "Posicion ocupada"
            self.escena_principal[position] = card

        elif stage == BACK_STAGE:
            if self.backstage[position]:
                raise IndexError, "Posicion ocupada"
            self.backstage[position] = card

        else:
            raise ValueError, "No existe esa stage"

    def can_play_climax_card(self, card):
        if self.area_climax:
            return False

        playable_colors = self.get_clock_colors()
        playable_colors += self.get_level_colors()

        if card.get_color() not in playable_colors:
            return False

        return True


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
            return self.weiss.declarar_ataque(posicion_atacante, posicion_defensor, self.schwarz,
                                              self.interface_handler)

        elif side == SCHWARZ_SIDE:
            return self.schwarz.declarar_ataque(posicion_atacante, posicion_defensor, self.weiss,
                                                self.interface_handler)

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
            return self.current(side).can_play_climax_card(card)

        else:
            return self.current(side).can_play_normal_card(card)

    def play_character(self, side, card, stage, position):
        self.current(side).play_character(card, stage, position)

    def get_winner(self):
        if self.weiss.get_level() == MAX_LEVEL:
            return WEISS_SIDE
        if self.schwarz.get_level() == MAX_LEVEL:
            return SCHWARZ_SIDE
        return NONE_SIDE
