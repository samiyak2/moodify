import base64
import json
from google.cloud import storage
import datetime
import requests
import os

def subscribe_and_process(event, context):
    if 'data' not in event:
        print("❌ No data found in Pub/Sub message")
        return

    # Decode message
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    data = json.loads(pubsub_message)

    mood = data.get("mood", "")
    language = data.get("language", "")
    artist = data.get("artist", "")
    timestamp = datetime.datetime.utcnow().isoformat()

    # Step 1: Get Spotify Access Token
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        auth=(client_id, client_secret)
    )

    if auth_response.status_code != 200:
        print("❌ Failed to authenticate with Spotify")
        return

    access_token = auth_response.json().get('access_token')

    # Step 2: Search Spotify for a playlist
    query = f"{mood} {language} {artist}".strip()
    headers = {"Authorization": f"Bearer {access_token}"}
    search_url = "https://api.spotify.com/v1/search"
    params = {
        "q": query,
        "type": "playlist",
        "limit": 1
    }

    search_response = requests.get(search_url, headers=headers, params=params)

    playlist_url = "https://open.spotify.com"
    if search_response.status_code == 200:
        items = search_response.json().get('playlists', {}).get('items', [])
        if items:
            playlist_url = items[0].get("external_urls", {}).get("spotify", playlist_url)

    # Step 3: Save to Cloud Storage
    result = {
        "mood": mood,
        "language": language,
        "artist": artist,
        "playlist_url": playlist_url,
        "timestamp": timestamp
    }

    bucket_name = "moodify"
    filename = f"{mood}_{language}_{timestamp}.json"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(
        data=json.dumps(result, indent=2),
        content_type="application/json"
    )

    print(f"✅ Saved playlist result to {filename}")