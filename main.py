import json

f = open("data.json", 'r')
fr = f.read()
data = json.loads(fr)
