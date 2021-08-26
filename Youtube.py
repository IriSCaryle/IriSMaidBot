import Config
from googleapiclient.discovery import build, key2param
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import requests
DEVELOPER_KEY = Config.YOUTUBE_TOKEN


def serchYoutube(key):
    url = f"https://www.googleapis.com/youtube/v3/search?type=video&part=snippet&q={key}&key={DEVELOPER_KEY}"

    res = requests.get(url)

    data = res.json()
    print(data)

    return data["items"][0]["id"]["videoId"], GetTitle(data)


def GetTitle(data):
    return data["items"][0]["snippet"]["title"]
