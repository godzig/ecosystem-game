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
""" Simulation of the Ecosystem game by Genius Games.

Generates endgame board scenarios.
"""

from player import Player

from random import shuffle
from absl import logging


class Game(object):

  def __init__(self, id, players=3):
    self.cardset = set([
        'bear', 'bee', 'meadow', 'trout', 'eagle', 'rabbit', 'dragonfly', 'fox',
        'deer', 'stream', 'wolves'
    ])
    self.deck = ['bear']   * 12 + \
       ['bee']   * 8 + \
       ['meadow']   * 20 + \
       ['trout']   * 10 + \
       ['eagle']   * 8 + \
       ['rabbit']   * 8 + \
       ['dragonfly']  * 8 + \
       ['fox']   * 12 + \
       ['deer']   * 12 + \
       ['stream']   * 20 + \
       ['wolves']   * 12
    if players < 3 or players > 6:
      logging.fatal('There must be 3-6 players.')
    self.players = players
    self.id = id
    self._deal()
    self._scoreGame()

  def _deal(self):
    shuffle(self.deck)
    players = []
    for p in range(self.players):
      board = self.deck[p * 20:(p + 1) * 20]
      score = {card: 0 for card in self.cardset}
      players.append(Player(board, score))
    self.players = players

  def _scoreGame(self):
    for player in self.players:
      for card in self.cardset - set(['dragonfly']):
        if card in player.board:
          player.score[card] = self._cardScore(card, player)
      if 'dragonfly' in player.board:
        player.score['dragonfly'] = self._cardScore('dragonfly', player)

    # build wolf payout: 12/ 8/ 4 for most wolves
    wolfCounts = [player.score['wolves'] for player in self.players]
    wolf_1 = max(wolfCounts)
    wolfPayout = {}
    if wolfCounts.count(wolf_1) > 2:
      wolfPayout[wolf_1] = 12
    elif wolfCounts.count(wolf_1) == 2:
      wolfCounts.remove(wolf_1)
      wolfCounts.remove(wolf_1)
      wolf_2 = max(wolfCounts)
      wolfPayout[wolf_1] = 12
      wolfPayout[wolf_2] = 4
    elif wolfCounts.count(wolf_1) == 1:
      wolfCounts.remove(wolf_1)
      wolf_2 = max(wolfCounts)
      if wolfCounts.count(wolf_2) > 1:
        wolfPayout[wolf_1] = 12
        wolfPayout[wolf_2] = 8
      else:
        wolfCounts.remove(wolf_2)
        wolf_3 = max(wolfCounts)
        wolfPayout[wolf_1] = 12
        wolfPayout[wolf_2] = 8
        wolfPayout[wolf_3] = 4
    wolfPayout[0] = 0

    # build stream payout. 8/5 for longest streams
    streamCounts = [player.score['stream'] for player in self.players]
    stream_1 = max(streamCounts)
    streamPayout = {}
    if streamCounts.count(stream_1) > 1:
      streamPayout[stream_1] = 8
    else:
      streamCounts.remove(stream_1)
      stream_2 = max(streamCounts)
      streamPayout[stream_1] = 8
      streamPayout[stream_2] = 5
    streamPayout[0] = 0

    # assign each player scores for streams, wolves and gaps
    for player in self.players:
      player.score['stream'] = streamPayout.get(player.score['stream'], 0)
      player.score['wolves'] = wolfPayout.get(player.score['wolves'], 0)
      gaps = len([_ for _ in player.score.values() if _ == 0])
      gapPayout = {0: 12, 1: 12, 2: 12, 3: 7, 4: 3, 5: 0, 6: -6}
      player.score['gaps'] = gapPayout.get(gaps, -6)

  def _cardScore(self, card, player):
    board = player.board
    score = 0
    positions = [i for (i, j) in enumerate(board) if j == card]

    if card == 'bear':
      for bear in positions:
        score += 2 * self._adjacent(board, bear, ['trout', 'bee'])

    if card == 'bee':
      for bee in positions:
        score += 3 * self._adjacent(board, bee, ['meadow'])

    if card == 'trout':
      for trout in positions:
        score += 2 * self._adjacent(board, trout, ['dragonfly', 'stream'])

    if card == 'fox':
      for fox in positions:
        if self._adjacent(board, fox, ['bear', 'wolves']) == 0:
          score += 3

    if card == 'rabbit':
      score += 1 * len(positions)

    if card == 'eagle':
      for eagle in positions:
        score += 2 * self._adjacent(board, eagle, ['trout', 'rabbit'], True)

    if card == 'deer':
      score += 2 * self._deerLines(board, positions)

    if card == 'wolves':
      score = len(positions)

    if card == 'stream':
      player.streams = self._getAreas(positions)
      score = max([len(stream) for stream in player.streams])

    if card == 'meadow':
      player.meadows = self._getAreas(positions)
      meadowPayout = {1: 0, 2: 3, 3: 6, 4: 10, 5: 15}
      score = sum([meadowPayout.get(len(m), 15) for m in player.meadows])

    # - dragonfly: points for length of adj streams
    if card == 'dragonfly':
      for dragonfly in positions:
        for stream in player.streams:
          for s in stream:
            if self._checkAdjacent(dragonfly, s):
              score += len(stream)
              break

    return score

  def _getAreas(self, positions):
    areas = []
    merged = False
    while positions:
      area = [positions.pop()]
      for index in positions:
        if self._checkAdjacent(area[0], index):
          area.append(index)
          positions.remove(index)
      for i, group in enumerate(areas):
        for g in group:
          if self._checkAdjacent(area[0], g):
            areas[i] = group.union(set(area))
            merged = True
      if not merged:
        areas.append(set(area))
      merged = False
    return (areas)

  def _checkAdjacent(self, index1, index2):
    # check above
    if index1 > 4 and index2 + 5 == index1:
      return True
    # check below
    elif index1 < 15 and index2 - 5 == index1:
      return True
    # check right
    elif index1 not in [4, 9, 14, 19] and index2 - 1 == index1:
      return True
    # check left
    elif index1 not in [0, 5, 10, 15] and index2 + 1 == index1:
      return True
    else:
      return False

  def _adjacent(self, board, index, cards, eagle=False):
    #   0   1   2   3   4
    #   5   6   7   8   9
    #   10  11  12  13  14
    #   15  16  17  18  19
    adjacent_count = 0

    # check above
    if index > 4 and board[index - 5] in cards:
      adjacent_count += 1
    # check below
    if index < 15 and board[index + 5] in cards:
      adjacent_count += 1
    # check right
    if index not in [4, 9, 14, 19] and board[index + 1] in cards:
      adjacent_count += 1
    # check left
    if index not in [0, 5, 10, 15] and board[index - 1] in cards:
      adjacent_count += 1

    if eagle:
      # check far above
      if index > 9 and board[index - 10] in cards:
        adjacent_count += 1
      # check far below
      if index < 10 and board[index + 10] in cards:
        adjacent_count += 1
      # check far right
      if index not in [3, 4, 8, 9, 13, 14, 18, 19
                      ] and board[index + 2] in cards:
        adjacent_count += 1
      # check far left
      if index not in [0, 1, 5, 6, 10, 11, 15, 16
                      ] and board[index - 2] in cards:
        adjacent_count += 1
      # check upper right
      if index > 4 and index not in [4, 9, 14, 19
                                    ] and board[index - 4] in cards:
        adjacent_count += 1
      # check lower right
      if index < 15 and index not in [4, 9, 14, 19
                                     ] and board[index + 6] in cards:
        adjacent_count += 1
      # check lower left
      if index < 15 and index not in [0, 5, 10, 15
                                     ] and board[index + 4] in cards:
        adjacent_count += 1
      # check upper left
      if index > 4 and index not in [0, 5, 10, 15
                                    ] and board[index - 6] in cards:
        adjacent_count += 1
    return adjacent_count

  def _deerLines(self, board, positions):
    rows = [
        set([0, 1, 2, 3, 4]),
        set([5, 6, 7, 8, 9]),
        set([10, 11, 12, 13, 14]),
        set([15, 16, 17, 18, 19])
    ]
    cols = [
        set([0, 5, 10, 15]),
        set([1, 6, 11, 16]),
        set([2, 7, 12, 17]),
        set([3, 8, 13, 18]),
        set([4, 9, 14, 19])
    ]
    count = 0
    for row in rows:
      if set(positions) & row:
        count += 1
    for col in cols:
      if set(positions) & col:
        count += 1
    return count

  def print(self):
    for p in self.players:
      print(p.total())
      print(p.score)
      print(p.board[:5])
      print(p.board[5:10])
      print(p.board[10:15])
      print(p.board[15:20])
      print('\n')

  def report(self):
    results = []
    for p in self.players:
      readout = p.score.copy()
      readout['game'] = self.id
      readout['total'] = p.total()
      readout['board'] = p.board
      results.append(readout)
    return results
