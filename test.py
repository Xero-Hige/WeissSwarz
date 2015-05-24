import random

from board import GameBoard
import board
import card_maker

__author__ = 'hige'


def clocking(gameboard, player, side):
    print "Before clocking"
    print player
    print "Clock level:", gameboard.get_clock_level(side)
    card = random.choice(player)
    player.remove(card)
    print "During clocking"
    card_maker.show_card(card,"Card to clock",4)
    print "Card to clock:", card
    print player
    cards = gameboard.clocking(side, card)
    player += cards
    for card in cards:
        card_maker.show_card(card,"Drew cards")
    print "After clocking"
    print player
    print "Clock level:", gameboard.get_clock_level(side)


def play_character(gameboard, player, side):
    card = random.choice(player)
    player.remove(card)
    if gameboard.can_be_played(side, card):
        card_maker.show_card(card,"Can play:",4)
        gameboard.play_character(side, card, board.FRONT_STAGE, board.FRONT_LEFT)
    else:
        card_maker.show_card(card,"Can't play:",4)
        player.append(card)


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
    play_character(gameboard, player1_hand, board.WEISS_SIDE)

    print "Before attack"
    print "Schwarz clock level:", gameboard.get_clock_level(board.SCHWARZ_SIDE)

    gameboard.atack(board.WEISS_SIDE, board.FRONT_LEFT, board.FRONT_RIGHT)

    print "After attack"
    print "Schwarz clock level:", gameboard.get_clock_level(board.SCHWARZ_SIDE)


simulate_game()
