# songselector

Website for selecting Songs for the 2026 Abitur

## Features
- FastAPI backend for handling song and user submissions
- Frontend HTML (in /public) for user interaction
- Song submissions are saved to JSON files
- Supports both iTunes ID and custom link for song identification

## Backend (FastAPI)
- Located in `src/app.py`
- Endpoints:
  - `POST /send`: Accepts form submissions with `name` and `code` (not used by the song submission frontend)
  - `GET /submit.html`: Accepts song submissions via query parameters:
    - Required: `artist`, `title`, `start`
    - One of: `itunesId` or `link`
    - Example: `http://localhost:8000/submit.html?artist=Artist&title=Song&itunesId=123456&start=0`
    - Saves each submission to `src/song_submissions.json`
    - Returns a styled confirmation page

## Frontend
- HTML files are in the `public/` directory
- `submit.html` reads song data from the URL and sends it to the backend `/submit.html` endpoint
- Confirmation and error messages are shown based on backend response

## Setup & Usage
1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn
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
- Song submissions support both iTunes ID and custom links.
- All data is saved as JSON in the `src/` directory.
