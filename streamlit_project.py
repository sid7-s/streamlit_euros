import json
import pandas as pd
import streamlit as st
from mplsoccer import VerticalPitch

# Set Title and Subtitle
st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all of their shots")

# Load Data, convert shot location from json as string to list object
df = pd.read_csv("Euro2024_shots.csv")
df["location"] = df["location"].apply(json.loads)

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

# Create the pitch
pitch = VerticalPitch(pitch_type='statsbomb', half =True)
fig,ax = pitch.draw(figsize=(10, 10))

def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['type'] == 'goal' else 0.5,
            zorder=2 if x['type'] == 'goal' else 1
        )

plot_shots(filtered_df, ax, pitch)

# plot it on streamlit
st.pyplot(fig)