import configparser
import sqlalchemy
import pandas as pd
import requests
from datetime import datetime
import datetime
import sqlite3
from pprint import pprint

# read local `config.ini` file which contains database and token details
config = configparser.ConfigParser()
config.read('config.ini')
token = config.get('USER DETAILS', 'TOKEN')
database = config.get('USER DETAILS', 'DATABASE_LOCATION')


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # checking response code
    if r.status_code == 200:
        print("OK. The request has succeeded.")
    else:
        print("There has been an error. Please check you have a valid token.")

    # checking if dataframe is empty
    # reasons could be empty: something went wrong in extract stage or no songs were listened to in last 24 hours
    if df.empty:
        print("No songs downloaded. Execution finished.")
        return False

    # primary key check, using played_at as primary key
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary key check is violated.")

    # checking for nulls
    if df.isnull().values.any():
        raise Exception("Null values found.")

    return True


if __name__ == "__main__":
    # populating fields according to API instructions
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?after={yesterday_unix_timestamp}"
                     , headers=headers)

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

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    pd.set_option('display.max_columns', None)
    # print(song_df)

    # validation
    if check_if_valid_data(song_df):
        print("Data has been validated. Proceed to load stage.")

    # load

    # initiating connection to database
    conn = sqlite3.connect('my_played_tracks.sqlite')
    # cursor allows us to refer to specific rows in the database
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Database created.")

    # writing the dataframe to an SQL database
    try:
        song_df.to_sql("my_played_tracks", conn, index=False, if_exists="append")
    except:
        print("Data already exists in database.")

    conn.close()
    print("Database closed.")

