# coding=utf-8
import random

CLOCKING_AMOUNT = 2

MAX_LEVEL = 4

MAX_CLOCK_LEVEL = 7

BACK_STAGE = 2
FRONT_STAGE = 1

STAGES = [BACK_STAGE, FRONT_STAGE]

FRONT_LEFT = -1
FRONT_CENTER = 0
FRONT_RIGHT = 1

FRONT_STAGE_POSITIONS = [FRONT_LEFT, FRONT_CENTER, FRONT_RIGHT]

BACK_LEFT = 0
BACK_RIGHT = 1

BACK_STAGE_POSITIONS = [BACK_LEFT, BACK_RIGHT]

SCHWARZ_SIDE = "Schwarz"
WEISS_SIDE = "Weiss"
NONE_SIDE = ""

CONTINUA = 0
TEMPORAL = 1

__author__ = 'hige'

from deck import Deck
from cards import ClimaxCard, CharacterCard, EventCard


class _PlayerSide(object):
    """Simulates a player field"""

    def __init__(self, nombre):
        self.area_clock = []
        self.area_stock = []
        self.area_nivel = []

        self.area_climax = None

        self.area_espera = []

        self.escena_principal = [None, None, None]
        self.backstage = [None, None]

        self.deck = Deck("swartz")

        self.nombre = nombre

    def declarar_ataque(self, posicion_atacante, posicion_defensor, lado_oponente, interface):
        """

        :param posicion_atacante:
        :param posicion_defensor:
        :param lado_oponente:
        :return: Una lista de la forma [posicion_atacante_destruir,posicion_defensor_destruir]. -1 en caso que no haya que destruir
        """
        posicion_atacante = FRONT_STAGE_POSITIONS.index(posicion_atacante)
        posicion_defensor = FRONT_STAGE_POSITIONS.index(posicion_defensor)

        atacker_card = self.escena_principal[posicion_atacante]
        defender_card = lado_oponente.escena_principal[posicion_defensor]

        resultado = [-1, -1]

        # Empate o perdida
        if defender_card and atacker_card.power <= defender_card.power:  # Si es menor o igual se destruye el atacante
            resultado[0] = posicion_atacante
            if atacker_card.power == defender_card.power:  # Si son iguales se destruyen ambas
                resultado[0] = posicion_defensor
            return

        trigger_card = self.deck.draw_card()
        trigger_icon = trigger_card.get_trigger_icon()
        soul_points = atacker_card.soul_points + trigger_icon

        if not defender_card:  # Ataque directo
            soul_points += 1

        elif atacker_card.power > defender_card.power:
            resultado[0] = posicion_defensor

        interface.show_card(trigger_card, "Trigered card: +" + str(trigger_icon) + " soul points")
        lado_oponente.get_hit(soul_points, interface)

        self.area_stock.append(trigger_card)

        return resultado

    def level_up(self, interface):

        # Choice
        selected_card = random.choice(self.area_clock)
        self.area_clock.remove(selected_card)
        # Choice

        self.area_nivel.append(selected_card)

        self.area_espera += self.area_clock
        self.area_clock = []

        interface.show_info("Jugador: " + self.nombre + " subio de nivel\n\nNivel actual:" + str(self.get_level()),
                            "Aumento de nivel")


    def get_hit(self, soul_points, interface):
        damage = []
        for x in xrange(soul_points):
            damage.append(self.deck.draw_card())
            if isinstance(damage[-1], ClimaxCard):
                interface.show_info("Sacada carta: {0}\n Daño cancelado".format(str(damage[-1])), "Daño cancelado")
                for card in damage:
                    self.area_espera.append(card)
                return

        self.area_clock += damage

        interface.show_info("Jugador " + self.nombre + "daño recibido: " + str(soul_points) + " puntos de daño",
                            "Daño hecho")

        if len(self.area_clock) >= MAX_CLOCK_LEVEL:
            self.level_up(interface)

    def remove_card(self, escena, card_number):
        """Remueve una carta de caracter del campo"""
        if escena == FRONT_STAGE:
            card = self.escena_principal[card_number]
            self.escena_principal[card_number] = None
        elif escena == BACK_STAGE:
            card = self.backstage[card_number]
            self.backstage[card_number] = None

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

    def pagar_coste(self, coste_a_pagar):
        for coste in range(coste_a_pagar):
            cost_card = self.area_stock.pop(-1)  # Desapilo
            self.area_espera.append(cost_card)

    def play_character(self, card, interface):
        if not self.can_play_normal_card(card):
            return False

        while True:
            stage = interface.get_integer("Ingrese la stage donde jugar la carta:\n\n[1] Front stage\n[2] Back_stage",
                                          title="Seleccion de stage", number_range=[1, len(STAGES) + 1])

            if not stage:
                return False

            escena = None
            position = None

            if stage == FRONT_STAGE:
                position = interface.get_integer(
                    "Ingrese la posicion dentro del stage:\n\nAreas: [1-" + str(len(FRONT_STAGE_POSITIONS)) + "]",
                    title="Seleccion de area", number_range=[1, len(FRONT_STAGE_POSITIONS)])
                escena = self.escena_principal
            elif stage == BACK_STAGE:
                position = interface.get_integer(
                    "Ingrese la posicion dentro del stage:\n\nAreas: [1-" + str(len(BACK_STAGE_POSITIONS)) + "]",
                    title="Seleccion de area", number_range=[1, len(BACK_STAGE_POSITIONS)])
                escena = self.backstage

            if not position:
                return False

            position -= 1
            if self.escena_principal[position]:
                interface.show_info("No se puede jugar en esa posicion, esta ocupada", title="")
                if not interface.ask_yesno("Elegir otra posicion?", title=""):
                    return False
            else:
                escena[position] = card
                self.pagar_coste(card.get_cost())
                return True


    def can_play_climax_card(self, card):
        if self.area_climax:
            return False

        playable_colors = self.get_clock_colors()
        playable_colors += self.get_level_colors()

        if card.get_color() not in playable_colors:
            return False

        return True

    def play_event(self, card, interface_handler):
        if not self.can_play_normal_card(card):
            return False
        self.pagar_coste(card.get_cost())
        return True

    def play_climax(self, card, interface_handler):
        if not self.can_play_climax_card(card):
            return False
        self.area_climax = card
        return True

    def remover_climax(self):
        if not self.area_climax:
            return
        self.area_espera.append(self.area_climax)
        self.area_climax = None


