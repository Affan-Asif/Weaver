from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import markdown

app = FastAPI()

class MarkdownRequest(BaseModel):
    text: str

@app.post("/convert")
def convert_markdown(payload: MarkdownRequest):
    html = markdown.markdown(payload.text, extensions=['extra', 'codehilite', 'toc'])
    return {"html": html}

@app.get("/", response_class=HTMLResponse)
def _index():
    p = Path(__file__).resolve().parent.parent / "index.html"
    return HTMLResponse(p.read_text(encoding="utf-8"))