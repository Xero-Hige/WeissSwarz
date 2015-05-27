import random

from  board import GameBoard
import board
from interface import WindowInterface

__author__ = 'hige'

TURN = [board.SCHWARZ_SIDE, board.WEISS_SIDE]
# Todo class hand
HANDS = [[], []]


def main():
    """ """

    interface = WindowInterface()

    # Create decks

    # Decides order
    player_index = random.choice([0, 1])

    gameboard = GameBoard(interface)


    # Generate hand
    HANDS[player_index] = gameboard.draw(TURN[player_index], 4)
    HANDS[(player_index + 1) % 2] = gameboard.draw(TURN[(player_index + 1) % 2], 4)

    while not gameboard.get_winner():
        player = TURN[player_index % 2]
        player_hand = HANDS[player_index % 2]

        # TODO: names
        interface.show_info(player, "Turno jugador")

        # Draw (firs turn skip)
        drew_card = gameboard.draw(player)[0]
        player_hand.append(drew_card)

        interface.show_info(str(drew_card), "Carta robada: ")

        # Clocking

        # Play cards

        # Battle phase
        # atack

        # revive

        # Play cards

        # Turn end
        player_index += 1


main()
