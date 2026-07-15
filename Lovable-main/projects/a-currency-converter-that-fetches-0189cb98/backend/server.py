from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
import httpx
import os

app = FastAPI()

# Using ExchangeRate-API (Free tier)
API_BASE = "https://api.exchangerate-api.com/v4/latest"

@app.get("/", response_class=HTMLResponse)
def _index():
    p = Path(__file__).resolve().parent.parent / "index.html"
    return HTMLResponse(p.read_text(encoding="utf-8"))

@app.get("/api/currencies")
async def get_currencies():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/USD")
        return list(resp.json()['rates'].keys())

@app.get("/api/convert")
async def convert(amount: float, from_curr: str, to: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/{from_curr}")
        data = resp.json()
        rate = data['rates'].get(to, 1.0)
        return {"result": amount * rate}