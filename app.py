import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from subprocess import Popen

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def main():

    st.title('UEFA Team Statistics')
    st.write('Explore UEFA team statistics with Streamlit!')

    # Load data
    file_path = 'src/uefa_team_data.csv'
    df = load_data(file_path)

    st.subheader('Data Overview')
    st.write(df)

    st.subheader('Top Teams by Points')
    top_teams_points = df.sort_values(by='Points', ascending=False).head(10)
    fig_points, ax_points = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Points', y='Team', data=top_teams_points, palette='viridis', ax=ax_points)
    ax_points.set_title('Top Teams by Points')
    st.pyplot(fig_points)

    st.subheader('Top Teams by Goal Difference')
    top_teams_goal_diff = df.sort_values(by='Goal Difference', ascending=False).head(10)
    fig_goal_diff, ax_goal_diff = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Goal Difference', y='Team', data=top_teams_goal_diff, palette='mako', ax=ax_goal_diff)
    ax_goal_diff.set_title('Top Teams by Goal Difference')
    st.pyplot(fig_goal_diff)

    st.subheader('Top Teams by Wins')
    top_teams_wins = df.sort_values(by='Won', ascending=False).head(10)
    fig_wins, ax_wins = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Won', y='Team', data=top_teams_wins, palette='rocket', ax=ax_wins)
    ax_wins.set_title('Top Teams by Wins')
    st.pyplot(fig_wins)

    if st.button('Reset Data'):
        st.write("Resetting data...")
        Popen(["python", "src/scraping.py"])  # Replace with appropriate command if necessary
        st.write("Data reset complete. Refresh the page to load new data.")

if __name__ == '__main__':
    main()
