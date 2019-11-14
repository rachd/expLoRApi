from lor_deckcodes import LoRDeck


def decode(deck):
    codes = list(LoRDeck.from_deckcode(deck))
    cards = []
    for code in codes:
        for i in range(int(code[0])):
            cards.append(code[2:])
    return " ".join(cards)

def get_all_cards(decks):
    all_cards = []
    for deck in decks:
        for card in deck:
            all_cards.append(card)
    return all_cards

def get_cards_info(deck, card_json):
    decoded_deck = decode(deck)
    card_json = [card_json[card] for card in decoded_deck.split()]
    return card_json