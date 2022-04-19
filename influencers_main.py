import time
import numpy as np
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
# from mctspy.games.examples.tictactoe import TicTacToeGameState
from mctspy.games.examples.influencers import InfluencersGameState


start = time.time()

state = np.zeros(16)
# not sure if these should go here

# TODO: change this to be the full list
# TODO: implement random player to play against
initial_game_token_list = [1, 1]

# initial_game_token_list is a list of red's tokens numbered from 1 up by type, eg. [1,1,1,2,2]
# means 3 tokens of type 1 and 2 tokens of type 2; assumption of symmetry with blue
unplayed_tokens = [c * (-1) ** p  # red +ive, blue -ive
                   for p in range(2)
                   for c in initial_game_token_list]

initial_board_state = InfluencersGameState(state=state,
                                           unplayed_tokens=unplayed_tokens,
                                           next_to_move=1)

root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial_board_state)
mcts = MonteCarloTreeSearch(root)
best_node = mcts.best_action(100)
print('run took', time.time() - start, 'seconds.')
print('')

not_done = True
print("Let's play a game, AI goes first.")
while not_done:
    pass
