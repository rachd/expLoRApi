from explor.deckstats import deck_analytics, player_analytics
from explor.similarCards import get_similar_cards
from explor.helpers import decode, get_card_array
from explor.recommend import recommend_decks
from explor.playerstats import region_stats
import json
from flask import Flask, request, Response
import requests
app = Flask(__name__)

def get_card_json():
    with app.open_resource("data/cards.json") as input_json:
        return json.load(input_json)

def get_similar_cards_json():
    with app.open_resource("data/similar_cards.json") as input_json:
        return json.load(input_json)

def response_to_json(out_obj):
    return Response(out_obj, mimetype='application/json')

@app.route("/deck-stats", methods=['POST'])
def deck_stats():
    deck_codes = request.json['deck_codes']
    card_json = get_card_json()
    return response_to_json(json.dumps({"keywords": deck_analytics(deck_codes, card_json)}))


@app.route("/suggested-cards", methods=['POST'])
def suggest_cards():
    deck = request.json['deck_code']
    player_id = request.json['player_id']
    missing_cards = request.json['missing_cards']
    player_stats = requests.get(
        'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/players/stats?player_name='+player_id).json()
    player_cards = list(player_stats["stats"]["cards"].keys())
    similar_cards = get_similar_cards_json()
    return response_to_json(json.dumps(get_similar_cards(decode(deck), missing_cards, player_cards, similar_cards)))

def get_recommended_decks(player_stats):
    player_decks = player_stats["stats"]["decks"]
    top_player_decks = sorted(player_decks.keys(), key=(lambda x: player_decks[x]["uses"]))
    player_decks_decoded = [decode(deck) for deck in top_player_decks[0:5]]
    top_decks = requests.get('http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/decks/top-decks?n=50').json()
    top_decks_decoded = [decode(deck['deck_code']) for deck in top_decks["top_decks"]]
    top_recommendations = recommend_decks(player_decks_decoded, top_decks_decoded, [deck['score'] for deck in top_decks["top_decks"]])
    return (top_decks["top_decks"][0:3], top_recommendations)

@app.route("/player-stats/<playerID>", methods=['GET'])
def get_player_stats(playerID):	
    player_stats = requests.get('http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/players/stats?player_name='+playerID).json()
    card_json = get_card_json()
    regions = region_stats(player_stats["stats"]["cards"], card_json)
    (top_decks, recommended_decks) = get_recommended_decks(player_stats)
    (playstyle, playstyle_winning) = player_analytics(player_stats["stats"]["decks"], card_json)
    output = {}
    output.update(regions)
    output['popular_decks'] = top_decks
    output['recommended_decks'] = recommended_decks
    output['playstyle'] = playstyle
    output['playstyle_winning'] = playstyle_winning
    return response_to_json(json.dumps(output))

@app.route("/submit-match", methods=['POST'])
def submit_match():
    deck = request.json['deck_code']
    player_id = request.json['player_id']
    result = request.json['result']
    card_json = get_card_json()
    deck_stats = deck_analytics(deck_codes, card_json)
    decoded_deck = get_card_array(deck)
    return response_to_json(json.dumps({
        "deck_code": deck,
        "player_id": player_id,
        "result": result,
        "cards": decoded_deck,
        "keywords": deck_stats
    }))