import json
import os

deck_files = os.listdir("/home/HSLPDEV7/agot/decks20/")
decks = {}
card_all = {}
for deck_file_name in deck_files:
    if "deck" in deck_file_name:
        deck_file = file("/home/HSLPDEV7/agot/decks20/%s" % deck_file_name)
        cont_json = json.load(deck_file)
        deck_file.close()
        decks[cont_json['info']['id']] = cont_json
        for card in cont_json['cards']:
            if card['type'] == u"House Card":
                cont_json['info']['house'] = card['name']
for deck in decks.values():
    for card in deck['cards']:
        if card_all.has_key(card['id']):
            card_all[card['id']]['num'] += 1
            card_all[card['id']]['cnum'] += int(card['num'])
            card_all[card['id']]['house'][deck['info']['house']] += 1
            card_all[card['id']]['chouse'][deck['info']['house']] += int(card["num"])
        else:
            card_all[card['id']] = card
            card_all[card['id']]['num'] = 1
            card_all[card['id']]['cnum'] = int(card['num'])
            card_all[card['id']]['house'] = {
                "House Stark":0,
                "House Lannister":0,
                "House Baratheon":0,
                "House Martell":0,
                "House Greyjoy":0,
                "House Targaryen":0
            }
            card_all[card['id']]['chouse'] = {
                "House Stark":0,
                "House Lannister":0,
                "House Baratheon":0,
                "House Martell":0,
                "House Greyjoy":0,
                "House Targaryen":0
            }
            house = "Baratheon"
            card_all[card['id']]['chouse'][deck['info']['house']] = int(card['num'])
sorted_card_all = sorted(card_all.items(),
    key=lambda x:x[1]["chouse"]['House %s' % house]+x[1]["house"]['House %s' % house]*1.5, reverse=True)
for card_id, card in sorted_card_all:
    if card['num'] > 5:
        print "%s, %s, %s, %s (%s)"\
              % (card['name'], card['set'], card['house']['House %s' % house], card["chouse"]['House %s' % house],
                 card["chouse"]['House %s' % house] + card["house"]['House %s' % house]*1.5)


