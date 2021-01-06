class Session():

	def __init__(self):
		self.decklist = []
		self.decks = {}
		self.current_deck = False
		self.settings = {
			"input-prompt": "-> ",
			"ignore-decks": []
		}
		self.error_messages = {
			"no-deck-open": "You haven't opened a deck yet! Type `open-deck` [deckname] to open a deck.",
			"unknown-command": "That isn't a valid command.",
			"no-due-cards": "No cards are due in this deck!"
		}

	def error_message(self, error_name):
		print(self.error_messages[error_name])

	def add_deck(self, name):
		self.decklist.append(name)
		self.decks[name] = Deck(name)

	def list_decks(self):
		for name in self.decklist:
			print(name)

	def open_deck(self, deckname):
		self.current_deck = self.decks[deckname]

	def close_deck(self):
		self.current_deck = False

	def add_cards(self, num_cards=1):
		if self.current_deck:
			for i in range(0, int(num_cards)):
				prompt = input("Card prompt: ")
				answer = input("Correct answer: ")
				self.current_deck.add_card(prompt, answer)
		else:
			self.error_message("no-deck-open")

	def quiz(self):
		if self.current_deck:
			deck = self.current_deck
			if deck.check_due_cards():
				deck.quiz()
			else:
				self.error_message("no-due-cards")	
		else:
			self.error_message("no-deck-open")

	def listen_loop(self):
		self.load()
		self.command_guide = {
			"add-deck": self.add_deck,
			"list-decks": self.list_decks,
			"open-deck": self.open_deck,
			"close-deck": self.close_deck,
			"add-card": self.add_cards,
			"quiz": self.quiz,
			"exit": lambda: print("Exiting...")		
		}

		command = ""
		while command != "exit":
			command_input = input(self.settings["input-prompt"])
			command_strings = command_input.split(" ")
			command = command_strings[0]
			args = command_strings[1:]
			if command in self.command_guide:
				self.command_guide[command](*args)
			else:
				self.error_message("unknown-command")

		self.save()
		for name in self.decks:
			self.decks[name].save()

	def to_dict(self):
		dict = {"decklist": self.decklist, "settings": self.settings}
		return dict

	def from_dict(self, dict):
		self.decklist = dict["decklist"]
		self.settings = dict["settings"]

	def save(self):
		filename = "session-data.json"
		f = open(filename, "w+")
		dict_string = json.dumps(self.to_dict())
		f.write(dict_string)
		f.close()

	def load(self):
		filename = "session-data.json"
		try:
			f = open(filename, "r")
			fr = f.read()
			f.close()
			dict = json.loads(fr)
			self.from_dict(dict)
			self.decks = {name: Deck(0).load(name) for name in self.decklist}
		except IOError:
			print("No preexisting data found. You must be a new user!")
		return self
