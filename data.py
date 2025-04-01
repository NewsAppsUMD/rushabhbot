import os
import csv
import requests
from bs4 import BeautifulSoup
from slack import WebClient
from slack.errors import SlackApiError

with open('orioles_contract_data.csv', 'r', newline='') as csvfile:
    file_reader = csv.reader(csvfile)

slack_token = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=slack_token)

orioles_transactions_url = "https://www.spotrac.com/mlb/transactions/_/start/2025-01-01/end/2025-12-31/team/bal"
response = requests.get(orioles_transactions_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'})
soup = BeautifulSoup(response.text, 'html.parser')
orioles_transactions = []
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
    orioles_transactions.append(orioles_contract)
    sentence = f"The O's have made a roster move, {orioles_player_name}, {orioles_contract_details}. Hit the link to learn more: {orioles_player_url}"
    msg = sentence
    print(msg)
    # try:
    #     response = client.chat_postMessage(
    #        channel="slack-bots",
    #        text=msg,
    #        unfurl_links=True, 
    #        unfurl_media=True
    #     )
    #     print("success!")
    # except SlackApiError as e:
    #     assert e.response["ok"] is False
    #     assert e.response["error"]
    #     print(f"Got an error: {e.response['error']}")

with open('orioles_contract_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Player Name', 'Player URL', 'Contract Details']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for row in orioles_transactions:
        writer.writerow(row)



    # add if statement to see if the contract details already exist
