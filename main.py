import numpy as np
import math
import random
import time

ROWS = 6
COLS = 7
turn = 0

PLAYER_PIECE = 1
AI_PIECE = 2

def create_board():
    board = np.zeros((ROWS, COLS))
    return board


def dropPiece(board, row, col, piece):
    board[row][col] = piece


def isValidLocation(board, col):
    return board[0][col] == 0


def getNextOpenRow(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winningMove(board, piece):
    # Check horizontal locations for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    # Check positive diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
    # Check negative diagonals
    for c in range(3, COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c - 1] == piece and board[r - 2][c - 2] == piece and board[r - 3][c - 3] == piece:
                return True

    return False


board = create_board()
game_over = False


def is_terminal_node(board):
    return winningMove(board, PLAYER_PIECE) or winningMove(board, AI_PIECE) or len(getValidLocations(board)) == 0


def evaluateWindow(window, piece):
    Score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        Score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        Score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        Score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        Score -= 4

    return Score


def score_position(board, piece):
    Score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLS // 2])]
    centerCount = center_array.count(piece)
    Score += centerCount * 3

    # Score horizontal
    for r in range(ROWS):
        rowArray = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = rowArray[c:c + 4]
            Score += evaluateWindow(window, piece)

    # Score vertical
    for c in range(COLS):
        colArray = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = colArray[r:r + 4]
            Score += evaluateWindow(window, piece)

    # Score positive diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            Score += evaluateWindow(window, piece)

    # Score negative diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            Score += evaluateWindow(window, piece)

    return Score

def minimax(board, depth, alpha, beta, maximizingPlayer):
    validLocations = getValidLocations(board)
    isTerminal = is_terminal_node(board)

    if depth == 0 or isTerminal:
        if isTerminal:
            if winningMove(board, AI_PIECE):
                return (None, 10000000)
            elif winningMove(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(validLocations)

        for col in validLocations:
            row = getNextOpenRow(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break

        return column, value

    else:
        value = math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getNextOpenRow(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value