class GameBoard(object):
    """Simulates the gameboard"""

    def __init__(self, interface):
        """Creates an empty gameboard"""

        # White (Weiss)
        self.weiss = _PlayerSide(WEISS_SIDE)

        # Black (Schwarz)
        self.schwarz = _PlayerSide(SCHWARZ_SIDE)

        self.interface_handler = interface

        self.habilidades_aplicadas = []  # cola

    def current(self, side):
        if side == WEISS_SIDE:
            return self.weiss
        return self.schwarz

    def declarar_ataque(self, side, posicion_atacante):
        """

        :param side:
        :param posicion_atacante:Posicion en el tablero del jugador de la carta que ataca Left Center Right (ctes)
        :return:
        """

        atacante = None
        defensor = None
        enemy_side = None
        if side == WEISS_SIDE:
            atacante = self.weiss
            defensor = self.schwarz
            enemy_side = SCHWARZ_SIDE
        elif side == SCHWARZ_SIDE:
            defensor = self.weiss
            atacante = self.schwarz
            enemy_side = SCHWARZ_SIDE

        resultado = atacante.declarar_ataque(posicion_atacante, -1 * posicion_atacante, defensor,
                                             self.interface_handler)

        if (resultado[0] != -1):
            removed_card = atacante.remove_card(FRONT_STAGE, FRONT_STAGE_POSITIONS.index(resultado[0]))
            self.desaplicar_habilidades(side, removed_card)
            self.remover_habilidad(side, removed_card.get_ability())

        if (resultado[1] != -1):
            removed_card = defensor.remove_card(FRONT_STAGE, FRONT_STAGE_POSITIONS.index(resultado[1]))
            self.desaplicar_habilidades(enemy_side, removed_card)
            self.remover_habilidad(enemy_side, removed_card.get_ability())

    def play_card(self, side, card):
        if isinstance(card, CharacterCard):
            if self.play_character(side, card):
                self.aplicar_habilidad(side, card.get_ability(), CONTINUA)
                return True
            return False

        elif isinstance(card, EventCard):
            if self.play_event(side, card):
                self.aplicar_habilidad(side, card.get_ability(), TEMPORAL)
                return True
            return False


        elif isinstance(card, ClimaxCard):
            if self.play_climax(side, card):
                self.aplicar_habilidad(side, card.get_ability(), TEMPORAL)
                return True
            return False

        else:
            return False


    def play_character(self, side, card):
        if not self.current(side).play_character(card, self.interface_handler):
            return False

        nueva_cola = []
        while len(self.habilidades_aplicadas) > 0:  # Mientras cola no esta vacia
            side, habilidad, continuidad = self.habilidades_aplicadas.pop()  # Sacar primero
            habilidad.apply_on_card(card)
            nueva_cola.append((side, habilidad, CONTINUA))
        self.habilidades_aplicadas = nueva_cola

        return True


    def play_event(self, side, card):
        return self.current(side).play_event(card, self.interface_handler)


    def play_climax(self, side, card):
        return self.current(side).play_climax(card, self.interface_handler)


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


    def get_winner(self):
        if self.weiss.get_level() == MAX_LEVEL:
            return WEISS_SIDE
        if self.schwarz.get_level() == MAX_LEVEL:
            return SCHWARZ_SIDE
        return NONE_SIDE


    def get_front_stage_cards(self, side):
        return self.current(side).escena_principal[:]


    def get_back_stage_cards(self, side):
        return self.current(side).backstage[:]


    def get_all_front_stage_cards(self):
        """Devuelve una lista de cartas con las cartas de la escena principal.
            Las primeras 3 posiciones corresponden a las cartas de weiss, las ultimas 3 a las cartas schwarz."""

        cartas = []
        cartas += self.weiss.escena_principal
        cartas += self.schwarz.escena_principal

        return cartas


    def terminar_turno(self):
        nueva_cola = []
        while len(self.habilidades_aplicadas) > 0:  # Mientras cola no esta vacia
            side, habilidad, continuidad = self.habilidades_aplicadas.pop()  # Sacar primero
            habilidad.revert_on_board(self, side)
            if continuidad == CONTINUA:
                nueva_cola.append((side, habilidad, CONTINUA))
        self.habilidades_aplicadas = nueva_cola

        self.weiss.remover_climax()
        self.schwarz.remover_climax()


    def iniciar_turno(self):
        nueva_cola = []
        while len(self.habilidades_aplicadas) > 0:  # Mientras cola no esta vacia
            side, habilidad, continuidad = self.habilidades_aplicadas.pop()  # Sacar primero
            habilidad.apply_on_board(self, side)
            nueva_cola.append((side, habilidad, CONTINUA))
        self.habilidades_aplicadas = nueva_cola


    def aplicar_habilidad(self, side, habilidad, continuidad):
        if not habilidad:
            return
        habilidad.apply_on_board(self, side)
        self.habilidades_aplicadas.append((side, habilidad, continuidad))

    def desaplicar_habilidades(self, side, card):
        """Le remueve las habilidades aplicadas a una carta"""
        nueva_cola = []
        while len(self.habilidades_aplicadas) > 0:  # Mientras cola no esta vacia
            side, habilidad, continuidad = self.habilidades_aplicadas.pop()  # Sacar primero
            habilidad.revert_on_card(self, side)
            nueva_cola.append((side, habilidad, CONTINUA))
        self.habilidades_aplicadas = nueva_cola

    def remover_habilidad(self, side, undo_ability):
        nueva_cola = []
        while len(self.habilidades_aplicadas) > 0:  # Mientras cola no esta vacia
            ability_side, habilidad, continuidad = self.habilidades_aplicadas.pop()  # Sacar primero
            if ability_side == side and habilidad == undo_ability:
                habilidad.revert_on_board(self, side)
            else:
                nueva_cola.append((side, habilidad, CONTINUA))
        self.habilidades_aplicadas = nueva_cola
