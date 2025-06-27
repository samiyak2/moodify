from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import pubsub_v1
import os
import json

app = Flask(__name__)
CORS(app)

# Environment variables from Cloud Run deployment
PROJECT_ID = os.environ.get("GCP_PROJECT")
TOPIC_ID = os.environ.get("PUBSUB_TOPIC", "moodify-topic")

# Pub/Sub publisher setup
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.route("/")
def home():
    return "✅ Moodify Backend is Running", 200

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    mood = data.get("mood", "").lower()
    language = data.get("language", "").lower()
    artist = data.get("artist", "").strip()

    if not mood or not language:
        return jsonify({"status": "error", "message": "Mood and language are required."}), 400

    message = {
        "mood": mood,
        "language": language,
        "artist": artist or "unknown"
    }

    # Publish to Pub/Sub topic for Cloud Function
    try:
        publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
    except Exception as e:
        return jsonify({"status": "error", "message": f"Pub/Sub publish failed: {str(e)}"}), 500

    # Get playlist URL
    playlist_url = get_playlist_url(mood, language)

    return jsonify({
        "status": "success",
        "playlist_url": playlist_url
    }), 200

def get_playlist_url(mood, language):
    playlists = {
        "happy": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DWYkaDif7Ztbp",
            "punjabi": "https://open.spotify.com/playlist/2yS7J0v3LkY5rZtvfhNQ1u",
            "k-pop": "https://open.spotify.com/playlist/37i9dQZF1DX9tPFwDMOaN1",
            "spanish": "https://open.spotify.com/playlist/37i9dQZF1DX3j9EYdzv2N9",
            "arabic": "https://open.spotify.com/playlist/37i9dQZF1DX1YPTAhwehsC"
        },
        "sad": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DX3Y2yN9G3MDC",
            "punjabi": "https://open.spotify.com/playlist/6Qo1ZpPp10YkAgq4K6doRC",
            "k-pop": "https://open.spotify.com/playlist/5vSz0Iqk6yGsFtdLLGyEBF",
            "spanish": "https://open.spotify.com/playlist/4qg1bjADs4nwhpLb2GASuv",
            "arabic": "https://open.spotify.com/playlist/6XDnK6yDQ2gYQDCmmz2DCt"
        },
        "romantic": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DWYmmr74INQlb",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DX8bCfueEwWQd",
            "punjabi": "https://open.spotify.com/playlist/4VVeqhp3WxEk49IKkIgWEv",
            "k-pop": "https://open.spotify.com/playlist/3V3wLROzZ0OlhlRE3K0JAB",
            "spanish": "https://open.spotify.com/playlist/3DUJz4sl9GcZfKeIXBuMRB",
            "arabic": "https://open.spotify.com/playlist/3AwyoqVmlTYvwVYYQQeOe5"
        },
        "energetic": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DX8tZsk68tuDw",
            "hindi": "https://open.spotify.com/playlist/0XTr2mUV1dyI43q0dk5a9R",
            "punjabi": "https://open.spotify.com/playlist/0IZGkhIX6K9ByFdAgAAtWf",
            "k-pop": "https://open.spotify.com/playlist/37i9dQZF1DWUZ5bk6qqDSy",
            "spanish": "https://open.spotify.com/playlist/37i9dQZF1DWViva4SU1VgM",
            "arabic": "https://open.spotify.com/playlist/6btHxMCr5MBZQKPipqZBIq"
        },
        "calm": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DX3PIPIT6lEg5",
            "hindi": "https://open.spotify.com/playlist/0ap9F6TfJflDFHidjQMLtH",
            "punjabi": "https://open.spotify.com/playlist/3cuCzI0ZXTSi5FtA77FBEG",
            "k-pop": "https://open.spotify.com/playlist/3FfHbwQAZLz53j6ZhmnqlY",
            "spanish": "https://open.spotify.com/playlist/2lVnMZblKP7vJr6Ug8VSnk",
            "arabic": "https://open.spotify.com/playlist/2QQWYrJW7rJz6fyRTY6sTP"
        },
        "moody": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DWVxoleDT3ILq",
            "hindi": "https://open.spotify.com/playlist/6zDK1gYy7yxBEvMkM6x51L",
            "punjabi": "https://open.spotify.com/playlist/3Yx25dCDs8DAZYzuRno1kq",
            "k-pop": "https://open.spotify.com/playlist/3kSMmKkG7zoA20cxZKjUHe",
            "spanish": "https://open.spotify.com/playlist/3BMk5r1KYzjc7zMmv2MYPH",
            "arabic": "https://open.spotify.com/playlist/4Ox7iO6g1sBnMSyxUjIHgU"
        }
    }

    return playlists.get(mood, {}).get(language, "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6")  # default fallback

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)