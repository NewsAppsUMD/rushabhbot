import os
import requests
from bs4 import BeautifulSoup
from slack import WebClient
from slack.errors import SlackApiError

slack_token = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=slack_token)

orioles_trans_url = "https://www.spotrac.com/mlb/transactions/_/start/2025-01-01/end/2025-12-31/team/bal"
r = requests.get(orioles_trans_url)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())





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