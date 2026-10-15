# Native Python Setup for NNY EM Dashboard
# No Docker required - runs directly on Windows

## Quick Start

### 1. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Create Environment Variables
```powershell
# Create .env file
New-Item -Path ".env" -ItemType File -Force

# Edit with:
notepad .env
# Copy content from .env.example into it
```

### 3. Set Up PostgreSQL
```powershell
# Install PostgreSQL (if not already installed)
# Download from: https://www.postgresql.org/download/windows/
# Or use Docker for PostgreSQL only

# Or use SQLite for development (simpler)
# Edit api/app/core/db.py to use SQLite
```

### 4. Run the API Server
```powershell
cd api
python app/main.py
```

Access: http://localhost:8000/docs

## Alternative: Docker Desktop Setup

### Install Docker Desktop
1. Download: https://www.docker.com/products/docker-desktop/
2. Install and start Docker Desktop
3. Wait for Docker icon to appear in system tray

### Verify Docker is Running
```powershell
docker --version
docker ps
```

### Start Services
```powershell
docker-compose up -d
```

## Recommended Setup for Windows

### Use Docker for Database Only
```powershell
# Start PostgreSQL and Redis only
docker run -d `
  --name nny_em_pg `
  -e POSTGRES_DB=nny_em_dashboard `
  -e POSTGRES_USER=emdash `
  -e POSTGRES_PASSWORD=emdash_password `
  -p 5432:5432 `
  timescale/postgres:16-latest

docker run -d `
  --name nny_em_redis `
  -p 6379:6379 `
  redis:7-alpine

# Wait for DB to initialize
Start-Sleep -Seconds 10

# Run migrations
docker exec -i nny_em_pg psql -U emdash -d nny_em_dashboard -f database/schema.sql
```

### Run API and Frontend Natively
```powershell
# Terminal 1: API Server
cd api
python app/main.py

# Terminal 2: Frontend
cd frontend
npm install
npm start
```

## Migration Path to VM

1. Develop locally with native Python
2. Test all features
3. Deploy to Ubuntu VM with Docker
4. Use native Python on VM if preferred

## Current Setup Status

- [x] API server code (native Python)
- [x] Ingestion worker code (native Python)
- [x] Transcription worker code (native Python)
- [x] Frontend code (native Node.js)
- [ ] PostgreSQL (use Docker or install on Windows)
- [ ] Redis (use Docker or install on Windows)

## For This Session (Windows)

Let's run PostgreSQL and Redis via Docker containers, then run API/frontend natively:

```powershell
# Start database services
docker run -d --name nny_em_pg -e POSTGRES_DB=nny_em_dashboard -e POSTGRES_USER=emdash -e POSTGRES_PASSWORD=emdash_secure -p 5432:5432 timescale/postgres:16-latest

docker run -d --name nny_em_redis -p 6379:6379 redis:7-alpine

# Wait for DB
Start-Sleep -Seconds 10

# Run migrations
docker exec -i nny_em_pg psql -U emdash -d nny_em_dashboard -f database/schema.sql

# Run API server
cd api
python app/main.py
```

## Next Steps

1. Start Docker Desktop (if not running)
2. Run the database containers above
3. Run migrations
4. Start API server
5. Access http://localhost:8000/docs

Which approach do you prefer? (Docker for all, or native Python with Docker for DB only)
