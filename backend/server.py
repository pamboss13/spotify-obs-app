# backend/server.py
# Basic Flask server structure - will be expanded later

from flask import Flask, jsonify, redirect, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = os.urandom(64) # For session management

# --- Spotify Configuration --- #
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'user-read-currently-playing'
CACHE_PATH = 'spotify_cache'

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_PATH,
        show_dialog=True
    )

def get_spotify_client():
    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        # No token, need to authorize
        return None, None # Indicate no client and need for auth

    # Refresh token if needed
    now = int(time.time())
    is_token_expired = token_info['expires_at'] - now < 60
    if is_token_expired:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return spotipy.Spotify(auth=token_info['access_token']), token_info['access_token']

# --- Routes --- #

@app.route('/')
def index():
    # Serve the frontend index.html
    return app.send_static_file('index.html')

@app.route('/login')
def login():
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = get_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    # Don't store the token in the session, rely on cache file
    # session['spotify_token_info'] = token_info
    return redirect('/') # Redirect back to the main page

@app.route('/current-song')
def current_song():
    sp, access_token = get_spotify_client()

    if not sp:
        # Not authenticated yet, redirect to login or send error
        # For an API, sending an error is better
        return jsonify({'error': 'Not authenticated', 'auth_needed': True}), 401

    current_track = sp.current_user_playing_track()

    if current_track is None or not current_track['is_playing']:
        return jsonify({'is_playing': False})

    track_info = {
        'is_playing': True,
        'item': {
            'id': current_track['item']['id'],
            'name': current_track['item']['name'],
            'artists': [{'name': artist['name']} for artist in current_track['item']['artists']],
            'album': {
                'name': current_track['item']['album']['name'],
                'images': current_track['item']['album']['images']
            }
        },
        'progress_ms': current_track['progress_ms'],
        'duration_ms': current_track['item']['duration_ms'],
        'access_token': access_token # Optionally send token if frontend needs direct access (less secure)
    }
    return jsonify(track_info)

if __name__ == '__main__':
    print("IMPORTANT: Your browser will likely show a security warning for the self-signed certificate.")
    print("You will need to accept the risk or proceed anyway to continue.")
    print("Visit https://localhost:5000 in your browser.") # Changed to HTTPS
    # Check if auth needed
    sp, _ = get_spotify_client()
    if not sp:
        # Note: The /login endpoint needs to be visited via HTTPS now too.
        print("Authentication required. Please visit https://localhost:5000/login to authorize.") # Changed to HTTPS

    # Use debug=False in production
    # Add ssl_context='adhoc' to enable HTTPS with a self-signed certificate
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc') 