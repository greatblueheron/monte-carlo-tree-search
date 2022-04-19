import numpy as np
from mctspy.games.common import TwoPlayersAbstractGameState, AbstractGameAction
from mctspy.games.compute_winner.winner import Winner


# not sure if this is the right way to do this?
winner = Winner()


class InfluencersMove(AbstractGameAction):
    def __init__(self, idx, token, player):
        # player was 'value', changed it; player = +1 (red) or -1 (blue)
        # token is a pointer to which type of token is placed (assuming each player has more than one type)
        # idx is a 1-D index of game board position; currently these are where tokens can be placed
        self.idx = idx
        self.token = token
        self.player = player

    def __repr__(self):
        # like idx:12 t:-2 p:-1 means blue places token -2 on board position 12
        # tokens are -ive for blue and +ive for red
        return "idx:{0} t:{1} p:{2}".format(self.idx, self.token, self.player)


class InfluencersGameState(TwoPlayersAbstractGameState):

    # used to be x and o respectively
    red = 1
    blue = -1

    def __init__(self, state, unplayed_tokens, next_to_move=1):
        # initial state is np.zeros(number_of_sites)

        # next_to_move is whose turn it is to move
        self.board = state
        self.unplayed_tokens = unplayed_tokens
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        # check if game is over.
        # this is whatever determines if the game is over; in this case, all tokens placed
        if len(self.unplayed_tokens) == 0:
            # this function returns +1 if red won, -1 if blue won, and 0 if draw
            return winner.winner(self.board)
        else:   # game not over - no result
            return None

    def is_game_over(self):
        # return self.game_result is not None   # might be better to use len(self.unplayed_tokens)
        return len(self.unplayed_tokens) == 0

    def is_move_legal(self, move):   # move is an action "idx: _ t: _ p: _"
        # check if correct player moves
        if move.player != self.next_to_move:
            return False

        # check if correct token sign
        if np.sign(move.player) != np.sign(move.token):
            return False

        # check if token available to play
        if move.token not in self.unplayed_tokens:
            return False

        # check if inside the board
        if not 0 <= move.idx < len(self.board):
            return False

        # finally check if board field not occupied yet
        return self.board[move.idx] == 0

    def move(self, move):   # move is an action "idx: _ t: _ p: _"
        if not self.is_move_legal(move):
            raise ValueError(
                "move {0} on board {1} is not legal". format(move, self.board)
            )
        new_board = np.copy(self.board)
        new_unplayed_tokens = self.unplayed_tokens.copy()

        # place token on game state, remove it from unplayed_tokens
        new_board[move.idx] = move.token   # I think this is right, as long as we choose token indices right
        new_unplayed_tokens.remove(move.token)

        if self.next_to_move == InfluencersGameState.red:
            next_to_move = InfluencersGameState.blue
        else:
            next_to_move = InfluencersGameState.red

        return InfluencersGameState(new_board, new_unplayed_tokens, next_to_move)

    def get_legal_actions(self):
        indices = np.where(self.board == 0)[0]   # double check this is doing what I think it is
        # we have to ask about tokens played here, and track that
        tokens_available = [each for each in self.unplayed_tokens if np.sign(each) == self.next_to_move]
        # I think this returns all the moves from all the available tokens to all the available positions
        return [InfluencersMove(coords, tokens, self.next_to_move) for coords in indices for tokens in tokens_available]
