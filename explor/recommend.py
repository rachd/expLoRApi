from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from explor.helpers import encode

def recommend_decks(player_decks, all_top_decks, scores):
    top_decks = [deck for deck in all_top_decks if not deck in player_decks]
    if len(top_decks) < 4:
        return top_decks

    vectorizer = TfidfVectorizer()
    all_vectors = vectorizer.fit_transform(top_decks + player_decks)
    cosine_similarities = cosine_similarity(all_vectors)
    player_sims = cosine_similarities[len(top_decks):]
    max_4 = [
        {'i': 0, 'j': 0, 'val': player_sims[0][0]},
        {'i': 0, 'j': 1, 'val': player_sims[0][1]},
        {'i': 0, 'j': 2, 'val': player_sims[0][2]},
        {'i': 0, 'j': 3, 'val': player_sims[0][3]}
    ]

    all_sims = []
    for i in range(len(player_sims)):
        for j in range(len(top_decks)):
            all_sims.append({'i': i, 'j': j, 'val': player_sims[i][j]})
    sorted_sims = sorted(all_sims, key=lambda x: x['val'], reverse=True)
    recommendations = []
    i = 0
    while len(recommendations) < 3:
        if not sorted_sims[i]["j"] in recommendations:
            recommendations.append(sorted_sims[i]["j"])
        i += 1
    recommendations = [{'deck': top_decks[i], 'score': scores[i]} for i in recommendations]
    return [{'deck': encode(recommendation['deck']), 'score': recommendation['score']} for recommendation in recommendations]
