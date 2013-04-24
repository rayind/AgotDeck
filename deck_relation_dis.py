# encoding=utf8
import json
json_fp = file("/home/HSLPDEV7/agot/data/relation1.data")
relation = json.load(json_fp)
json_fp.close()
json_fp = file("/home/HSLPDEV7/agot/data/card_pool1.data")
card_pool = json.load(json_fp)
json_fp.close()
json_fp = file("/home/HSLPDEV7/agot/data/card_pool1.data")
statistic = json.load(json_fp)
json_fp.close()
cards_re = {}
spec_cards = ['872']
for spec_card in spec_cards:
    cards_re_tmp = relation[spec_card]
    for card_id in cards_re_tmp:
        if cards_re.has_key(card_id):
            cards_re[card_id] += cards_re_tmp[card_id]
        else:
            cards_re[card_id] = cards_re_tmp[card_id]
cards_re_s = sorted(cards_re, key = lambda x:cards_re[x], reverse=True)
result = [
    "name:%s, set:%s, rate:%s"
    % (card_pool[card]['name'], card_pool[card]['set'], cards_re[card])\
    for card in cards_re_s[:100]
]
print "\n".join(result)
