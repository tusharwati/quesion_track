# Install and Run QuestionTrack

## Quick Installation

Since you already have Python installed, let's install the packages directly:

### Step 1: Install Backend Dependencies

Open PowerShell and navigate to the backend directory, then run:

```powershell
pip install --user faster-whisper==1.0.0 torch==2.1.1 torchaudio==2.1.1 librosa==0.10.1 soundfile==0.12.1 webrtcvad==2.0.10 sqlalchemy==2.0.23 alembic==1.12.1 rapidfuzz==3.5.2 textblob==0.17.1 python-dotenv==1.0.0 aiofiles==23.2.1 httpx==0.25.2 pytest==7.4.3 pytest-asyncio==0.21.1 structlog==23.2.0 PyPDF2==3.0.1 pydantic-settings==2.1.0
```

**Note**: This will take 5-10 minutes as it downloads PyTorch (~2GB) and Whisper models.

### Step 2: Start Backend

After installation completes:

```powershell
cd backend
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
pip install --user torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

Then install the rest:

```powershell
pip install --user faster-whisper librosa soundfile webrtcvad sqlalchemy alembic rapidfuzz textblob python-dotenv aiofiles httpx pytest pytest-asyncio structlog PyPDF2 pydantic-settings
```

---

## Testing Without Full Installation

If you want to test the frontend without backend:

1. Skip backend setup
2. Install and run frontend only
3. The UI will load (transcription won't work until backend is running)

---

## Verify Installation

Check if packages are installed:

```powershell
pip list | Select-String -Pattern "faster-whisper"
pip list | Select-String -Pattern "torch"
pip list | Select-String -Pattern "fastapi"
```

You should see version numbers for each.

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
- Run: `pip install --user faster-whisper`

### "Port 8000 already in use"
- Another program is using port 8000
- Stop it or change backend port in .env

### "npm not found"
- Install Node.js from https://nodejs.org/
- Restart PowerShell after installation

### Backend starts but crashes
- Check the error message in PowerShell
- Likely missing a dependency
- Install it with: `pip install --user <package-name>`

---

## Manual Installation Alternative

If automatic installation has issues, install packages one at a time:

```powershell
pip install --user fastapi
pip install --user uvicorn[standard]
pip install --user sqlalchemy
pip install --user pydantic
pip install --user pydantic-settings
pip install --user python-dotenv
pip install --user structlog
# ... repeat for each package
```

---

## Stopping the Application

1. In backend window: Press `Ctrl+C`
2. In frontend window: Press `Ctrl+C`

---

**Need help? Check the error messages in PowerShell windows!**
