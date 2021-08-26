import requests
import Config
import json
# Annict Access Token
TOKEN = Config.ANNICT_TOKEN
ENDPOINT = 'https: // api.annict.com/graphql'

SERCH_ANIME_INFO = f"https://api.annict.com/v1/works?access_token={TOKEN}&filter_title="

headers = {"content-type": "application/json"}


def serchAnime(title):
    req = requests.get(SERCH_ANIME_INFO+title, headers=headers)
    data = req.json()
    result, titles = getInfo(data)
    return result, titles


def getInfo(j):
    titles = [c["title"] for i, c in enumerate(j["works"])]
    ids = [c["id"] for i, c in enumerate(j["works"])]
    officialURLs = [c["official_site_url"] for i, c in enumerate(j["works"])]
    wikis = [c["wikipedia_url"] for i, c in enumerate(j["works"])]
    episodeNums = [c["episodes_count"] for i, c in enumerate(j["works"])]
    try:
        seasons = [c["season_name_text"] for i, c in enumerate(j["works"])]
    except:
        print("シーズンがありません")
        seasons = None
    return displayInfo(ids, titles, officialURLs, wikis, episodeNums, seasons), titles


def displayInfo(id, title, ofURL, Wiki, episodeNum, season):
    if season != None:
        l = [f"""タイトル:{title[i]} 
        シーズン:{season[i]}
        エピソード数:{episodeNum[i]}
        公式HP:{ofURL[i]} 
        Wiki:{Wiki[i]} 
        APIのid:{id[i]} """
             for i in range(len(id))]
    else:
        l = [f"""タイトル:{title[i]} 
        エピソード数:{episodeNum[i]}
        公式HP:{ofURL[i]} 
        Wiki:{Wiki[i]} 
        APIのid:{id[i]} """
             for i in range(len(id))]

    return l


# serchAnime("ぶらっくらぐーん")
