import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIASES_PATH = ROOT / "data" / "team_aliases.json"


def load_aliases():
    if not ALIASES_PATH.exists():
        return {}
    return json.loads(ALIASES_PATH.read_text(encoding="utf-8"))


ALIASES = load_aliases()


def normalise(team):
    if not team:
        return team
    return ALIASES.get(team, team)
