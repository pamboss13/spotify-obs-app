# Spotify OBS Overlay

This project displays the currently playing Spotify song as an overlay in OBS.

## Features

*   Shows current song title, artist, and album art.
*   Automatically updates when the song changes.

## Setup

1.  **Spotify API Credentials:**
    *   Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    *   Create a new application.
    *   Note down your `Client ID` and `Client Secret`.
    *   Edit the app settings and add `http://127.0.0.1:8000/callback` to the "Redirect URIs". Ensure this exactly matches the `SPOTIPY_REDIRECT_URI` in your `.env` file.

2.  **Backend Setup:**
    *   Navigate to the `backend` directory.
    *   Create a `.env` file by copying `.env.example`:
        ```bash
        cp .env.example .env
        ```
    *   Fill in your `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI` (`http://127.0.0.1:8000/callback`) in the `.env` file.
    *   Install dependencies:
        ```bash
        # Ensure pip is available or use python -m pip
        python -m pip install -r requirements.txt
        ```
    *   Run the server:
        ```bash
        python server.py
        ```
    *   The server will run on `http://127.0.0.1:8000`.
    *   If it's your first time or the cache is cleared, visit `http://127.0.0.1:8000/login` in your browser to authorize the app with your Spotify account.

3.  **Frontend Setup:**
    *   (No specific setup needed).

4.  **OBS Integration:**
    *   Add a "Browser" source in OBS.
    *   Set the URL to `http://127.0.0.1:8000`.
    *   Adjust the width and height as needed.

## How it Works

The backend (`server.py`) uses the [Spotipy](https://spotipy.readthedocs.io/) library to authenticate with the Spotify API and fetch the currently playing track. It provides an API endpoint (`/current-song`) that the frontend can query.

The frontend (`index.html`, `style.css`, `script.js`) fetches the song data from the backend endpoint periodically and updates the display. 