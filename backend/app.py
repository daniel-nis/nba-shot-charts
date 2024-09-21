from flask import Flask, request, jsonify, send_from_directory
from models import Database, Player, ShotData, Statistics
from plotting import ShotChart
from team_colors import team_colors
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Ensure the static directory exists
os.makedirs('static', exist_ok=True)

@app.route('/api/players', methods=['GET'])
def get_player_suggestions():
    search_query = request.args.get('q', '').lower()
    if not search_query:
        return jsonify([])

    db = Database('nba_shot_data.db')
    conn = db.connect()
    cursor = conn.cursor()

    # Fetch player names matching the search query
    cursor.execute("""
        SELECT player_name FROM Players
        WHERE LOWER(player_name) LIKE ?
        ORDER BY player_name ASC
        LIMIT 10
    """, ('%' + search_query + '%',))
    players = [row[0] for row in cursor.fetchall()]
    conn.close()

    return jsonify(players)

@app.route('/api/shot_chart', methods=['GET'])
def get_shot_chart():
    player_name = request.args.get('player_name', '')
    if not player_name:
        return jsonify({'error': 'Player name is required.'}), 400

    db = Database('nba_shot_data.db')

    try:
        # Create a Player instance
        player = Player(player_name, db)

        # Get the shot data
        shot_data = ShotData(player, db)
        shot_df = shot_data.shot_df

        if shot_df.empty:
            return jsonify({'error': f"No shot data available for {player_name}."}), 404

        # Calculate statistics
        stats = Statistics(shot_df)

        # Create the shot chart and get the base64 image
        shot_chart = ShotChart(shot_df, player_name, player.team_name, team_colors, stats)
        image_base64 = shot_chart.plot_shot_chart()

        stats_data = {
            'total_shots': stats.total_shots,
            'total_make_percentage': stats.total_make_percentage,
            'three_point_attempts': len(stats.three_point_shots),
            'three_point_percentage': stats.three_point_percentage,
            'two_point_attempts': len(stats.two_point_shots),
            'two_point_percentage': stats.two_point_percentage,
            'average_shot_distance': stats.average_shot_distance,
            'clutch_attempts': stats.clutch_attempts,
            'clutch_fg_percentage': stats.clutch_fg_percentage,
            'games_played': stats.games_played,
        }

        favorite_shots_data = stats.favorite_shots.to_dict()

        # Return the base64 image data
        return jsonify({'image_base64': image_base64, 'statistics': stats_data, 'favorite_shots': favorite_shots_data})

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/ping')
def ping():
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
