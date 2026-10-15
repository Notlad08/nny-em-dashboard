# Getting Started - NNY Emergency Dashboard

## Quick Start (5 minutes)

### Prerequisites
- Python 3.11+ installed
- Docker Desktop running
- Git (for cloning)

### Step 1: Clone the Project
```bash
cd C:\Users\dalto\projects
git clone <your-repo-url> nny-em-dashboard
cd nny-em-dashboard
```

### Step 2: Create Environment File
```bash
copy .env.example .env
```

Edit `.env`:
```env
# Change these!
JWT_SECRET_KEY=your-secure-random-key
POSTGRES_PASSWORD=your-secure-password
```

### Step 3: Start Services
```bash
docker-compose up -d
```

### Step 4: Wait for Database
```bash
# Wait 10 seconds for PostgreSQL to initialize
timeout /t 10 >nul
```

### Step 5: Run Migrations
```bash
docker exec -i nny_em_pg psql -U emdash -d postgres -c "CREATE DATABASE nny_em_dashboard;"
docker exec -i nny_em_pg psql -U emdash -d nny_em_dashboard -f database/schema.sql
```

### Step 6: Access the System
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000 (will show login)
- **Health Check**: http://localhost:8000/health

## Development Mode

### Using Makefile (Recommended)
```bash
make start-dev
```

This starts all services in detached mode.

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f ingestion
docker-compose logs -f transcription
```

### Stop Services
```bash
docker-compose down
```

## Testing the API

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Create Test Incident
```bash
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T14:30:00Z",
    "units": ["Engine 1", "Engine 2", "Medic 1"],
    "address": "123 Main St, Jefferson County, NY",
    "incident_type": "Vehicle Accident",
    "transcription": "Engine 1 and 2 responding to vehicle accident at 123 Main St. Multiple casualties reported. Medic 1 on scene."
  }'
```

### Register Test Unit
```bash
curl -X POST http://localhost:8000/api/v1/units \
  -H "Content-Type: application/json" \
  -d '{
    "unit_id": "engine-001",
    "callsign": "Engine 1"
  }'
```

## Next Steps

### 1. Configure SDRtrunk
Edit `.env` with your SDRtrunk connection details:
```env
SDRTRUNK_HOST=your-sdrrtrunk-host
SDRTRUNK_PORT=8000
SDRTRUNK_STREAM_URL=tcp://your-sdrrtrunk-host:8000/stream
```

### 2. Download Whisper Model
```bash
cd models
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.ggml -O ggml-base.en.ggml
cd ..
```

### 3. Test Transcription
```bash
# Start transcription worker
docker-compose up -d transcription

# Upload a test audio file
# (You'll need to implement the upload endpoint first)
```

### 4. Build Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

## Common Issues

### "Port already in use"
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Kill the process or change API_PORT in .env
```

### "Database connection refused"
```bash
# Check PostgreSQL is running
docker ps | grep nny_em_pg

# Check database exists
docker exec nny_em_pg psql -U postgres -c "\l"
```

### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "CORS error in browser"
Edit `.env`:
```env
CORS_ORIGINS=http://localhost:3000
```

## Project Documentation

- **README.md**: Project overview and features
- **ARCHITECTURE.md**: System design and component details
- **DEPLOYMENT.md**: Production deployment guide
- **SETUP.md**: Detailed setup instructions
- **PROJECT.md**: Project summary and roadmap

## Support

- Check logs: `docker-compose logs -f <service>`
- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`
- Database: `docker exec nny_em_pg psql -U emdash -d nny_em_dashboard -c "SELECT * FROM incidents LIMIT 5;"`

## What to Build First

1. **Core Pipeline** (Priority: High)
   - Connect ingestion worker to SDRtrunk
   - Implement audio chunk storage
   - Integrate Whisper.cpp for transcription
   - Build NLP entity extraction
   - Create database records

2. **Mapping** (Priority: Medium)
   - Geocode addresses to coordinates
   - Integrate Leaflet map
   - Display incident locations

3. **External Data** (Priority: Medium)
   - NOAA weather API integration
   - Outage data integration
   - Map overlay

4. **Production Hardening** (Priority: High)
   - Authentication (JWT)
   - HTTPS/SSL
   - Monitoring (Prometheus)
   - Backup strategy

Happy building! 🚀
