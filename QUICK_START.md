# QuestionTrack - Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.11+ installed
- ✅ Node.js 18+ installed
- ✅ ffmpeg installed (for audio processing)

## Step-by-Step Installation

### Step 1: Set Up Backend

Open PowerShell in the project root directory and run:

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item ..\.env.example .env
```

### Step 2: Start Backend Server

With the virtual environment still activated:

```powershell
# Run the backend
python run.py
```

The backend will start at: **http://localhost:8000**

On first run, it will download the Whisper model (74MB for 'base' model). This may take 30-60 seconds.

### Step 3: Set Up Frontend (New PowerShell Window)

Open a NEW PowerShell window in the project root:

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start at: **http://localhost:5173**

### Step 4: Access the Application

Open your browser to: **http://localhost:5173**

You should see the QuestionTrack interface!

## Quick Test

1. Click **"Start Recording"** (allow microphone access when prompted)
2. Speak a question: "How does YOLO v7 work?"
3. Click **"Stop Recording"**
4. Wait for processing (a few seconds)
5. See your question appear in "Latest Questions"

## Troubleshooting

### Backend Won't Start

**Issue**: ModuleNotFoundError
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: Port 8000 already in use
```powershell
# Find and kill process using port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

### Frontend Won't Start

**Issue**: npm not found
- Install Node.js from https://nodejs.org/

**Issue**: Port 5173 already in use
- The error message will show the alternate port (usually 5174)

### Whisper Model Errors

**Issue**: "Failed to load Whisper model"
- Ensure you have internet connection for first-time download
- Check disk space (need ~500MB free)
- Try using smaller model in .env: `STT_MODEL=tiny`

### Microphone Not Working

**Issue**: "Microphone access denied"
- Check browser permissions (click lock icon in address bar)
- Ensure no other app is using the microphone

**Issue**: Recording but no transcription
- Check backend logs in the PowerShell window
- Ensure audio is clear and in English

## Manual Testing Without Recording

If you want to test without recording:

1. Find a .wav or .mp3 audio file
2. Click **"Upload Audio"** button
3. Select your file
4. Wait for processing

## Checking System Status

Visit these URLs to verify everything is working:

- **Backend Health**: http://localhost:8000/api/health
- **API Docs**: http://localhost:8000/api/docs
- **Frontend**: http://localhost:5173

## Stopping the Application

To stop the servers:

1. In the backend PowerShell window: Press `Ctrl+C`
2. In the frontend PowerShell window: Press `Ctrl+C`
3. Type `deactivate` to exit the Python virtual environment

## Next Steps

Once running:

1. Try recording different questions
2. Test technical term correction (say "yolo", "esp thirty two", etc.)
3. Use the search in Question History
4. Try dark mode (moon icon in header)
5. Open Settings (gear icon) to configure

## Production Deployment

For production deployment without Docker, see the README.md section on "Manual Deployment".

## Need Help?

- Check backend logs in the PowerShell window where you ran `python run.py`
- Check browser console (F12) for frontend errors
- Verify .env configuration matches .env.example
- Ensure all dependencies installed correctly

---

**Enjoy using QuestionTrack!**
