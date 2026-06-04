import streamlit as st
from datetime import datetime
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# ============================================================================
# FIREBASE SETUP
# ============================================================================

@st.cache_resource
def init_firebase():
    """Initialize Firebase connection"""
    try:
        # Check if Firebase app is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Firebase app not initialized, initialize it
        try:
            # Try to load from Streamlit secrets (for cloud deployment)
            firebase_config = st.secrets["firebase"]
            cred = credentials.Certificate(firebase_config)
        except (KeyError, FileNotFoundError):
            # Fallback to local JSON file
            try:
                cred = credentials.Certificate("firebase_credentials.json")
            except FileNotFoundError:
                st.error("❌ Firebase credentials not found. Please configure Firebase.")
                st.stop()
        
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

# Initialize Firestore
try:
    db = init_firebase()
    firebase_enabled = True
except Exception as e:
    st.warning(f"⚠️ Firebase not configured. Using local storage only. Error: {e}")
    firebase_enabled = False
    db = None

# ============================================================================
# FIREBASE FUNCTIONS
# ============================================================================

def save_prediction_to_firebase(prediction):
    """Save prediction to Firebase Firestore"""
    if not firebase_enabled:
        return False
    
    try:
        # Check if user already has a prediction and update it
        existing = db.collection("predictions").where("name", "==", prediction["name"]).stream()
        existing_docs = list(existing)
        
        if existing_docs:
            # Update existing prediction
            db.collection("predictions").document(existing_docs[0].id).update(prediction)
        else:
            # Add new prediction
            db.collection("predictions").add(prediction)
        
        return True
    except Exception as e:
        st.error(f"Error saving to Firebase: {e}")
        return False

def get_predictions_from_firebase():
    """Get all predictions from Firebase Firestore"""
    if not firebase_enabled:
        return []
    
    try:
        docs = db.collection("predictions").stream()
        predictions = [doc.to_dict() for doc in docs]
        return predictions
    except Exception as e:
        st.error(f"Error fetching from Firebase: {e}")
        return []

def delete_prediction_from_firebase(user_name):
    """Delete prediction from Firebase"""
    if not firebase_enabled:
        return False
    
    try:
        docs = db.collection("predictions").where("name", "==", user_name).stream()
        for doc in docs:
            db.collection("predictions").document(doc.id).delete()
        return True
    except Exception as e:
        st.error(f"Error deleting from Firebase: {e}")
        return False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(page_title="The Richards World Cup 2026 Predictor", page_icon="🏆", layout="wide")

st.title("🏆 The Richards World Cup 2026 Predictor")

# Firebase status indicator
if firebase_enabled:
    st.sidebar.success("✅ Connected to Firebase")
else:
    st.sidebar.warning("⚠️ Using local storage only")

# Initialize session state for local storage fallback
if 'predictions' not in st.session_state:
    st.session_state.predictions = []
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Sidebar for navigation
page = st.sidebar.radio("Navigation", ["Make Prediction", "Leaderboard", "All Predictions"])

