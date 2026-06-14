def generate_events(match, points_by_player):
    events = []
    t1 = match.get("team1")
    t2 = match.get("team2")
    s1 = match.get("score1")
    s2 = match.get("score2")

    events.append({
        "type": "FULL_TIME",
        "text": f"{t1} {s1}-{s2} {t2}"
    })

    for name, points in points_by_player.items():
        if points:
            events.append({
                "type": "POINTS",
                "text": f"{name} +{points}"
            })

    return events
