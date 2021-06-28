import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime
import datetime
import sqlite3
from pprint import pprint

# creating constants
DATABASE_LOCATION = "sqlite://my_played_tracks.sqlite"
USER_ID = "kd2187"
TOKEN = "BQClU3Yiq6bvHhGBU6fes39pfznTf8e7Q8w8hlILYIV50PVIUiobgYwVo91D2CGQUFtY_oQng0XNnzGcuvzT16MLuF8wiaD_9EYkKN_-SrN2-iHcUV8SUbpUU15nXw4qt48MdlIYVoGQ1T0"

if __name__ == "__main__":
    # populating fields according to API instructions
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".
                     format(time=yesterday_unix_timestamp), headers=headers)

    data = r.json()

    # pprint(data)

    # extracting only relevant info
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    # preparing dictionary for insertion into dataframe
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_names", "played_at", "timestamp"])

    pd.set_option('display.max_columns', None)
    # print(song_df)
