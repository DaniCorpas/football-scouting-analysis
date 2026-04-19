# Football Scouting Analysis

ETL pipeline for identifying undervalued football players using StatsBomb open data.

## Tech stack
- Python , Pandas , SQLite , Jupyter , Power BI

## Project structure
football-scouting-analysis/
|-- data/         <- ignored in git (see below)
|-- notebooks/    <- exploration and analysis
|-- src/          <- pipeline modules
|   |-- extract.py
|   |-- transform.py
|-- visuals/      <- charts and dashboards

## Setup

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

## Pipeline
StatsBomb JSON --> extract.py --> transform.py --> SQLite --> Power BI
