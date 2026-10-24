# 🚀 START HERE - QuestionTrack

Welcome! This guide will get QuestionTrack running on your Windows machine in a few simple steps.

## ⚡ Quick Start (2 Steps)

### Step 1: Start the Backend

Open PowerShell in the project directory and run:

```powershell
cd backend
.\start_backend.ps1
```

**Wait for**: "Application startup complete"

Leave this PowerShell window open.

### Step 2: Start the Frontend

Open a **NEW** PowerShell window in the project directory and run:

```powershell
cd frontend
.\start_frontend.ps1
```

**Wait for**: "Local: http://localhost:5173"

### Step 3: Open the App

Open your browser to: **http://localhost:5173**

🎉 **Done!** QuestionTrack is now running.

---

## 🎯 First-Time Setup Notes

### If PowerShell Scripts Are Blocked

If you see "script execution is disabled", run this once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### What Happens on First Run

**Backend (1-2 minutes)**:
- Creates Python virtual environment
- Installs Python packages
- Downloads Whisper model (~74MB)

**Frontend (30 seconds - 1 minute)**:
- Installs npm packages (~200MB)
- Starts development server

---

## 📱 Using QuestionTrack

### Recording a Question

1. Click **"Start Recording"**
2. Allow microphone access when prompted
3. Speak clearly: *"How does YOLO v7 detect objects?"*
4. Click **"Stop Recording"**
5. Wait 2-5 seconds for processing
6. Your question appears corrected and formatted!

### Uploading Audio

1. Click **"Upload Audio"**
2. Select a .wav, .mp3, or other audio file
3. Wait for processing
4. Question appears if detected

### Features to Try

- ✅ Record multiple questions
- ✅ Search question history
- ✅ Toggle dark mode (moon icon)
- ✅ Open settings (gear icon)
- ✅ Copy questions to clipboard
- ✅ Delete individual questions
- ✅ Clear all history

---

## 🛠️ Troubleshooting

### Backend Won't Start

**Issue**: "Python not recognized"
- Install Python 3.11+ from https://www.python.org/downloads/

**Issue**: "ModuleNotFoundError"
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Issue**: Port 8000 busy
```powershell
# Find what's using port 8000
Get-NetTCPConnection -LocalPort 8000

# Stop it if needed
Stop-Process -Id <ProcessId>
```

### Frontend Won't Start

**Issue**: "node is not recognized"
- Install Node.js from https://nodejs.org/ (get the LTS version)

**Issue**: Installation fails
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### Microphone Not Working

1. Check browser permissions (click 🔒 in address bar)
2. Ensure no other app is using your microphone
3. Try restarting your browser

### No Questions Detected

- Speak clearly in English
- Say questions (start with: how, what, why, when, etc.)
- Check backend terminal for errors
- Try uploading a test audio file instead

---

## 🔍 Verify Everything Works

Visit these URLs:

- ✅ Frontend: http://localhost:5173
- ✅ Backend Health: http://localhost:8000/api/health
- ✅ API Docs: http://localhost:8000/api/docs

All should load successfully.

---

## ⚙️ Configuration

### Change Whisper Model

Edit `.env` in project root:

```env
STT_MODEL=tiny    # Fastest, good for testing
STT_MODEL=base    # Balanced (default)
STT_MODEL=small   # Most accurate, slower
```

Restart backend after changes.

### Add Custom Technical Terms

Edit `backend/data/technical_terms.json`:

```json
{
  "terms": [
    {"term": "YourTerm", "case_sensitive": true},
    {"term": "AnotherTerm", "case_sensitive": false}
  ]
}
```

---

## 🛑 Stopping the Application

1. In backend PowerShell: Press `Ctrl+C`
2. In frontend PowerShell: Press `Ctrl+C`
3. Type `deactivate` in backend window (if virtual env is active)

---

## 📚 Next Steps

- Read **QUICK_START.md** for detailed setup
- Read **README.md** for full documentation
- Read **PROJECT_SUMMARY.md** for architecture details

---

## 🆘 Still Having Issues?

Check the PowerShell windows for error messages:

**Backend errors** appear in the window where you ran `start_backend.ps1`

**Frontend errors** appear in the window where you ran `start_frontend.ps1`

**Browser errors**: Press F12 → Console tab

---

## ✨ Everything Working?

Great! Now you can:

1. **Test technical terms**: Say "ESP thirty two" → becomes "ESP32"
2. **Try different questions**: What, Why, How, When questions
3. **Use the history**: Search for past questions
4. **Customize**: Open Settings to change model or theme

---

**Enjoy QuestionTrack! 🎤➡️📝**
