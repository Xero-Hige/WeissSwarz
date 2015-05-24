import random

from board import GameBoard
import board
import card_maker

__author__ = 'hige'


def clocking(gameboard, player_hand , side):
    print "Choose a card to play:"
    for i in range(len(player_hand)):
        card_maker.show_card(player_hand[i],"Hand: "+player_hand[i].get_name())

    print player_hand

    card_to_play = int(raw_input("Card number:"))-1
    card = player_hand.pop(card_to_play)

    print "DEBUG: Before clocking"
    print "DEBUG: Clock level:", gameboard.get_clock_level(side)

    print "DEBUG: During clocking"
    card_maker.show_card(card,"Card to clock",4)
    print "DEBUG: Card to clock:", card

    cards = gameboard.clocking(side, card)

    print "Drew cards: ",cards
    for card in cards:
        card_maker.show_card(card,"Drew cards")

    print "DEBUG: After clocking"
    print "DEBUG: Clock level:", gameboard.get_clock_level(side)

    return cards

def play_character(gameboard, player_hand, side):
    print "Choose a card to play:"
    for i in range(len(player_hand)):
        card_maker.show_card(player_hand[i],"Hand: "+player_hand[i].get_name())

    print player_hand

    card_to_play = int(raw_input("Card number:"))-1
    card = player_hand.pop(card_to_play)

    if gameboard.can_be_played(side, card):
        card_maker.show_card(card,"Can play:",4)
        gameboard.play_character(side, card, board.FRONT_STAGE, board.FRONT_LEFT)
        return []
    else:
        card_maker.show_card(card,"Can't play:",4)
        return [card]


def simulate_game():
    """  """
    # Board creation
    gameboard = GameBoard()

    # Init
    player1_hand = gameboard.draw(board.WEISS_SIDE, 5)
    player2_hand = gameboard.draw(board.SCHWARZ_SIDE, 5)

    print "Opening hand"
    print player1_hand
    print player2_hand

    # first turn
    print "Weiss first turn"
    print "Weiss clocking"
    player1_hand += clocking(gameboard, player1_hand, board.WEISS_SIDE)

    print "Weiss play"
    player1_hand += play_character(gameboard, player1_hand, board.WEISS_SIDE)

    print "Before attack"
    print "Schwarz clock level:", gameboard.get_clock_level(board.SCHWARZ_SIDE)

    triggered_card = gameboard.atack(board.WEISS_SIDE, board.FRONT_LEFT, board.FRONT_RIGHT)
    card_maker.show_card(triggered_card,"Triggered")

    print "After attack"
    print "Schwarz clock level:", gameboard.get_clock_level(board.SCHWARZ_SIDE)


simulate_game()
