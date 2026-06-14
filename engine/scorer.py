import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from engine.normaliser import normalise
from engine.tournament import detect_stage, winner_for_match

ROOT = Path(__file__).resolve().parents[1]

POINTS = {
    "group_win": 3,
    "group_draw": 1,
    "round_of_32": 5,
    "round_of_16": 5,
    "quarter_final": 5,
    "semi_final": 10,
    "final": 10,
    "winner": 15,
    "top_scoring_team": 5,
    "knockout_clean_sheet": 2
}


def load(path, fallback):
    p = ROOT / path
    if not p.exists():
        return fallback
    return json.loads(p.read_text(encoding="utf-8"))


def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def player_teams(players):
    return {
        p["name"]: {normalise(team) for team in p.get("teams", [])}
        for p in players
    }


def calculate():
    players = load("data/players.json", [])
    matches = load("data/live_matches.json", [])
    owned = player_teams(players)
    scores = defaultdict(int)
    goals_by_team = defaultdict(int)
    clean_sheets = defaultdict(int)
    events = []

    # Ensure every player appears even before matches begin.
    for p in players:
        scores[p["name"]] += 0

    for i, raw_match in enumerate(matches):
        match = dict(raw_match)
        match["team1"] = normalise(match.get("team1"))
        match["team2"] = normalise(match.get("team2"))
        stage = match.get("stage") or detect_stage(i)
        match["stage"] = stage

        t1, t2 = match["team1"], match["team2"]
        s1, s2 = match.get("score1"), match.get("score2")
        if s1 is None or s2 is None:
            continue

        goals_by_team[t1] += s1
        goals_by_team[t2] += s2

        team_points = defaultdict(int)
        winner = winner_for_match(match)
        if stage == "group":
            if winner:
                team_points[winner] += POINTS["group_win"]
            else:
                team_points[t1] += POINTS["group_draw"]
                team_points[t2] += POINTS["group_draw"]
        else:
            team_points[t1] += POINTS.get(stage, 0)
            team_points[t2] += POINTS.get(stage, 0)
            if s2 == 0:
                clean_sheets[t1] += 1
                team_points[t1] += POINTS["knockout_clean_sheet"]
            if s1 == 0:
                clean_sheets[t2] += 1
                team_points[t2] += POINTS["knockout_clean_sheet"]
            if stage == "final" and winner:
                team_points[winner] += POINTS["winner"]

        match_impacts = []
        for player, teams in owned.items():
            gained = sum(team_points[team] for team in teams)
            if gained:
                scores[player] += gained
                match_impacts.append({"player": player, "points": gained})
                events.append({"type": "POINTS", "text": f"{player} +{gained} from {t1} vs {t2}"})
        match["impacts"] = match_impacts

    top_scoring_teams = []
    if goals_by_team:
        max_goals = max(goals_by_team.values())
        top_scoring_teams = [team for team, goals in goals_by_team.items() if goals == max_goals]
        for player, teams in owned.items():
            if any(team in teams for team in top_scoring_teams):
                scores[player] += POINTS["top_scoring_team"]
                events.append({"type": "BONUS", "text": f"{player} +5 top-scoring nation bonus"})

    leaderboard = []
    for rank, item in enumerate(sorted(players, key=lambda p: (-scores[p["name"]], p["name"])), start=1):
        name = item["name"]
        leaderboard.append({
            "rank": rank,
            "name": name,
            "teams": item.get("teams", []),
            "points": scores[name]
        })

    state = {
        "leaderboard": leaderboard,
        "matches": matches,
        "events": events[-30:],
        "insights": {
            "top_scoring_teams": top_scoring_teams,
            "goals_by_team": dict(goals_by_team),
            "clean_sheets": dict(clean_sheets),
            "wooden_spoon": leaderboard[-1]["name"] if leaderboard else None,
            "leader": leaderboard[0]["name"] if leaderboard else None
        },
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    save("data/state.json", state)
    print("Saved leaderboard/state to data/state.json")


if __name__ == "__main__":
    calculate()
