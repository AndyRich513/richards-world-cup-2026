import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="The Richards World Cup 2026 Predictor", page_icon="🏆", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
    }
    .team-card {
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 The Richards World Cup 2026 Predictor")
st.markdown("---")

# Sidebar for user input
st.sidebar.header("⚙️ Settings")

# World Cup 2026 Teams (organized by region)
teams_data = {
    "CONCACAF": ["Canada", "Mexico", "USA", "Costa Rica", "Panama", "Jamaica"],
    "South America": ["Argentina", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay"],
    "Europe": ["England", "France", "Germany", "Italy", "Netherlands", "Poland", "Spain", "Portugal", "Belgium", "Croatia"],
    "Africa": ["Egypt", "Cameroon", "Morocco", "Nigeria", "Senegal", "South Africa", "Algeria"],
    "Asia": ["Japan", "South Korea", "Australia", "Iran", "Saudi Arabia", "Qatar", "Uzbekistan"],
}

# Flatten teams list
all_teams = []
for region, teams in teams_data.items():
    all_teams.extend(teams)

st.sidebar.markdown("### Select Your Favorites")
selected_teams = st.sidebar.multiselect(
    "Pick teams you think will advance to the knockout stage:",
    all_teams,
    default=["Brazil", "Argentina", "France", "England"]
)

prediction_method = st.sidebar.radio(
    "Prediction Method:",
    ["Random Predictor", "Favorites", "Statistical Model"]
)

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Tournament Overview")
    
    overview_data = {
        "Tournament": "FIFA World Cup 2026",
        "Host Countries": "USA, Canada, Mexico",
        "Teams Participating": "48 teams",
        "Tournament Start": "June 2026",
        "Finals Date": "July 2026"
    }
    
    for key, value in overview_data.items():
        st.metric(key, value)

with col2:
    st.subheader("🎯 Your Selection")
    if selected_teams:
        st.success(f"You've selected {len(selected_teams)} team(s)")
        for team in selected_teams:
            st.write(f"• {team}")
    else:
        st.info("Select teams from the sidebar to get started!")

st.markdown("---")

# Predictions Section
st.subheader("🔮 Tournament Predictions")

if st.button("Generate Predictions", type="primary"):
    
    if prediction_method == "Random Predictor":
        st.info("🎲 Generating random predictions...")
        
        # Simulate knockout stage
        semi_finalists = random.sample(all_teams, 4)
        finalists = random.sample(semi_finalists, 2)
        champion = random.choice(finalists)
        runner_up = [t for t in finalists if t != champion][0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🥇 **Champion: {champion}**")
        with col2:
            st.info(f"🥈 **Runner-up: {runner_up}**")
        
        # Semifinalists
        st.markdown("### Semifinalists")
        other_semis = [t for t in semi_finalists if t not in finalists]
        for i, team in enumerate(other_semis, 1):
            st.write(f"{i}. {team}")
    
    elif prediction_method == "Favorites":
        st.info("⭐ Predicting based on your selected favorites...")
        
        if selected_teams:
            # Use favorites if selected
            potential_finalists = selected_teams[:2] if len(selected_teams) >= 2 else selected_teams
            champion = random.choice(potential_finalists)
            runner_up = [t for t in selected_teams if t != champion][0] if len(selected_teams) > 1 else random.choice(all_teams)
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🥇 **Champion: {champion}**")
            with col2:
                st.info(f"🥈 **Runner-up: {runner_up}**")
        else:
            st.warning("Please select favorite teams first!")
    
    else:  # Statistical Model
        st.info("📈 Applying statistical model based on historical performance...")
        
        # Simulate statistical predictions
        top_teams = ["Brazil", "France", "Argentina", "England", "Germany", "Spain"]
        champion = random.choice(top_teams)
        runner_up = random.choice([t for t in top_teams if t != champion])
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🥇 **Champion: {champion}**")
        with col2:
            st.info(f"🥈 **Runner-up: {runner_up}**")

st.markdown("---")

# Teams by Region
st.subheader("🌍 Teams by Region")

tabs = st.tabs(list(teams_data.keys()))

for tab, (region, teams) in zip(tabs, teams_data.items()):
    with tab:
        cols = st.columns(3)
        for i, team in enumerate(teams):
            with cols[i % 3]:
                if team in selected_teams:
                    st.success(f"✓ {team}")
                else:
                    st.write(f"• {team}")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
<p>🏆 The Richards World Cup 2026 Predictor | Last Updated: 2026</p>
<p><small>Predictions are for entertainment purposes only</small></p>
</div>
""", unsafe_allow_html=True)