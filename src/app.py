from fastapi import FastAPI, Form, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import json
import os

from pydantic import BaseModel

SONG_SUBMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'song_submissions.json')
class SongBase(BaseModel):
    name: str
    token: int
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




@app.post("/send")
def submit_song(songdata: SongBase):  
    if not songdata.itunesId and not songdata.link:
        raise HTTPException(status_code=400, detail="Either link or itunesId is required")

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

    if check_token(songdata.token):
        if os.path.exists(SONG_SUBMISSIONS_FILE):
            with open(SONG_SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
                try:
                    submissions = json.load(f)
                except json.JSONDecodeError:
                    submissions = []
        else:
            submissions = []

        # Remove previous submission with same token
        submissions = [s for s in submissions if s.get('token') != songdata.token]

        # Build new submission
        submission = {
            "name": songdata.name,
            "token": songdata.token,
            "artist": songdata.artist,
            "title": songdata.title,
            "start": songdata.start
        }
        if songdata.itunesId:
            submission["itunesId"] = songdata.itunesId
        if songdata.link:
            submission["link"] = songdata.link

        submissions.append(submission)

        with open(SONG_SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, ensure_ascii=False, indent=2)

        return HTMLResponse(content="success")
    else:
        return HTMLResponse(content="invalid_token")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
