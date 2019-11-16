import json

def get_top_3(object_to_sort):
    return sorted(object_to_sort, key=object_to_sort.get, reverse=True)[0:3]

def top_cards(card_stats, card_json):
    all_games = {}
    winning = {}
    champs = {}
    winning_champs = {}
    regions = {}
    winning_regions = {}
    for card in card_stats.keys():
        card_info = card_json[card]
        wins = card_stats[card]['wins']
        losses = card_stats[card]['losses']
        if card_info['rarity'] == 'Champion':
            champs[card] = wins + losses
            winning_champs[card] = wins
        else:
            all_games[card] = wins + losses
            winning[card] = wins

        region = card_info['region']
        if region in regions.keys():
            regions[region] += wins + losses
            winning_regions[region] += wins
        else:
            regions[region] = wins + losses
            winning_regions[region] = wins
    return ({'all': regions, 'winning': winning_regions}, {'all_games': get_top_3(all_games), 'winning': get_top_3(winning), 'champs': get_top_3(champs), 'winning_champs': get_top_3(winning_champs)})

