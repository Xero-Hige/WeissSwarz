import random

import board
from interface import WindowInterface

__author__ = 'hige'

TURN = [board.SCHWARZ_SIDE, board.WEISS_SIDE]


def main():
    """ """

    player_index = random.choice([0, 1])
    interface = WindowInterface()
    gameboard = board.GameBoard(interface)

    while not gameboard.get_winner():
        interface.get_integer("Carta a jugar", "Jugar desde la mano", [0, 5])


main()
