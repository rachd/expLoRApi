from explor.deckstats import deck_analytics, player_analytics, get_regions
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


def get_recommended_decks(player_stats):
    try:
        player_decks = player_stats["stats"]["decks"]
        player_deck_codes = player_decks.keys()
        top_player_decks = sorted(player_decks, key=(
            lambda x: player_decks[x]["uses"]))
        player_decks_decoded = [decode(deck) for deck in top_player_decks[0:5]]
        deck_data = requests.get(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/decks/top-decks?n=50').json()
        top_decks = deck_data["top_decks"]
        top_decks_filtered = [
            deck for deck in top_decks if not deck["deck_code"] in player_deck_codes]
        top_decks_decoded = [decode(deck['deck_code'])
                             for deck in top_decks_filtered]
        top_recommendations = recommend_decks(player_decks_decoded, top_decks_decoded, [
            deck['score'] for deck in top_decks_filtered])
        return (top_decks[0:3], top_recommendations)
    except:
        return {}


@app.route("/player-stats/<playerID>", methods=['GET'])
def get_player_stats(playerID):
    try:
        player_stats = requests.get(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/players/stats?player_name='+playerID).json()
        card_json = get_card_json()
        regions = region_stats(player_stats["stats"]["cards"], card_json)
        (top_decks, recommended_decks) = get_recommended_decks(player_stats)
        (playstyle, playstyle_winning) = player_analytics(
            player_stats["stats"]["decks"], card_json)
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


@app.route("/bookmarks/<playerID>", methods=['GET', 'POST'])
def bookmarks(playerID):
    if request.method == 'GET':
        bookmarks = requests.get(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/my/decks?player_name='+playerID).json()
        return response_to_json(json.dumps({"bookmarks": bookmarks["decks"]}))
    elif request.method == 'POST':
        deck = request.json['deck_code']
        status = request.json['status']
        data_to_send = {"deck_code": deck, "player_name": playerID}
        result = {}
        if status == 1:
            result = requests.post(
                'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/my/decks/favorite', data=data_to_send)
        else:
            result = requests.post(
                "http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/my/decks/unfavorite", data=data_to_send)
        if result.status_code == 201:
            return response_to_json(json.dumps({"status": "Success"}))
        else:
            return response_to_json(json.dumps({"status": "Fail"}))


@app.route("/profile/<playerID>", methods=['GET'])
def get_profile(playerID):
    try:
        output = {}
        card_json = get_card_json()
        player_stats = requests.get(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/players/stats?player_name='+playerID).json()
        match_history = player_stats["stats"]["match_history"]
        for match in match_history:
            match.update(
                {"deck_tags": deck_analytics(match["deck"], card_json)})
        output["match_history"] = match_history
        top_decks = requests.get(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/decks/top-decks?n=20').json()
        bookmarks = requests.get(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/my/decks?player_name='+playerID).json()
        output["decks"] = {
            "most_popular": top_decks["top_decks"], "bookmarks": bookmarks["decks"]}
        return response_to_json(json.dumps(output))
    except:
        return {}


@app.route("/cards/<playerID>", methods=['GET', 'POST'])
def player_cards(playerID):
    if request.method == 'GET':
        cards = requests.get(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/my/cards?player_name='+playerID).json()
        return response_to_json(json.dumps({"cards": cards}))
    elif request.method == 'POST':
        card = request.json['card']
        count = request.json['count']
        data_to_send = {"card_code": card,
                        "count": count, "player_name": playerID}
        result = requests.post(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/my/cards/add', data=data_to_send)
        if result.status_code == 201:
            return response_to_json(json.dumps({"status": "Success"}))
        else:
            return response_to_json(json.dumps({"status": "Fail"}))


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
        output = {
            "deck_code": deck,
            "player_id": player_id,
            'opponent': opponent,
            "result": result,
            "regions": regions,
            "cards": decoded_deck,
            "keywords": deck_stats,
        }
        requests.post(
            'http://ec2-54-85-199-0.compute-1.amazonaws.com:81/api/players/record-match', data=output)
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
