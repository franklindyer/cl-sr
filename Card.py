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

	def __init__(self, id, prompt, answer, initial_wait=timedelta(hours = 1)):
		self.id = id
		self.created = datetime.now()
		self.prompt = prompt
		self.answer = answer
		self.attempts = []
		self.num_attempts = 0
		self.last_attempt = datetime.now()
		self.waittime = initial_wait

	def is_due(self):
		return (datetime.now() > self.last_attempt + self.waittime)

	def new_attempt(self, value, start_time, end_time):
		self.num_attempts += 1
		time_elapsed = end_time - start_time
		attempt = Attempt(self.num_attempts, value, time_elapsed)
		self.attempts.append(attempt)

	def update_wait(self, multiplier, min_wait, max_wait):
		wait_seconds = self.waittime.total_seconds()
		new_waittime = timedelta(seconds = wait_seconds * multiplier)
		if new_waittime < min_wait:
			new_waittime = min_wait
		elif new_waittime > max_wait:
			new_waittime = max_wait
		self.waittime = new_waittime

	def quiz(self):
		start_time = datetime.now()
		print("Prompt: " + self.prompt)
		guess = input("Answer: ")
		end_time = datetime.now()
		self.last_attempt = end_time
		correct = (guess == self.answer)
		while guess != self.answer:
			print("Incorrect! The correct answer was '" + self.answer + "'.")
			guess = input("Answer: ")
		self.new_attempt(correct, start_time, end_time)
		return correct
				
	def to_dict(self, dictify_attempts=True):
		created_string = self.created.strftime("%m/%d/%Y, %H:%M:%S")
		attempts_dict = [a.to_dict() for a in self.attempts]
		last_attempt_string = self.last_attempt.strftime("%m/%d/%Y, %H:%M:%S")
		waittime_string = self.waittime.total_seconds()
		dict = {"id": self.id, "created": created_string, "prompt": self.prompt, "answer": self.answer, "num_attempts": self.num_attempts, "last_attempt": last_attempt_string, "waittime": waittime_string}
		if dictify_attempts: dict["attempts"] = attempts_dict
		return dict

	def from_dict(self, dict):
		self.id = dict["id"]
		self.created = datetime.strptime(dict["created"], "%m/%d/%Y, %H:%M:%S")
		self.prompt = dict["prompt"]
		self.answer = dict["answer"]
		self.attempts = [Attempt(0, 0, 0).from_dict(d) for d in dict["attempts"]]
		self.num_attempts = dict["num_attempts"]
		self.last_attempt = datetime.strptime(dict["last_attempt"], "%m/%d/%Y, %H:%M:%S") 
		self.waittime = timedelta(seconds = dict["waittime"])
		return self
