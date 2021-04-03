from random import shuffle

class Game(object):
	"""Generate endgame states in Ecosystem by Genius Games"""
	def __init__(self, players = 3):
		self.cardset = set(['bear','bee','meadow','trout','eagle','rabbit','dragonfly','fox','deer','stream','wolves'])
		self.deck = ['bear'] 		* 12 + \
					['bee'] 		* 8 + \
					['meadow'] 		* 20 + \
					['trout'] 		* 10 + \
					['eagle'] 		* 8 + \
					['rabbit'] 		* 8 + \
					['dragonfly'] 	* 8 + \
					['fox'] 		* 12 + \
					['deer'] 		* 12 + \
					['stream'] 		* 20 + \
					['wolves'] 		* 12
		self.wolfCounts = []
		self.streamCounts = []
		if players < 3 or players > 6:
			raise Exception('There must be 3-6 players.')
		self.players = players
		self.deal()
		self.scoreGame()


	def deal(self):
		shuffle(self.deck)
		players = []
		for p in range(self.players):
			board = self.deck[ p*20 : (p+1)*20 ]
			score = { card: 0 for card in self.cardset }
			players.append(Player(board, score))
		self.players = players


	def scoreGame(self):
		for player in self.players:
			for card in self.cardset:
				if card in player.board:
					player.score[card] = self.cardScore(card, player.board)
			self.wolfCounts.append(player.score['wolves'])
			self.streamCounts.append(player.score['stream'])

		# resolve wolves 12/ 8/ 4 for most wolves
		# resolve streams 8/5 for longest stream
		# Gaps 6+, 5, 4, 3, 2
		# Points -6, 0, 3, 7, 12


	def cardScore(self, card, board):
		score = 0
		positions = [i for (i,j) in enumerate(board) if j==card]

		if card == 'bear':
			for bear in positions:
				score += 2 * self.adjacent(board, bear, ['trout', 'bee'])

		if card == 'bee':
			for bee in positions:
				score += 3 * self.adjacent(board, bee, ['meadow'])

		if card == 'trout':
			for trout in positions:
				score += 2 * self.adjacent(board, trout, ['dragonfly','stream'])

		if card == 'fox':
			for fox in positions:
				if self.adjacent(board, fox, ['bear', 'wolves']) == 0:
					score += 3

		if card == 'rabbit':
			score += 1 * len(positions)

		if card == 'eagle':
			for eagle in positions:
				score += 2 * self.adjacent(board, eagle, ['trout','rabbit'], True)

		if card == 'deer':
			score += 2 * self.deerLines(board, positions)

		if card == 'wolves':
			score = len(positions)

		if card == 'stream':
			score = 0
		# return length of largest stream

		# - stream, 20. largest stream 8/5
		# - dragonfly, 8. points for length of adj streams
		# - meadow, 20. 0/3/6/10/15 for 1/2/3/4/5 adj meadows
		return score


	def adjacent(self, board, index, cards, eagle=False):
		# 	0	1	2	3	4
		# 	5	6	7	8	9
		# 	10	11	12	13	14
		# 	15	16	17	18	19
		adjacent_count = 0

		# check above
		if index > 4 and board[index-5] in cards:
			adjacent_count += 1
		# check below
		if index < 15 and board[index+5] in cards:
			adjacent_count += 1
		# check right
		if index not in [4, 9, 14, 19] and board[index+1] in cards:
			adjacent_count += 1
		# check left
		if index not in [0, 5, 10, 15] and board[index-1] in cards:
			adjacent_count += 1

		if eagle:
			# check far above
			if index > 9 and board[index-10] in cards:
				adjacent_count += 1
			# check far below
			if index < 10 and board[index+10] in cards:
				adjacent_count += 1
			# check far right
			if index not in [3, 4, 8, 9, 13, 14, 18, 19] and board[index+2] in cards:
				adjacent_count += 1
			# check far left
			if index not in [0, 1, 5, 6, 10, 11, 15, 16] and board[index-2] in cards:
				adjacent_count += 1
			# check upper right
			if index > 4 and index not in [4, 9, 14, 19] and board[index-4] in cards:
				adjacent_count += 1
			# check lower right
			if index < 15 and index not in [4, 9, 14, 19] and board[index+6] in cards:
				adjacent_count += 1
			# check lower left
			if index < 15 and index not in [0, 5, 10, 15] and board[index+4] in cards:
				adjacent_count += 1
			# check upper left
			if index > 4 and index not in [0, 5, 10, 15] and board[index-6] in cards:
				adjacent_count += 1
		return adjacent_count


	def deerLines(self, board, positions):
		rows = [set([0,1,2,3,4]), set([5,6,7,8,9]), set([10,11,12,13,14]), set([15,16,17,18,19])]
		cols = [set([0,5,10,15]), set([1,6,11,16]), set([2,7,12,17]), set([3,8,13,18]), set([4,9,14,19])]
		count = 0
		for row in rows:
			if set(positions) & row:
				count += 1
		for col in cols:
			if set(positions) & col:
				count += 1
		return count


	def write(self):
		for p in self.players:
			print(p.total())
			print(p.score)
			print(p.board[:5])
			print(p.board[5:10])
			print(p.board[10:15])
			print(p.board[15:19])
			print('\n')



class Player(object):

	def __init__(self, board, score):
		self.board = board
		self.score = score


	def total(self):
		return sum([v for v in self.score.values()])

if __name__ == '__main__':
	g = Game()
	g.write()
