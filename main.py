import numpy as np
import random
import math
import time

ROWS = 6
COLS = 7
PLAYER_PIECE = 1
AI_PIECE = 2
turn = 0


def create_board():  #creating board of size 6 * 7 and fill its elements with zeros
	board = np.zeros((ROWS,COLS))
	return board

def getNextOpenRow(board, col): #col: indix of valid column
	for r in range(ROWS):  #iteration on every row of valid column
		if board[r][col] == 0:  #check every row of valid column if it's empty
			return r  #return indix of row

def dropPiece(board, row, col, piece):  #put given piece(player_piece or AI_piece) in given row and column
    board[row][col] = piece

def print_board(board):
    print(np.flip(board, 0))  #(0 axis:flip rows in inverse order (last row-> first row->) && (first row->last row)

def isValidLocation(board, col):  #checker if col is valid column(there is free locations to put pieces in this col) when it's 5th row(surface of matrix) isn't filled
	if board[ROWS - 1][col] == 0:  #ROW_COUNT-1 : 5th row(surface of board)
		return True   #column isn't filled
	else:
		return False   #the selected column by the player is filled with pieces


def getValidLocations(board):
	valid_locations = []  #list that have valid columns to play in
	for col in range(COLS):  #iteration in board from col 0 to 6
		if isValidLocation(board, col): #check col that i iterate in from col=0 to col=7-1=6 if its valid column when 5th row is empty
			valid_locations.append(col)  #adding indices of valid column to list
	return valid_locations   #return list of indices of valid columns



#win(return true) if there are 4 pieces allocated successively(horizontally or vertically or diagonally)
def winningMove(board, piece):  #piece-> player piece or AI piece
	# Check horizontal locations for win on each row
	for c in range(COLS-3): #iteration from 0:3
		                           #ColumnCount=7-3=4 as we seek to reach 4 coins to win
		for r in range(ROWS):  #iteration on every row
			# checker that the first 4 cols are filled with piece as when c=0 we adding 1 till c=3 (from cols= 0 to 3) and the last 4 cols (from 3 to 6) as when c=3 we adding 1 till c=6
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win on each column
	for c in range(COLS):  #iteration on every column
		for r in range(ROWS-3):   #iteration from 0:2
# checker that the last 4 rows are filled with piece as when r=0 we adding 1 till r=2 (from rows= 0 to 2) and the 1st 4 rows(from rows=2 to 5 the surface) as when c=2 we adding 1 till c=5
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check right diaganols for win
	for c in range(COLS-3):  #iteration from 0:3
		for r in range(ROWS-3):  #iteration from 0:2
			  # 0	#1	#2	#3	#4	#5	#6
			# 5
			# 4
			# 3				*
			# 2			*
			# 1		*
			# 0	*
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check left diaganols for win
	for c in range(COLS-3): #iteration from 0:3
		for r in range(3, ROWS): #start from  3:5
			 # 0	#1	#2	#3	#4	#5	#6
			# 5
			# 4
			# 3	*
			# 2		*
			# 1			*
			# 0				*
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True



#if player or ai win or length of returned valid_locations list from get_valid_locations(board) = 0(no more places to put piece in, Game is over)
#then the is_terminal_node  will be true
def is_terminal_node(board):
	if winningMove(board, PLAYER_PIECE) or winningMove(board, AI_PIECE) or len(getValidLocations(board)) == 0:
		return True
	else:
		return False


def evaluateWindow(window, piece):
    Score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE  #check if given piece is AI piece, so opp piece-> player piece, else its given player piece,so opp piece-> AI piece

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



