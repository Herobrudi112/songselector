from fastapi import FastAPI, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUBMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'submissions.json')

# POST endpoint for form submissions (name and code)
@app.post("/send")
def send_form(name: str = Form(...), code: str = Form(...)):
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
    return JSONResponse(content=f"""""")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
