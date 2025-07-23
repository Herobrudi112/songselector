from fastapi import FastAPI, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from fastapi.responses import HTMLResponse

app = FastAPI()

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SONG_SUBMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'song_submissions.json')


@app.get("/send")
def submit_song(
    artist: str = Query(...),
    title: str = Query(...),
    itunesId: str = Query(...),
    start: str = Query(...)
):
    # Load existing song submissions
    if os.path.exists(SONG_SUBMISSIONS_FILE):
        with open(SONG_SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
            try:
                submissions = json.load(f)
            except json.JSONDecodeError:
                submissions = []
    else:
        submissions = []
    # Add new song submission
    submissions.append({
        "artist": artist,
        "title": title,
        "itunesId": itunesId,
        "start": start
    })
    # Save back to file
    with open(SONG_SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)
    # Return a simple HTML confirmation
    return JSONResponse(content=f"")

@app.get("/submit.html")
def submit_song(
    artist: str = Query(...),
    title: str = Query(...),
    start: str = Query(...),
    itunesId: str = Query(None),
    link: str = Query(None)
):
    # Load existing song submissions
    if os.path.exists(SONG_SUBMISSIONS_FILE):
        with open(SONG_SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
            try:
                submissions = json.load(f)
            except json.JSONDecodeError:
                submissions = []
    else:
        submissions = []
    # Add new song submission
    submission = {
        "artist": artist,
        "title": title,
        "start": start
    }
    if itunesId:
        submission["itunesId"] = itunesId
    if link:
        submission["link"] = link
    submissions.append(submission)
    # Save back to file
    with open(SONG_SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)
    # Build confirmation HTML
    extra = f"<p><span class='font-semibold'>iTunes ID:</span> {itunesId}</p>" if itunesId else f"<p><span class='font-semibold'>Link:</span> {link}</p>"
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>Song Submission Received</title>
        <script src=\"https://cdn.tailwindcss.com\"></script>
    </head>
    <body class=\"bg-gray-900 min-h-screen flex flex-col items-center justify-center\">
        <div class=\"bg-gray-800 rounded-xl shadow-lg p-8 max-w-md w-full text-center\">
            <h2 class=\"text-2xl font-bold text-green-400 mb-4\">Song submission received!</h2>
            <div class=\"text-white text-lg space-y-2\">
                <p><span class=\"font-semibold\">Artist:</span> {artist}</p>
                <p><span class=\"font-semibold\">Title:</span> {title}</p>
                {extra}
                <p><span class=\"font-semibold\">Start:</span> {start}</p>
            </div>
            <a href=\"/public/select.html\" class=\"mt-6 inline-block bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition\">Zurück zur Auswahl</a>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
