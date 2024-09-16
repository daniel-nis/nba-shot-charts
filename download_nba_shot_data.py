# download_nba_shot_data.py

import sqlite3
import pandas as pd
import time
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players, teams
from nba_api.stats.library.parameters import SeasonTypeAllStar

# Function to pause execution respecting rate limits
def rate_limit_pause():
    time.sleep(0.6)  # Adjust if necessary

# Connect to SQLite database (or create it)
conn = sqlite3.connect('nba_shot_data.db')
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS Players')
cursor.execute('DROP TABLE IF EXISTS Teams')
cursor.execute('DROP TABLE IF EXISTS Shots')
conn.commit()

# Create Players table
cursor.execute('''
CREATE TABLE Players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT
)
''')

# Create Teams table
cursor.execute('''
CREATE TABLE Teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT
)
''')

# Create Shots table with all columns from shot_df
cursor.execute('''
CREATE TABLE Shots (
    shot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    grid_type TEXT,
    game_id TEXT,
    game_event_id INTEGER,
    player_id INTEGER,
    player_name TEXT,
    team_id INTEGER,
    team_name TEXT,
    period INTEGER,
    minutes_remaining INTEGER,
    seconds_remaining INTEGER,
    event_type TEXT,
    action_type TEXT,
    shot_type TEXT,
    shot_zone_basic TEXT,
    shot_zone_area TEXT,
    shot_zone_range TEXT,
    shot_distance INTEGER,
    loc_x INTEGER,
    loc_y INTEGER,
    shot_attempted_flag INTEGER,
    shot_made_flag INTEGER,
    game_date TEXT,
    htm TEXT,
    vtm TEXT,
    FOREIGN KEY(player_id) REFERENCES Players(player_id),
    FOREIGN KEY(team_id) REFERENCES Teams(team_id)
)
''')
conn.commit()

# Get all active players
print("Fetching list of all active players...")
all_players = players.get_active_players()
print(f"Total active players found: {len(all_players)}")

# Get team information
team_info = teams.get_teams()

# Create a mapping for teams to avoid duplicate entries
team_id_name_map = {}

# Function to insert team data
def insert_team(team_id, team_name):
    if team_id not in team_id_name_map:
        cursor.execute('INSERT OR IGNORE INTO Teams (team_id, team_name) VALUES (?, ?)', (team_id, team_name))
        team_id_name_map[team_id] = team_name
        conn.commit()

# Iterate over each player and fetch their shot data
for idx, player in enumerate(all_players, start=1):
    player_id = player['id']
    player_name = player['full_name']
    print(f"Processing ({idx}/{len(all_players)}): {player_name} (ID: {player_id})")

    # Insert player into Players table
    cursor.execute('INSERT OR IGNORE INTO Players (player_id, player_name) VALUES (?, ?)', (player_id, player_name))
    conn.commit()

    # Fetch shot data
    try:
        shot_data = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable='2023-24',
            season_type_all_star='Regular Season',
            context_measure_simple='FGA'
        )
        shot_df = shot_data.get_data_frames()[0]

        if shot_df.empty:
            print(f"No shot data available for {player_name}.")
            rate_limit_pause()
            continue  # Skip if no data

        # Insert team data
        team_id = int(shot_df['TEAM_ID'].iloc[0])
        team_name = shot_df['TEAM_NAME'].iloc[0]
        insert_team(team_id, team_name)

        # Prepare shots DataFrame
        shots = shot_df.copy()

        # Ensure data types match the database schema
        # Convert integer columns
        int_columns = [
            'GAME_EVENT_ID', 'PLAYER_ID', 'TEAM_ID', 'PERIOD', 'MINUTES_REMAINING',
            'SECONDS_REMAINING', 'SHOT_DISTANCE', 'LOC_X', 'LOC_Y',
            'SHOT_ATTEMPTED_FLAG', 'SHOT_MADE_FLAG'
        ]
        for col in int_columns:
            shots[col] = shots[col].fillna(0).astype(int)

        # Convert text columns
        text_columns = [
            'GRID_TYPE', 'GAME_ID', 'PLAYER_NAME', 'TEAM_NAME', 'EVENT_TYPE',
            'ACTION_TYPE', 'SHOT_TYPE', 'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA',
            'SHOT_ZONE_RANGE', 'GAME_DATE', 'HTM', 'VTM'
        ]
        for col in text_columns:
            shots[col] = shots[col].fillna('').astype(str)

        # Add 'player_id' and 'player_name' if not present
        if 'PLAYER_ID' not in shots.columns:
            shots['PLAYER_ID'] = player_id
        if 'PLAYER_NAME' not in shots.columns:
            shots['PLAYER_NAME'] = player_name

        # Add 'team_id' and 'team_name' if not present
        if 'TEAM_ID' not in shots.columns:
            shots['TEAM_ID'] = team_id
        if 'TEAM_NAME' not in shots.columns:
            shots['TEAM_NAME'] = team_name

        # Select the columns to insert (ensure all columns are included)
        shots = shots[[
            'GRID_TYPE', 'GAME_ID', 'GAME_EVENT_ID', 'PLAYER_ID', 'PLAYER_NAME',
            'TEAM_ID', 'TEAM_NAME', 'PERIOD', 'MINUTES_REMAINING',
            'SECONDS_REMAINING', 'EVENT_TYPE', 'ACTION_TYPE', 'SHOT_TYPE',
            'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'SHOT_DISTANCE',
            'LOC_X', 'LOC_Y', 'SHOT_ATTEMPTED_FLAG', 'SHOT_MADE_FLAG', 'GAME_DATE',
            'HTM', 'VTM'
        ]]

        # Rename columns to match database schema (lowercase)
        shots.columns = [col.lower() for col in shots.columns]

        # Insert shots into Shots table
        shots.to_sql('Shots', conn, if_exists='append', index=False)

        print(f"Inserted shot data for {player_name}.")

        # Pause to respect rate limits
        rate_limit_pause()

    except Exception as e:
        print(f"Error fetching data for {player_name}: {e}")
        continue

conn.close()
print("Data fetching and storing completed.")
