# QuestionTrack - Project Summary

## Project Structure

```
questiontrack/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── api/               # REST API endpoints
│   │   │   ├── health.py      # Health check endpoint
│   │   │   ├── settings.py    # Settings management
│   │   │   └── transcription.py # Transcription endpoints
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py      # Settings and environment
│   │   │   └── logging.py     # Structured logging
│   │   ├── database/          # Database layer
│   │   │   └── base.py        # SQLAlchemy setup
│   │   ├── models/            # Database models
│   │   │   ├── question.py    # Question model
│   │   │   ├── setting.py     # Settings model
│   │   │   └── technical_term.py # Glossary model
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── transcription.py
│   │   │   └── settings.py
│   │   ├── services/          # Business logic
│   │   │   ├── audio_service.py       # Audio processing
│   │   │   ├── glossary_service.py    # Technical terms
│   │   │   ├── question_detector.py   # Question detection
│   │   │   ├── question_service.py    # Question CRUD
│   │   │   ├── transcription_service.py # Main pipeline
│   │   │   └── whisper_service.py     # Speech-to-text
│   │   └── main.py            # FastAPI app entry
│   ├── data/
│   │   └── technical_terms.json # Technical glossary
│   ├── tests/                 # Test suite
│   │   ├── conftest.py        # Test fixtures
│   │   ├── test_api.py        # API tests
│   │   ├── test_glossary_service.py
│   │   └── test_question_detector.py
│   ├── requirements.txt       # Python dependencies
│   ├── pytest.ini             # Test configuration
│   └── run.py                 # Application runner
│
├── frontend/                  # React TypeScript Frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   │   ├── AppShell.tsx
│   │   │   ├── AudioRecorder.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── LatestQuestions.tsx
│   │   │   ├── QuestionCard.tsx
│   │   │   ├── QuestionHistory.tsx
│   │   │   ├── SettingsPanel.tsx
│   │   │   ├── StatusIndicator.tsx
│   │   │   └── TranscriptPanel.tsx
│   │   ├── hooks/             # State management
│   │   │   └── useStore.ts    # Zustand store
│   │   ├── services/          # API client
│   │   │   └── api.ts
│   │   ├── styles/            # CSS
│   │   │   └── index.css
│   │   ├── types/             # TypeScript types
│   │   │   └── index.ts
│   │   ├── utils/             # Utilities
│   │   │   └── index.ts
│   │   ├── App.tsx            # Main app component
│   │   └── main.tsx           # Entry point
│   ├── public/                # Static assets
│   ├── package.json           # Dependencies
│   ├── tailwind.config.js     # Tailwind config
│   ├── vite.config.ts         # Vite config
│   ├── Dockerfile             # Frontend Docker
│   └── nginx.conf             # Nginx config
│
├── docker/                    # Docker configs
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── docker-compose.yml         # Docker Compose
├── Dockerfile                 # Backend Docker
└── README.md                  # Documentation

```

## Technologies Used

### Backend
- **Python 3.11+** - Programming language
- **FastAPI** - Modern web framework
- **faster-whisper** - Optimized Whisper implementation
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **structlog** - Structured logging
- **PyTorch** - ML framework for Whisper
- **librosa** - Audio processing
- **rapidfuzz** - Fuzzy string matching

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS
- **Zustand** - State management
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **Vite** - Build tool

### Infrastructure
- **Docker** - Containerization
- **Nginx** - Web server for production
- **SQLite** - Database

## Key Features Implemented

### 1. Speech-to-Text Transcription
- Whisper model integration (tiny/base/small options)
- Voice Activity Detection (VAD)
- Multiple audio format support
- Configurable compute type (CPU/GPU)

### 2. Technical Term Correction
- Configurable glossary with 100+ technical terms
- Fuzzy matching for approximate corrections
- Case-sensitive matching
- Import from file capability

### 3. Question Detection
- Pattern-based detection (question words, inversions)
- Command form recognition
- Tag question detection
- Confidence scoring

### 4. Question Management
- Create, read, delete operations
- Search functionality
- Recent questions tracking
- Full history with metadata

