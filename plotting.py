'''import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.font_manager as font_manager
import os

class ShotChart:
    def __init__(self, shot_df, player_name, team_name, team_colors, statistics):
        self.shot_df = shot_df
        self.player_name = player_name
        self.team_name = team_name
        self.team_colors = team_colors
        self.team_color = team_colors.get(team_name, "#000000")  # Default to black
        self.statistics = statistics

        # Font properties
        self.font_props = font_manager.FontProperties(fname='assets/Arvo-Regular.ttf')
        self.font_props_bold = font_manager.FontProperties(fname='assets/Arvo-Bold.ttf')

    def draw_court(self, ax=None, color='white', lw=2):
        if ax is None:
            ax = plt.gca()
        
        # Basketball hoop
        hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
        # Backboard
        backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
        # The paint
        outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
        inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
        # Free throw top arc
        top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
        # Free throw bottom arc
        bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
        # Restricted area
        restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
        # Three point line
        corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
        corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
        # Center court
        center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
        center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
        
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]
        
        for element in court_elements:
            ax.add_patch(element)

        for spine in ax.spines.values():
            spine.set_edgecolor('white')
        
        return ax

    def plot_shot_chart(self, output_path='shot_chart.png'):
        background_color = "#1c1c1e"
        court_color = "white"

        # Create the figure and main axis for the shot chart
        fig = plt.figure(figsize=(12, 11), facecolor=background_color, dpi=200)
        ax = fig.add_subplot(111)

        self.draw_court(ax, color=court_color)

        # Plot the shots
        made_shots = self.shot_df[self.shot_df['shot_made_flag'] == 1]
        missed_shots = self.shot_df[self.shot_df['shot_made_flag'] == 0]

        ax.scatter(missed_shots['loc_x'], missed_shots['loc_y'], c=background_color, s=170, alpha=0.8,
                   linewidths=0.8, edgecolors='white', zorder=2, label='Missed')
        ax.scatter(made_shots['loc_x'], made_shots['loc_y'], c=self.team_color, s=170, alpha=0.8,
                   linewidths=0.8, edgecolors='white', zorder=2, label='Made')

        # Customize the shot chart axis
        ax.set_facecolor(background_color)
        ax.set_xlim(-250, 250)
        ax.set_ylim(-47.5, 422.5)
        ax.set_xticks([])
        ax.set_yticks([])

        # Add legend
        legend = ax.legend(loc='upper left', fontsize=12, frameon=False)
        for text in legend.get_texts():
            text.set_color('white')
            text.set_fontproperties(self.font_props)

        # Create a separate axis for the title
        ax_title = fig.add_axes([0.1, 1.0, 0.8, 0.1])  # (left, bottom, width, height)
        ax_title.set_axis_off()

        ax_title.text(0.5, 0.6, f"{self.player_name}", fontproperties=self.font_props_bold, fontsize=24,
                      ha='center', color='white')
        ax_title.text(0.5, 0.3, "Shot Chart for the 2023-2024 Season", fontproperties=self.font_props, fontsize=18,
                      ha='center', color='white')

        # Create a separate axis for statistics
        ax_stats = fig.add_axes([0.1, -0.2, 0.8, 0.2])  # (left, bottom, width, height)
        ax_stats.set_axis_off()

        # Add statistics
        stats = self.statistics
        ax_stats.text(0.5, 0.8, f"Total Shot Attempts: {stats.total_shots} | Total Make %: {stats.total_make_percentage:.1%}",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        ax_stats.text(0.5, 0.6, f"3-Point Shot Attempts: {stats.three_point_shots.shape[0]} | 3-Point %: {stats.three_point_percentage:.1%}",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        ax_stats.text(0.5, 0.4, f"2-Point Shot Attempts: {stats.two_point_shots.shape[0]} | 2-Point %: {stats.two_point_percentage:.1%}",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        ax_stats.text(0.5, 0.2, f"Avg. Shot Distance: {stats.average_shot_distance:.1f} ft.",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        ax_stats.text(0.5, 0.0, f"Clutch Shot Attempts: {stats.clutch_shots.shape[0]}",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        ax_stats.text(0.5, -0.2, f"Clutch Shot %: {stats.clutch_fg_percentage:.1%}",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')

        plt.tight_layout()

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the figure to an image file
        plt.savefig(output_path, dpi=200, bbox_inches='tight')

        # Close the figure to free up memory
        plt.close(fig)'''

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.font_manager as font_manager
import os
import io
import base64

