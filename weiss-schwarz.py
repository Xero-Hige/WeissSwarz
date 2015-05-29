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

        # Show hand

        # Clocking
        if (interface.ask_yesno("Desea clockear una carta?", "Clocking phase")):
            cards = "Player hand:\n"
            for i in range(len(player_hand)):
                cards += "[" + str(i + 1) + "]" + str(player_hand[i]) + "\n"

            card_to_clock = None
            while not card_to_clock:
                i = interface.get_integer(cards, "Choose a card to clock", [1, len(player_hand)])
                interface.show_card(player_hand[i - 1])
                if not interface.ask_yesno("Clock: " + str(player_hand[i - 1]) + "?", "Clocking card"):
                    continue
                card_to_clock = player_hand[i - 1]

        # Play cards

        # Battle phase
        # atack

        # revive

        # Play cards

        # Turn end
        player_index += 1
        interface.show_info(player, "Fin turno jugador")


main()
