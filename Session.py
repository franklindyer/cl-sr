class Session():

	def __init__(self):
		self.decklist = []
		self.decks = {}
		self.current_deck = False
		self.settings = {
			"ignore-decks": [],
			"input-prompt": "->"
		}
		self.error_messages = {
			"no-deck-open": "You haven't opened a deck yet! \nType `open-deck` [deckname] to open a deck.",
			"unknown-command": "That isn't a valid command.",
			"no-due-cards": "No cards are due in this deck!",
			"no-such-deck": "No records of such a deck exist.",
			"deck-ignored": "This deck hasn't been loaded because you've ignored it. \nRun `unignore-deck [deckname]` to unignore it."
		}

	def error_message(self, error_name):
		print(self.error_messages[error_name])

	def due_report(self):
		for name in self.decks:
			deck = self.decks[name]
			due_cards = deck.check_due_cards()
			num_due = len(due_cards)
			print("Deck {}: {} cards due".format(name, num_due))

	def add_deck(self, name):
		self.decklist.append(name)
		self.decks[name] = Deck(name)

	def list_decks(self):
		for name in self.decklist:
			end = "\n"
			if name in self.settings["ignore-decks"]: end = " (ignored)\n"
			print(name, end=end)

	def open_deck(self, deckname):
		if deckname in self.decks:
			self.current_deck = self.decks[deckname]
		elif deckname in self.settings["ignore-decks"]:
			self.error_message("deck-ignored")
		else:
			self.error_message("no-such-deck")

	def close_deck(self):
		self.current_deck = False

	def ignore_deck(self, deckname):
		self.settings["ignore-decks"].append(deckname)

	def unignore_deck(self, deckname):
		if deckname in self.decklist:
			self.settings["ignore-decks"].remove(deckname)
			self.load_deck(deckname)
		else:
			self.error_message("no-such-deck")

	def list_settings(self):
		print("GENERAL SETTINGS:")
		for s in self.settings:
			print("{}: {}".format(s, self.settings[s]))
		if self.current_deck:
			print("DECK SETTINGS:")
			current_deck = self.current_deck
			for s in current_deck.settings:
				print("{}: {}".format(s, current_deck.settings[s]))

	def configure(self, key, value):
		self.settings[key] = value

	def configure_deck(self, key, value):
		if self.current_deck:
			self.current_deck.settings[key] = value
		else:
			error_message("no-deck-open")

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
				quiz = deck.quiz()
				stats = quiz.get_stats()
				print("Quiz complete!")
				print("Total cards answered: {}".format(stats["num-cards"]))
				print("Accuracy: {} percent".format(stats["percent-correct"]))
				print("Average time per card: {} seconds".format(stats["average-seconds"]))
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
			"ignore-deck": self.ignore_deck,
			"unignore-deck": self.unignore_deck,
			"add-card": self.add_cards,
			"quiz": self.quiz,
			"list-settings": self.list_settings,
			"configure": self.configure,
			"configure-deck": self.configure_deck,
			"exit": lambda: print("Exiting...")		
		}

		command = ""
		while command != "exit":
			command_input = input(self.settings["input-prompt"] + " ")
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

	def load_deck(self, deckname):
		self.decks[deckname] = Deck(0).load(deckname)

	def load(self):
		filename = "session-data.json"
		try:
			f = open(filename, "r")
			fr = f.read()
			f.close()
			dict = json.loads(fr)
			self.from_dict(dict)
			self.decks = {}
			for name in self.decklist:
				if name not in self.settings["ignore-decks"]:
					self.load_deck(name)
		except IOError:
			print("No preexisting data found. You must be a new user!")
		return self
