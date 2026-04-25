import sqlite3
import pandas as pd
import os

#Database stored in the data folder
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "scouting.db")

def get_connection():
    """
    Returns a connection to the SQLite database
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  #ensure data directory exists
    return sqlite3.connect(DB_PATH)

def create_tables():
    """
    Creates the database schema if tables do not exist yet
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS shots(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        match_id INTEGER NOT NULL,
                        player_name TEXT NOT NULL,
                        team_name TEXT NOT NULL,
                        minute INTEGER,
                        xg REAL,
                        is_goal INTEGER
        );
                         
        CREATE TABLE IF NOT EXISTS player_stats(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_name TEXT NOT NULL,
                        team_name TEXT NOT NULL,
                        total_xg REAL,
                        total_shots INTEGER,
                        total_goals INTEGER,
                        matches_played INTEGER,
                        minutes INTEGER,
                        goals_p90 REAL,
                        xg_p90 REAL,
                        performance_score REAL
        );
                         
        CREATE TABLE IF NOT EXISTS undervalued_players(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_name TEXT NOT NULL,
                        team_name TEXT NOT NULL,
                        total_xg REAL,
                        total_shots INTEGER,
                        total_goals INTEGER,
                        matches_played INTEGER,
                        minutes INTEGER,
                        goals_p90 REAL,
                        xg_p90 REAL,
                        performance_score REAL
        );
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully")

def load_to_db(df, table_name, if_exists="replace"):
    """
    Loads a DataFrame into the specified SQLite table.
    if_exists options: 'replace' (default) or 'append'
    """
    conn = get_connection()
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    conn.close()
    print(f"Loaded {len(df)} rows into table '{table_name}'.")

def query_db(sql):
    """
    Executes a SQL query and returns the result as a DataFrame
    """
    conn = get_connection()
    result = pd.read_sql_query(sql, conn)
    conn.close()
    return result