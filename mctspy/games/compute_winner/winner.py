import neal    # requires pip install dwave-ocean-sdk
import random
import numpy as np


class Winner(object):
    def __init__(self):
        self.vertex_count = 16
        self.edge_list = [(0, 2), (0, 3), (0, 8), (0, 10),
                          (1, 2), (1, 3), (1, 9), (1, 11),
                          (2, 8), (2, 9),
                          (3, 10), (3, 11),
                          (4, 8), (4, 10), (4, 12), (4, 14),
                          (5, 9), (5, 11), (5, 13), (5, 15),
                          (6, 8), (6, 9), (6, 12), (6, 13),
                          (7, 10), (7, 11), (7, 14), (7, 15),
                          (12, 13), (12, 14),
                          (13, 15),
                          (14, 15)]
        self.jay = {k: random.choice([-1, 0, 1]) for k in self.edge_list}
        self.h = {k: 0 for k in range(self.vertex_count)}

    def convert(self, state):
        """ converts state to h, jay values, in this format
        h = {0: -1, 1: -1}
        J = {(0, 1): -1}
        initially state will be 16 long with tokens that bias according to their token_idx
        """
        result = np.where(state != 0)[0]   # should be list of non-zero indices
        for each in result:
            self.h[each] = - state[each]    # the minus is there to make sure +1 wins if +1 is played

    def winner(self, state):
        """ returns +1 if red wins, -1 if blue wins, 0 if draw """
        self.convert(state)
        sampler = neal.SimulatedAnnealingSampler()
        sample_set = sampler.sample_ising(self.h, self.jay, num_reads=100)
        return process(sample_set)


def process(sample_set):
    """ utility function to post-process result of sampler
    returns +1 if red wins, -1 if blue wins, 0 if draw """
    best_energy = sample_set.first.energy
    good_states = list(set([tuple(each[0]) for each in sample_set.record if each[1] == best_energy]))
    game_result_list = [sum(each) for each in good_states]
    red_wins = sum(1 for i in game_result_list if i > 0)
    blue_wins = sum(1 for i in game_result_list if i < 0)

    if red_wins > blue_wins:
        return 1
    if blue_wins > red_wins:
        return -1
    else:
        return 0


def main():

    num_trials = 1000
    max_red_tokens = 8

    red_results = [0]*max_red_tokens
    blue_results = [0]*max_red_tokens
    draw_results = [0]*max_red_tokens

    for each_trial in range(num_trials):
        w = Winner()   # create new random board

        # check random token placement statistics
        for num_tokens in range(max_red_tokens):
            state = np.zeros(w.vertex_count)
            for each in range(num_tokens):
                place = random.sample(range(w.vertex_count), 2 * num_tokens)
                for k in place[:num_tokens]:
                    state[k] = 1
                for k in place[num_tokens:]:
                    state[k] = -1

            ret = w.winner(state)
            if ret == 1:
                red_results[num_tokens] += 1
            if ret == -1:
                blue_results[num_tokens] += 1
            if ret == 0:
                draw_results[num_tokens] += 1

    print(red_results)
    print(blue_results)
    print(draw_results)


if __name__ == "__main__":
    main()
