# encoding=utf8
'''deck process'''
import json
import os

HOUSE_CARD = {
    "House Greyjoy":2,
    "House Baratheon":1,
    "House Stark":5,
    "House Martell":4,
    "House Lannister":3,
    "House Targaryen":6
}
def add_to_card_pool(card, card_pool):
    '''add card in decks to the card pool'''
    house_card = HOUSE_CARD
    card_id = card['id']
    if card['type'] == u"House Card":
        card['id'] = house_card[card['name']]
        card['set'] = "Core Set"
        card['set_id'] = 17
    if not card_pool.has_key(card_id):
        card_pool[card_id] = card

def update_card_relation(card_list, card_relation):
    '''update card_relation table by cards in every deck'''
    card_in_deck = {card[0]:1 for card in card_list}
    for card in card_list:
        card_id = card[0]
        card_type = card[2]
        card_num = card[1] if card_type in ["Plots", "House Card", "Agendas"] else 3
        for related_card in card_list:
            related_card_id = related_card[0]
            related_card_type = related_card[2]
            related_card_num = related_card[1] if related_card_type in ["Plots", "House Card", "Agendas"] else 3
            if related_card_id == card_id:
                continue
            card_relation[card_id][related_card_id] += \
                    (1 + card_num * 0.3) * (0.5 + 0.1 * related_card_num)
        for every_card in card_relation[card_id].keys():
            if not card_in_deck.has_key(every_card):
                card_relation[card_id][every_card] -= 0.2

def init_card_relation(card_pool):
    '''init card relation table'''
    return {card['id']:{
        related_card['id']:0 for related_card in card_pool.values() \
        if related_card['id'] != card['id']
    } for card in card_pool.values()}

def main():
    '''main func'''
    deck_files = os.listdir("/home/HSLPDEV7/agot/decks20/")
    decks = {}
    card_statistic = {}
    card_pool = {}

    for deck_file_name in deck_files:
        if "deck" in deck_file_name:
            deck_file = file("/home/HSLPDEV7/agot/decks20/%s" % deck_file_name)
            cont_json = json.load(deck_file)
            deck_file.close()
            decks[cont_json['info']['id']] = cont_json
            for card in cont_json['cards']:
                card['id'] = int(card['id'])
                card['num'] = int(card['num'])
                card['set_id'] = int(card['set_id'])
                add_to_card_pool(card, card_pool)
                if card['type'] == u"House Card":
                    cont_json['info']['house'] = card['name']
    card_relation = init_card_relation(card_pool)
    print len(card_pool)
    for deck in decks.values():
        print "deck %s" % deck['info']['id']
        card_in_deck = []
        house_of_deck = deck['info']['house']
        for card in deck['cards']:
            card_id = card['id']
            if card_statistic.has_key(card_id):
                card_statistic[card_id]['num'] += 1
                card_statistic[card_id]['cnum'] += int(card['num'])
                card_statistic[card_id]['house']\
                        [house_of_deck] += 1
                card_statistic[card_id]['chouse']\
                        [house_of_deck] += int(card["num"])
            else:
                card_statistic[card_id] = {}
                card_statistic[card_id]['num'] = 1
                card_statistic[card_id]['cnum'] = int(card['num'])
                card_statistic[card_id]['house'] = {
                    "House Stark":0,
                    "House Lannister":0,
                    "House Baratheon":0,
                    "House Martell":0,
                    "House Greyjoy":0,
                    "House Targaryen":0
                }
                card_statistic[card_id]['chouse'] = {
                    "House Stark":0,
                    "House Lannister":0,
                    "House Baratheon":0,
                    "House Martell":0,
                    "House Greyjoy":0,
                    "House Targaryen":0
                }
                card_statistic[card_id]['chouse']\
                        [house_of_deck] = int(card['num'])
            card_in_deck.append((card['id'], card['num'], card['type']))
        update_card_relation(card_in_deck, card_relation)
    relation_fp = file("/home/HSLPDEV7/agot/data/relation1.data", "w+")
    json.dump(card_relation, relation_fp)
    relation_fp.close()
    card_pool_fp = file("/home/HSLPDEV7/agot/data/card_pool1.data", "w+")
    json.dump(card_pool, card_pool_fp)
    card_pool_fp.close()
    statistic_fp = file("/home/HSLPDEV7/agot/data/statistic1.data", "w+")
    json.dump(card_statistic, statistic_fp)
    statistic_fp.close()
    #sorted_card_all = sorted(card_all.items(),
                         #key=lambda x:x[1]["chouse"]['house %s' % house] \
                                 #+ x[1]["house"]['house %s' % house] * 1.5,
                         #reverse=true)
if __name__ == "__main__":
    main()
