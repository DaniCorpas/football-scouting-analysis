# Football Scouting Analysis

ETL pipeline for identifying undervalued football players using StatsBomb open data.

## Tech stack
- Python · Pandas · SQLite · Jupyter · Power BI

## Project structure
```
football-scouting-analysis/
├── data/         <- ignored in git (see below)
├── notebooks/    <- exploration and analysis
│   ├── 01_exploration.ipynb
│   └── 02_visualizations.ipynb
├── src/          <- pipeline modules
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── visualize.py
└── visuals/      <- charts and dashboards
```
## Setup

```bash
# 1 - Clone this repo
git clone https://github.com/DaniCorpas/football-scouting-analysis.git

# 2 - Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate.ps1  # Windows

# 3 - Install dependencies
pip install -r requirements.txt

# 4 - Download StatsBomb open data
git clone https://github.com/statsbomb/open-data.git
# Copy open-data/data into data/statsbomb/
```

## Pipeline
StatsBomb JSON --> extract.py --> transform.py --> load.py --> SQLite --> Power BI

## Architecture decisions
This project uses **SQLite** as the local database for simplicity and portability - the `scouting.db` file can be 
opened by anyone without installing a server.

In a production environment this would be replaced by:
- **PostgreSQL** -> for a self-hosted or cloud pipeline
- **Snowflake / BigQuery** -> for a cloud data warehouse at scale

The ETL logic in `extract.py`, `transform.py` and `load.py` is database-agnostic and would
require minimal changes to connect to any of the above.
