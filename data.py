import os
import csv
import requests
from bs4 import BeautifulSoup
from slack import WebClient
from slack.errors import SlackApiError

with open('orioles_contract_data.csv', 'r', newline='') as csvfile:
    file_reader = csv.reader(csvfile)
    existing_contracts = list(file_reader)

slack_token = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=slack_token)

orioles_transactions_url = "https://www.spotrac.com/mlb/transactions/_/start/2025-01-01/end/2025-12-31/team/bal"
response = requests.get(orioles_transactions_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'})
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('ul', attrs = {'class': 'list-group'})

for row in table.findAll('li', attrs = {'class': 'list-group-item'}):
    orioles_contract = {}
    a_tag = row.find('a')
    if not a_tag:
        continue
    small_tag = row.find('small')
    if not small_tag:
        continue
    orioles_player_name = row.find('a').text
    orioles_player_url = row.find('a')['href']
    orioles_contract_details = row.find('small').text
    orioles_contract = {
        'Player Name': orioles_player_name,
        'Player URL': orioles_player_url,
        'Contract Details': orioles_contract_details
    }
    if list(orioles_contract.values()) not in existing_contracts:
        print(orioles_contract.values())
        existing_contracts.append(list(orioles_contract.values()))
        sentence = f"⚾️ Guess what? Your Baltimore Orioles made a move! {orioles_player_name}, {orioles_contract_details}. Follow the link to learn more about the move: {orioles_player_url}. For all other Orioles news, visit https://www.mlb.com/orioles! Go 0's!"
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

with open('orioles_contract_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in existing_contracts:
        writer.writerow(row)


