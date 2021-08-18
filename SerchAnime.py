import requests
import Config
import json

TOKEN = Config.ANNICT_TOKEN

ENDPOINT = 'https: // api.annict.com/graphql'

SERCH_ANIME_INFO = f"https://api.annict.com/v1/works?access_token={TOKEN}&filter_title="

headers = {"content-type": "application/json"}


def serchAnime(title):

    req = requests.get(SERCH_ANIME_INFO+title, headers=headers)

    data = req.json()

    return data


print(serchAnime("BLACK"))
