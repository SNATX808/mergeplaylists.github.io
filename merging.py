import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='21c6b1a5496745ca9434016de07d7031',
    client_secret='e0f503801cb447d9ad08445338bdacb0',
    redirect_uri='http://localhost:8888/callback',
    scope="playlist-read-private"
))

# YouTube Music Authentication
ytmusic = YTMusic('headers_auth.json')  # You need to create headers_auth.json using ytmusicapi setup

def get_spotify_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in results['items']:
        track = item['track']
        tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name']
        })
    return tracks

def search_youtube_music_track(track_name, artist_name):
    search_results = ytmusic.search(query=f"{track_name} {artist_name}", filter="songs")
    if search_results:
        return search_results[0]['videoId']  # First result ID
    return None

def create_youtube_music_playlist(playlist_name, description, track_ids):
    playlist_id = ytmusic.create_playlist(playlist_name, description)
    ytmusic.add_playlist_items(playlist_id, track_ids)
    return playlist_id

# Main function to combine playlists
def combine_playlists_to_youtube_music(spotify_playlist_id, youtube_playlist_name):
    # Step 1: Get tracks from Spotify
    spotify_tracks = get_spotify_tracks(spotify_playlist_id)

    # Step 2: Search for each track on YouTube Music
    youtube_track_ids = []
    for track in spotify_tracks:
        video_id = search_youtube_music_track(track['name'], track['artist'])
        if video_id:
            youtube_track_ids.append(video_id)

    # Step 3: Create a YouTube Music playlist and add tracks
    if youtube_track_ids:
        playlist_id = create_youtube_music_playlist(youtube_playlist_name, "Combined playlist from Spotify", youtube_track_ids)
        print(f"Playlist created with ID: {playlist_id}")
    else:
        print("No matching tracks found on YouTube Music.")

# Example usage
spotify_playlist_id = "your_spotify_playlist_id"
youtube_playlist_name = "My Combined Playlist"
combine_playlists_to_youtube_music(spotify_playlist_id, youtube_playlist_name)
