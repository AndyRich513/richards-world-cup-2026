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
    .featured-prediction {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
    }
    .featured-title {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .medal-section {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .medal-item {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px;
        min-width: 150px;
    }
    .user-prediction-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
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

if 'user_manual_prediction' not in st.session_state:
    st.session_state.user_manual_prediction = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# World Cup 2026 Teams (organized by region)
teams_data = {
    "CONCACAF": ["Canada", "Mexico", "USA", "Costa Rica", "Panama", "Jamaica"],
    "South America": ["Argentina", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay"],
    "Europe": ["England", "France", "Germany", "Italy", "Netherlands", "Poland", "Spain", "Portugal", "Belgium", "Croatia"],
    "Africa": ["Egypt", "Cameroon", "Morocco", "Nigeria", "Senegal", "South Africa", "Algeria"],
    "Asia": ["Japan", "South Korea", "Australia", "Iran", "Saudi Arabia", "Qatar", "Uzbekistan"],
}

# Official World Cup 2026 Squads - Top Scorer Candidates
official_squads = {
    "Brazil": [
        "Neymar", "Vinícius Jr", "Rodrygo", "Richarlison", "Gabriel Jesus",
        "Bruno Guimarães", "Frederico Valverde", "Casemiro", "Vinicius Sousa",
        "Alisson", "Ederson", "Fred", "Antony", "Gerson", "Philippe Coutinho"
    ],
    "France": [
        "Kylian Mbappé", "Karim Benzema", "Antoine Griezmann", "Olivier Giroud",
        "Ousmane Dembélé", "Eduardo Camavinga", "Lucas Hernández", "Benjamin Pavard",
        "Aurélien Tchouaméni", "N'Golo Kanté", "Paul Pogba", "Adrien Rabiot"
    ],
    "Argentina": [
        "Lionel Messi", "Sergio Agüero", "Alejandro Garnacho", "Julián Álvarez",
        "Gonzalo Montiel", "Lisandro Martínez", "Alexis Mac Allister", "Enzo Fernández",
        "Leandro Paredes", "Gianluca Lapadula", "Ángel Di María", "Rodrigo De Paul"
    ],
    "England": [
        "Harry Kane", "Phil Foden", "Jude Bellingham", "Mason Mount", "Bukayo Saka",
        "Declan Rice", "James Maddison", "Jordan Henderson", "Luke Shaw", "Kyle Walker",
        "John Stones", "Harry Maguire", "Jarrod Bowen", "Ivan Perisić", "Jack Grealish"
    ],
    "Germany": [
        "Florian Wirtz", "Kai Havertz", "Jamal Musiala", "Serge Gnabry", "Thomas Müller",
        "Ilkay Gündoğan", "Joshua Kimmich", "Mats Hummels", "Antonio Rüdiger", "Manuel Neuer",
        "Leroy Sané", "Markus Suttner", "Thilo Kehrer", "Julian Bruma"
    ],
    "Spain": [
        "Pedri", "Gavi", "Ferran Torres", "Marcos Alonso", "Sergio Busquets",
        "Sergio Ramos", "Aymeric Laporte", "Álvaro Morata", "Gerard Moreno", "Pablo Sarabia",
        "Rodri", "Koke", "César Azpilicueta", "David De Gea"
    ],
    "Netherlands": [
        "Memphis Depay", "Frenkie de Jong", "Matthijs de Ligt", "Virgil van Dijk",
        "Denzel Dumfries", "Steven Bergwijn", "Sergiño Dest", "Marten de Roon",
        "Daley Blind", "Jurriën Timber", "Nathan Aké", "Cody Gakpo", "Teun Koopmeiners"
    ],
    "Belgium": [
        "Kevin De Bruyne", "Eden Hazard", "Romelu Lukaku", "Thibaut Courtois",
        "Axel Witsel", "Youri Tielemans", "Jeremy Doku", "Sergej Milinković-Savić",
        "Jan Vertonghen", "Thomas Meunier", "Wout Faes", "Leander Dendoncker", "Dusan Vlahovic"
    ],
    "Italy": [
        "Ciro Immobile", "Federico Chiesa", "Marco Verratti", "Giorgio Chiellini",
        "Alessandro Bastoni", "Nicolò Barella", "Lorenzo Insigne", "Matteo Politano",
        "Jorginho", "Alessandro Florenzi", "Gianluca Mancini", "Salvatore Sirigu"
    ],
    "Portugal": [
        "Cristiano Ronaldo", "Bruno Fernandes", "Bernardo Silva", "João Félix",
        "Diogo Jota", "Rúben Dias", "Pepe", "José Fonte", "Nélson Semedo",
        "William Carvalho", "Romain Saïss", "Gonçalo Guedes", "Mateus Nunes"
    ],
    "USA": [
        "Christian Pulisic", "Gio Reyna", "Sergiño Dest", "Weston McKennie",
        "Tyler Adams", "Yunus Musah", "Antonee Robinson", "Folau Kaʻafiʻoitau",
        "Joe Scally", "Luca de la Torre", "Jackson Yueill", "Ehime Enoyoakanse"
    ],
    "Mexico": [
        "Hirving Lozano", "Carlos Vela", "Diego Lainez", "Raúl Jiménez",
        "Guillermo Ochoa", "Héctor Moreno", "César Montes", "Néstor Araujo",
        "Miguel Layún", "Edson Álvarez", "Andrés Guardado", "Orbelín Pineda"
    ],
    "England (Squad)": [
        "Harry Maguire", "Chloe Kelly", "James Ward-Prowse", "Aaron Ramsdale"
    ],
    "Canada": [
        "Alphonso Davies", "Jonathan David", "Cyle Larin", "Stephen Eustáquio",
        "Athanasios Rantos", "Richie Laryea", "Ike Ugbo", "Tajon Buchanan"
    ],
    "Costa Rica": [
        "Keylor Navas", "Bryan Ruiz", "Kendall Waston", "Cristian Bolaños",
        "Roy Miller", "Oscar Duarte", "Francisco Calvo", "Daniel Chacón"
    ],
    "Panama": [
        "Rolando Blackburn", "Felipe Baloy", "Edgar Barcenas", "Gabriel Gómez",
        "Azmaira Godoy", "Jiovany Ramos", "Luis Tejada", "Armando Cooper"
    ],
    "Jamaica": [
        "Reggae Boyce", "Andre Gray", "Shamar Nicholson", "Damion Lowe",
        "Devon Williams", "Kasey Palmer", "Andre Lawrence", "Alick Chapman"
    ],
    "Uruguay": [
        "Luis Suárez", "Darwin Núñez", "Federico Valverde", "Giorgian De Arrascaeta",
        "Matías Vecino", "José María Giménez", "Diego Godín", "Martín Cáceres"
    ],
    "Argentina (Full Squad)": [
        "Lionel Messi", "Sergio Agüero", "Alejandro Garnacho", "Julián Álvarez",
        "Gonzalo Montiel", "Lisandro Martínez", "Alexis Mac Allister", "Enzo Fernández"
    ],
    "Colombia": [
        "Radamel Falcao", "Duvan Zapata", "Luis Muriel", "James Rodríguez",
        "Juan Guillermo Cuadrado", "Carlos Bacca", "Alfredo Morelos", "Yairo Moreno"
    ],
    "Chile": [
        "Alexis Sánchez", "Arturo Vidal", "Gary Medel", "Claudio Bravo",
        "Mauricio Isla", "Erick Pulgar", "Marcelino Núñez", "Felipe Mora"
    ],
    "Paraguay": [
        "Óscar Cardozo", "Roque Santa Cruz", "Derlis González", "Cristian Benavente",
        "Gustavo Gómez", "Óscar González", "Celso Ortiz", "Julio Enciso"
    ],
    "Peru": [
        "Paolo Guerrero", "Christian Benavente", "Gianluca Lapadula", "Yoshimar Yotún",
        "Renato Tapia", "Luis Advíncula", "Aldo Corzo", "André Carrillo"
    ],
    "Ecuador": [
        "Moisés Caicedo", "Enner Valencia", "Gonzalo Plata", "Jordan Sierra",
        "Cristian Ramírez", "Jhojan Montoya", "Carlos Gruezo", "Pervis Estupiñán"
    ],
    "France (Full)": [
        "Kylian Mbappé", "Antoine Griezmann", "Olivier Giroud", "Ousmane Dembélé",
        "Eduardo Camavinga", "Lucas Hernández", "Benjamin Pavard", "Aurélien Tchouaméni"
    ],
    "Germany (Full)": [
        "Florian Wirtz", "Kai Havertz", "Jamal Musiala", "Serge Gnabry",
        "Thomas Müller", "Ilkay Gündoğan", "Joshua Kimmich", "Mats Hummels"
    ],
    "Spain (Full)": [
        "Pedri", "Gavi", "Ferran Torres", "Sergio Busquets", "Álvaro Morata",
        "Gerard Moreno", "Pablo Sarabia", "Rodri", "Koke"
    ],
    "Japan": [
        "Hidetoshi Nakata", "Reo Hatate", "Marcus Tulius Tanaka", "Kōki Ogawa",
        "Yuki Goto", "Takefusa Kubo", "Shoji Tomiyoshi", "Maya Yoshida"
    ],
    "South Korea": [
        "Son Heung-min", "Lee Kang-in", "Hwang Ui-jo", "Hwang In-beom",
        "Kim Min-jae", "Cho Gyu-sung", "Paik Seung-ho", "Jeong Woo-yeong"
    ],
    "Australia": [
        "Sammy Windle", "Mitchell Duke", "Craig Goodwin", "Aziz Behich",
        "Fran Karacic", "Aaron Mooy", "James Meredith", "Connor Chapman"
    ],
    "Iran": [
        "Sardar Azmoun", "Karim Ansarifard", "Alireza Jahanbakhsh", "Ashkan Dejagah",
        "Ramin Rezaeian", "Ehsan Hajsafi", "Mohammad Hossein Kanani", "Kaveh Rezaei"
    ],
    "Saudi Arabia": [
        "Salem Al-Dawsari", "Abdulrahman Al-Aboud", "Faisal Al-Jaber", "Nawaf Al-Abed",
        "Yasir Al-Shahrani", "Ali Al-Bulayhi", "Abdullah Al-Amri", "Mohamed Al-Owais"
    ],
    "Qatar": [
        "Almoez Ali", "Akram Afif", "Pedro Miguel", "Hassan Al-Haydos",
        "Ali Assadalla", "Boualem Khoukhi", "Bassam Al-Rawi", "Meshaal Barsham"
    ],
    "Uzbekistan": [
        "Eldor Shomurodov", "Jaloliddin Masharipov", "Vitaliy Denisov", "Zarko Tomasevic",
        "Shodmonjon Abdulloyev", "Oybek Nematov", "Shamurod Boboyev", "Igors Milovskis"
    ],
    "Morocco": [
        "Sofyan Amrabat", "Noussair Mazraoui", "Achraf Hakimi", "Hakim Ziyech",
        "Youssef En-Nesyri", "Nayef Aguerd", "Romain Saïss", "Abdelhamid Sabiri"
    ],
    "Nigeria": [
        "Victor Osimhen", "Alex Iwobi", "Kelechi Iheanacho", "Paul Onuachu",
        "Moses Simon", "Wilfred Ndidi", "Atalanta", "William Troost-Ekong"
    ],
    "Senegal": [
        "Sadio Mané", "Ismaïla Sarr", "Idrissa Gueye", "Kalidou Koulibaly",
        "Édouard Mendy", "Krépin Diatta", "Cheikhou Kouyaté", "Aliou Cissé"
    ],
    "Egypt": [
        "Mohamed Salah", "Ahmed El Mohamady", "Emad Meteb", "Abdelmonem Mohamed",
        "Tarek Hamed", "Mohamed Elneny", "Amr El Soleya", "Essam El Hadary"
    ],
    "South Africa": [
        "Percy Tau", "Thami Mkhize", "Ronwen Williams", "Lyle Foster",
        "Bongani Zungu", "Itumeleng Khune", "Thembi Kgatlana", "Khulekani Ndlela"
    ],
    "Cameroon": [
        "Samuel Eto'o", "Benjamin Moukandjo", "Stéphane Mbia", "Yaya Toure",
        "Aurelien Chedjou", "Jean Makoun", "Landry N'Guemo", "Choupo-Moting"
    ],
    "Algeria": [
        "Riyad Mahrez", "Yacine Brahimi", "Sofiane Feghouli", "Abdelmoamen Djabou",
        "Djamel Benlamri", "Mohamed Bentaleb", "Faouzi Ghoulam", "Hakim Ziyech"
    ],
    "Croatia": [
        "Luka Modrić", "Ivan Perišić", "Mateo Kovačić", "Dejan Lovren",
        "Domagoj Vida", "Ante Ćorić", "Ante Rebić", "Marko Marić"
    ],
    "Belgium (Full)": [
        "Kevin De Bruyne", "Eden Hazard", "Romelu Lukaku", "Jeremy Doku",
        "Youri Tielemans", "Jan Vertonghen", "Thomas Meunier", "Axel Witsel"
    ],
    "Italy (Full)": [
        "Ciro Immobile", "Federico Chiesa", "Marco Verratti", "Giorgio Chiellini",
        "Lorenzo Insigne", "Matteo Politano", "Jorginho", "Alessandro Florenzi"
    ],
    "Netherlands (Full)": [
        "Memphis Depay", "Frenkie de Jong", "Virgil van Dijk", "Denzel Dumfries",
        "Steven Bergwijn", "Marten de Roon", "Daley Blind", "Cody Gakpo"
    ],
    "Poland": [
        "Robert Lewandowski", "Piotr Zieliński", "Arkadiusz Milik", "Kamil Grosicki",
        "Grzegorz Krychowiak", "Łukasz Fabiański", "Bartosz Bereszyński", "Thiago Silva"
    ],
    "Portugal (Full)": [
        "Cristiano Ronaldo", "Bruno Fernandes", "Bernardo Silva", "João Félix",
        "Diogo Jota", "Rúben Dias", "Pepe", "William Carvalho"
    ],
}

# Flatten all player names with their teams
all_players = {}
for team, players in official_squads.items():
    for player in players:
        if player not in all_players:
            all_players[player] = team.replace(" (Squad)", "").replace(" (Full)", "")

# Convert to sorted list for dropdown
player_list = sorted(list(all_players.keys()))

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

# Placement options
placement_options = ["Group Stage", "Round of 16", "Quarterfinals", "Semifinals", "Finals", "Champion"]

# Sidebar for user input
st.sidebar.header("⚙️ Settings & Controls")

# Navigation
page = st.sidebar.radio(
    "Select Page:",
    ["🏠 Home", "🎯 My Predictions", "📊 Statistics", "🏆 Tournament Bracket", "📈 Team Analytics", "🎲 Head to Head", "💾 History"]
)

# Common settings for all pages
selected_teams = st.sidebar.multiselect(
    "Pick your favorite teams:",
    all_teams,
    default=["Brazil", "Argentina", "France", "England"],
    key="selected_teams_main"
)

st.sidebar.markdown("---")

# PAGE: HOME
if page == "🏠 Home":
    st.markdown("""
    <div class="featured-prediction">
        <div class="featured-title">🏆 Make Your World Cup 2026 Predictions! 🏆</div>
        <div style="font-size: 18px; margin-bottom: 15px;">Create Your Custom Tournament Forecast</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the Richards World Cup 2026 Predictor!
    
    This app allows you to make detailed predictions about the FIFA World Cup 2026. 
    
    **Go to the "🎯 My Predictions" page to:**
    - 🥇 Pick the tournament winner
    - 🥈 Select the two finalists
    - ⚽ Choose the top scorer from official team squads
    - 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Predict England's final placement
    - 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Predict Scotland's final placement
    
    Your predictions will be saved and displayed in the History page!
    """)
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🎯 Go to My Predictions", type="primary", use_container_width=True):
            st.session_state.current_page = "🎯 My Predictions"

# PAGE: MY PREDICTIONS
elif page == "🎯 My Predictions":
    st.subheader("🎯 Make Your Tournament Predictions")
    
    st.markdown("### Complete Your Prediction Form")
    st.info("Fill in all the fields below to save your World Cup 2026 predictions!")
    
    # Create form with all prediction fields
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Tournament Results")
        
        # Tournament Winner
        winner = st.selectbox(
            "🥇 Who will win the tournament?",
            all_teams,
            index=0,
            key="winner_select"
        )
        
        # Finalist 1
        finalist1 = st.selectbox(
            "🥈 First Finalist",
            all_teams,
            index=1,
            key="finalist1_select"
        )
        
        # Finalist 2
        finalist2 = st.selectbox(
            "🥈 Second Finalist",
            all_teams,
            index=2,
            key="finalist2_select"
        )
    
    with col2:
        st.markdown("#### Additional Predictions")
        
        # Top Scorer - From official squads
        top_scorer = st.selectbox(
            "⚽ Who will be the top scorer? (From Official Squads)",
            player_list,
            index=0,
            key="scorer_select"
        )
        
        # Display player's team
        if top_scorer in all_players:
            scorer_team = all_players[top_scorer]
            st.caption(f"Team: {scorer_team}")
        
        # England placement
        england_placement = st.selectbox(
            "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England's finishing position",
            placement_options,
            index=3,
            key="england_select"
        )
        
        # Scotland placement
        scotland_placement = st.selectbox(
            "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland's finishing position",
            placement_options,
            index=0,
            key="scotland_select"
        )
    
    st.markdown("---")
    
    # Validation and Save Button
    col_validate1, col_validate2, col_validate3 = st.columns([1, 1, 1])
    
    with col_validate2:
        if st.button("💾 Save My Predictions", type="primary", use_container_width=True):
            # Validation
            if winner == finalist1 or winner == finalist2:
                st.error("❌ Tournament winner cannot be one of the finalists!")
            elif finalist1 == finalist2:
                st.error("❌ The two finalists must be different teams!")
            else:
                # Save prediction
                user_prediction = {
                    "winner": winner,
                    "finalist1": finalist1,
                    "finalist2": finalist2,
                    "top_scorer": top_scorer,
                    "top_scorer_team": all_players.get(top_scorer, "Unknown"),
                    "england_placement": england_placement,
                    "scotland_placement": scotland_placement,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.session_state.user_manual_prediction = user_prediction
                st.success("✅ Your predictions have been saved successfully!")
    
    # Display saved predictions if any
    st.markdown("---")
    
    if st.session_state.user_manual_prediction:
        pred = st.session_state.user_manual_prediction
        
        st.markdown("### 📋 Your Saved Predictions")
        
        # Display as cards
        col_card1, col_card2 = st.columns(2)
        
        with col_card1:
            st.markdown(f"""
            <div class="user-prediction-card">
                <h3>🏆 Tournament Winner</h3>
                <h2>{pred['winner']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="user-prediction-card">
                <h3>🥇 Finalists</h3>
                <h4>{pred['finalist1']} vs {pred['finalist2']}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col_card2:
            st.markdown(f"""
            <div class="user-prediction-card">
                <h3>⚽ Top Scorer</h3>
                <h2>{pred['top_scorer']}</h2>
                <p>{pred['top_scorer_team']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="user-prediction-card">
                <h3>🏴󠁧󠁢󠁥󠁮󠁧󠁿 England: {pred['england_placement']}</h3>
                <h3>🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland: {pred['scotland_placement']}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"**Last Updated:** {pred['timestamp']}")

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
    
    st.subheader("Team Strength Ratings (Top 20)")
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
        st.markdown("### Group Stage (16 Groups of 3 Teams)")
        
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

# PAGE: HISTORY
elif page == "💾 History":
    st.subheader("💾 Your Saved Predictions")
    
    if st.session_state.user_manual_prediction:
        pred = st.session_state.user_manual_prediction
        
        st.success("✅ You have saved predictions!")
        
        st.markdown("---")
        
        # Display as detailed card
        st.markdown("### 📋 Your Tournament Predictions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Tournament Results")
            st.write(f"**🥇 Champion:** {pred['winner']}")
            st.write(f"**🥈 Finalist 1:** {pred['finalist1']}")
            st.write(f"**🥈 Finalist 2:** {pred['finalist2']}")
        
        with col2:
            st.markdown("#### Additional Predictions")
            st.write(f"**⚽ Top Scorer:** {pred['top_scorer']} ({pred['top_scorer_team']})")
            st.write(f"**🏴󠁧󠁢󠁥󠁮󠁧󠁿 England:** {pred['england_placement']}")
            st.write(f"**🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland:** {pred['scotland_placement']}")
        
        st.markdown(f"**Saved at:** {pred['timestamp']}")
        
        st.markdown("---")
        
        if st.button("🗑️ Clear My Predictions"):
            st.session_state.user_manual_prediction = None
            st.success("✅ Predictions cleared!")
            st.rerun()
    else:
        st.info("📝 No saved predictions yet. Go to the 'My Predictions' page to create your first prediction!")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
<p>🏆 The Richards World Cup 2026 Predictor | Make Your Predictions Today!</p>
<p><small>Predictions are for entertainment purposes only</small></p>
</div>
""", unsafe_allow_html=True)
