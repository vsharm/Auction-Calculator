import facebook
import requests
import re
import csv
import argparse
from bs4 import BeautifulSoup


GROUP_ID = '310613432384064'

def find_dollars(current_cost, line):
    re_new_cost = re.search("\d+",line)
    if re_new_cost != None:
        return re_new_cost.group()
    return current_cost

def capitalize_name(raw_name):
    name_tokens = raw_name.split(' ')
    cap_name_tokens = []
    for name in name_tokens:
        cap_name_tokens.append(name[0].upper() + name[1:])
    return " ".join(cap_name_tokens)

def get_player_name(line):
    # remove $ and any number
    line = re.sub("\$|\d+", '', line)
    if len(line) == 0:
        return False
    # remove leading or trailing space
    if line[-1] == ' ':
        line = line[:-1]
    if line[0] == ' ':
        line = line[1:]
    return capitalize_name(line)

def get_owner_first_name(full_name):
    return full_name.split(' ')[0]

# warning does not return a value
# changes underlying object
def update_with_paging(obj):
    if 'paging' in obj and 'next' in obj['paging']:
        page = requests.get(obj['paging']['next']).json()
        obj = dict(obj.items() + page.items())
        return update_with_paging(obj)
    return obj

parser = argparse.ArgumentParser(
    description='Generate a CSV of Fantasy auction results.'
)
parser.add_argument(
    'fbid', 
    metavar='fbid', 
    type=int, 
    help='Facebook ID for auction post'
)
parser.add_argument(
    'access_token', 
    metavar='access_token', 
    type=str,
    help=("Facebook Access Token." 
          + " Get one here: https://developers.facebook.com/tools/explorer/")
    )

access_token = ''
fbid = ''
try:
    arguments = parser.parse_args()
    access_token = arguments.access_token
    fbid = arguments.fbid
except IOError, msg:
    parser.error(str(msg))

graph = facebook.GraphAPI(
    access_token=access_token, 
    version='2.7',
)
comments = graph.get_connections(
    id=GROUP_ID + '_' + str(fbid),
    connection_name='comments',
)
comments = update_with_paging(comments)

auction_results = []
for comment in comments['data']:
    message = comment['message']
    player = get_player_name(message)
    if not player:
        continue
    cost = find_dollars(1, message)
    owner = get_owner_first_name(comment['from']['name'])
    fbid = comment['id']    
    replies = graph.get_connections(
        id=fbid,
        connection_name='comments',
    )
    replies = update_with_paging(replies)
    for reply in replies['data']:
        message = reply['message']
        if find_dollars(cost, message) == cost:
            continue
        owner = get_owner_first_name(reply['from']['name'])
        cost = find_dollars(cost, message)
    auction_results.append([owner, player, cost])

with open("input.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(auction_results)
