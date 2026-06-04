import streamlit as st
import pandas as pd
import random
from datetime import datetime
import json

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
    .prediction-box {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .stat-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 The Richards World Cup 2026 Predictor")
st.markdown("---")

# Initialize session state for storing predictions
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

if 'bracket_data' not in st.session_state:
    st.session_state.bracket_data = None

if 'top_scorer_pick' not in st.session_state:
    st.session_state.top_scorer_pick = None

# World Cup 2026 Teams (organized by region)
teams_data = {
    "CONCACAF": ["Canada", "Mexico", "USA", "Costa Rica", "Panama", "Jamaica"],
    "South America": ["Argentina", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay"],
    "Europe": ["England", "France", "Germany", "Italy", "Netherlands", "Poland", "Spain", "Portugal", "Belgium", "Croatia"],
    "Africa": ["Egypt", "Cameroon", "Morocco", "Nigeria", "Senegal", "South Africa", "Algeria"],
    "Asia": ["Japan", "South Korea", "Australia", "Iran", "Saudi Arabia", "Qatar", "Uzbekistan"],
}

# Top Scorers Database - Real players with their teams
top_scorers_db = {
    "Kylian Mbappé": {"team": "France", "rating": 98, "goals_avg": 12},
    "Erling Haaland": {"team": "Norway", "rating": 96, "goals_avg": 11},
    "Harry Kane": {"team": "England", "rating": 94, "goals_avg": 10},
    "Vinicius Jr": {"team": "Brazil", "rating": 92, "goals_avg": 9},
    "Phil Foden": {"team": "England", "rating": 91, "goals_avg": 9},
    "Jude Bellingham": {"team": "England", "rating": 90, "goals_avg": 8},
    "Florian Wirtz": {"team": "Germany", "rating": 89, "goals_avg": 8},
    "Vinícius Sousa": {"team": "Brazil", "rating": 88, "goals_avg": 8},
    "Federico Valverde": {"team": "Uruguay", "rating": 87, "goals_avg": 7},
    "Pedri": {"team": "Spain", "rating": 86, "goals_avg": 7},
    "Alejandro Garnacho": {"team": "Argentina", "rating": 85, "goals_avg": 7},
    "Rodrygo Goes": {"team": "Brazil", "rating": 84, "goals_avg": 6},
    "Gavi": {"team": "Spain", "rating": 83, "goals_avg": 6},
    "Eduardo Camavinga": {"team": "France", "rating": 82, "goals_avg": 6},
    "Lucas Hernández": {"team": "France", "rating": 81, "goals_avg": 5},
    "Alphonso Davies": {"team": "Canada", "rating": 80, "goals_avg": 5},
    "Sergiño Dest": {"team": "USA", "rating": 79, "goals_avg": 5},
    "Mason Mount": {"team": "England", "rating": 78, "goals_avg": 5},
    "Alexis Mac Allister": {"team": "Argentina", "rating": 77, "goals_avg": 4},
    "Gio Reyna": {"team": "USA", "rating": 76, "goals_avg": 4},
}

# Team strength ratings (for statistical model)
team_ratings = {
    "Brazil": 95,
    "France": 93,
    "Argentina": 92,
    "England": 90,
    "Germany": 89,
    "Spain": 88,
    "Netherlands": 87,
    "Belgium": 86,
    "Italy": 85,
    "Portugal": 84,
    "Croatia": 83,
    "Poland": 82,
    "USA": 81,
    "Mexico": 80,
    "Uruguay": 79,
    "Colombia": 78,
    "Chile": 77,
    "Japan": 76,
    "South Korea": 75,
    "Australia": 74,
    "Canada": 73,
    "Ecuador": 72,
    "Peru": 71,
    "Paraguay": 70,
    "Egypt": 69,
    "Morocco": 68,
    "Nigeria": 67,
    "Senegal": 66,
    "South Africa": 65,
    "Cameroon": 64,
    "Algeria": 63,
    "Iran": 62,
    "Saudi Arabia": 61,
    "Qatar": 60,
    "Uzbekistan": 59,
    "Costa Rica": 58,
    "Panama": 57,
    "Jamaica": 56,
}

# Flatten teams list
all_teams = []
for region, teams in teams_data.items():
    all_teams.extend(teams)

# Sidebar for user input
st.sidebar.header("⚙️ Settings & Controls")

# Navigation
page = st.sidebar.radio(
    "Select Page:",
    ["🎯 Predictions", "📊 Statistics", "🏆 Tournament Bracket", "📈 Team Analytics", "🎲 Head to Head", "⚽ Top Scorer", "💾 History"]
)

# Common settings for all pages
selected_teams = st.sidebar.multiselect(
    "Pick your favorite teams:",
    all_teams,
    default=["Brazil", "Argentina", "France", "England"],
    key="selected_teams_main"
)

prediction_method = st.sidebar.radio(
    "Prediction Method:",
    ["Random Predictor", "Favorites", "Statistical Model", "Expert Algorithm"]
)

st.sidebar.markdown("---")

# PAGE: PREDICTIONS
if page == "🎯 Predictions":
    st.subheader("🔮 Tournament Predictions")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Generate Your Custom Predictions")
        col_a, col_b = st.columns(2)
        
        with col_a:
            num_semi_finalists = st.slider("Number of teams in semifinals:", 4, 8, 4)
        
        with col_b:
            include_dark_horse = st.checkbox("Include dark horse pick?", value=False)
    
    with col2:
        st.subheader("📊 Overview")
        st.metric("Teams Selected", len(selected_teams))
        st.metric("Prediction Method", prediction_method)
    
    if st.button("🎲 Generate Predictions", type="primary"):
        
        if prediction_method == "Random Predictor":
            st.info("🎲 Generating random predictions...")
            
            semi_finalists = random.sample(all_teams, num_semi_finalists)
            finalists = random.sample(semi_finalists, 2)
            champion = random.choice(finalists)
            runner_up = [t for t in finalists if t != champion][0]
            third_place = random.choice([t for t in semi_finalists if t not in finalists])
            
            prediction_result = {
                "method": "Random",
                "champion": champion,
                "runner_up": runner_up,
                "third": third_place,
                "semi_finalists": semi_finalists,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        elif prediction_method == "Favorites":
            st.info("⭐ Predicting based on your selected favorites...")
            
            if selected_teams:
                sorted_favorites = selected_teams[:num_semi_finalists]
                champion = random.choice(sorted_favorites[:2]) if len(sorted_favorites) >= 2 else sorted_favorites[0]
                runner_up = random.choice([t for t in sorted_favorites if t != champion])
                third_place = random.choice([t for t in sorted_favorites if t not in [champion, runner_up]])
                
                prediction_result = {
                    "method": "Favorites",
                    "champion": champion,
                    "runner_up": runner_up,
                    "third": third_place,
                    "semi_finalists": sorted_favorites,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                st.warning("Please select favorite teams first!")
                prediction_result = None
        
        elif prediction_method == "Statistical Model":
            st.info("📈 Applying statistical model based on team ratings...")
            
            # Sort teams by rating
            sorted_teams = sorted(all_teams, key=lambda x: team_ratings.get(x, 50), reverse=True)
            semi_finalists = sorted_teams[:num_semi_finalists]
            champion = semi_finalists[0]
            runner_up = semi_finalists[1]
            third_place = semi_finalists[2]
            
            prediction_result = {
                "method": "Statistical Model",
                "champion": champion,
                "runner_up": runner_up,
                "third": third_place,
                "semi_finalists": semi_finalists,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        else:  # Expert Algorithm
            st.info("🧠 Applying expert algorithm combining multiple factors...")
            
            # Combine statistical ratings with favorites
            base_teams = sorted([t for t in all_teams if t in selected_teams] + 
                               [t for t in all_teams[:5] if t not in selected_teams])[:num_semi_finalists]
            champion = base_teams[0]
            runner_up = base_teams[1] if len(base_teams) > 1 else random.choice(all_teams)
            third_place = base_teams[2] if len(base_teams) > 2 else random.choice(all_teams)
            
            prediction_result = {
                "method": "Expert Algorithm",
                "champion": champion,
                "runner_up": runner_up,
                "third": third_place,
                "semi_finalists": base_teams,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        if prediction_result:
            # Store in history
            st.session_state.prediction_history.append(prediction_result)
            
            # Display results
            st.markdown("---")
            st.subheader("🏆 Final Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.success(f"🥇 **Champion**\n\n# {prediction_result['champion']}")
            with col2:
                st.info(f"🥈 **Runner-up**\n\n# {prediction_result['runner_up']}")
            with col3:
                st.warning(f"🥉 **Third Place**\n\n# {prediction_result['third']}")
            
            st.markdown("### Semifinalists")
            semi_col1, semi_col2 = st.columns(2)
            with semi_col1:
                for i, team in enumerate(prediction_result['semi_finalists'][:len(prediction_result['semi_finalists'])//2]):
                    st.write(f"{i+1}. {team}")
            with semi_col2:
                for i, team in enumerate(prediction_result['semi_finalists'][len(prediction_result['semi_finalists'])//2:]):
                    st.write(f"{len(prediction_result['semi_finalists'])//2 + i + 1}. {team}")

# PAGE: STATISTICS
elif page == "📊 Statistics":
    st.subheader("📊 World Cup 2026 Statistics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Teams", len(all_teams))
    with col2:
        st.metric("Regions", len(teams_data))
    with col3:
        st.metric("Your Picks", len(selected_teams))
    
    st.markdown("---")
    
    st.subheader("Teams per Region")
    region_stats = pd.DataFrame({
        "Region": list(teams_data.keys()),
        "Teams": [len(teams) for teams in teams_data.values()]
    })
    
    st.bar_chart(region_stats.set_index("Region"))
    
    st.markdown("---")
    
    st.subheader("Team Strength Ratings")
    top_teams_df = pd.DataFrame({
        "Team": list(team_ratings.keys())[:20],
        "Rating": list(team_ratings.values())[:20]
    }).sort_values("Rating", ascending=False)
    
    st.bar_chart(top_teams_df.set_index("Team"))

# PAGE: TOURNAMENT BRACKET
elif page == "🏆 Tournament Bracket":
    st.subheader("🏆 Interactive Tournament Bracket")
    
    if st.button("Generate Tournament Bracket", type="primary"):
        # Generate a bracket
        all_teams_shuffled = all_teams.copy()
        random.shuffle(all_teams_shuffled)
        
        st.session_state.bracket_data = all_teams_shuffled
        
        st.success("✅ Bracket generated!")
    
    if st.session_state.bracket_data:
        st.markdown("### Group Stage")
        
        # Create groups (for 48 teams: 16 groups of 3)
        groups_of_3 = [st.session_state.bracket_data[i:i+3] for i in range(0, len(st.session_state.bracket_data), 3)]
        
        cols = st.columns(4)
        for idx, group in enumerate(groups_of_3):
            with cols[idx % 4]:
                st.markdown(f"**Group {chr(65+idx)}**")
                for team in group:
                    st.write(f"• {team}")

# PAGE: TEAM ANALYTICS
elif page == "📈 Team Analytics":
    st.subheader("📈 Team Analytics & Ratings")
    
    selected_team = st.selectbox("Select a team for analysis:", all_teams)
    
    if selected_team:
        rating = team_ratings.get(selected_team, 50)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Team Strength Rating", rating, delta="out of 100")
            
            # Determine region
            for region, teams in teams_data.items():
                if selected_team in teams:
                    st.metric("Region", region)
                    break
        
        with col2:
            # Win probability
            win_prob = (rating / 95) * 100
            st.metric("Championship Probability", f"{win_prob:.1f}%")
            
            # Ranking
            rank = sorted(team_ratings.items(), key=lambda x: x[1], reverse=True)
            team_rank = next(i+1 for i, (t, _) in enumerate(rank) if t == selected_team)
            st.metric("Global Rank", team_rank, delta=f"out of {len(team_ratings)}")
        
        st.markdown("---")
        st.markdown("### Performance Analysis")
        
        # Create a radar-like representation
        categories = ["Offense", "Defense", "Midfield", "Experience", "Youth"]
        values = [rating - 5, rating - 2, rating, rating + 3, rating - 8]
        values = [max(0, min(100, v)) for v in values]
        
        perf_df = pd.DataFrame({
            "Category": categories,
            "Score": values
        })
        
        st.bar_chart(perf_df.set_index("Category"))

# PAGE: HEAD TO HEAD
elif page == "🎲 Head to Head":
    st.subheader("🎲 Head to Head Matchup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        team1 = st.selectbox("Team 1:", all_teams, key="team1")
    
    with col2:
        team2 = st.selectbox("Team 2:", all_teams, key="team2", index=1)
    
    if team1 != team2 and st.button("⚽ Simulate Match", type="primary"):
        rating1 = team_ratings.get(team1, 50)
        rating2 = team_ratings.get(team2, 50)
        
        # Calculate win probabilities
        total = rating1 + rating2
        prob1 = (rating1 / total) * 100
        prob2 = (rating2 / total) * 100
        
        # Simulate match
        winner = team1 if random.random() < (prob1 / 100) else team2
        
        st.markdown("---")
        st.subheader("⚽ Match Result")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"{team1}", f"{int(prob1)}% chance")
        with col2:
            st.success(f"**WINNER: {winner}**", icon="🏆")
        with col3:
            st.metric(f"{team2}", f"{int(prob2)}% chance")
    elif team1 == team2:
        st.warning("Please select two different teams!")

# PAGE: TOP SCORER
elif page == "⚽ Top Scorer":
    st.subheader("⚽ Golden Ball - Top Scorer Predictions")
    
    st.markdown("### Top Scorer Candidates")
    
    # Display top scorers
    scorers_df = pd.DataFrame({
        "Player": list(top_scorers_db.keys()),
        "Team": [v["team"] for v in top_scorers_db.values()],
        "Rating": [v["rating"] for v in top_scorers_db.values()],
        "Avg Goals": [v["goals_avg"] for v in top_scorers_db.values()]
    }).sort_values("Rating", ascending=False)
    
    st.dataframe(scorers_df, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎲 Random Prediction")
        if st.button("🎲 Pick Random Top Scorer", type="primary"):
            random_scorer = random.choice(list(top_scorers_db.keys()))
            st.session_state.top_scorer_pick = random_scorer
            st.success(f"🥇 **Top Scorer: {random_scorer}** ({top_scorers_db[random_scorer]['team']})")
            st.metric("Predicted Goals", top_scorers_db[random_scorer]['goals_avg'])
    
    with col2:
        st.subheader("🧠 Statistical Prediction")
        if st.button("📊 Best Statistical Pick", type="primary"):
            best_scorer = max(top_scorers_db.items(), key=lambda x: x[1]["rating"])
            st.session_state.top_scorer_pick = best_scorer[0]
            st.success(f"🥇 **Top Scorer: {best_scorer[0]}** ({best_scorer[1]['team']})")
            st.metric("Predicted Goals", best_scorer[1]['goals_avg'])
            st.metric("Rating", best_scorer[1]['rating'], delta="out of 100")
    
    st.markdown("---")
    
    st.subheader("👤 Select Your Prediction")
    selected_scorer = st.selectbox("Choose a player as your top scorer pick:", list(top_scorers_db.keys()))
    
    if st.button("✅ Confirm My Pick", type="primary"):
        st.session_state.top_scorer_pick = selected_scorer
        scorer_info = top_scorers_db[selected_scorer]
        st.success(f"✅ You've picked **{selected_scorer}** from **{scorer_info['team']}** as top scorer!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Player Rating", scorer_info['rating'])
        with col2:
            st.metric("Expected Goals", scorer_info['goals_avg'])
    
    if st.session_state.top_scorer_pick:
        st.markdown("---")
        st.info(f"✅ **Your Current Pick:** {st.session_state.top_scorer_pick}")

# PAGE: HISTORY
elif page == "💾 History":
    st.subheader("💾 Prediction History")
    
    if st.session_state.prediction_history or st.session_state.top_scorer_pick:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tournament Predictions", len(st.session_state.prediction_history))
        with col2:
            st.metric("Top Scorer Pick", st.session_state.top_scorer_pick or "None")
        
        st.markdown("---")
        
        if st.session_state.prediction_history:
            st.subheader("Tournament Predictions")
            for idx, pred in enumerate(reversed(st.session_state.prediction_history), 1):
                with st.expander(f"Prediction #{len(st.session_state.prediction_history) - idx + 1} - {pred['timestamp']} ({pred['method']})"):
                    st.write(f"**Method:** {pred['method']}")
                    st.write(f"**Champion:** 🥇 {pred['champion']}")
                    st.write(f"**Runner-up:** 🥈 {pred['runner_up']}")
                    st.write(f"**Third Place:** 🥉 {pred['third']}")
                    st.write(f"**Semifinalists:** {', '.join(pred['semi_finalists'])}")
        
        if st.button("🗑️ Clear All History"):
            st.session_state.prediction_history = []
            st.session_state.top_scorer_pick = None
            st.rerun()
    else:
        st.info("No predictions yet. Go to the Predictions or Top Scorer pages to generate some!")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
<p>🏆 The Richards World Cup 2026 Predictor | Advanced Analytics Edition</p>
<p><small>Predictions are for entertainment purposes only</small></p>
</div>
""", unsafe_allow_html=True)
