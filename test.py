import random

from board import GameBoard
import board

__author__ = 'hige'

# Board creation
gameboard = GameBoard()

# Init
player1_hand = gameboard.draw(board.WEISS_SIDE, 5)
player2_hand = gameboard.draw(board.SCHWARZ_SIDE, 5)

print "Opening hand"
print player1_hand
print player2_hand


def clocking(player, side):
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

# first turn
clocking(player1_hand, board.WEISS_SIDE)
