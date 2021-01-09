import json
import re
from datetime import datetime, timedelta
import random

exec(open("Card.py").read())
exec(open("Deck.py").read())
exec(open("Session.py").read())

d = Deck("fuckyland")
d.add_card("Eat shit? ", "Yes")
d.add_card("Eat cupcakes? ", "No")

s = Session()
s.listen_loop()
