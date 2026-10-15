# Deployment Guide for NNY Emergency Dashboard
## Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Node.js 18+

### Setup
```bash
# Clone or navigate to project
cd nny-em-dashboard

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Build and start services
docker-compose up -d

# Wait for PostgreSQL to initialize
sleep 30

# Run database migrations
docker-compose exec pg psql -U emdash -d nny_em_dashboard -f database/schema.sql

# Access API docs
http://localhost:8000/docs
```

### Development
```bash
# Start all services
make start-dev

# Or use Makefile directly
make dev
```

### Database Setup
```bash
# Create Timescale extension
make db

# Run migrations
make migrate
```

## Production Deployment (Ubuntu VM)

### VM Setup
```bash
# Install dependencies on Ubuntu VM
sudo apt update
sudo apt install -y docker.io docker-compose git curl wget

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Clone repository
git clone <your-repo-url> /opt/em-dashboard
cd /opt/em-dashboard

# Copy environment file
scp .env.example emdash:/etc/em-dashboard/
scp .env emdash:/etc/em-dashboard/

# Or deploy via script
./deploy.sh
```

### Docker Compose on VM
```bash
# Create .env file on VM
cp .env.example /etc/em-dashboard/.env

# Build and start
docker-compose up -d

# Or use systemd service
systemctl enable nny-em-dashboard
systemctl start nny-em-dashboard
```

### Systemd Service Unit
Create `/etc/systemd/system/nny-em-dashboard.service`:
```ini
[Unit]
Description=NNY Emergency Dashboard
After=network.target postgresql.service

[Service]
Type=simple
User=emdash
Group=emdash
WorkingDirectory=/opt/em-dashboard
ExecStart=/usr/bin/docker-compose up -d
Restart=always
Environment=DATABASE_URL=postgresql://emdash:password@localhost:5432/nny_em_dashboard

[Install]
WantedBy=multi-user.target
```

### Firewall Configuration
```bash
# Allow required ports
sudo ufw allow 22  # SSH
sudo ufw allow 5432  # PostgreSQL (internal only)
sudo ufw allow 6379  # Redis (internal only)
sudo ufw allow 8000  # API
sudo ufw allow 3000  # Frontend
sudo ufw allow 80//tcp  # HTTP
sudo ufw allow 443/https  # HTTPS

# Enable firewall
sudo ufw enable
```

## Security Checklist

- [ ] Change JWT_SECRET_KEY in .env
- [ ] Change PostgreSQL password in .env
- [ ] Restrict CORS_ORIGINS in production
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Configure firewall rules
- [ ] Set up backup schedule
- [ ] Enable monitoring (Prometheus + Grafana)

## Monitoring

### Health Check Endpoints
```bash
# API health
http://your-server:8000/health

# Database health
http://your-server:5432 (via pg_isready)

# Redis health
http://your-server:6379 (redis-cli ping)
```

### Prometheus Setup
```bash
# Add to docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

# Create prometheus.yml
# Scrape API, ingestion, transcription services
```

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose logs pg

# Verify connection
docker-compose exec pg psql -U emdash -d nny_em_dashboard -c "SELECT 1;"
```

### Redis Issues
```bash
# Check Redis
docker-compose exec redis redis-cli ping

# Clear Redis cache (if needed)
docker-compose exec redis redis-cli FLUSHALL
```

### API Not Starting
```bash
# Check API logs
docker-compose logs api

# Try with verbose logging
docker-compose up -d api --log-level debug
```

## Next Steps

1. Configure SDRtrunk connection
2. Implement transcription pipeline
3. Set up external data integrations (weather, outages)
4. Add authentication (JWT/OAuth)
5. Implement frontend mapping features
6. Set up monitoring and alerts

## Support

- Documentation: See main README.md
- Issues: Create GitHub issue
- Deployment: Contact sysadmin
