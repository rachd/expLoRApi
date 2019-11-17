from explor.deckstats import deck_analytics, player_analytics
from explor.similarCards import get_similar_cards
from explor.helpers import decode
from explor.recommend import recommend_decks
from explor.playerstats import top_cards
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
        'http://ec2-54-85-199-0.compute-1.amazonaws.com/api/players/stats?player_name='+player_id).json()
    player_cards = list(player_stats["stats"]["cards"].keys())
    similar_cards = get_similar_cards_json()
    return response_to_json(json.dumps(get_similar_cards(decode(deck), missing_cards, player_cards, similar_cards)))

def get_recommended_decks(player_stats):
    player_cards = list(player_stats["stats"]["cards"].keys())
    player_decks_decoded = [decode(deck) for deck in player_stats["stats"]["decks"].keys()]
    top_decks = []#requests.get('').json()   FETCH TOP 100 DECKS
    top_all_cards = [] #requests.get('').json() FETCH TOP 100 DECKS WHERE ALL CARDS IN PLAYER's CARDS
    top_decks_decoded = [decode(deck) for deck in top_decks]
    top_all_cards_decoded = [decode(deck) for deck in top_all_cards]
    top_recommendations = recommend_decks(player_decks_decoded, top_decks_decoded)
    all_cards_recommendations = recommend_decks(player_decks_decoded, top_all_cards_decoded)
    return (top_recommendations, all_cards_recommendations)

@app.route("/player-stats/<playerID>", methods=['GET'])
def get_player_stats(playerID):	
    player_stats = requests.get('http://ec2-54-85-199-0.compute-1.amazonaws.com/api/players/stats?player_name='+playerID).json()
    # playstyle, regions, top deck recommendations, all your cards recommendations
    # also include top cards and top champs?
    card_json = get_card_json()
    (region_stats, cards_stats) = top_cards(player_stats["stats"]["cards"], card_json)
    (top_recommendations, all_cards_recommendations) = get_recommended_decks(player_stats)
    playstyle = player_analytics(player_stats["stats"]["decks"], card_json)
    return response_to_json(json.dumps({'playstyle': playstyle, 'cards': cards_stats, 'regions': region_stats, 'top_recommendations': top_recommendations, 'all_card_recommendations': all_cards_recommendations}))
