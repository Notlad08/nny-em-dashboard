# NNY Emergency Dashboard

A comprehensive system for monitoring, ingesting, and managing emergency communications data from SDRtrunk radio systems.

## Features
- Ingestion of radio calls from SDRtrunk (audio chunks)
- Self-hosted Whisper.cpp transcription pipeline
- Real-time incident detection and tracking
- Unit response tracking
- Address extraction
- Incident mapping and timeline
- External data integration (weather, outages, etc.)

## Architecture
- **Backend**: Python FastAPI with WebSocket support
- **Database**: PostgreSQL + TimescaleDB
- **Queue**: Redis (Celery + Pub/Sub)
- **Transcription**: Whisper.cpp (self-hosted, CPU-optimized)
- **Frontend**: React + Leaflet

## Quick Start (Local Development)
```bash
# Install dependencies
pip install -r requirements.txt

# Start services
docker-compose up -d

# Access API docs
http://localhost:8000/docs
```

## Project Structure
```
nny-em-dashboard/
├── api/                  # FastAPI server
│   ├── app/
│   │   ├── core/        # Config, logging, DB
│   │   ├── models/      # SQLAlchemy models
│   │   ├── routes/      # API endpoints
│   │   └── workers/     # Celery tasks
│   ├── Dockerfile
│   └── requirements.txt
├── ingestion/            # SDRtrunk ingestion worker
│   ├── app/
│   │   ├── core/
│   │   ├── handlers/
│   │   └── workers/
│   ├── Dockerfile
│   └── requirements.txt
├── transcription/        # Whisper.cpp worker
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   └── workers/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # React app
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── Makefile              # Development scripts
```

## Deployment
1. Build local prototype
2. Test all components
3. Deploy to VM (Ubuntu 26.04)
4. Configure systemd services

## Tech Stack
- Python 3.11+
- FastAPI
- SQLAlchemy
- Celery + Redis
- Whisper.cpp
- PostgreSQL + TimescaleDB
- React

## License
MIT
