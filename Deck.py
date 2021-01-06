import random

class Quiz():

	def __init__(self, id, start_time, cards, results):
		self.id = id
		self.start_time = start_time
		self.end_time = datetime.now()
		self.cards = cards
		self.results = results

	def to_dict(self):
		start_time_string = self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
		end_time_string = self.end_time.strftime("%m/%d/%Y, %H:%M:%S")
		cards_dict = [c.to_dict() for c in self.cards]
		dict = {"id": self.id, "start_time": start_time_string, "end_time": end_time_string, "cards": cards_dict, "results": self.results}
		return dict

	def from_dict(self, dict):
		self.id = dict["id"]
		self.start_time = datetime.strptime(dict["start_time"], "%m/%d/%Y, %H:%M:%S")
		self.end_time = datetime.strptime(dict["end_time"], "%m/%d/%Y, %H:%M:%S")
		self.cards = [Card(0,0,0).from_dict(c) for c in dict["cards"]]
		self.results = dict["results"]
		return self

	def save(self, deckname):
		filename = deckname + "-Q" + str(self.id) + ".json"
		f = open("quiz-logs/" + filename, "w+")
		dict_string = json.dumps(self.to_dict())
		f.write(dict_string)
		f.close()

	def load(self, deckname, id):
		filename = deckname + "-Q" + str(id) + ".json"
		f = open("quiz-logs/" + filename, "r")
		fr = f.read()
		f.close()
		dict = json.loads(fr)
		self.from_dict(dict)
		return self

class Deck():

	def __init__(self, name):
		self.name = name
		self.num_cards = 0
		self.cards = []
		self.due_cards = []
		self.num_quizzes = 0
		self.quizzes = []
		self.settings = {
			"correct-multiplier": 1.5,
			"incorrect-multiplier": 0.2,
			"max-wait": 31557600,
			"min-wait": 5,
			"initial-wait": 5
		}

	def add_card(self, prompt, answer):
		self.num_cards += 1
		card = Card(self.num_cards, prompt, answer, initial_wait=timedelta(seconds = self.settings["initial-wait"]))
		self.cards.append(card)

	def add_quiz(self, start_time, cards, results):
		self.num_quizzes += 1
		quiz = Quiz(self.num_quizzes, start_time, cards, results)
		self.quizzes.append(quiz)

	def check_due_cards(self):
		self.due_cards = [c.id for c in self.cards if c.is_due()]
		return self.due_cards

	def quiz(self):
		start_time = datetime.now()
		shuffled_cards = [self.cards[id-1] for id in self.due_cards]
		card_copies = [Card(0,0,0).from_dict(c.to_dict()) for c in shuffled_cards]
		random.shuffle(shuffled_cards)
		results = {}
		min_wait = timedelta(seconds = self.settings["min-wait"])
		max_wait = timedelta(seconds = self.settings["max-wait"])
		for c in shuffled_cards:
			correct = c.quiz()
			results[c.id] = correct
			multiplier = self.settings["incorrect-multiplier"]
			if correct: multiplier = self.settings["correct-multiplier"]
			c.update_wait(multiplier, min_wait, max_wait)
		self.add_quiz(start_time, card_copies, results)

	def to_dict(self):
		cards_dict = [c.to_dict() for c in self.cards]
		quizzes_dict = [q.to_dict() for q in self.quizzes]
		dict = {
			"name": self.name,
			"num_cards": self.num_cards,
			"cards": cards_dict,
			"due_cards": self.due_cards,
			"num_quizzes": self.num_quizzes,
			"settings": self.settings	
		}
		return dict

	def from_dict(self, dict):
		self.name = dict["name"]
		self.num_cards = dict["num_cards"]
		self.cards = [Card(0,0,0).from_dict(c) for c in dict["cards"]]
		self.due_cards = dict["due_cards"]
		self.num_quizzes = dict["num_quizzes"]
		self.settings = dict["settings"]
		return self

	def save(self):
		filename = "deck-" + self.name + ".json"
		f = open("decks/" + filename, "w+")
		dict_string = json.dumps(self.to_dict())
		f.write(dict_string)
		f.close()
		
	def load(self, deckname):
		filename = "deck-" + deckname + ".json"
		f = open("decks/" + filename, "r")
		fr = f.read()
		f.close()
		dict = json.loads(fr)
		self.from_dict(dict)
		return self
