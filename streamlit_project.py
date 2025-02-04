import json
import pandas as pd
import streamlit as st
from mplsoccer import VerticalPitch
import matplotlib.pyplot as plt
import statistics

# Set Title and Subtitle
st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all of their shots")

# Load Data, convert shot location from json as string to list object
df = pd.read_csv("Euro2024_shots.csv")
df["location"] = df["location"].apply(json.loads)
df = df[df['shot_type'] != 'Penalty']

# Create filters on streamlit
team = st.selectbox("Select a team", df["team"].sort_values().unique(), index=None)
player = st.selectbox("Select a player", df[df["team"]==team]["player"].sort_values().unique(), index=None)

# Function to filter data by team and player
def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

# Filter data
filtered_df = filter_data(df, team, player)
total_shots = filtered_df.shape[0]
total_goals = filtered_df[filtered_df['shot_outcome'] == 'Goal'].shape[0]
total_xG = filtered_df['shot_statsbomb_xg'].sum()
xG_per_shot = total_xG/total_shots
points_average_distance = statistics.mean([x[0] for x in filtered_df['location']])
average_shot_distance = 120 - points_average_distance
background_color = '#000000'
line_color = '#fcfaf9'
goal_color = '#48e5c2'

fig = plt.figure(figsize=(8,12))
fig.patch.set_facecolor(background_color)

ax1 = fig.add_axes([0, 0.7, 1, 0.2])
ax1.set_facecolor(background_color)
ax1.set_xlim(0,1)
ax1.set_ylim(0,1)


if player:
    heading = player
elif team:
    heading = team
else:
    heading = "All Teams"

ax1.text(
    x=0.5,
    y=.85,
    s=heading,
    fontsize=20,
    fontweight='bold',
    color=line_color,
    ha='center'
)
ax1.text(
    x=0.5,
    y=.7,
    s=f'All shots in the 2024 Euros',
    fontsize=14,
    fontweight='bold',
    color=line_color,
    ha='center'
)
ax1.text(
    x=0.25,
    y=0.5,
    s=f'Low Quality Chance',
    fontsize=12,
    color=line_color,
    ha='center'
)

# add a scatter point between the two texts
ax1.scatter(
    x=0.38,
    y=0.53,
    s=60,
    color=background_color,
    edgecolor=line_color,
    linewidth=.8
)
ax1.scatter(
    x=0.425,
    y=0.53,
    s=120,
    color=background_color,
    edgecolor=line_color,
    linewidth=.8
)
ax1.scatter(
    x=0.48,
    y=0.53,
    s=180,
    color=background_color,
    edgecolor=line_color,
    linewidth=.8
)
ax1.scatter(
    x=0.54,
    y=0.53,
    s=240,
    color=background_color,
    edgecolor=line_color,
    linewidth=.8
)
ax1.scatter(
    x=0.6,
    y=0.53,
    s=300,
    color=background_color,
    edgecolor=line_color,
    linewidth=.8
)

ax1.text(
    x=0.75,
    y=0.5,
    s=f'High Quality Chance',
    fontsize=12,
    color=line_color,
    ha='center'
)


ax1.text(
    x=0.45,
    y=0.27,
    s=f'Goal',
    fontsize=10,
    color=line_color,
    ha='right'
)
ax1.scatter(
    x=0.47,
    y=0.3,
    s=100,
    color=goal_color,
    edgecolor=line_color,
    linewidth=.8,
    alpha=.7
)


ax1.scatter(
    x=0.53,
    y=0.3,
    s=100,
    color=background_color,
    edgecolor=line_color,
    linewidth=.8
)

ax1.text(
    x=0.55,
    y=0.27,
    s=f'No Goal',
    fontsize=10,
    color=line_color,
    ha='left'
)

ax1.set_axis_off()

pitch = VerticalPitch(
    pitch_type='statsbomb',
    half=True,
    pitch_color=background_color,
    pad_bottom=.5,
    line_color=line_color,
    linewidth=.75,
    axis=True, label=True
)

ax2 = fig.add_axes([0.05, 0.25, 0.9, 0.5])
ax2.set_facecolor(background_color)

pitch.draw(ax=ax2)

# create a scatter plot at y 100 - average_distance
ax2.scatter(
    x=10,
    y=points_average_distance,
    s=100,
    color=line_color,
    linewidth=.8
)
# create a line from the bottom of the pitch to the scatter point
ax2.plot(
    [10, 10],
    [120, points_average_distance],
    color=line_color,
    linewidth=2
)

# Add a text label for the average distance
ax2.text(
    x=10,
    y=points_average_distance - 5,
    s=f'Avg Shot Distance\n{average_shot_distance:.1f} yards',
    fontsize=10,
    color=line_color,
    ha='center'
)

for x in filtered_df.to_dict(orient='records'):
    pitch.scatter(
        x['location'][0],
        x['location'][1],
        s=300 * x['shot_statsbomb_xg'],
        color=goal_color if x['shot_outcome'] == 'Goal' else background_color,
        ax=ax2,
        alpha=0.75 if x['shot_outcome'] == 'Goal' else 0.5,
        zorder=2 if x['shot_outcome'] == 'Goal' else 1,
        linewidth=.8,
        edgecolor=line_color
    )

ax2.set_axis_off()

# add another axis for the stats
ax3 = fig.add_axes([0, .2, 1, .05])
ax3.set_facecolor(background_color)
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)

ax3.text(
    x=0.2,
    y=.5,
    s='Shots',
    fontsize=20,
    fontweight='bold',
    color=line_color,
    ha='center'
)

ax3.text(
    x=0.2,
    y=0,
    s=f'{total_shots}',
    fontsize=16,
    color=goal_color,
    ha='center'
)

ax3.text(
    x=0.4,
    y=.5,
    s='Goals',
    fontsize=20,
    fontweight='bold',
    color=line_color,
    ha='center'
)

ax3.text(
    x=0.4,
    y=0,
    s=f'{total_goals}',
    fontsize=16,
    color=goal_color,
    ha='center'
)

ax3.text(
    x=0.6,
    y=.5,
    s='xG',
    fontsize=20,
    fontweight='bold',
    color=line_color,
    ha='center'
)

ax3.text(
    x=0.6,
    y=0,
    s=f'{total_xG:.2f}',
    fontsize=16,
    color=goal_color,
    ha='center'
)

ax3.text(
    x=0.8,
    y=.5,
    s='xG/Shot',
    fontsize=20,
    fontweight='bold',
    color=line_color,
    ha='center'
)

ax3.text(
    x=0.8,
    y=0,
    s=f'{xG_per_shot:.2f}',
    fontsize=16,
    color=goal_color,
    ha='center'
)

ax3.set_axis_off()

# plot it on streamlit
st.pyplot(fig)
