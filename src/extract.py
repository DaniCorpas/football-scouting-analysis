import json
import os
import pandas as pd     #convierte los datos en un DataFrame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "statsbomb")             #constante que define donde viven los datos

def load_competitions():
    """Carga todas las competiciones disponibles"""
    path = os.path.join(DATA_PATH, "competitions.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def load_matches(competition_id, season_id):
    """Carga los partidos de una competición y temporada"""
    path = os.path.join(DATA_PATH, "matches", str(competition_id), f"{season_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def load_events(match_id):
    """Carga todos los eventos de un partido"""
    path = os.path.join(DATA_PATH, "events", f"{match_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def load_all_events(match_ids):
    """Carga y concatena eventos de múltiples partidos"""
    all_events = []
    for match_id in match_ids:
        df = load_events(match_id)
        df["match_id"] = match_id       #Guardamos el origen
        all_events.append(df)
    return pd.concat(all_events, ignore_index=True)