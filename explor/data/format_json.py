import json

json_data = {}
with open("explor/data/set1-en_us.json", "r") as input_file:
    json_data = json.load(input_file)

output = {}
for obj in json_data:
    output[obj['cardCode']] = obj

with open("explor/data/cards.json", "w") as output_file:
    json.dump(output, output_file)