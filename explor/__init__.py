from explor.deckstats import deck_analytics, player_analytics, get_regions
from explor.similarCards import get_similar_cards
from explor.helpers import decode, get_card_array
from explor.recommend import recommend_decks
from explor.playerstats import region_stats
import json
from flask import Flask, request, Response
from flask_restplus import Api
import requests
app = Flask(__name__)
api = Api(app)

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
    try:
        deck_code = request.json['deck_code']
        card_json = get_card_json()
        return response_to_json(json.dumps({"keywords": deck_analytics(deck_code, card_json)}))
    except: 
        return {}

@app.route("/suggested-cards", methods=['POST'])
def suggest_cards():
    try:
        deck = request.json['deck_code']
        player_id = request.json['player_id']
        missing_cards = request.json['missing_cards']
        player_stats = requests.get(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/players/stats?player_name='+player_id).json()
        player_cards = list(player_stats["stats"]["cards"].keys())
        similar_cards = get_similar_cards_json()
        return response_to_json(json.dumps(get_similar_cards(decode(deck), missing_cards, player_cards, similar_cards)))
    except:
        return {}

def get_recommended_decks(player_stats):
    try: 
        player_decks = player_stats["stats"]["decks"]
        top_player_decks = sorted(player_decks.keys(), key=(lambda x: player_decks[x]["uses"]))
        player_decks_decoded = [decode(deck) for deck in top_player_decks[0:5]]
        top_decks = requests.get('http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/decks/top-decks?n=50').json()
        top_decks_decoded = [decode(deck['deck_code']) for deck in top_decks["top_decks"]]
        top_recommendations = recommend_decks(player_decks_decoded, top_decks_decoded, [deck['score'] for deck in top_decks["top_decks"]], True)
        return (top_decks["top_decks"][0:3], top_recommendations)
    except:
        return {}

@app.route("/player-stats/<playerID>", methods=['GET'])
def get_player_stats(playerID):	
    try:
        player_stats = requests.get('http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/players/stats?player_name='+playerID).json()
        card_json = get_card_json()
        regions = region_stats(player_stats["stats"]["cards"], card_json)
        (top_decks, recommended_decks) = get_recommended_decks(player_stats)
        (playstyle, playstyle_winning) = player_analytics(player_stats["stats"]["decks"], card_json)
        output = {}
        output.update(regions)
        output['popular_decks'] = top_decks
        output['recommended_decks'] = recommended_decks
        output['match_history'] = player_stats["stats"]["match_history"]
        output['playstyle'] = playstyle
        output['playstyle_winning'] = playstyle_winning
        return response_to_json(json.dumps(output))
    except:
        return {}

@app.route("/bookmark/<playerID>", methods=['GET'])
def get_bookmarks(playerID):
    try:
        # TODO hit brandon's endpoint to get bookmarks for player
        return {}
    except:
        pass

@app.route("/bookmark", methods=['POST'])
def bookmark():
    try:
        deck = request.json['deck_code']
        player_id = request.json['player_id']
        # TODO hit brandon's endpoint to save bookmark
        return response_to_json(json.dumps({"status": "Success"}))
    except:
        return response_to_json(json.dumps({"status": "Fail"}))

@app.route("/profile/<playerID>", methods=['GET'])
def get_profile(playerID):
    try:
        output = {}
        card_json = get_card_json()
        player_stats = requests.get('http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/players/stats?player_name='+playerID).json()
        match_history = player_stats["stats"]["match_history"]
        for match in match_history:
            match.update({"deck_tags": deck_analytics(match["deck"], card_json)})
        output["match_history"] = match_history
        top_decks = requests.get('http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/decks/top-decks?n=20').json()
        bookmarks = [] #TODO get bookmarks
        output["decks"] = {"most_popular": top_decks["top_decks"], "bookmarks": bookmarks}
        return response_to_json(json.dumps(output))
    except:
        return {}

# TODO put in GET and POST card library endpoints
@app.route("/cards/<playerID>", methods=['GET', 'POST'])
def player_cards(playerID):
    if request.method == 'GET':
        cards = []
        return response_to_json(json.dumps({"cards": cards}))
    elif request.method == 'POST':
        card = request.json['card']
        count = request.json['count']
        return response_to_json(json.dumps({"status": "Success"}))

@app.route("/submit-match", methods=['POST'])
def submit_match():
    try:
        deck = request.json['deck_code']
        player_id = request.json['player_id']
        result = request.json['result']
        opponent = request.json['opponent']
        card_json = get_card_json()
        deck_stats = deck_analytics(deck, card_json)
        decoded_deck = get_card_array(deck)
        regions = get_regions(deck, card_json)
        json_output = response_to_json(json.dumps({
            "deck_code": deck,
            "player_id": player_id,
            'opponent': opponent,
            "result": result,
            "regions": regions,
            "cards": decoded_deck,
            "keywords": deck_stats,
        }))
        # TODO pass json_output to brandon's endpoint
        return response_to_json(json.dumps({"status": "Success"}))
    except:
        return response_to_json(json.dumps({"status": "Fail"}))

@app.route("/suggest-decks", methods=["POST"])
def suggest_decks():
    try:
        required_cards = request.json['required_cards']
        required_keywords = request.json['required_keywords']
        player_cards = request.json['player_cards']
        player_id = request.json['player_id']
        # TODO get top 100 decks matching the parameters
        top_decks = []
        return response_to_json(json.dumps({"decks": top_decks}))
    except:
        return {}