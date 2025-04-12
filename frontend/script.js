const spotifyWidget = document.getElementById('spotify-widget');
const albumArt = document.getElementById('album-art');
const trackName = document.getElementById('track-name');
const artistName = document.getElementById('artist-name');
const albumName = document.getElementById('album-name');
// const progressBar = document.getElementById('progress-bar'); // Uncomment if using progress bar
const authMessage = document.getElementById('auth-message');
const noSongMessage = document.getElementById('no-song-message');

let currentTrackId = null; // Keep track of the current song to avoid unnecessary updates
let updateInterval; // To store the interval ID

async function fetchCurrentSong() {
    try {
        const response = await fetch('/current-song');

        if (response.status === 401) {
            // Authentication needed
            console.log("Authentication required.");
            spotifyWidget.classList.add('hidden');
            noSongMessage.classList.add('hidden');
            authMessage.classList.remove('hidden');
            // Optionally stop polling if auth is needed
            if (updateInterval) clearInterval(updateInterval);
            return;
        }

        if (!response.ok) {
            console.error('Error fetching song:', response.statusText);
            // Maybe show a temporary error message?
            return;
        }

        const data = await response.json();

        // Hide auth message if we get here
        authMessage.classList.add('hidden');

        if (data.is_playing) {
            noSongMessage.classList.add('hidden');
            spotifyWidget.classList.remove('hidden');

            // Only update DOM if the track is different
            if (data.item.id !== currentTrackId) {
                currentTrackId = data.item.id;
                updateUI(data);
            }
            // Update progress bar even if song is the same (if implemented)
            // updateProgressBar(data.progress_ms, data.item.duration_ms);

        } else {
            // No song playing
            currentTrackId = null;
            spotifyWidget.classList.add('hidden');
            noSongMessage.classList.remove('hidden');
        }

    } catch (error) {
        console.error('Error fetching current song:', error);
        // Handle network errors, etc.
        spotifyWidget.classList.add('hidden');
        noSongMessage.classList.add('hidden');
        // Don't show auth message for general network errors
    }
}

function updateUI(data) {
    trackName.textContent = data.item.name;
    artistName.textContent = data.item.artists.map(artist => artist.name).join(', ');
    albumName.textContent = data.item.album.name;

    // Find the best image URL (e.g., medium size)
    let imageUrl = 'placeholder.png'; // Default placeholder
    if (data.item.album.images && data.item.album.images.length > 0) {
        // Prefer 64px or smallest available if larger doesn't exist
        const suitableImage = data.item.album.images.find(img => img.height >= 64 && img.height <= 100) || data.item.album.images[data.item.album.images.length - 1];
         if (suitableImage) {
             imageUrl = suitableImage.url;
         }
    }
    albumArt.src = imageUrl;
    albumArt.alt = `Album art for ${data.item.album.name}`;
}

/* // Uncomment if using progress bar
function updateProgressBar(progressMs, durationMs) {
    if (progressBar && progressMs != null && durationMs != null && durationMs > 0) {
        const progressPercent = (progressMs / durationMs) * 100;
        progressBar.style.width = `${progressPercent}%`;
    }
}
*/

// --- Initialization ---

// Fetch the song immediately on load
fetchCurrentSong();

// Set an interval to fetch the song periodically (e.g., every 5 seconds)
// Adjust interval as needed - less frequent is less load on Spotify API
updateInterval = setInterval(fetchCurrentSong, 5000); 