# cache.py

import sqlite3
from datetime import datetime
import os
import json

CACHE_DB = 'cache.db'
CACHE_CAPACITY = 100  # Set cache capacity based on limitations

# Ensure the cache database file exists
def initialize_cache_db():
    if not os.path.exists(CACHE_DB):
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE Cache (
                player_name TEXT PRIMARY KEY,
                image_base64 TEXT NOT NULL,
                statistics TEXT NOT NULL,
                favorite_shots TEXT NOT NULL,
                team_color TEXT NOT NULL,
                access_count INTEGER DEFAULT 1,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

def get_cached_data(player_name):
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT image_base64, statistics, favorite_shots, team_color FROM Cache WHERE player_name = ?",
        (player_name,)
    )
    result = cursor.fetchone()
    if result:
        # Update access_count and last_accessed
        cursor.execute(
            "UPDATE Cache SET access_count = access_count + 1, last_accessed = ? WHERE player_name = ?",
            (datetime.utcnow(), player_name)
        )
        conn.commit()
        conn.close()
        image_base64, statistics_json, favorite_shots_json, team_color = result
        # Deserialize JSON strings
        statistics = json.loads(statistics_json)
        favorite_shots = json.loads(favorite_shots_json)
        return {
            'image_base64': image_base64,
            'statistics': statistics,
            'favorite_shots': favorite_shots,
            'team_color': team_color
        }
    conn.close()
    return None

def cache_data(player_name, image_base64, statistics, favorite_shots, team_color):
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    # Serialize statistics and favorite_shots to JSON strings
    statistics_json = json.dumps(statistics)
    favorite_shots_json = json.dumps(favorite_shots)
    cursor.execute(
        "INSERT OR REPLACE INTO Cache (player_name, image_base64, statistics, favorite_shots, team_color, access_count, last_accessed) VALUES (?, ?, ?, ?, ?, 1, ?)",
        (player_name, image_base64, statistics_json, favorite_shots_json, team_color, datetime.utcnow())
    )
    conn.commit()
    enforce_cache_size_limit(cursor)
    conn.close()

def enforce_cache_size_limit(cursor):
    # Delete least frequently used items if cache exceeds capacity
    cursor.execute("SELECT COUNT(*) FROM Cache")
    count = cursor.fetchone()[0]
    if count > CACHE_CAPACITY:
        # Calculate number of entries to delete
        entries_to_delete = count - CACHE_CAPACITY
        # Delete entries with lowest access_count and oldest last_accessed
        cursor.execute(
            """
            DELETE FROM Cache
            WHERE player_name IN (
                SELECT player_name FROM Cache
                ORDER BY access_count ASC, last_accessed ASC
                LIMIT ?
            )
            """,
            (entries_to_delete,)
        )
        cursor.connection.commit()
