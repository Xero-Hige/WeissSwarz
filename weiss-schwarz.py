import random

from  board import GameBoard
import board
from interface import WindowInterface

__author__ = 'hige'

TURN = [board.SCHWARZ_SIDE, board.WEISS_SIDE]


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

            if gameboard.play_card(player, card_to_play):
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


def fase_de_batalla(gameboard, interface, player):
    front_stage = gameboard.get_front_stage_cards(player)
    while interface.ask_yesno("Desea atacar con alguna carta?", "Fase de ataque"):
        position = interface.get_integer("Elija carta con la que atacar:", "Seleccion de atacante",
                                         [1, len(board.FRONT_STAGE_POSITIONS)])

        if not position:
            continue

        if not front_stage[position - 1]:
            interface.show_info("No es una carta valida para atacar", "No se puede atacar")
            continue

        interface.show_card(front_stage[position - 1], "Carta atacante")

        front_stage[position - 1] = None
        gameboard.declarar_ataque(player, board.FRONT_STAGE_POSITIONS[position - 1])
        interface.update_board(gameboard)


def main():
    """ """

    interface = WindowInterface()
    hands = [[], []]

    # Create decks

    # Decides order
    player_index = random.choice([0, 1])

    gameboard = GameBoard(interface)

    l = [gameboard.weiss,gameboard.schwarz]

    from cards import CharacterCard

    c1 = CharacterCard("Bride Saber", "green", 2, None, "\"Answer me:\n   Are you my Praetor?.\"", 0, 0, 15000,2, ("Warrior", "Heroic") )
    c2 = CharacterCard("Elegant Lily", "yellow", 2, None,"\"Even if he is not a Master, our contract will not go away.\nI have sworn to protect him and to be his sword.\"",2, 2, 11000, 2, ("Warrior", "Heroic"))
    c3 = CharacterCard("Archer", "red", 1, None,"\"But it's all a fake. Such hypocrisy cannot save anything.\nNo, first of all, I did not know what I wanted to save!\"", 2, 0, 8000, 1, ("Archer", "Heroic"))

    for s in l:
        s.area_climax = c1

        c_ = [c1, c2, c3]
        c_c_ = [c1, c2]

        random.shuffle(c_)
        random.shuffle(c_c_)

        s.escena_principal = c_[:]
        s.backstage = c_c_[:]

        random.shuffle(c_)
        s.area_espera = c_[:]

        c_c_c_ = [c1, c2, c3, c1]
        random.shuffle(c_c_c_)
        s.area_nivel = c_c_c_[:]

        random.shuffle(c_c_c_)
        s.area_nivel = c_c_c_[:]

        random.shuffle(c_c_c_)
        s.area_stock = c_c_c_[:]
        s.area_climax = random.choice([c3,c1,c2])

        a=[c1,c1,c2,c2,c3,c3,c3]
        random.shuffle(a)
        s.area_clock = a[:]

    # Generate hand
    hands[player_index] = gameboard.draw(TURN[player_index], 4)
    hands[(player_index + 1) % 2] = gameboard.draw(TURN[(player_index + 1) % 2], 4)

    interface.update_board(gameboard)

    while not gameboard.get_winner():
        player = TURN[player_index % 2]
        player_hand = hands[player_index % 2]

        # TODO: names
        interface.show_info(player, "Turno jugador")

        gameboard.iniciar_turno()
        interface.update_board(gameboard)


        # Draw (firs turn skip)
        drew_card = gameboard.draw(player)[0]
        player_hand.append(drew_card)

        interface.show_info(str(drew_card), "Carta robada: ")
        show_hand(interface, player, player_hand)

        # Clocking
        clocking_phase(gameboard, interface, player, player_hand)
        interface.update_board(gameboard)
        show_hand(interface, player, player_hand)

        # Play cards
        main_phase(gameboard, interface, "Main Phase 1", player, player_hand)
        interface.update_board(gameboard)

        # Battle phase
        fase_de_batalla(gameboard, interface, player)
        interface.update_board(gameboard)

        show_hand(interface, player, player_hand)
        # Play cards
        main_phase(gameboard, interface, "Main Phase 2", player, player_hand)
        interface.update_board(gameboard)

        # Turn end
        player_index += 1
        interface.show_info(player, "Fin turno jugador")

        gameboard.terminar_turno()


    interface.show_info("Gano el jugador " + gameboard.get_winner(), "Fin del juego")


main()
