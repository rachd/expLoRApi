import json
from gensim import models

training_data = []
with open("explor/old_app/all_training_data.txt", "r") as input_file:
    for line in input_file:
        training_data.append(line.split())

model = models.Word2Vec(training_data, min_count=1,
                        size=50, workers=3, window=40, sg=1)

card_codes = []
with open("explor/data/cards.json", "r") as card_file:
    card_json = json.load(card_file)
    card_codes = [card_code for card_code in card_json.keys(
    ) if card_json[card_code]["collectible"]]

recommendations = {}
for card_code in card_codes:
    try:
        recommendations[card_code] = model.most_similar(card_code)
    except:
        recommendations[card_code] = []

with open("explor/data/similar_cards.json", "w") as output_file:
    json.dump(recommendations, output_file)
