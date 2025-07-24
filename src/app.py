from fastapi import FastAPI, Form, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import json
import os

from pydantic import BaseModel

SONG_SUBMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'song_submissions.json')

class SongBase(BaseModel):
    artist: str
    title: str
    start: str
    itunesId: str = ''
    link: str = ''

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

def check_token(token: int):
    tokens_file = os.path.join(os.path.dirname(__file__), 'tokens.json')
    if os.path.exists(tokens_file):
        with open(tokens_file, 'r', encoding='utf-8') as f:
            try:
                tokens = json.load(f)
            except json.JSONDecodeError:
                tokens = []
    else:
        tokens = []
    return token in tokens

@app.get("/send")
def submit_song_get(
    name: str = Query(...),
    token: int = Query(...),
    artist: str = Query(...),
    title: str = Query(...),
    start: str = Query(...),
    itunesId: str = Query(None),
    link: str = Query(None)
):
    if not (itunesId or link):
        return HTMLResponse(content="Missing itunesId or link", status_code=400)
    if check_token(token):
        # Load existing song submissions
        if os.path.exists(SONG_SUBMISSIONS_FILE):
            with open(SONG_SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
                try:
                    submissions = json.load(f)
                except json.JSONDecodeError:
                    submissions = []
        else:
            submissions = []
        # Remove any existing submission with the same token
        submissions = [s for s in submissions if s.get('token') != token]
        # Add new song submission
        submission = {
            "name": name,
            "token": token,
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
        return HTMLResponse(content=f"Submission successful!{extra}")
    else:
        return HTMLResponse(content=f"token invalid")

@app.post("/send")
def submit_song_post(songdata: SongBase):
    if songdata.itunesId == '' and songdata.link == '':
        raise HTTPException(status_code=400, detail="Either link or itunesId is required")
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
        "artist": songdata.artist,
        "title": songdata.title,
        "start": songdata.start
    }
    if songdata.itunesId != "":
        submission["itunesId"] = songdata.itunesId
    if songdata.link != "":
        submission["link"] = songdata.link
    submissions.append(submission)
    # Save back to file
    with open(SONG_SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, indent=2)
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
