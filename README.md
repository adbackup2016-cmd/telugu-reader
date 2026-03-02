# తెలుగు పాఠకుడు · Telugu Text Reader

A web app that reads Telugu text aloud using Google TTS (gTTS).

## Deploy on Render (Free)

1. Upload these 3 files to a new GitHub repository:
   - `app.py`
   - `requirements.txt`
   - `Procfile`

2. Go to https://render.com and sign up (free)

3. Click **New → Web Service**

4. Connect your GitHub repo

5. Render auto-detects the settings. Confirm:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

6. Click **Deploy** — your app will be live at:
   `https://your-app-name.onrender.com`

## Run Locally

```bash
pip install flask gtts gunicorn
python app.py
# Open http://localhost:5000
```

## Notes
- Free Render tier may sleep after 15 min inactivity (first request takes ~30s to wake)
- gTTS requires internet connection on the server
- Max text length: 5000 characters per request