class ShotChart:
    def __init__(self, shot_df, player_name, team_name, team_colors, statistics):
        self.shot_df = shot_df
        self.player_name = player_name
        self.team_name = team_name
        self.team_colors = team_colors
        self.team_color = team_colors.get(team_name, "#000000")  # Default to black
        self.statistics = statistics

        # Font properties
        self.font_props = font_manager.FontProperties(fname='assets/Arvo-Regular.ttf')
        self.font_props_bold = font_manager.FontProperties(fname='assets/Arvo-Bold.ttf')

    def draw_court(self, ax=None, color='white', lw=2):
        if ax is None:
            ax = plt.gca()

        # Basketball hoop
        hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
        # Backboard
        backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
        # The paint
        outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
        inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
        # Free throw top arc
        top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
        # Free throw bottom arc
        bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
        # Restricted area
        restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
        # Three point line
        corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
        corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
        # Center court
        center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
        center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]

        for element in court_elements:
            ax.add_patch(element)

        # Remove ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(-250, 250)
        ax.set_ylim(-47.5, 422.5)

        # Set the spines (the borders) to white
        for spine in ax.spines.values():
            spine.set_edgecolor('white')

        return ax

    def plot_shot_chart(self):
        background_color = "#1c1c1e"
        court_color = "white"

        # Create the figure and main axis for the shot chart
        fig = plt.figure(figsize=(12, 11), facecolor=background_color, edgecolor=background_color, dpi=200)
        ax = fig.add_subplot(111)

        self.draw_court(ax, color=court_color)

        # Plot the shots
        made_shots = self.shot_df[self.shot_df['shot_made_flag'] == 1]
        missed_shots = self.shot_df[self.shot_df['shot_made_flag'] == 0]

        ax.scatter(missed_shots['loc_x'], missed_shots['loc_y'], c=background_color, s=170, alpha=0.8,
                   linewidths=0.8, edgecolors='white', zorder=2, label='Missed')
        ax.scatter(made_shots['loc_x'], made_shots['loc_y'], c=self.team_color, s=170, alpha=0.8,
                   linewidths=0.8, edgecolors='white', zorder=2, label='Made')

        # Customize the shot chart axis
        ax.set_facecolor(background_color)
        # Axis limits, ticks, and spines are handled in draw_court()

        # Add legend
        legend = ax.legend(loc='upper left', fontsize=12, frameon=False)
        for text in legend.get_texts():
            text.set_color('white')
            text.set_fontproperties(self.font_props)

        '''
        # Create a separate axis for the title
        ax_title = fig.add_axes([0.1, 0.93, 0.8, 0.07])  # Adjusted positions
        ax_title.set_axis_off()

        ax_title.text(0.5, 0.5, f"{self.player_name}", fontproperties=self.font_props_bold, fontsize=24,
                      ha='center', va='center', color='white')
        ax_title.text(0.5, 0.2, "Shot Chart for the 2023-2024 Season", fontproperties=self.font_props, fontsize=18,
                      ha='center', va='center', color='white')

        
        # Create a separate axis for statistics
        ax_stats = fig.add_axes([0.1, 0.01, 0.8, 0.15])  # Adjusted positions
        ax_stats.set_axis_off()

        
        # Add statistics
        stats = self.statistics
        ax_stats.text(0.5, 0.8, f"Total Shot Attempts: {stats.total_shots} | Total Make %: {stats.total_make_percentage:.1%}",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        ax_stats.text(0.5, 0.6, f"3-Point Attempts: {stats.three_point_shots.shape[0]} | 3-Point %: {stats.three_point_percentage:.1%}",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        ax_stats.text(0.5, 0.4, f"2-Point Attempts: {stats.two_point_shots.shape[0]} | 2-Point %: {stats.two_point_percentage:.1%}",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        ax_stats.text(0.5, 0.2, f"Avg. Shot Distance: {stats.average_shot_distance:.1f} ft.",
                      fontproperties=self.font_props, fontsize=14, ha='center', color='white')
        '''

        plt.tight_layout()

        # Save the figure to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=200, bbox_inches='tight', facecolor=background_color, edgecolor=background_color)
        plt.close(fig)
        buf.seek(0)

        # Encode the image data in base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        # Return the base64 string
        return image_base64

