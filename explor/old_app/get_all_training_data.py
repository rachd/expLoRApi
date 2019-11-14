import json

json_data = {}
with open("data.json", "r") as input_data:
    json_data = json.load(input_data)


with open("all_training_data.txt", "w") as output:
    for deck in json_data['decks']:
        # get cards in deck
        cards = []
        for card in deck['cards']:
            for i in range(card['count']):
                cards.append(card['id'])

        # print deck to test data rating number of times
        for i in range(deck['rating']):
            output.write(" ".join(cards) + '\n')


# MAKE SURE TO RUN ELMO CODE WITH PYTHON 3.5!!!!