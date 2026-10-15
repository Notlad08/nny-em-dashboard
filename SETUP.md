# NNY Emergency Dashboard - Development Setup

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Environment File
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Set Up Database
```bash
# Start PostgreSQL
docker run -d \
  --name nny_em_pg \
  -e POSTGRES_DB=nny_em_dashboard \
  -e POSTGRES_USER=emdash \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  timescale/postgres:16-latest

# Wait 10 seconds for DB to initialize
sleep 10

# Run migrations
docker run --rm \
  -e PGPASSWORD=your_password \
  -e DATABASE_URL=postgresql://emdash:your_password@localhost:5432/nny_em_dashboard \
  -v $(pwd)/database/schema.sql:/docker-entrypoint-initdb.d/schema.sql \
  timescale/postgres:16-latest \
  sh -c "sleep 10 && psql -U emdash -d nny_em_dashboard -f /docker-entrypoint-initdb.d/schema.sql"
```

### 4. Start Development Server
```bash
cd api
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access API Docs
```
http://localhost:8000/docs
```

## Testing

### Run Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=api --cov-report=html
```

### Run Linting
```bash
flake8 api/
isort api/
black api/
```

## Docker Development

### Start All Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f api
docker-compose logs -f ingestion
docker-compose logs -f transcription
```

### Stop Services
```bash
docker-compose down
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Ingest Audio Chunk
```bash
curl -X POST http://localhost:8000/api/v1/ingest/chunk \
  -H "Content-Type: application/json" \
  -d '{
    "stream_id": "test-stream",
    "audio_data": "base64_encoded_audio"
  }'
```

### List Incidents
```bash
curl http://localhost:8000/api/v1/incidents
```

### Create Incident
```bash
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-01T12:00:00Z",
    "units": ["Unit1", "Unit2"],
    "address": "123 Main St",
    "incident_type": "Fire",
    "transcription": "Unit1 responding to fire at 123 Main St"
  }'
```

### Register Unit
```bash
curl -X POST http://localhost:8000/api/v1/units \
  -H "Content-Type: application/json" \
  -d '{
    "unit_id": "unit-001",
    "callsign": "Engine 1"
  }'
```

## Common Issues

### Database Connection Error
```bash
# Check PostgreSQL is running
docker ps | grep nny_em_pg

# Check connection
psql -U emdash -h localhost -p 5432 -d nny_em_dashboard -c "SELECT 1;"
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Or change port in .env
API_PORT=8001
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. Configure SDRtrunk connection
2. Implement audio chunk processing
3. Set up Whisper.cpp for transcription
4. Create NLP pipeline for entity extraction
5. Build mapping visualization
6. Add authentication layer
