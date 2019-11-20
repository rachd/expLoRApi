from explor.helpers import get_all_cards, get_cards_info


def get_spell_counts(cards, keyword_only):
    spell_counts = {}
    total_spells = 0
    for card in cards:
        for keyword in card['keywords']:
            if keyword in ["Slow", "Burst", "Fast"]:
                total_spells += 1
                if keyword in spell_counts.keys():
                    spell_counts[keyword] += 1
                else:
                    spell_counts[keyword] = 1
    spell_styles = [key for key in spell_counts.keys(
    ) if spell_counts[key] > total_spells / 3]
    if keyword_only:
        return spell_styles
    else:
        return [spell_style + " spells" for spell_style in spell_styles]


def get_keyword_counts(cards, keyword_only):
    keyword_counts = {}
    for card in cards:
        for keyword in card['keywords']:
            if not keyword in ["Slow", "Burst", "Fast"]:
                if keyword in keyword_counts.keys():
                    keyword_counts[keyword] += 1
                else:
                    keyword_counts[keyword] = 1
    top_3_keywords = sorted(
        keyword_counts, key=keyword_counts.get, reverse=True)[0:3]
    output = []
    for key in top_3_keywords:
        if keyword_only:
            output.append(key)
        else:
            output.append(key + " cards")
    return output


def analyze_mana_curve(cards):
    card_costs = [card['cost'] for card in cards]
    low = len([cost for cost in card_costs if cost <= 3])
    high = len([cost for cost in card_costs if cost >= 6])
    playstyle = ""
    if low % 40 >= 27:
        playstyle = "Low"
    elif high % 40 >= 10:
        playstyle = "High"
    else:
        playstyle = "Balanced"
    return [playstyle + " mana curve decks"]


def analyze_type_percentage(cards, keyword_only):
    card_types = [card['type'] for card in cards]
    isChampion = [1 if card['supertype'] ==
                  'Champion' else 0 for card in cards]
    champions = sum(isChampion)
    spells = len(
        [card_type for card_type in card_types if card_type == 'Spell'])
    units = len(
        [card_type for card_type in card_types if card_type == 'Unit'])
    tags = []
    if champions % 40 < 5:
        tags.append('Low Champion')
    if spells % 40 > 20:
        tags.append('High Spell')
    if units % 40 >= 27:
        tags.append('High Unit')
    if keyword_only:
        return tags
    else:
        return [tag + " count decks" for tag in tags]


def get_stats(cards, keyword_only=False):
    keyword_counts = get_keyword_counts(cards, keyword_only)
    spell_counts = get_spell_counts(cards, keyword_only)
    mana_curve_desc = analyze_mana_curve(cards)
    type_percents = analyze_type_percentage(cards, keyword_only)
    return keyword_counts + spell_counts + type_percents + mana_curve_desc


def player_analytics(player_history, card_json):
    decks_with_cards = []
    winning_decks_with_cards = []
    for deck in player_history.keys():
        cards_info = get_cards_info(deck, card_json)
        for count in range(player_history[deck]["wins"]):
            winning_decks_with_cards.append(cards_info)
        for count in range(player_history[deck]["uses"]):
            decks_with_cards.append(cards_info)
    return (get_stats(get_all_cards(decks_with_cards)), get_stats(get_all_cards(winning_decks_with_cards)))


def deck_analytics(deck, card_json):
    deck_data = get_cards_info(deck, card_json)
    return get_stats(deck_data, True)

def get_regions(deck, card_json)
    deck_data = get_cards_info(deck, card_json)
    regions = []
    for card in deck_data:
        if not card['regionRef'] in regions:
            regions.append({'region': card['region'], 'regionRef': card['regionRef']})
    return regions