#if maximizingPlayer = True -> AI player
def minimax(board, depth, maximizingPlayer):
	validLocations = getValidLocations(board)  #return list of valid columns
	is_terminal = is_terminal_node(board)  #return true if player or ai win or no more places to put piece in(Game is over)
	if depth == 0 or is_terminal:
		if is_terminal:  # true if player or ai win or no more places to put piece in
			if winningMove(board, PLAYER_PIECE):   #true if player win horizontally/vertically/diagonally
				return (None, -10000000000000)   #assign very small score to player as minimax fnc works for AI only
			elif winningMove(board, AI_PIECE):  #true if ai win horizontally/vertically/diagonally
				return (None, 100000000000000)   #assign very large score to AI as minimax fnc works for him only
			else:  #true if no more places to put piece in (tie),score=0
				return (None, 0)
		else: # Depth of search is zero (then find heuristic value of the board)
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer: #maximizingPlayer -> AI player
		value = -math.inf  #initialize value of score with very small value
		column = random.choice(validLocations)  #initializa column given to AI with randomly column from valid columns
		for col in validLocations: #assign values in valid_locations list(indices of valid columns) for col and iterate till size of list
			row = getNextOpenRow(board, col)  #return index of empty row of valid column
			b_copy = board.copy()
			dropPiece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, False)[1]
			if new_score > value:
				value = new_score
				column = col
		return column, value

	else: #the opponent's turn and the algorithm will try to find the move with the minimize opponent's score.
		# Minimizing player ->
		value = math.inf
		column = random.choice(validLocations)
		for col in validLocations:
			row = getNextOpenRow(board, col)
			b_copy = board.copy()
			dropPiece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, True)[1]
			if new_score < value:
				value = new_score
				column = col
		return column, value

game_over = False

def end_game():
    global game_over
    game_over = True
    print(game_over)


#intial board ->filled with zeros
board = create_board()

while not game_over:

    if turn == 0:
		# ask for player 1(player) input
		# player 1 choose which column he want to put his piece in
        col = int(input("Player 1, Make your Selection(0-6):"))
		# Player will drop a piece on the board
        if isValidLocation(board, col): #checker if selected column is valid
            row = getNextOpenRow(board, col)  #return index of empty row of selected valid column
            dropPiece(board, row, col, PLAYER_PIECE)   #put given piece(player_piece) in given row and column
            turn = 1  #to make the turn for player 2(AI)
    else:
        # AI player's turn
        depth = 4  # Depth of minimax search, you can adjust this
        start_time = time.time()
		# minimax algorithm is used in the AI turn only to find optimal move for AI, in player's turn, there is no need to call the minimax function bec player's move based on their  input column
        col, _ = minimax(board, depth, True)  #colu,_ : interested in return of column whatever return of value is from minmax function
        end_time = time.time()
        print(f"AI Player's move took {end_time - start_time:.3f} seconds")
        if isValidLocation(board, col):  #checker if selected column is valid
            row = getNextOpenRow(board, col)  #return index of empty row of selected valid column
            dropPiece(board, row, col, AI_PIECE)  #put given piece(AI_piece) in given row and column
            turn = 0  #to make the turn for player 1(player)


    print_board(board)
    if winningMove(board, PLAYER_PIECE):
        print("Player 1 wins!")
        end_game()
    elif winningMove(board, AI_PIECE):
        print("AI Player wins!")
        end_game()
    elif len(getValidLocations(board)) == 0:
        print("It's a tie!")
        end_game()

# import numpy as np
# import math
# import random
# import time

# ROWS = 6
# COLS = 7
# turn = 0

# PLAYER_PIECE = 1
# AI_PIECE = 2

# def create_board():
#     board = np.zeros((ROWS, COLS))
#     return board


# def dropPiece(board, row, col, piece):
#     board[row][col] = piece


# def isValidLocation(board, col):
#     return board[0][col] == 0


# def getNextOpenRow(board, col):
#     for r in range(ROWS):
#         if board[r][col] == 0:
#             return r


# def print_board(board):
#     print(np.flip(board, 0))


# def winningMove(board, piece):
#     # Check horizontal locations for win
#     for c in range(COLS - 3):
#         for r in range(ROWS):
#             if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
#                 return True
#     # Check vertical locations for win
#     for c in range(COLS):
#         for r in range(ROWS - 3):
#             if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
#                 return True
#     # Check positive diagonals
#     for c in range(COLS - 3):
#         for r in range(3, ROWS):
#             if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
#                 return True
#     # Check negative diagonals
#     for c in range(3, COLS):
#         for r in range(3, ROWS):
#             if board[r][c] == piece and board[r - 1][c - 1] == piece and board[r - 2][c - 2] == piece and board[r - 3][c - 3] == piece:
#                 return True

#     return False


# board = create_board()
# game_over = False


# def is_terminal_node(board):
#     return winningMove(board, PLAYER_PIECE) or winningMove(board, AI_PIECE) or len(getValidLocations(board)) == 0


