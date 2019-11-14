import json

sorted_codes = []
with open("data.json", "r") as input_file:
    json_data = json.load(input_file)
    decks = json_data['decks']
    card_counts = {}
    for deck in decks:
        for card in deck['cards']:
            card_code = card['id']
            card_count = card['count']
            if card_code in card_counts.keys():
                card_counts[card_code] += card_count
            else:
                card_counts[card_code] = card_count
    sorted_codes = sorted(card_counts, key=card_counts.get, reverse=True)

with open("set1-en_us.json", "r") as input_file:
    json_data = json.load(input_file)
    for card in json_data:
        if not card['cardCode'] in sorted_codes and card['collectible'] == True:
            sorted_codes.append(card['cardCode'])
    
with open("vocabulary.txt", "w") as output:
    output.write("<S>\n</S>\n<UNK>\n")
    for code in sorted_codes:
        output.write(code + '\n')