# ============================================================================
# PAGE 1: MAKE PREDICTION
# ============================================================================
if page == "Make Prediction":
    st.subheader("Enter Your Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        participant_name = st.text_input("Your Name:", placeholder="Enter your name here", key="name_input")
    
    with col2:
        st.info("💡 Tip: Use the same name to update your prediction")
    
    if participant_name:
        st.session_state.current_user = participant_name
        st.success(f"Welcome, {participant_name}! 🎉")
        
        st.markdown("### Your World Cup 2026 Predictions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            winner = st.selectbox("Tournament Winner:", ["Argentina", "France", "Brazil", "England", "Germany", "Spain", "Netherlands", "Other"])
        
        with col2:
            runner_up = st.selectbox("Runner-Up:", ["France", "Argentina", "Brazil", "Germany", "England", "Spain", "Netherlands", "Other"])
        
        with col3:
            top_scorer = st.text_input("Top Scorer Name:", placeholder="e.g., Mbappé")
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_goals = st.number_input("Total Goals in Tournament:", min_value=50, max_value=200, value=150, step=5)
        
        with col2:
            surprise_team = st.text_input("Surprise Team (Dark Horse):", placeholder="e.g., Uruguay")
        
        confidence = st.slider("Confidence Level (%)", 0, 100, 50)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Prediction", use_container_width=True):
                prediction = {
                    "name": participant_name,
                    "winner": winner,
                    "runner_up": runner_up,
                    "top_scorer": top_scorer,
                    "total_goals": int(total_goals),
                    "surprise_team": surprise_team,
                    "confidence": int(confidence),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Save to Firebase (if enabled) and local storage
                firebase_success = save_prediction_to_firebase(prediction) if firebase_enabled else True
                
                # Also update local session state
                existing = [p for p in st.session_state.predictions if p['name'].lower() == participant_name.lower()]
                if existing:
                    st.session_state.predictions = [p for p in st.session_state.predictions if p['name'].lower() != participant_name.lower()]
                
                st.session_state.predictions.append(prediction)
                
                if firebase_success:
                    st.success("✅ Prediction saved successfully!" + (" (Synced to Firebase)" if firebase_enabled else ""))
                else:
                    st.success("✅ Prediction saved locally!")
        
        with col2:
            if st.button("🔄 Clear Prediction", use_container_width=True):
                # Delete from Firebase if enabled
                if firebase_enabled:
                    delete_prediction_from_firebase(participant_name)
                
                # Delete from local storage
                st.session_state.predictions = [p for p in st.session_state.predictions if p['name'].lower() != participant_name.lower()]
                st.warning("Prediction cleared!")

# ============================================================================
# PAGE 2: LEADERBOARD (Mock + Real Data)
# ============================================================================
elif page == "Leaderboard":
    st.subheader("🏆 Leaderboard - Confidence Rankings")
    
    # Mock data for other participants
    mock_predictions = [
        {"name": "John Smith", "confidence": 85, "winner": "Argentina", "timestamp": "2026-06-01 10:30:00"},
        {"name": "Sarah Johnson", "confidence": 78, "winner": "France", "timestamp": "2026-06-02 14:15:00"},
        {"name": "Mike Wilson", "confidence": 92, "winner": "Brazil", "timestamp": "2026-06-03 09:45:00"},
        {"name": "Emma Davis", "confidence": 72, "winner": "England", "timestamp": "2026-06-01 16:20:00"},
        {"name": "Alex Martinez", "confidence": 88, "winner": "Spain", "timestamp": "2026-06-03 11:00:00"},
    ]
    
    # Get predictions from Firebase or use local storage
    firebase_predictions = get_predictions_from_firebase() if firebase_enabled else []
    
    # Combine mock data with actual predictions
    all_predictions = mock_predictions + firebase_predictions + st.session_state.predictions
    
    # Remove duplicates (keep Firebase version if exists)
    seen_names = set()
    unique_predictions = []
    for pred in all_predictions:
        name_lower = pred['name'].lower()
        if name_lower not in seen_names:
            seen_names.add(name_lower)
            unique_predictions.append(pred)
    
    if unique_predictions:
        # Sort by confidence descending
        sorted_predictions = sorted(unique_predictions, key=lambda x: x['confidence'], reverse=True)
        
        # Create leaderboard dataframe
        leaderboard_data = []
        for idx, pred in enumerate(sorted_predictions, 1):
            leaderboard_data.append({
                "Rank": idx,
                "Participant": pred['name'],
                "Confidence": f"{pred['confidence']}%",
                "Winner Pick": pred.get('winner', 'N/A'),
                "Submitted": pred.get('timestamp', 'N/A')
            })
        
        df_leaderboard = pd.DataFrame(leaderboard_data)
        
        # Display with styling
        st.dataframe(df_leaderboard, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Participants", len(unique_predictions))
        with col2:
            avg_confidence = sum([p['confidence'] for p in unique_predictions]) / len(unique_predictions)
            st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
    else:
        st.info("No predictions yet. Be the first to make a prediction! 🎯")

# ============================================================================
# PAGE 3: ALL PREDICTIONS (Detailed View)
# ============================================================================
elif page == "All Predictions":
    st.subheader("📊 All Participants' Predictions")
    
    # Mock data
    mock_predictions = [
        {
            "name": "John Smith",
            "winner": "Argentina",
            "runner_up": "France",
            "top_scorer": "Mbappé",
            "total_goals": 148,
            "surprise_team": "Uruguay",
            "confidence": 85,
            "timestamp": "2026-06-01 10:30:00"
        },
        {
            "name": "Sarah Johnson",
            "winner": "France",
            "runner_up": "Brazil",
            "top_scorer": "Neymar",
            "total_goals": 155,
            "surprise_team": "Portugal",
            "confidence": 78,
            "timestamp": "2026-06-02 14:15:00"
        },
        {
            "name": "Mike Wilson",
            "winner": "Brazil",
            "runner_up": "Argentina",
            "top_scorer": "Vinicius Jr",
            "total_goals": 160,
            "surprise_team": "Chile",
            "confidence": 92,
            "timestamp": "2026-06-03 09:45:00"
        },
    ]
    
    # Get predictions from Firebase or use local storage
    firebase_predictions = get_predictions_from_firebase() if firebase_enabled else []
    
    # Combine with actual predictions
    all_predictions = mock_predictions + firebase_predictions + st.session_state.predictions
    
    # Remove duplicates
    seen_names = set()
    unique_predictions = []
    for pred in all_predictions:
        name_lower = pred['name'].lower()
        if name_lower not in seen_names:
            seen_names.add(name_lower)
            unique_predictions.append(pred)
    
    if unique_predictions:
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Card View", "Table View"])
        
        with tab1:
            st.write("### Prediction Cards")
            for idx, pred in enumerate(unique_predictions, 1):
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**{pred['name']}**")
                        st.caption(pred.get('timestamp', 'N/A'))
                    
                    with col2:
                        st.write(f"🏆 Winner: **{pred.get('winner', 'N/A')}**")
                        st.write(f"🥈 Runner-up: **{pred.get('runner_up', 'N/A')}**")
                    
                    with col3:
                        st.metric("Confidence", f"{pred.get('confidence', 0)}%")
                    
                    st.divider()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"⚽ Top Scorer: {pred.get('top_scorer', 'N/A')}")
                    with col2:
                        st.write(f"🎯 Total Goals: {pred.get('total_goals', 'N/A')}")
                    with col3:
                        st.write(f"🌟 Dark Horse: {pred.get('surprise_team', 'N/A')}")
        
        with tab2:
            st.write("### All Predictions Table")
            df_all = pd.DataFrame(unique_predictions)
            # Select columns to display
            display_cols = ['name', 'winner', 'runner_up', 'top_scorer', 'confidence', 'timestamp']
            df_display = df_all[display_cols].rename(columns={
                'name': 'Participant',
                'winner': 'Winner',
                'runner_up': 'Runner-up',
                'top_scorer': 'Top Scorer',
                'confidence': 'Confidence',
                'timestamp': 'Submitted'
            })
            st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No predictions yet. Start by making your prediction! 🎯")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
storage_info = "Firebase + Local" if firebase_enabled else "Local session-based"
st.markdown(f"""
<div style='text-align: center; color: #999; font-size: 12px; padding: 20px;'>
    🏆 The Richards World Cup 2026 Predictor | Data stored: {storage_info}
</div>
""", unsafe_allow_html=True)
