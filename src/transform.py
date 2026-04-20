import pandas as pd

def extract_shots_features(shots_df):
    """
    Recieves the raw shots DataFrame and returns a clean one with relevant nested fields flattened
    """
    df = shots_df.copy()

    #Extract nested fields
    df["player_name"] = df["player"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
    df["team_name"] = df["team"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
    df["xg"] = df["shot"].apply(lambda x: x.get("statsbomb_xg") if isinstance(x, dict) else None)
    df["outcome"] = df["shot"].apply(lambda x: x.get("outcome", {}).get("name") if isinstance(x, dict) else None)
    df["is_goal"] = (df["outcome"] == "Goal").astype(int)

    #Keep only relevant columns
    clean = df[["match_id", "player_name", "team_name", "minute", "xg", "is_goal"]].copy()
    clean = clean.dropna(subset=["player_name", "xg"])

    return clean

def calculate_player_stats(clean_shots_df, matches_df):
    """
    Aggregates by player and calculates scouting metrics:
    - Total xG
    - Total goals
    - Minutes played (aproximated from matches played)
    - Goals per 90 minutes
    - xG per 90 minutes
    - Performance score
    """
    #Approximate minutes from number of matches played
    matches_played = (
        clean_shots_df.groupby("player_name")["match_id"]
        .nunique()
        .reset_index()
        .rename(columns={"match_id": "matches_played"})
    )
    matches_played["minutes"] = matches_played["matches_played"] * 90

    #Aggregate stats per player
    stats = (
        clean_shots_df.groupby("player_name")
        .agg(
            team_name = ("team_name", "last"),
            total_xg = ("xg", "sum"),
            total_shots = ("xg", "count"),
            total_goals = ("is_goal", "sum")
        )
        .reset_index()
    )

    #Merge minutes
    stats = stats.merge(matches_played, on = "player_name")

    #Per 90 minutes
    stats["goals_p90"] = (stats["total_goals"] / stats["minutes"] * 90).round(2)
    stats["xg_p90"] = (stats["total_xg"] / stats["minutes"] * 90).round(2)

    #Performance score - weighted combination of xG quality and finishing
    stats["performance_score"] = (
        (stats["xg_p90"] * 0.5) + (stats["goals_p90"] * 0.5)
    ).round(3)

    #Sort by performance score descending
    stats = stats.sort_values("performance_score", ascending=False).reset_index(drop=True)

    return stats

def get_undervalued_players(stats_df, min_shots=5, xg_threshold=0.25, min_matches=3):
    """
    Identifies undervalued players:
    - Generate quality chances (high xg_p90)
    - Minimum shot threshold for statistical relevance
    """
    mask = (
        (stats_df["total_shots"] >= min_shots) &
        (stats_df["xg_p90"] >= xg_threshold) &
        (stats_df["matches_played"] >= min_matches)
    )
    return stats_df[mask].reset_index(drop=True)