import random

from  board import GameBoard
import board
from cards import ClimaxCard
from interface import WindowInterface

__author__ = 'hige'

TURN = [board.SCHWARZ_SIDE, board.WEISS_SIDE]
# Todo class hand
HANDS = [[], []]


def clocking_phase(gameboard, interface, player, player_hand):
    if not interface.ask_yesno("Desea clockear una carta?", "Clocking phase"):
        return

    player_hand_string = "Player hand:\n\n"
    for i in range(len(player_hand)):
        player_hand_string += "[" + str(i + 1) + "]" + str(player_hand[i]) + "\n"

    card_to_clock = None
    while not card_to_clock:
        i = interface.get_integer(player_hand_string, "Choose a card to clock", [1, len(player_hand)])

        if (not i):
            return

        interface.show_card(player_hand[i - 1])
        if not interface.ask_yesno("Clock: " + str(player_hand[i - 1]) + "?", "Clocking card"):
            continue

        card_to_clock = player_hand[i - 1]
        player_hand.remove(card_to_clock)

    drew_cards = gameboard.clocking(player, card_to_clock)
    for i in range(len(drew_cards)):
        interface.show_card(drew_cards[i], "Drew " + str(i + 1) + " Card")
        player_hand.append(drew_cards[i])

    interface.update_board(gameboard)



def main_phase(gameboard, interface, phase, player, player_hand):
    player_hand_string = "Player hand:\n\n"
    for i in range(len(player_hand)):
        player_hand_string += str(player_hand[i]) + "\n"
    while interface.ask_yesno(player_hand_string + "\nDesea jugar una carta?", phase):
        player_hand_string = "Player hand:\n\n"
        for i in range(len(player_hand)):
            player_hand_string += "[" + str(i + 1) + "]" + str(player_hand[i]) + "\n"

        card_to_play = None
        while not card_to_play:
            i = interface.get_integer(player_hand_string, "Choose a card to play", [1, len(player_hand)])

            if (not i):
                break

            if not gameboard.can_be_played(player, player_hand[i - 1]):
                interface.show_info("No se puede jugar: " + str(player_hand[i - 1]))
                continue

            interface.show_card(player_hand[i - 1], "Card to play")
            if not interface.ask_yesno("Play: " + str(player_hand[i - 1]) + "?", "Card"):
                continue
            card_to_play = player_hand[i - 1]

            gameboard.play_character(player,card_to_play)
            player_hand.remove(card_to_play)
            interface.update_board(gameboard)

        player_hand_string = "Player hand:\n\n"
        for i in range(len(player_hand)):
            player_hand_string += str(player_hand[i]) + "\n"


def show_hand(interface, player, player_hand):
    player_hand_string = "Player hand:\n\n"
    for i in range(len(player_hand)):
        player_hand_string += str(player_hand[i]) + "\n"
    interface.show_info(player_hand_string, "Mano del jugador " + player)


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

    interface.update_board(gameboard)

    while not gameboard.get_winner():
        player = TURN[player_index % 2]
        player_hand = HANDS[player_index % 2]

        # TODO: names
        interface.show_info(player, "Turno jugador")

        # Draw (firs turn skip)
        drew_card = gameboard.draw(player)[0]
        player_hand.append(drew_card)

        interface.show_info(str(drew_card), "Carta robada: ")
        show_hand(interface, player, player_hand)

        # Clocking
        clocking_phase(gameboard, interface, player, player_hand)
        show_hand(interface, player, player_hand)

        # Play cards
        main_phase(gameboard, interface, "Main Phase 1", player, player_hand)

        # Battle phase
        front_stage = gameboard.get_front_stage_cards(player)
        while interface.ask_yesno("Desea atacar con alguna carta?","Fase de ataque"):
            position = interface.get_integer("Elija carta con la que atacar:","Seleccion de atacante",[1,len(board.FRONT_STAGE_POSITIONS)])

            if not position:
                continue

            if not front_stage[position-1]:
                interface.show_info("No es una carta valida para atacar","No se puede atacar")
                continue

            interface.show_card(front_stage[position-1],"Carta atacante")

            gameboard.declarar_ataque(player,board.FRONT_STAGE_POSITIONS[position-1])


        show_hand(interface, player, player_hand)
        # Play cards
        main_phase(gameboard, interface, "Main Phase 2", player, player_hand)

        # Turn end
        player_index += 1
        interface.show_info(player, "Fin turno jugador")

    interface.show_info("Gano el jugador "+gameboard.get_winner(),"Fin del juego")


main()
