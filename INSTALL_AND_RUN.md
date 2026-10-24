# Install and Run QuestionTrack

## Quick Installation

### Step 1: Install Backend Dependencies

Open PowerShell and navigate to the backend directory, then run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

This installs all backend dependencies, including FastAPI and Uvicorn. The first install can take several minutes because it downloads PyTorch.

### Step 2: Start Backend

With the virtual environment activated:

```powershell
python run.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Leave this window open!**

### Step 3: Install Frontend Dependencies

Open a **NEW** PowerShell window:

```powershell
cd frontend
npm install
```

This takes 1-2 minutes.

### Step 4: Start Frontend

After npm install completes:

```powershell
npm run dev
```

You should see:
```
  VITE v5.0.6  ready in 500 ms

  ➜  Local:   http://localhost:5173/
```

### Step 5: Open in Browser

Go to: **http://localhost:5173**

---

## If Installation Fails

### Alternative: Install Lighter Dependencies

If PyTorch download is too large or slow, you can install CPU-only version:

```powershell
python -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

Then install the rest:

```powershell
python -m pip install fastapi "uvicorn[standard]" faster-whisper librosa soundfile webrtcvad sqlalchemy alembic rapidfuzz textblob python-dotenv aiofiles httpx pytest pytest-asyncio structlog PyPDF2 pydantic pydantic-settings
```

---

## Testing Without Full Installation

If you want to test the frontend without backend:

1. Skip backend setup
2. Install and run frontend only
3. The UI will load (transcription won't work until backend is running)

---

## Verify Installation

Check that the active Python can import the server dependency:

```powershell
python -m pip show uvicorn
python -c "import uvicorn; print(uvicorn.__version__)"
```

If that import fails, activate the backend virtual environment and run `python -m pip install -r requirements.txt` from the `backend` directory.

---

## After Installation

Once both are running:

1. Open http://localhost:5173
2. Click "Start Recording"
3. Allow microphone access
4. Speak a question
5. Click "Stop Recording"
6. Wait for transcription

---

## Common Issues

### "No module named 'faster_whisper'"
- Run: `python -m pip install faster-whisper`

### "Port 8000 already in use"
- Another program is using port 8000
- Stop it or change backend port in .env

### "npm not found"
- Install Node.js from https://nodejs.org/
- Restart PowerShell after installation

### Backend starts but crashes
- Check the error message in PowerShell
- Likely missing a dependency
- Install it with: `python -m pip install <package-name>`

---

## Manual Installation Alternative

If automatic installation has issues, install packages one at a time:

```powershell
python -m pip install fastapi
python -m pip install "uvicorn[standard]"
python -m pip install sqlalchemy
python -m pip install pydantic
python -m pip install pydantic-settings
python -m pip install python-dotenv
python -m pip install structlog
# ... repeat for each package
```

---

## Stopping the Application

1. In backend window: Press `Ctrl+C`
2. In frontend window: Press `Ctrl+C`

---

**Need help? Check the error messages in PowerShell windows!**