### 5. Professional UI
- Clean, modern design
- Responsive layout
- Dark mode support
- Accessibility features
- Real-time status indicators

### 6. Configuration & Settings
- Environment-based configuration
- Persistent user settings
- Model selection
- Customizable question count

## How to Install

### Prerequisites
- Python 3.11+
- Node.js 18+
- ffmpeg

### Quick Start

1. **Clone and Setup Backend**:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python run.py
```

2. **Setup Frontend**:
```bash
cd frontend
npm install
npm run dev
```

3. **Access Application**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## How to Run with Docker

```bash
# Build and start all services
docker compose up --build

# Run in background
docker compose up -d
```

## How to Configure Whisper

Edit `.env` file:
```env
STT_MODEL=base      # tiny/base/small
STT_DEVICE=cpu      # cpu/cuda
STT_COMPUTE_TYPE=int8  # int8/float16/float32
```

### Model Comparison

| Model | Size | RAM | Speed | Accuracy |
|-------|------|-----|-------|----------|
| tiny  | 39MB | ~1GB | Fastest | Good for real-time |
| base  | 74MB | ~1GB | Fast | Balanced |
| small | 244MB | ~2GB | Moderate | Best quality |

## How to Deploy

### Backend Deployment

**Option 1: Docker (Recommended)**
```bash
docker compose up -d
```

**Option 2: Manual**
```bash
# Set production environment
export API_RELOAD=false
export LOG_LEVEL=WARNING

# Run with production server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment

```bash
cd frontend
npm run build

# Deploy dist/ folder to any static host
```

### GPU Deployment

For GPU acceleration:
```env
STT_DEVICE=cuda
STT_COMPUTE_TYPE=float16
```

Update docker-compose.yml to enable GPU access.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STT_MODEL` | base | Whisper model size |
| `STT_DEVICE` | cpu | Compute device |
| `STT_COMPUTE_TYPE` | int8 | Quantization type |
| `DATABASE_URL` | sqlite:///./data/questiontrack.db | Database connection |
| `API_HOST` | 0.0.0.0 | API host |
| `API_PORT` | 8000 | API port |
| `MAX_AUDIO_FILE_SIZE` | 52428800 | Max upload (50MB) |
| `LOG_LEVEL` | INFO | Logging level |

## Testing Instructions

### Backend Tests
```bash
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html
```

### Test Coverage
- API endpoints
- Question detection
- Technical term correction
- Database operations

## Known Limitations

1. **Language**: Currently supports English only
2. **Real-time**: Audio must be complete before processing
3. **Model Loading**: Initial load takes 30-60 seconds
4. **Speaker ID**: No speaker identification
5. **Meeting Integration**: Does not integrate with video conferencing apps (by design for privacy)

## Future Improvements

### Planned Features
- Real-time streaming transcription
- Multi-language support
- Speaker diarization
- Custom project vocabularies
- API authentication
- Webhook notifications
- Cloud storage integration
- Team collaboration

### Architecture Evolution
- RAG-based technical correction
- Vector database for semantic search
- WebSocket real-time updates
- Microservices architecture
- Horizontal scaling support

## Project Status

✅ **Production Ready**

All core features are implemented and tested:
- [x] Speech-to-text transcription
- [x] Technical term correction
- [x] Question detection
- [x] Question history
- [x] Search functionality
- [x] Settings management
- [x] Dark mode
- [x] Docker deployment
- [x] API documentation
- [x] Test suite

## Development Notes

### Key Architectural Decisions

1. **Whisper Singleton**: Model loaded once and reused for performance
2. **Separate Raw/Corrected Text**: Preserve original transcription
3. **SQLite for Portability**: Easy setup, can upgrade to PostgreSQL
4. **Zustand over Redux**: Simpler state management
5. **FastAPI + Pydantic**: Automatic validation and documentation

### Design Philosophy

- Professional, clean UI (no emojis, no unnecessary decorations)
- Privacy-first (no meeting app injection)
- Modular architecture (easy to extend)
- Production-ready code quality
- Comprehensive error handling

## Credits

Built with modern best practices and production-quality standards.

---

**For detailed documentation, see README.md**
