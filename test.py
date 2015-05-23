from board import GameBoard
import board

__author__ = 'hige'

# Board creation
gameboard = GameBoard()

# first turn
player1_hand = gameboard.draw(board.WEISS_SIDE, 5)
player2_hand = gameboard.draw(board.SCHWARZ_SIDE, 5)
