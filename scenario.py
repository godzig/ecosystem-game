import time
import pandas as pd
from ecosystem import Game


class Scenario(object):

    def __init__(self, **kwargs):
        """
        Scenario runs a number of games.

        :param int games: Number of games to return. ie. one 3 player game will return 3 boards.
        :param int players: Number of players. Accepts 3-6 players.
        :param int floor: Minimum score that must be attained to include the game in result set.

        """
        boards = kwargs.get('games', 10)
        players = kwargs.get('players', 3)
        floor = kwargs.get('floor', -10)
        self.results = []
        index = 0
        while len(self.results) < boards:
            run = Game(index, players)
            outcome = run.report()
            top_score = max([outcome[p]['total'] for p in range(players)])
            if top_score >= floor:
                self.results.extend(run.report())
                index += 1

    def report(self):
        return self.results


if __name__ == '__main__':
    start_time = time.time()
    s = Scenario(games=1, players=3, floor=-100)
    df = pd.DataFrame(s.report())
    df.to_csv('output.csv', mode='w', header=True)
    print('{} seconds'.format(time.time() - start_time))
