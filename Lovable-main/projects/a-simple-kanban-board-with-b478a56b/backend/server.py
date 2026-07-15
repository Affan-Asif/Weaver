from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def _index():
    p = Path(__file__).resolve().parent.parent / "index.html"
    return HTMLResponse(p.read_text(encoding="utf-8"))