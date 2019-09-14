import spotipy
import json
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import datetime

def lambda_handler(event, context):
    artist_limit = 50
    lastfm_user = "XXXX"
    lastfm_api_key = "XXXX"
    notify_id = "XXXX"
    spotify_client_id = "XXXX"
    spotify_client_secret = "XXXX"


    client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    notify_url ="https://notify.run/" + notify_id
    lastfm_url = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+ lastfm_user + "&api_key=" + lastfm_api_key + "&format=json&limit=" + str(artist_limit)
    yesterday = str(datetime.date.fromordinal(datetime.date.today().toordinal()-1))
    response = requests.get(lastfm_url)
    data = json.loads(response.text)


    artists = []
    album_releases = []

    def album_finder(artist):
        #print(artist)
        try:
            uri = sp.search(q='artist:' + artist, type='artist')["artists"]["items"][0]["uri"]
            album_search = sp.artist_albums(uri, limit=1)
            album_details = [artist, album_search["items"][0]["name"],album_search["items"][0]["release_date"],album_search["items"][0]["external_urls"]["spotify"]]
            
        except:
            print(artist,"Failed Search!")
            album_details = [artist,"NA","NA","NA"]
        
        return album_details

    for i in range(artist_limit):
        artist = data["topartists"]["artist"][i]["name"]
        artists.append(artist)
        album = album_finder(artist)
        if album[2] == yesterday:
            album_releases.append(album)
            album_string = " ".join(album)
            requests.post(url = notify_url, data = album_string)

    print(yesterday, album_releases)

    if len(album_releases) == 0:
         requests.post(url = notify_url, data = "No Releases"
                       )
