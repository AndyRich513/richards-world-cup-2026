# Firebase Integration for Richards World Cup 2026 Predictor

This file contains functions to integrate Firebase Firestore for persistent data storage.

## Setup Instructions

1. Install Firebase Admin SDK:
   ```bash
   pip install firebase-admin
   ```

2. Create a Firebase project and download service account credentials

3. Add credentials to `.streamlit/secrets.toml`

## Firebase Functions

```python
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
from datetime import datetime

# Initialize Firebase (only runs once per session)
@st.cache_resource
def init_firebase():
    try:
        # Using Streamlit secrets
        firebase_config = st.secrets["firebase"]
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
    except:
        # Fallback to service account JSON file
        cred = credentials.Certificate("firebase_credentials.json")
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

db = init_firebase()

# Save prediction to Firestore
def save_prediction_to_db(prediction):
    try:
        db.collection("predictions").add(prediction)
        return True
    except Exception as e:
        st.error(f"Error saving prediction: {e}")
        return False

# Get all predictions from Firestore
def get_all_predictions():
    try:
        docs = db.collection("predictions").stream()
        predictions = [doc.to_dict() for doc in docs]
        return predictions
    except Exception as e:
        st.error(f"Error fetching predictions: {e}")
        return []

# Update user prediction
def update_prediction(user_name, prediction):
    try:
        # Query for existing prediction by user
        docs = db.collection("predictions").where("name", "==", user_name).stream()
        for doc in docs:
            db.collection("predictions").document(doc.id).update(prediction)
        return True
    except Exception as e:
        st.error(f"Error updating prediction: {e}")
        return False

# Delete prediction
def delete_prediction(user_name):
    try:
        docs = db.collection("predictions").where("name", "==", user_name).stream()
        for doc in docs:
            db.collection("predictions").document(doc.id).delete()
        return True
    except Exception as e:
        st.error(f"Error deleting prediction: {e}")
        return False
```

## Usage in Main App

Replace the session state storage with Firebase calls:

```python
# Save prediction
if st.button("💾 Save Prediction"):
    prediction = {
        "name": participant_name,
        "winner": winner,
        "runner_up": runner_up,
        "timestamp": datetime.now().isoformat()
    }
    save_prediction_to_db(prediction)
    st.success("Prediction saved!")

# Load predictions
all_predictions = get_all_predictions()
```

## Firestore Collection Structure

```
predictions/
├── document1
│   ├── name: "John Smith"
│   ├── winner: "Argentina"
│   ├── runner_up: "France"
│   ├── timestamp: "2026-06-01T10:30:00"
│   └── confidence: 85
├── document2
│   └── ...
```

## Security Rules (Firestore)

Add to your Firestore Security Rules for public access:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /predictions/{document=**} {
      allow read, write;
    }
  }
}
```

**Note**: For production, implement proper authentication!

## Alternative: SQLite (Local Database)

If you prefer local SQLite instead of Firebase:

```python
import sqlite3

def init_db():
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY,
            name TEXT,
            winner TEXT,
            runner_up TEXT,
            confidence INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    return conn

def save_to_sqlite(prediction):
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO predictions 
        (name, winner, runner_up, confidence, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (prediction['name'], prediction['winner'], 
          prediction['runner_up'], prediction['confidence'],
          prediction['timestamp']))
    conn.commit()
    conn.close()
```
