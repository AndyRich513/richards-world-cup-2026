# Richards World Cup 2026 Predictor

A Streamlit web app where participants can make predictions about the 2026 FIFA World Cup and view other participants' predictions on a live leaderboard.

## Features

- 🎯 **Make Predictions** - Submit your World Cup 2026 predictions
- 🏆 **Leaderboard** - View ranked predictions by confidence level
- 📊 **View All Predictions** - See detailed predictions from all participants
- 🔄 **Real-time Updates** - Live leaderboard with mock and real participant data
- 💾 **Data Storage** - Predictions stored in Firestore (or local session)

## Installation

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AndyRich513/richards-world-cup-2026.git
   cd richards-world-cup-2026
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run richards_world_cup_2026.py
   ```

The app will open at `http://localhost:8501`

## Cloud Deployment

### Deploy to Streamlit Cloud (Free & Easy)

1. **Fork/Push to GitHub** - Make sure your repo is on GitHub
2. **Sign up at Streamlit Cloud** - Go to https://share.streamlit.io
3. **Connect your GitHub repo** - Select your repository
4. **Deploy!** - Streamlit Cloud will automatically deploy your app

Your app will be live at: `https://<username>-<repo-name>.streamlit.app`

### Deploy to Heroku (Alternative)

See `DEPLOYMENT.md` for detailed instructions.

## Database Setup (Firebase Firestore)

To enable persistent storage across sessions:

1. **Create a Firebase Project**:
   - Go to https://console.firebase.google.com
   - Click "Create Project"
   - Enable Firestore Database

2. **Download Service Account Key**:
   - Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Save as `firebase_credentials.json` in project root

3. **Create `.streamlit/secrets.toml`**:
   ```toml
   [firebase]
   type = "service_account"
   project_id = "your-project-id"
   # ... (rest of your Firebase credentials)
   ```

4. **Update app to use Firebase**:
   - See `firebase_integration.md` for Firebase implementation

## File Structure

```
richards-world-cup-2026/
├── richards_world_cup_2026.py      # Main Streamlit app
├── firebase_integration.md          # Firebase database guide
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── DEPLOYMENT.md                    # Deployment guide
├── .gitignore                       # Git ignore rules
└── .streamlit/
    └── config.toml                  # Streamlit configuration
```

## Features Explained

### Make Prediction
- Enter your name
- Select tournament winner and runner-up
- Predict top scorer and total goals
- Predict a "dark horse" surprise team
- Set confidence level (0-100%)

### Leaderboard
- Ranked by confidence level
- Shows all participants
- Mock data demonstrates app functionality
- Real-time updates as predictions are submitted

### All Predictions
- **Card View** - Beautiful card layout of all predictions
- **Table View** - Spreadsheet view for easy comparison

## Data Privacy

- **Local Mode**: Predictions stored in browser session (temporary)
- **Cloud Mode**: Predictions stored in Firestore (persistent)
- **No Personal Data Collected**: Only prediction information

## Roadmap

- [ ] Integrate Firebase Firestore for persistent storage
- [ ] Add user authentication
- [ ] Add scoring system (automatic scoring when tournament ends)
- [ ] Add notifications when predictions are updated
- [ ] Add prediction comparison tool
- [ ] Add historical World Cup predictions

## Contributing

Feel free to fork and submit pull requests!

## License

This project is open source and available under the MIT License.

---

**Made with ❤️ for World Cup 2026** 🏆
