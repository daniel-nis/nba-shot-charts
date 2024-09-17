# models.py

import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_path='nba_shot_data.db'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

class Player:
    def __init__(self, player_name, db):
        self.player_name = player_name
        self.db = db
        self.player_id = None
        self.team_id = None
        self.team_name = None
        self.get_player_info()

    def get_player_info(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT player_id FROM Players WHERE player_name = ?', (self.player_name,))
        result = cursor.fetchone()
        if result:
            self.player_id = result[0]
        else:
            conn.close()
            raise ValueError(f"Player '{self.player_name}' not found in the database.")

        # Get team_id and team_name
        cursor.execute('''
            SELECT DISTINCT team_id FROM Shots WHERE player_id = ?
        ''', (self.player_id,))
        team_result = cursor.fetchone()
        if team_result:
            self.team_id = team_result[0]
            cursor.execute('SELECT team_name FROM Teams WHERE team_id = ?', (self.team_id,))
            team_name_result = cursor.fetchone()
            if team_name_result:
                self.team_name = team_name_result[0]
        conn.close()

class ShotData:
    def __init__(self, player, db):
        self.player = player
        self.db = db
        self.shot_df = None
        self.get_shot_data()

    def get_shot_data(self):
        conn = self.db.connect()
        query = '''
        SELECT * FROM Shots WHERE player_id = ?
        '''
        self.shot_df = pd.read_sql_query(query, conn, params=(self.player.player_id,))
        conn.close()

class Statistics:
    def __init__(self, shot_df):
        self.shot_df = shot_df
        self.calculate_statistics()

    def calculate_statistics(self):
        self.total_shots = self.shot_df.shape[0]
        self.total_makes = self.shot_df[self.shot_df['shot_made_flag'] == 1].shape[0]
        self.total_make_percentage = self.total_makes / self.total_shots if self.total_shots > 0 else 0

        # 3-point shots
        self.three_point_shots = self.shot_df[self.shot_df['shot_type'] == '3PT Field Goal']
        self.three_point_makes = self.three_point_shots[self.three_point_shots['shot_made_flag'] == 1]
        self.three_point_percentage = self.three_point_makes.shape[0] / self.three_point_shots.shape[0] if self.three_point_shots.shape[0] > 0 else 0

        # 2-point shots
        self.two_point_shots = self.shot_df[self.shot_df['shot_type'] == '2PT Field Goal']
        self.two_point_makes = self.two_point_shots[self.two_point_shots['shot_made_flag'] == 1]
        self.two_point_percentage = self.two_point_makes.shape[0] / self.two_point_shots.shape[0] if self.two_point_shots.shape[0] > 0 else 0

        # Clutch shots (last 5 minutes of 4th quarter or overtime)
        self.clutch_shots = self.shot_df[(self.shot_df['minutes_remaining'] < 5) & (self.shot_df['period'] >= 4)]
        self.clutch_makes = self.clutch_shots['shot_made_flag'].sum()
        self.clutch_attempts = self.clutch_shots.shape[0]
        self.clutch_fg_percentage = self.clutch_makes / self.clutch_attempts if self.clutch_attempts > 0 else 0

        # Games played
        self.games_played = self.shot_df['game_id'].nunique()

        # 3-point attempts per game
        self.three_point_attempts_per_game = self.three_point_shots.shape[0] / self.games_played if self.games_played > 0 else 0

        # Paint shots
        self.paint_shots_attempted = self.shot_df[self.shot_df['shot_zone_basic'] == 'Restricted Area'].shape[0]
        self.paint_shots_made = self.shot_df[(self.shot_df['shot_zone_basic'] == 'Restricted Area') & (self.shot_df['shot_made_flag'] == 1)].shape[0]

        # Mid-range shots
        self.mid_range_shots_attempted = self.shot_df[self.shot_df['shot_zone_basic'] == 'Mid-Range'].shape[0]
        self.mid_range_shots_made = self.shot_df[(self.shot_df['shot_zone_basic'] == 'Mid-Range') & (self.shot_df['shot_made_flag'] == 1)].shape[0]

        # Favorite shots
        action_types = self.shot_df['action_type'].value_counts()
        self.favorite_shots = action_types.head(5)

        # Frequent shot zones
        shot_zones = self.shot_df['shot_zone_basic'].value_counts()
        self.frequent_zones = shot_zones.head(5)

        # Average shot distance
        self.average_shot_distance = self.shot_df['shot_distance'].mean()
