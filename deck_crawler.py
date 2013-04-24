import urllib2
import urllib
import time
import re
import json
from BeautifulSoup import BeautifulSoup
import deck_config
DECK_LIST_URL = "http://www.agotcards.org/deck/house/"
LOGIN_URL = "http://www.agotcards.org/access/login"
DOMAIN = "http://www.agotcards.org"
DECK_URL = "http://www.agotcards.org/deck/deck_list/"
deck_index = [0, 1, 2, 3, 4, 5]
#deck_index = [0]
login_username = "rayind1"
login_password = "anu.pwd1"
deck_list_content_html = {}
cookie = urllib2.HTTPCookieProcessor()

def login(user, pwd, cookie):
    data = {
            "username":user,
            "password":pwd
            }
    response = post(LOGIN_URL, data, cookie)
    print response

def open_deck_lists(cookie):
    for deck_list in deck_index:
        url = "%s%s" % (DECK_LIST_URL, deck_list)
        deck_list_content_html[deck_list] = get(url, cookie)
        print "deck %s" % deck_list
        time.sleep(0.1)

def post(url, data, cookie=None):
    req = urllib2.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.2.18) Gecko/20110621 Fedora/3.6.18-1.fc14 Firefox/3.6.18")
    data = urllib.urlencode(data)
    #enable cookie  
    opener = urllib2.build_opener(cookie) if cookie else urllib2.build_opener()
    response = opener.open(req, data)
    return response.read()

def get(url, cookie=None):
    req = urllib2.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.2.18) Gecko/20110621 Fedora/3.6.18-1.fc14 Firefox/3.6.18")
    opener = urllib2.build_opener(cookie) if cookie else urllib2.build_opener()
    response = opener.open(req)
    return response.read()

def read_deck_lists(deck_list_content_html):
    decks = []
    for i in deck_index:
        list_html = deck_list_content_html[i]
        soup = BeautifulSoup(list_html)
        decks_html_cont = soup.findAll("div", {"class":"sub-panel"})[0]
        decks_html = decks_html_cont.findAll("li")
        for deck_html in decks_html[:40 * 2]:
            deck_info_html = deck_html.findAll("a", {"class":"underlineable"})
            if len(deck_info_html) < 2:
                continue
            deck_name = deck_info_html[0].string
            deck_author= deck_info_html[1].string
            print deck_info_html[0]
            deck_re = re.match("/deck/v/(\d+)", deck_info_html[0]['href'])
            if deck_re:
                deck_id = int(deck_re.group(1))
                deck = {
                        "id":deck_id,
                        "name":deck_name,
                        "author":deck_author
                        }
                decks.append(deck)
            else:
                print deck_info_html[0]
    return decks

def read_deck(decks):
    decks_info = {}
    for i, deck in enumerate(decks):
        cards = []
        deck_id = deck["id"]
        deck_url = "%s%s" % (DECK_URL, deck_id)
        print i
        deck_html = get(deck_url, cookie)
        #print deck_html
        soup = BeautifulSoup(deck_html)
        trs = soup.findAll("tr")
        for tr in trs:
            span = tr.findAll("span")
            card = tr.findAll("a")
            #print span, card
            if len(span):
                card_type_re = re.match("([A-Za-z ]*) \(\d+\)", span[0].contents[1])
                card_type = card_type_re.group(1)
                #print card_type
            if len(card):
                tds = tr.findAll("td")
                card_info = read_card(card, card_type)
                card_num = tds[2].contents[0]
                card_info['num'] = card_num
                cards.append(card_info)
        decks_info[deck_id] = {
            "cards":cards,
            "info":deck
        }

        #for card_html in cards_html:
            #read_card(card_html)
        #deck_info = {}
        #deck_info.update(deck)
        #decks_info[deck["id"]] = deck_info
    return decks_info

def read_card(card_html, card_type):
    card_id = 0
    card_set_id = 0
    card_id_re = re.match("/card/v/(\d+)", card_html[0]['href'])
    if card_id_re:
        card_id = card_id_re.group(1)
    card_name = card_html[0].contents[0]
    card_set_id_re = re.match("/set/listing/(\d+)", card_html[1]['href'])
    if card_id_re:
        card_set_id = card_set_id_re.group(1)
    card_set = card_html[1].contents[0]
    card = {
        "name":card_name,
        "id":card_id,
        "set":card_set,
        "set_id":card_set_id,
        "type":card_type
    }
    return card

def output_deck(decks):
    for deck_id in decks:
        deck = decks[deck_id]
        deck_file = file("%s%s.deck" % (deck_config.DECK_DIR, deck["info"]["id"]), "w+")
        file_json = json.dumps(deck)
        deck_file.write(file_json)
        deck_file.close()

login(login_username, login_password, cookie)
open_deck_lists(cookie)
decks = read_deck_lists(deck_list_content_html)
decks_info = read_deck(decks)
output_deck(decks_info)
