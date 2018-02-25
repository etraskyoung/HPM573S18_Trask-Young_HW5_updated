import numpy as np
import scr.FigureSupport as Fig

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin
        self._reward = 0
        self._loss = 0
        self._max = 0
        self._min = 0

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        reward = 100*self._countWins - 250
        self.reward = reward
        return self.reward

    def get_loss(self):
        if self.reward < 0:
            self.loss = 1
        else:
            self.loss = 0
        return self.loss

class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._gameLosses = []
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())
            self._gameLosses.append(game.get_loss())

    def get_gameRewards(self):
        return self._gameRewards

    def get_min(self):
        self.min = min(self._gameRewards)
        return self.min

    def get_max(self):
        self.max = max(self._gameRewards)
        return self.max

    def get_gameLosses(self):
        return self._gameLosses

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)
    
    def get_probability_loss(self):
            """ returns the average reward from all games"""
            return sum(self._gameLosses) / len(self._gameLosses)

# run trail of 1000 games to calculate expected reward
games = SetOfGames(prob_head=0.5, n_games=1000)
# print the average reward
print('Expected reward when the probability of head is 0.5:', games.get_ave_reward())
print('Expected minimum reward when the probability of head is 0.5:', games.get_min())
print('Expected maximum reward when the probability of head is 0.5:', games.get_max())
print('Expected probability of loosing money when the probability of head is 0.5:', games.get_probability_loss())

Fig.graph_histogram(
    observations = games.get_gameRewards(),
    title = 'Histogram of Game Rewards',
    x_label = 'Game Rewards ($)',
    y_label = 'Count')

Fig.graph_histogram(
    observations = games.get_gameLosses(),
    title = 'Histogram of Game Losses',
    x_label = '0 = win ; 1 = loss',
    y_label = 'Count')
