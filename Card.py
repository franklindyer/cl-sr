from datetime import datetime, timedelta
import json

class Attempt:

	def __init__(self, id, value, time_elapsed):
		self.id = id
		self.value = value
		self.timestamp = datetime.now()
		self.time_elapsed = time_elapsed

	def to_dict(self):
		timestamp_string = self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
		elapsed_string = self.time_elapsed.total_seconds()
		dict = {"id": self.id, "value": self.value, "timestamp": timestamp_string, "time_elapsed": elapsed_string}
		return dict

	def from_dict(self, dict):
		self.id = dict["id"]
		self.value = dict["value"]
		self.timestamp = datetime.strptime(dict["timestamp"], "%m/%d/%Y, %H:%M:%S")
		self.time_elapsed = timedelta(seconds = dict["time_elapsed"])
		return self

class Card:

	def __init__(self, id, prompt, answer):
		self.id = id
		self.prompt = prompt
		self.answer = answer
		self.attempts = []
		self.num_attempts = 0
		self.waittime = timedelta(hours = 1)

	def new_attempt(self, value, start_time, end_time):
		self.num_attempts += 1
		time_elapsed = end_time - start_time
		attempt = Attempt(self.num_attempts, value, time_elapsed)
		self.attempts.append(attempt)

	def update_wait(multiplier, min_wait, max_wait):
		wait_seconds = self.waittime.total_seconds()
		new_waittime = timedelta(seconds = wait_seconds * multiplier)
		if new_waittime < min_wait:
			new_waittime = min_wait
		elif new_waittime > max_wait:
			new_waittime = max_wait
		self.waittime = new_waittime

	def quiz(self):
		start_time = datetime.now()
		guess = input(self.prompt)
		end_time = datetime.now()
		correct = (guess == self.answer)
		self.new_attempt(correct, start_time, end_time)
		return correct
				
	def to_dict(self):
		attempts_dict = [a.to_dict() for a in self.attempts]
		waittime_string = self.waittime.total_seconds()
		dict = {"id": self.id, "prompt": self.prompt, "answer": self.answer, "attempts": attempts_dict, "num_attempts": self.num_attempts, "waittime": waittime_string}
		return dict

	def from_dict(self, dict):
		self.id = dict["id"]
		self.prompt = dict["prompt"]
		self.answer = dict["answer"]
		self.attempts = [Attempt(0, 0, 0).from_dict(d) for d in dict["attempts"]]
		self.num_attempts = dict["num_attempts"]
		self.waittime = timedelta(seconds = dict["waittime"])
		return self
