from engine.normaliser import normalise

GROUP_MATCHES = 72
ROUND_OF_32_END = 88
ROUND_OF_16_END = 96
QUARTER_FINAL_END = 100
SEMI_FINAL_END = 102
FINAL_END = 104


def detect_stage(match_index):
    number = match_index + 1
    if number <= GROUP_MATCHES:
        return "group"
    if number <= ROUND_OF_32_END:
        return "round_of_32"
    if number <= ROUND_OF_16_END:
        return "round_of_16"
    if number <= QUARTER_FINAL_END:
        return "quarter_final"
    if number <= SEMI_FINAL_END:
        return "semi_final"
    return "final"


def winner_for_match(match):
    team1 = normalise(match.get("team1"))
    team2 = normalise(match.get("team2"))
    score1 = match.get("score1")
    score2 = match.get("score2")

    if score1 is None or score2 is None:
        return None
    if score1 > score2:
        return team1
    if score2 > score1:
        return team2
    return None
