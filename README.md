# QuestionTrack

**Professional Speech-to-Text Question Tracking Application**

QuestionTrack is a production-ready application that transcribes speech, detects questions, and maintains a searchable history with technical term correction.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)

---

## Features

### Core Capabilities

- **Speech-to-Text Transcription** - Powered by faster-whisper with multiple model options
- **Technical Term Correction** - Automatically corrects technical terms (YOLO, ESP32, Python, etc.)
- **Question Detection** - Identifies questions using linguistic patterns
- **Question History** - Searchable database of all detected questions
- **Real-time Status** - Live system status and model loading indicators

### User Interface

- Professional, clean design
- Responsive layout (desktop, tablet, mobile)
- Dark mode support
- Accessible controls with keyboard navigation
- Real-time recording status

### Audio Support

- Microphone recording
- File upload (WAV, MP3, FLAC, OGG, M4A, WebM)
- Configurable Whisper models (tiny, base, small)
- Voice Activity Detection (VAD)

---

## Architecture

```
questiontrack/
├── frontend/           # React + TypeScript + Tailwind CSS
│   ├── src/
│   │   ├── components/ # UI components
│   │   ├── hooks/      # State management (Zustand)
│   │   ├── services/   # API client
│   │   ├── types/      # TypeScript types
│   │   └── utils/      # Utilities
│   └── ...
├── backend/            # Python + FastAPI
│   ├── app/
│   │   ├── api/        # REST endpoints
│   │   ├── services/   # Business logic
│   │   ├── models/     # Database models
│   │   ├── schemas/    # Pydantic schemas
│   │   ├── core/       # Configuration
│   │   └── database/   # SQLite setup
│   ├── tests/          # Pytest tests
│   └── data/           # Technical terms glossary
└── docker/             # Docker configuration
```

### Technology Stack

**Frontend**
- React 18
- TypeScript
- Tailwind CSS
- Zustand (state management)
- Axios (HTTP client)
- Lucide React (icons)

**Backend**
- Python 3.11+
- FastAPI
- faster-whisper (speech recognition)
- SQLAlchemy (ORM)
- Pydantic (validation)
- structlog (logging)

**Database**
- SQLite (default)

---

## Installation

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- ffmpeg (for audio processing)
- Git

### Clone Repository

```bash
git clone https://github.com/yourusername/questiontrack.git
cd questiontrack
```

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment file:
```bash
cp ../.env.example ../.env
```

4. Run the backend:
```bash
python run.py
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Speech-to-Text Configuration
STT_MODEL=base              # Options: tiny, base, small
STT_DEVICE=cpu              # Options: cpu, cuda
STT_COMPUTE_TYPE=int8       # Options: int8, float16, float32

# Database
DATABASE_URL=sqlite:///./data/questiontrack.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Security
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Audio Processing
MAX_AUDIO_FILE_SIZE=52428800    # 50MB
UPLOAD_DIR=./uploads

# Logging
LOG_LEVEL=INFO
```

### Whisper Models

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny  | 39MB | Fastest | Lowest |
| base  | 74MB | Fast | Good |
| small | 244MB | Moderate | Best |

**Recommendation**: Use `base` for most use cases. Use `tiny` for real-time transcription. Use `small` for accuracy-critical applications.

---

## Docker Deployment

### Build and Run

```bash
# Build and start all services
docker compose up --build

# Run in detached mode
docker compose up -d
```

### Access

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/api/docs`

### Docker Compose Configuration

The `docker-compose.yml` file includes:
- Backend service with Whisper model support
- Frontend service with Nginx
- Volume mounts for data persistence
- Health checks

---

## API Documentation

### Endpoints

#### Health Check

```http
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_connected": true,
  "version": "1.0.0"
}
```

#### Transcribe Audio

```http
POST /api/transcribe
Content-Type: multipart/form-data

file: <audio_file>
```

Response:
```json
{
  "raw_text": "how does your yolo model detect object and what data set you use",
  "corrected_text": "How does your YOLO model detect objects, and what dataset did you use?",
  "is_question": true,
  "confidence": 0.94,
  "processing_time": 0.82
}
```

#### List Questions

```http
GET /api/questions?skip=0&limit=100&search=YOLO
```

Response:
```json
{
  "questions": [
    {
      "id": 1,
      "raw_text": "how does your yolo model work",
      "corrected_text": "How does your YOLO model work?",
      "is_question": true,
      "confidence": 0.92,
      "processing_time": 0.78,
      "created_at": "2026-10-24T10:30:00"
    }
  ],
  "total": 1
}
```

#### Get Recent Questions

```http
GET /api/questions/recent?count=2
```

#### Delete Question

```http
DELETE /api/questions/{id}
```

#### Clear All Questions

```http
DELETE /api/questions
```

#### Get Settings

```http
GET /api/settings
```

#### Update Settings

```http
PUT /api/settings
Content-Type: application/json

{
  "stt_model": "small",
  "recent_question_count": 3
}
```

---

## Testing

### Backend Tests

```bash
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm run test
```

### Test Coverage

Backend tests cover:
- API endpoints
- Question detection
- Technical term correction
- Database operations
- Error handling

---

## Production Deployment

### Backend Deployment

#### Option 1: Docker (Recommended)

```bash
docker compose -f docker-compose.prod.yml up -d
```

#### Option 2: Manual

1. Set production environment variables:
```env
STT_DEVICE=cpu
API_RELOAD=false
LOG_LEVEL=WARNING
```

2. Use production WSGI server:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment

1. Build production bundle:
```bash
cd frontend
npm run build
```

2. Serve with any static file server (Nginx, Apache, CDN)

### GPU Support

For GPU-accelerated transcription:

1. Use NVIDIA Docker runtime
2. Set environment:
```env
STT_DEVICE=cuda
STT_COMPUTE_TYPE=float16
```

3. Update docker-compose.yml:
```yaml
services:
  backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

## Limitations

### Current Limitations

1. **Language Support**: Currently optimized for English only
2. **Model Loading**: Whisper model loads on startup (can take 30-60 seconds)
3. **GPU Support**: Requires manual configuration for CUDA
4. **Real-time Streaming**: Not yet supported (audio must be complete before processing)
5. **Speaker Identification**: Not supported in current version
6. **Meeting Integration**: Does not integrate with Zoom/Teams/Meet (by design for privacy)

### Performance Considerations

- **CPU Mode**: Suitable for development and light usage
- **GPU Mode**: Recommended for production deployments
- **Model Size**: Larger models = better accuracy but slower
- **Audio Length**: Processing time scales with audio duration

---

## Future Improvements

### Planned Features

- [ ] Real-time streaming transcription
- [ ] Multi-language support
- [ ] Speaker diarization
- [ ] Meeting transcript import
- [ ] Custom vocabulary per project
- [ ] REST API authentication
- [ ] Webhook notifications
- [ ] Cloud storage integration
- [ ] Team collaboration features

### Architecture Improvements

- [ ] RAG-based technical term correction
- [ ] Vector database for semantic search
- [ ] WebSocket for real-time updates
- [ ] Microservices architecture option
- [ ] Horizontal scaling support

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Follow Airbnb style guide for TypeScript/React
- Write tests for new features
- Update documentation
- Keep PRs focused and atomic

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Optimized Whisper implementation
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/questiontrack/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/questiontrack/discussions)

---

**Built with care for developers, by developers.**
