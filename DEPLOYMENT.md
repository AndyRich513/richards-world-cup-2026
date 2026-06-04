# Streamlit Cloud Deployment Guide

## Quick Deploy to Streamlit Cloud (Recommended - Free)

### Step 1: Prepare Your Repository
1. Make sure all files are committed and pushed to GitHub
2. Verify `.gitignore` includes:
   - `firebase_credentials.json`
   - `.streamlit/secrets.toml`
   - Virtual environment folders

### Step 2: Sign Up for Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "Sign up" and authenticate with GitHub
3. Grant Streamlit access to your GitHub repositories

### Step 3: Deploy Your App
1. Click "Create app"
2. Select:
   - **Repository**: `AndyRich513/richards-world-cup-2026`
   - **Branch**: `main`
   - **Main file path**: `richards_world_cup_2026.py`
3. Click "Deploy"

Your app will be live in ~1-2 minutes at:
```
https://andyrich513-richards-world-cup-2026.streamlit.app
```

### Step 4: Add Secrets (for Firebase)
1. In Streamlit Cloud app dashboard, click "Settings" ⚙️
2. Go to "Secrets"
3. Paste your Firebase credentials:
   ```toml
   [firebase]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "xxx"
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "firebase-adminsdk-xxx@xxx.iam.gserviceaccount.com"
   client_id = "xxx"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "..."
   ```
4. Click "Save"

## Auto-Deployment

Every time you push to GitHub (`main` branch), Streamlit Cloud automatically redeploys your app! 🚀

## Alternative: Heroku Deployment

### Step 1: Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Create Heroku App
```bash
heroku login
heroku create richards-world-cup-2026
```

### Step 3: Add Procfile
Create `Procfile` in project root:
```
web: streamlit run --server.port $PORT --server.address 0.0.0.0 richards_world_cup_2026.py
```

### Step 4: Add Streamlit Config
Create `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
enableXsrfProtection = false

[browser]
serverAddress = "localhost"
```

### Step 5: Deploy
```bash
git push heroku main
```

Your app will be live at:
```
https://richards-world-cup-2026.herokuapp.com
```

## Comparison: Streamlit Cloud vs Heroku

| Feature | Streamlit Cloud | Heroku |
|---------|-----------------|--------|
| Cost | Free | Free tier available |
| Setup | 3 clicks | CLI required |
| Auto-deploy | Yes (on push) | Yes (on push) |
| Custom domain | $10/month | Yes |
| Performance | Excellent | Good |
| Best for | Streamlit apps | General apps |

**Recommendation**: Use **Streamlit Cloud** - it's built for Streamlit! 🚀

## Troubleshooting

### App won't load
- Check that `main_file_path` is correct
- Verify all dependencies in `requirements.txt`
- Check app logs for errors

### Firebase not working
- Verify secrets are added correctly
- Check Firebase credentials format
- Test credentials locally first

### App is slow
- Optimize Pandas operations
- Use `@st.cache_data` for expensive computations
- Enable query caching

## Share Your App

Once deployed, share the link:
```
📱 https://andyrich513-richards-world-cup-2026.streamlit.app
```

## Update Your App

Simply push changes to GitHub:
```bash
git add .
git commit -m "Add new features"
git push origin main
```

Streamlit Cloud will automatically redeploy! ✨
