import facebook
import argparse
from bs4 import BeautifulSoup

FINANCIAL_RECORDS = '1412228548889208'

parser = argparse.ArgumentParser(
	description='Generate a CSV of Fantasy auction results.'
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
except IOError, msg:
    parser.error(str(msg))

graph = facebook.GraphAPI(
	access_token=access_token, 
	version='2.7',
)

finanical_records = graph.get_object(id=FINANCIAL_RECORDS)
financial_records_html = finanical_records['message']
soup = BeautifulSoup(financial_records_html, 'html.parser')
financial_records_raw = soup.get_text('\n')

finaicial_records_string = ''
for line in financial_records_raw.split('\n'):
	finaicial_records_string += line + '\n'
	if 'Current Amount:' in line:
		finaicial_records_string += '\n'
finaicial_records_string = finaicial_records_string[:-2]

with open("financial_transactions.txt", "wb") as f:
	f.write(finaicial_records_string)
