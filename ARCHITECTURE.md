# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         NNY EM Dashboard                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │   SDRtrunk   │───▶│ Ingestion    │───▶│ PostgreSQL/       │  │
│  │   Stream     │    │  Worker      │    │  TimescaleDB      │  │
│  └──────────────┘    │              │    │  (incidents,      │  │
│                      │              │    │   units, timeline)│  │
│                      └──────────────┘    └──────────────────┘  │
│                               │                                   │
│                               ▼                                   │
│                      ┌──────────────────────┐                  │
│                      │  Whisper.cpp Worker  │                  │
│                      │  (Audio Chunks)      │                  │
│                      └──────────────────────┘                  │
│                               │                                   │
│                               ▼                                   │
│                      ┌──────────────────────┐                  │
│                      │    Celery Tasks      │                  │
│                      │  (Mapping, Timeline, │                  │
│                      │   External Data)     │                  │
│                      └──────────────────────┘                  │
│                               │                                   │
│                               ▼                                   │
│                      ┌──────────────────────┐                  │
│                      │  FastAPI Server      │                  │
│                      │  (REST + WebSocket)  │                  │
│                      └──────────────────────┘                  │
│                               │                                   │
│                               ▼                                   │
│                      ┌──────────────────────┐                  │
│                      │  React Frontend      │                  │
│                      │  (Real-time Dashboard)                   │
│                      └──────────────────────┘                  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ External Data Sources                                       │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ • Weather (NOAA Radar API)                                  │ │
│  │ • Power Outages (PSC Outage API)                            │ │
│  │ • Telecom Outages (Provider APIs)                            │ │
│  │ • Traffic Cameras                                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Ingestion Worker (Port 8001)
- Connects to SDRtrunk WebSocket stream
- Buffers audio data into 30-second chunks
- Stores chunks in storage
- Sends chunks to transcription worker via Redis queue

### Transcription Worker (Port 8002)
- Receives audio chunks from ingestion worker
- Processes with Whisper.cpp (CPU-optimized)
- Generates transcription text
- Saves to storage for later processing

### NLP/Extraction Worker (Port 8003)
- Receives transcriptions from transcription worker
- Extracts entities using NLP models:
  - Unit identifiers
  - Addresses
  - Incident types
  - Timestamps
- Creates incident records in database
- Creates timeline events

### API Server (Port 8000)
- REST API for CRUD operations
- WebSocket for real-time updates
- Authentication (JWT)
- External data integration endpoints

### Frontend (Port 3000)
- Real-time incident display
- Unit tracking
- Mapping visualization (Leaflet)
- Timeline viewer
- External data overlay

## Data Flow

### 1. Ingestion Pipeline
```
SDRtrunk → Ingestion Worker → Storage → Transcription Worker
```

### 2. Transcription Pipeline
```
Ingestion → Transcription Worker → NLP Worker → Database
```

### 3. External Data Pipeline
```
API Server → External APIs → Database Snapshots
```

## Technology Stack

| Component | Technology | Reason |
|-----------|------------|--------|
| Backend | Python 3.11 | Rich ML/AI ecosystem |
| Web Framework | FastAPI | Async, auto-docs, WebSocket support |
| Database | PostgreSQL + TimescaleDB | Time-series + geospatial |
| Queue | Redis | Pub/Sub + message broker |
| Transcription | Whisper.cpp | Self-hosted, CPU-optimized |
| Frontend | React + TypeScript | Modern, component-based |
| Mapping | Leaflet | Open-source, no API costs |
| Auth | JWT | Stateless, simple |

## Performance Considerations

### Audio Chunking
- **Chunk Size**: 30 seconds (480KB at 16kHz mono)
- **Buffering**: 5-10 seconds before processing (misses nothing)
- **Processing**: ~10-15 seconds per chunk (Whisper.cpp on CPU)

### Database Scaling
- **Timescale Hypertables**: Automatic partitioning for time-series
- **Indexes**: GIST for geospatial, B-tree for timestamps
- **Connection Pooling**: SQLAlchemy asyncpg pool

### Real-time Updates
- **WebSocket**: Push notifications for new incidents
- **Redis Pub/Sub**: Cross-service event propagation
- **Polling Fallback**: 5-second interval for compatibility

## Security Model

### Authentication
- JWT tokens (30-minute expiry)
- Simple username/password (todo: replace with OAuth/LDAP)
- Token stored in localStorage (todo: move to httpOnly cookie)

### Authorization
- Role-based access control (todo: implement)
- Admin: full access
- Operator: incident management
- Viewer: read-only

### Data Protection
- PostgreSQL password in environment variables
- JWT secret in environment variables
- CORS restricted in production
- No sensitive data in logs

## Deployment Strategy

### Phase 1: Local Prototype
- Docker Compose on local machine
- All services containerized
- Local PostgreSQL and Redis
- Local Whisper.cpp models

### Phase 2: VM Deployment
- Move to Ubuntu VM
- Systemd services for each component
- Persistent storage mounting
- SSL/TLS for API
- Firewall rules

### Phase 3: Production
- Load balancer (HAProxy/Nginx)
- Multiple API instances
- Redis cluster
- PostgreSQL with replication
- Monitoring (Prometheus + Grafana)

## Monitoring & Observability

### Health Checks
- API: `/health` endpoint
- Database: `pg_isready`
- Redis: `redis-cli ping`
- Transcription: Whisper model availability

### Metrics
- Request latency (FastAPI middleware)
- Queue depth (Redis)
- Database connections (pg_stat_activity)
- CPU/memory usage

### Logging
- Structured JSON logs
- Log aggregation (ELK/Loki)
- Error tracking (Sentry)

## Future Enhancements

1. **Real-time Alerting**: Push notifications to mobile
2. **Incident Clustering**: Group related incidents
3. **Predictive Analysis**: ML for incident prediction
4. **Live Map**: Real-time incident locations on map
5. **Chat Interface**: Real-time incident updates
6. **Report Generation**: PDF reports for incidents
7. **API Rate Limiting**: Prevent abuse
8. **Caching**: Redis cache for frequent queries
