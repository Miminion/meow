import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")
LEADERBOARD_FILE = Path("leaderboard.json")

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}


def load_settings():
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        settings = json.load(file)

    for key in DEFAULT_SETTINGS:
        if key not in settings:
            settings[key] = DEFAULT_SETTINGS[key]

    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not LEADERBOARD_FILE.exists():
        save_leaderboard([])
        return []

    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_leaderboard(scores):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


def add_score(name, score, distance, coins):
    scores = load_leaderboard()

    scores.append({
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })

    scores.sort(key=lambda item: item["score"], reverse=True)
    scores = scores[:10]

    save_leaderboard(scores)