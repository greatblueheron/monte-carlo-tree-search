import time
import numpy as np
from multiprocessing import Pool, Process, Manager
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
# from mctspy.games.examples.tictactoe import TicTacToeGameState
from mctspy.games.examples.influencers import InfluencersGameState
from mctspy.games.compute_winner.winner import Winner

num_trials = 20

red_search_depth = 100
blue_search_depth = 1


def competition_with_fixed_token_number(num_tokens, return_dict=None):

    print('beginning trials with num_tokens=', num_tokens)
    red_results = 0
    blue_results = 0
    draw_results = 0
    start = time.time()
    for each_trial in range(num_trials):    # could prob easy multithread this
        winner = Winner()  # create new random board for each game
        state = np.zeros(winner.vertex_count)
        unplayed_tokens = [1] * num_tokens
        # list of all tokens numbered by type; should be symmetric red <-> blue
        unplayed_tokens.extend([-each for each in unplayed_tokens])
        next_to_move = 1   # red = +1 goes first

        board_state = InfluencersGameState(state=state,
                                           unplayed_tokens=unplayed_tokens,
                                           next_to_move=next_to_move)

        # print("Let's play a game, better AI goes first.")
        for turn in range(len(unplayed_tokens)):
            # print('turn #', turn)
            root = TwoPlayersGameMonteCarloTreeSearchNode(state=board_state)
            mcts = MonteCarloTreeSearch(root)
            if turn % 2 == 0:   # even turns
                best_node = mcts.best_action(red_search_depth)
            else:
                best_node = mcts.best_action(blue_search_depth)
            board_state = best_node.state
            # print('board is now', best_node.state.board)
            # print('winner was', best_node.state.game_result)
            if best_node.state.game_result == 1:
                red_results += 1
            if best_node.state.game_result == -1:
                blue_results += 1
            if best_node.state.game_result == 0:
                draw_results += 1
    print('trials for', num_tokens, 'took', (time.time() - start) / 60., 'minutes.')
    if return_dict is None:
        return [red_results, blue_results, draw_results]
    else:
        return_dict[num_tokens] = [red_results, blue_results, draw_results]


def main():

    max_red_tokens = 8
    mp = True

    total_start = time.time()

    if mp:
        manager = Manager()
        return_dict = manager.dict()
        # with Pool(max_red_tokens) as p:
        #     results = p.map(competition_with_fixed_token_number, range(1, max_red_tokens+1))
        jobs = []
        for k in range(max_red_tokens):
            pr = Process(target=competition_with_fixed_token_number, args=(k+1, return_dict))
            jobs.append(pr)
            pr.start()
        for k in range(max_red_tokens):
            jobs[k].join()
        # 10v1 [[13, 4, 3], [13, 6, 1], [13, 6, 1], [18, 2, 0], [16, 4, 0], [15, 2, 3], [12, 7, 1], [20, 0, 0]]
        # 100v1 {1: [19, 0, 1], 2: [20, 0, 0], 3: [14, 5, 1], 4: [18, 0, 2], 5: [20, 0, 0], 6: [18, 1, 1], 7: [20, 0, 0], 8: [20, 0, 0]}
    else:
        return_dict = {}
        for k in range(1, max_red_tokens+1):
            ret = competition_with_fixed_token_number(num_tokens=k)
            return_dict[k] = ret

    # 6 minutes for 10v1 20 trial mp, 50 minutes for 100v1 20 trial mp
    print('Total time was', (time.time() - total_start)/60., 'minutes.')
    print(return_dict)

    print('')


if __name__ == "__main__":
    main()

