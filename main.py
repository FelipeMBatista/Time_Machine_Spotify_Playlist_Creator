from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests
import os

# Function to search the track infos.
def search_track(track, year):
    music = sp.search(q=f"track:{track} year:{year}", limit=1, type="track")["tracks"]["items"][0]
    try:
        music_uri = music["uri"]
    except IndexError:
        print(f"{track} doesn't exist in Spotify. Skipped.")
    return music_uri
#-------------------------------------------##-------------------------------------------#
date = input("Para que ano deseja viajar? Digite a data neste exato formato AAAA-MM-DD: ")
year = date.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
# Get the website necessary infos.
soup = BeautifulSoup(response.text, "html.parser")
song_titles = soup.select(selector="li #title-of-a-story")
song_artists = soup.select(selector="div div ul li ul li span")
top_100_song = [song.get_text().strip() for song in song_titles]
#-------------------------------------------##-------------------------------------------#
# Time do autenticate my spotify application.
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "https://example.com"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))
user_id = sp.current_user()["id"]
# Select the music URI's and saved in a list.
music_uri_list = [search_track(track=msc, year=year) for msc in top_100_song]
# Create and add the music on a playlist.
playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{date} Billboard 100",
                                   public=False
                                   )
sp.playlist_add_items(playlist_id=playlist["id"], items=music_uri_list)