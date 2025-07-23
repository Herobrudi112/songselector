from fastapi import FastAPI, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Mount /public to serve static files
app.mount("/public", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../public")), name="public")

SUBMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'submissions.json')

@app.post("/submit")
def submit_form(name: str = Form(...), code: str = Form(...)):
    # Load existing submissions
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
            try:
                submissions = json.load(f)
            except json.JSONDecodeError:
                submissions = []
    else:
        submissions = []
    # Add new submission
    submissions.append({"name": name, "code": code})
    # Save back to file
    with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)
    return JSONResponse(content={"success": True, "message": "Submission saved."})

SONG_SUBMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'song_submissions.json')

@app.get("/submit.html")
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
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Song Submission Received</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 min-h-screen flex flex-col items-center justify-center">
        <div class="bg-gray-800 rounded-xl shadow-lg p-8 max-w-md w-full text-center">
            <h2 class="text-2xl font-bold text-green-400 mb-4">Song submission received!</h2>
            <div class="text-white text-lg space-y-2">
                <p><span class="font-semibold">Artist:</span> {artist}</p>
                <p><span class="font-semibold">Title:</span> {title}</p>
                <p><span class="font-semibold">iTunes ID:</span> {itunesId}</p>
                <p><span class="font-semibold">Start:</span> {start}</p>
            </div>
            <a href="/public/select.html" class="mt-6 inline-block bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition">Zurück zur Auswahl</a>
        </div>
    </body>
    </html>
    """)

@app.get("/")
def serve_root():
    # Serve select.html at the root
    select_path = os.path.join(os.path.dirname(__file__), "../public/select.html")
    return FileResponse(select_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
