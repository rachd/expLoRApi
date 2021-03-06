from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from explor.helpers import encode


def recommend_decks(player_decks, top_decks, ranks):
    if len(top_decks) <= 3:
        return top_decks

    vectorizer = TfidfVectorizer()
    all_vectors = vectorizer.fit_transform(top_decks + player_decks)
    cosine_similarities = cosine_similarity(all_vectors)
    player_sims = cosine_similarities[:len(top_decks)]
    all_sims = []
    for i in range(len(player_sims)):
        for j in range(len(top_decks)):
            all_sims.append({'i': i, 'j': j, 'val': player_sims[i][j]})
    sorted_sims = sorted(all_sims, key=lambda x: x['val'], reverse=True)
    recommendations = []
    i = 0
    while len(recommendations) <= 3:
        if not sorted_sims[i]["j"] in recommendations:
            recommendations.append(sorted_sims[i]["j"])
        i += 1
    recommendations = [{'deck': top_decks[i], 'rank': ranks[i]}
                       for i in recommendations]
    return [{'deck_code': encode(recommendation['deck']), 'rank': recommendation['rank']} for recommendation in recommendations]
