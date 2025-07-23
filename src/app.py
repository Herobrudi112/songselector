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
    return HTMLResponse(content=f"""""")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
