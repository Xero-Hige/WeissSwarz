import random

from board import GameBoard
import board

__author__ = 'hige'


def clocking(gameboard, player, side):
    print "Before clocking"
    print player
    print "Clock level:", gameboard.get_clock_level(side)
    card = random.choice(player)
    player.remove(card)
    print "During clocking"
    print "Card to clock:", card
    print player
    cards = gameboard.clocking(side, card)
    player += cards
    print "Draw cards:", cards
    print "After clocking"
    print player
    print "Clock level:", gameboard.get_clock_level(side)


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
    clocking(gameboard, player1_hand, board.WEISS_SIDE)

    card = random.choice(player1_hand)
    player1_hand.remove(card)

    if gameboard.can_be_played(board.WEISS_SIDE, card):
        print "Can play:", card
        gameboard.play_character(board.WEISS_SIDE, card, "front", "center")
    else:
        print "Can't play: ", card


simulate_game()
