"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # create counters for X and O
    x_counter = 0
    o_counter = 0

    # loop through board and update counter for each space
    for i in board:
        for j in i:
            if j == X:
                x_counter += 1
            elif j == O:
                o_counter += 1
    
    # x gets first move therefore the counter should always be higher or equal
    if x_counter > o_counter:
        return O
    else: 
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # create set to hold board spaces
    possible_moves = set()

    # loop through board to add empty spaces to set
    for i in range(len(board)):
        for j in range(3):
            if board[i][j] == EMPTY:
                empty_space = (i, j)
                possible_moves.add(empty_space)

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check to see whose turn it is, assign it to value
    move = player(board)
    
    # make a deep copy of the board
    board_copy = deepcopy(board)

    # check to see if action on board is actually valid. If no, raise error. If yes, mark spot on deep copy.
    if board[action[0]][action[1]] != EMPTY:
        raise InputError("Action not valid for board.")
    else:
        board_copy[action[0]][action[1]] = move
    
    return board_copy



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check for horizontal wins
    for i in board:
        if i[0] == i[1] and i[1] == i[2]:
            if i[0] != EMPTY:
                return i[0]

    # check for vertical wins
    for x in range(3):
        if board[0][x] == board[1][x] and board[1][x] == board[2][x]:
            if board[0][x] != EMPTY:
                return board[0][x]

    # check for diagonal wins
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] != EMPTY:
            return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] != EMPTY:
            return board[0][2]

    # no winners, return none
    else:
        return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check first to see if there is a winner
    win = winner(board)

    # if there is a winner
    if win != None:
        return True

    # if no winner, check to see if all spots are filled
    else:

        # create counter to count empty spots
        empty_counter = 0

        # loop through spots
        for i in range(len(board)):
            for j in range(3):
                if board[i][j] == EMPTY:
                    empty_counter += 1

        # if empty counter greater than 0 game is over
        if empty_counter > 0:
            return False
        else:
            return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # declare the winner
    the_winner = winner(board)

    # set conditions
    if the_winner == None:
        return 0
    elif the_winner == X:
        return 1
    else:
        return -1

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # if the game is over then it is no ones turn
    if terminal(board):
        return None
    
    # else if player X turn
    elif player(board) == X:
        value, move = max_value(board)
        return move

    # else if player Y turn
    else:
        value, move = min_value(board)
        return move


def max_value(board):
    # if end of game return none
    if terminal(board):
        return utility(board), None

    # set variable to negative infinity, as all values will be higher
    v = float('-inf')

    # set a variable to track the ideal move
    move = None

    # loop through actions
    for action in actions(board):

        # run the program to see what the min player would do. Record utility value and action/move.
        temp, min_act = min_value(result(board, action))

        # if value is greater than v
        if temp > v:

            # set v to temp value
            v = temp

            # set move to the current action
            move = action

            # identify and return the move that garantees a win
            if v == 1:
                return v, move

    # return the next best
    return v, move


def min_value(board):

    # if game over return none
    if terminal(board):
        return utility(board), None

    # set variable to infinity since everything will be lower
    v = float('inf')

    # set variable to track the ideal move
    move = None

    # loop through actions
    for action in actions(board):

        # run the equation to see what the max player would do. Record the value and action/move
        temp, max_act = max_value(result(board, action))

        # if this is a better option
        if temp < v:

            # assign v to better option
            v = temp

            # set move to the best action
            move = action

            # if the move garantees a win, return move
            if v == -1:
                return v, move

    # return best option
    return v, move
