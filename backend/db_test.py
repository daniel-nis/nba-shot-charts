import sqlite3
import pandas as pd

conn = sqlite3.connect('nba_shot_data.db')

# Check the number of players
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM Players')
player_count = cursor.fetchone()[0]
print(f"Total players stored: {player_count}")

# Check the number of teams
cursor.execute('SELECT COUNT(*) FROM Teams')
team_count = cursor.fetchone()[0]
print(f"Total teams stored: {team_count}")

# Check the number of shots
cursor.execute('SELECT COUNT(*) FROM Shots')
shot_count = cursor.fetchone()[0]
print(f"Total shots stored: {shot_count}")

# Fetch some shot data
df = pd.read_sql_query("SELECT * FROM Shots LIMIT 5", conn)
print(df.head())

player_name = "Jalen Brunson"
# Fetch player data
cursor.execute("SELECT * FROM Players WHERE player_name = ?", (player_name,))
player_data = cursor.fetchone()
print(f"Data for player {player_name}: {player_data}")

shot_data = cursor.execute("SELECT * FROM Shots WHERE player_name = ?", (player_name,)).fetchall()

# Get columns for the shot data
columns = [column[0] for column in cursor.description]
shot_df = pd.DataFrame(shot_data, columns=columns)
print(shot_df)

# Get total shots for the player
total_shots = len(shot_df)
print(f"Total shots for {player_name}: {total_shots}")

# Get total makes for the player
total_makes = shot_df[shot_df['shot_made_flag'] == 1].shape[0]
print(f"Total makes for {player_name}: {total_makes}")



conn.close()
