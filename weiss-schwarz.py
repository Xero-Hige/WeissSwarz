import random

import board

__author__ = 'hige'

TURN = [board.SCHWARZ_SIDE, board.WEISS_SIDE]


def main():
    """ """

    player_index = random.choice([0, 1])
    gameboard = board.GameBoard(None)

    while not gameboard.get_winner():
        print "a"


main()
