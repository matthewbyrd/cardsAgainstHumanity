"""
Filename: 	cah.py 
Author: 	Matthew Bird

A 1-4 player game of Cards-Against Humanity. 

Formed of two core object-types: Game and Player. The Game generates answer cards -- phrases
which contain a blank or have an answer -- and the Players take it in turns to supply an answer 
card from their hands to fill in the blank or answer the question in the most humorous way possible.

"""

import random 
import os

questions = open('questions.txt').read().splitlines()
answers = open('answers.txt').read().splitlines()

class Game(object):
	"""
	Generates questions and governs the logic of player turns.
	"""

	def __init__(self, questions, answers):
		self.players = []
		self.questions = questions
		self.answers = answers
		self.current_question = ""

	def get_question(self):
		"""
		Generates a random question.
		"""
		self.current_question = random.choice(self.questions) 

	def player_turn(self, player):
		"""
		Prompt the last player to pass the computer to the next player.
		Deal that player the current question and shows their hand.
		Prompt the player to make a choice, save the choice, remove it from their hand.
		Deal the player a new card.
		"""
		os.system('clear')
		raw_input("%s, press enter!" % player.name)
		os.system('clear')
		print "QUESTION:"
		print "*" * 10
		print self.current_question
		print "*" * 10
		print "\n"
		print "HAND:"
		print "*" * 10
		player.get_cards()
		bullet = 1
		for card in player.hand:
			print "%s. %s" %(bullet, card)
			bullet+=1
		print "\n"
		choice = int(raw_input("Choose a card number to play: "))
		player.current_answer = player.hand[choice-1]
		player.hand.remove(player.hand[choice-1])
		player.get_cards()


	def round(self):
		"""
		Run a turn for each player in the game.
		"""

		self.get_question()
		for player in self.players:
			self.player_turn(player)
		self.results()

	def results(self):
		"""
		Display the results of a round.
		"""
		os.system('clear')
		print "RESULTS:"
		print "*" * 10
		print "The question was: \n"
		print self.current_question
		print "\n"
		print "*" * 10
		for player in self.players:
			raw_input(player.name + "'s answer:  "),
			print player.generate_answer()
			print "*" * 10



class Player(object):
	"""
	Deal answer cards and constructs answers using them.
	"""

	def __init__(self, name, game):
		self.name = name
		self.game = game
		self.games_won = 0
		self.hand = []
		self.current_answer = ""
		self.discard_limit = 0



	def get_cards(self):
		"""
		Deal cards to the player until the player has 7 cards in the hand.
		"""

		while len(self.hand) < 7:
			new_choice = random.choice(self.game.answers)
			self.hand.append(new_choice)


	def generate_answer(self):
		"""
		Insert the player's choice into the current question, depending on question type.
		"""

		answer = " ["+ self.current_answer + "]"
		question = self.game.current_question

		if " __________" in self.game.current_question:
			self.current_answer = question.replace(' __________', answer)
		elif "__________" in question and " __________" not in question:
			self.current_answer = question.replace('__________', answer)
		else:
			answer = " [" + answer[2].upper() + answer[3:]	#capitalize answer
			self.current_answer = question + answer+"."
		return self.current_answer


	def discard_a_card(self):
		pass


if __name__ == '__main__':
	# Make the game object
	game = Game(questions, answers)

	# Set up the players depending on how many there are
	number_of_players = int(raw_input("How many players do you have (up to 4)? "))
	name = raw_input("Player 1 name: ")
	player1 = Player(name, game)
	game.players.append(player1)
	if number_of_players > 1:
		name = raw_input("Player 2 name: ")
		player2 = Player(name, game)
		game.players.append(player2)
	if number_of_players > 2:
		name = raw_input("Player 3 name: ")
		player3 = Player(name, game)
		game.players.append(player3)
	if number_of_players > 3:
		name = raw_input("Player 4 name: ")
		player4 = Player(name, game)
		game.players.append(player4)

	# Run the game
	play = True
	while play:
		game.round()
		play_answer = raw_input("Play another round? Y/N  >")
		if play_answer.upper() == "Y":
			play = True
		else:
			play = False
