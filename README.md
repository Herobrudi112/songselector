# songselector

Website for selecting Songs for the 2026 Abitur
## Demo
- *https://static.mosstuff.de/songselector/public/start.html*
## Features
- FastAPI backend for handling song and user submissions
- Frontend HTML (in /public) for user interaction
- Song submissions are saved to JSON files
- Supports both iTunes ID and custom link for song identification

## Backend (FastAPI)
- Located in `src/app.py`
- Endpoints:
  - `POST /send`: Accepts song submissions via json in the request body:
    - Required: `artist`, `title`, `start`
    - `start` is in seconds
    - One of: `itunesId` or `link` (however, if both are provided it'll be also saved.)
    - Saves each submission to `src/song_submissions.json`

## Frontend
- HTML files are in the `public/` directory
- `submit.html` reads song data from the URL and sends it to the backend `/send` endpoint
- Confirmation and error messages are shown based on backend response

## Setup & Usage
1. **Install dependencies:**
   ```bash
   pip install src/requirements.txt
   ```
2. **Run the backend:**
   ```bash
   python src/app.py
   ```
   The server will be available at `http://localhost:8000`
3. **Open the frontend:**
   - Open `public/start.html` or `public/select.html` in your browser
   - Song submissions will redirect to `submit.html` with the appropriate query parameters

## Notes
- No static file serving is handled by FastAPI; open HTML files directly or serve them with a separate static server if needed.
- All data is saved as JSON in the `src/` directory.

(c) Copyright 2025 Moritz Schirmer (mosstuff.de), Simon Sachsenhauser (sach.si)