def get_max(obj):
    keys = obj.keys()
    return max(keys, key=(lambda key: obj[key]))

def format_region(region, total):
    return {
        'title': region['title'],
        'ref': region['ref'],
        'percent': int(region['count'] / total)
    }

def region_stats(card_stats, card_json):
    all_games = {}
    winning = {}
    regions = {}
    winning_regions = {}
    for card in card_stats.keys():
        card_info = card_json[card]
        wins = card_stats[card]['wins']
        losses = card_stats[card]['losses']
        all_games[card] = wins + losses
        winning[card] = wins

        region = card_info['region']
        regionRef = card_info['regionRef']
        if region in regions.keys():
            regions[region]['count'] += wins + losses
            winning_regions[region]['count'] += wins
        else:
            regions[region] = {'title': region, 'ref': regionRef, 'count': wins + losses}
            winning_regions[region] = {'title': region, 'ref': regionRef, 'count': wins}

    top_card = get_max(all_games)
    top_card_winning = get_max(winning)
    
    total_cards = len(card_stats.keys())
    region_percents = [format_region(regions[region], total_cards) for region in regions.keys()]
    region_percents_winning = [format_region(winning_regions[region], total_cards) for region in winning_regions.keys()]

    top_region = max(region_percents, key=lambda item: item['percent'])
    top_region_winning = max(region_percents_winning, key=lambda item: item['percent'])
    return ({
        'most_played_card_code': top_card, 
        'most_played_card_code_winning': top_card_winning, 
        'most_played_region': top_region, 
        'most_played_region_winning': top_region_winning, 
        'region_play': region_percents, 
        'region_play_winning': region_percents_winning
    })

def recent_matches(player_stats):
    return []