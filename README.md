# Spotify ETL Project

This Python project is an ETL pipeline that downloads information (from the Spotify API) on what songs a user has listened
to in the last 24 hours, and saves that information in an SQL database.

The project saves information on the song title, artist name, when it was played and its timestamp.

## Prerequisites

Before you continue, ensure you have met the following requirements:

* You have installed the latest version of Python
* You have installed the required packages by typing the following command in your terminal:
  
  ```pip install -r requirements.txt```
* You have a connection to an SQLite database

## How to use

* You must create a ```config.ini``` file and under ```[USER DETAILS]```, create the variables ```DATABASE_LOCATION```
  which is the location of your SQL database, ```USER_ID``` which is your Spotify username and ```TOKEN``` which is your
  unique token for the Spotify API and can be generated [here](https://developer.spotify.com/console/get-recently-played/).
  