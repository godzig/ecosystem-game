# Copyright 2021 Mike Godwin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from game import Game
from absl import logging


class Scenario(object):
  """ Scenario runs a number of games.

  Args:
      games: Number of boards to return. ie. a 3 player game will return 3
        boards.
      players: Number of players. Accepts 3-6 players.
      floor: Minimum score that must be attained to include the game in result
        set.
  """

  def __init__(self, **kwargs):

    boards = kwargs.get('boards', 10)
    players = kwargs.get('players', 3)
    floor = kwargs.get('floor', -10)
    logging.info('Scenario initialized. boards: %d players: %d floor: %d',
                 boards, players, floor)

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
