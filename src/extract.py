import json
import os
import pandas as pd     #converts data into a DataFrame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "statsbomb")             #constant defining where data lives

def load_competitions():
    """Loads all available competitions"""
    path = os.path.join(DATA_PATH, "competitions.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def load_matches(competition_id, season_id):
    """Loads matches for a given competition and season"""
    path = os.path.join(DATA_PATH, "matches", str(competition_id), f"{season_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def load_events(match_id):
    """Loads all events for a given match"""
    path = os.path.join(DATA_PATH, "events", f"{match_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def load_all_events(match_ids):
    """Loads and concatenates events from multiple matches"""
    all_events = []
    for match_id in match_ids:
        df = load_events(match_id)
        df["match_id"] = match_id       #Track the source match
        all_events.append(df)
    return pd.concat(all_events, ignore_index=True)