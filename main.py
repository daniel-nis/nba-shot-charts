from models import Database, Player, ShotData, Statistics
from plotting import ShotChart
from team_colors import team_colors

def main():
    # Initialize the database
    db = Database('nba_shot_data.db')

    # Specify the player name
    player_name = "LeBron James"

    try:
        # Create a Player instance
        player = Player(player_name, db)

        # Get the shot data
        shot_data = ShotData(player, db)
        shot_df = shot_data.shot_df

        if shot_df.empty:
            print(f"No shot data available for {player_name}.")
            return

        # Calculate statistics
        stats = Statistics(shot_df)

        # Create and save the shot chart
        shot_chart = ShotChart(shot_df, player_name, player.team_name, team_colors, stats)
        # Specify the output path for the image
        output_image_path = f'static/{player_name.replace(" ", "_")}_shot_chart.png'
        shot_chart.plot_shot_chart(output_path=output_image_path)

        print(f"Shot chart saved to {output_image_path}")

    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()