# def evaluateWindow(window, piece):
#     Score = 0
#     opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

#     if window.count(piece) == 4:
#         Score += 100
#     elif window.count(piece) == 3 and window.count(0) == 1:
#         Score += 5
#     elif window.count(piece) == 2 and window.count(0) == 2:
#         Score += 2

#     if window.count(opp_piece) == 3 and window.count(0) == 1:
#         Score -= 4

#     return Score


# def score_position(board, piece):
#     Score = 0

#     # Score center column
#     center_array = [int(i) for i in list(board[:, COLS // 2])]
#     centerCount = center_array.count(piece)
#     Score += centerCount * 3

#     # Score horizontal
#     for r in range(ROWS):
#         rowArray = [int(i) for i in list(board[r, :])]
#         for c in range(COLS - 3):
#             window = rowArray[c:c + 4]
#             Score += evaluateWindow(window, piece)

#     # Score vertical
#     for c in range(COLS):
#         colArray = [int(i) for i in list(board[:, c])]
#         for r in range(ROWS - 3):
#             window = colArray[r:r + 4]
#             Score += evaluateWindow(window, piece)

#     # Score positive diagonals
#     for r in range(ROWS - 3):
#         for c in range(COLS - 3):
#             window = [board[r + i][c + i] for i in range(4)]
#             Score += evaluateWindow(window, piece)

#     # Score negative diagonals
#     for r in range(ROWS - 3):
#         for c in range(COLS - 3):
#             window = [board[r + 3 - i][c + i] for i in range(4)]
#             Score += evaluateWindow(window, piece)

#     return Score

# def minimax(board, depth, alpha, beta, maximizingPlayer):
#     validLocations = getValidLocations(board)
#     isTerminal = is_terminal_node(board)

#     if depth == 0 or isTerminal:
#         if isTerminal:
#             if winningMove(board, AI_PIECE):
#                 return (None, 10000000)
#             elif winningMove(board, PLAYER_PIECE):
#                 return (None, -10000000)
#             else:
#                 return (None, 0)
#         else:
#             return (None, score_position(board, AI_PIECE))

#     if maximizingPlayer:
#         value = -math.inf
#         column = random.choice(validLocations)

#         for col in validLocations:
#             row = getNextOpenRow(board, col)
#             b_copy = board.copy()
#             dropPiece(b_copy, row, col, AI_PIECE)
#             new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
#             if new_score > value:
#                 value = new_score
#                 column = col
#             alpha = max(value, alpha)
#             if alpha >= beta:
#                 break

#         return column, value

#     else:
#         value = math.inf
#         column = random.choice(validLocations)
#         for col in validLocations:
#             row = getNextOpenRow(board, col)
#             b_copy = board.copy()
#             dropPiece(b_copy, row, col, PLAYER_PIECE)
#             new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
#             if new_score < value:
#                 value = new_score
#                 column = col
#             beta = min(value, beta)
#             if alpha >= beta:
#                 break
#         return column, value
    
#     def getValidLocations(board):
#     valid_locations = []

#     for column in range(COLS):
#         if isValidLocation(board, column):
#             valid_locations.append(column)

#     return valid_locations


# def end_game():
#     global game_over
#     game_over = True
#     print(game_over)


# while not game_over:
#     if turn == 0:
#         col = int(input("Player 1, Make your Selection(0-6):"))
#         if isValidLocation(board, col):
#             row = getNextOpenRow(board, col)
#             dropPiece(board, row, col, PLAYER_PIECE)
#             turn = 1
#     else:
#         # AI player's turn
#         depth = 4  # Depth of minimax search, you can adjust this
#         start_time = time.time()
#         col, _ = minimax(board, depth, -math.inf, math.inf, True)
#         end_time = time.time()
#         print(f"AI Player's move took {end_time - start_time:.3f} seconds")
#         if isValidLocation(board, col):
#             row = getNextOpenRow(board, col)
#             dropPiece(board, row, col, AI_PIECE)
#             turn = 0

#     print_board(board)
#     if winningMove(board, PLAYER_PIECE):
#         print("Player 1 wins!")
#         end_game()
#     elif winningMove(board, AI_PIECE):
#         print("AI Player wins!")
#         end_game()
#     elif len(getValidLocations(board)) == 0:
#         print("It's a tie!")
#         end_game()



