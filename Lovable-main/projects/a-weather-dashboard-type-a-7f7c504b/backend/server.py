import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()
db_path = Path("kanban.db")

def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    with get_db() as db:
        db.execute("CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY, text TEXT, status TEXT)")
        db.commit()

@app.get("/", response_class=HTMLResponse)
def _index():
    return HTMLResponse((Path(__file__).parent.parent / "index.html").read_text())

@app.get("/api/cards")
def get_cards():
    with get_db() as db:
        return [dict(row) for row in db.execute("SELECT * FROM cards").fetchall()]

class Card(BaseModel):
    text: str = None
    status: str

@app.post("/api/cards")
def add_card(card: Card):
    with get_db() as db:
        db.execute("INSERT INTO cards (text, status) VALUES (?, ?)", (card.text, card.status))
        db.commit()
    return {"status": "ok"}

@app.put("/api/cards/{card_id}")
def update_card(card_id: int, card: Card):
    with get_db() as db:
        db.execute("UPDATE cards SET status = ? WHERE id = ?", (card.status, card_id))
        db.commit()
    return {"status": "ok"}