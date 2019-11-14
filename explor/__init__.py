from flask import Flask, request
app = Flask(__name__)

import json
from explor.deckstats import deck_analytics

def get_card_json():
    with app.open_resource("data/cards.json") as input_json:
        return json.load(input_json)

@app.route("/deck-stats", methods=['POST'])
def deck_stats():
    deck_codes = request.json['deck_codes']
    card_json = get_card_json()
    return json.dumps({"keywords": deck_analytics(deck_codes, card_json)})