import json
import os
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "live_matches.json"

API_KEY = os.getenv("RAPIDAPI_KEY", "")
API_HOST = "api-football-v1.p.rapidapi.com"

# IMPORTANT: API-Football's World Cup league/season mapping may change.
# Default is 2026 World Cup league=1. Override with GitHub repository variables if needed:
# API_FOOTBALL_LEAGUE_ID and API_FOOTBALL_SEASON.
LEAGUE_ID = os.getenv("API_FOOTBALL_LEAGUE_ID", "1")
SEASON = os.getenv("API_FOOTBALL_SEASON", "2026")
URL = f"https://{API_HOST}/v3/fixtures?league={LEAGUE_ID}&season={SEASON}"
FINISHED = {"FT", "AET", "PEN"}


def fetch_matches():
    if not API_KEY:
        print("RAPIDAPI_KEY missing. Keeping existing data/live_matches.json unchanged.")
        return

    response = requests.get(
        URL,
        headers={
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": API_HOST,
        },
        timeout=30,
    )
    print(f"API status: {response.status_code}")
    response.raise_for_status()
    payload = response.json()

    matches = []
    for item in payload.get("response", []):
        status = item.get("fixture", {}).get("status", {}).get("short")
        if status not in FINISHED:
            continue

        matches.append({
            "fixture_id": item.get("fixture", {}).get("id"),
            "date": item.get("fixture", {}).get("date"),
            "team1": item.get("teams", {}).get("home", {}).get("name"),
            "team2": item.get("teams", {}).get("away", {}).get("name"),
            "score1": item.get("goals", {}).get("home"),
            "score2": item.get("goals", {}).get("away"),
            "status": status,
        })

    matches.sort(key=lambda m: (m.get("date") or "", m.get("fixture_id") or 0))
    OUTPUT.write_text(json.dumps(matches, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(matches)} finished matches to {OUTPUT}")


if __name__ == "__main__":
    fetch_matches()
