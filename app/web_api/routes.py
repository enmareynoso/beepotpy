from fastapi import FastAPI
from pymongo import MongoClient
from .mongodb import MongoDB
from fastapi.responses import HTMLResponse

app = FastAPI()
mongo = MongoDB()

@app.get("/sessions", summary="Get all SSH sessions")
async def get_sessions(limit: int = 100):
    with mongo.session() as sessions:
        return list(sessions.find().limit(limit))

@app.get("/commands", summary="Get executed commands")
async def get_commands(session_id: str):
    with mongo.commands() as commands:
        return list(commands.find({"session_id": session_id}))

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """
    <html>
        <h1>Honeypot Monitor</h1>
        <div id="sessions"></div>
        <script>
            fetch('/api/sessions')
                .then(r => r.json())
                .then(console.log)
        </script>
    </html>
    """