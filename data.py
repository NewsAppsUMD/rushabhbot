import os
import requests
from bs4 import BeautifulSoup
from slack import WebClient
from slack.errors import SlackApiError

slack_token = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=slack_token)

orioles_transactions_url = "https://www.spotrac.com/mlb/transactions/_/start/2025-01-01/end/2025-12-31/team/bal"
response = requests.get(orioles_transactions_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'})
soup = BeautifulSoup(response.text, 'html.parser')

orioles_transactions = []

table = soup.find('ul', attrs = {'class': 'list-group'})
for row in table.findAll('ul', attrs = {'class': 'ul'}):
    orioles_contracts = {}
    orioles_contracts['player url'] = row.a['href']
    orioles_transactions.append(orioles_contracts)

sentence = f"The O's have made a roster move, here it is: {orioles_contracts['player url']}"

msg = sentence
try:
    response = client.chat_postMessage(
        channel="slack-bots",
        text=msg,
        unfurl_links=True, 
        unfurl_media=True
    )
    print("success!")
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f"Got an error: {e.response['error']}")