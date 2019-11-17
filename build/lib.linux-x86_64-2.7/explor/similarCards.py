import json


def load_data():
    with open("./explor/data/similar_cards.json", "r") as input_file:
        return json.load(input_file)


def get_champion_count(data):
    return len([code for code in data.keys() if data[code]['rarity'] == 'Champion'])


def get_3_copy_cards(deck):
    card_counts = {}
    for card in deck:
        if card in card_counts.keys():
            card_counts[card] += 1
        else:
            card_counts[card] = 1
    return [code for code in card_counts.keys() if card_counts[code] == 3]


def filter_cards(deck, codes, player_cards):
    full_cards = get_3_copy_cards(codes)
    print(full_cards)
    return [code for code in codes if code in player_cards]


def get_similar_cards(deck, missing_cards, player_cards):
    data = load_data()
    output = []
    for card in missing_cards:
        recommendations = ([datum[0] for datum in data[card]])
        output.append(filter_cards(deck, recommendations, player_cards))
    return output
