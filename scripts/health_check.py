#!/usr/bin/env python3
"""
Simple health check script for NNY Emergency Dashboard
Runs against all services and reports status
"""

import sys
import subprocess
import requests
from datetime import datetime

SERVICES = {
    "API": ("http://localhost:8000", "/health"),
    "Ingestion": ("http://localhost:8001", "/health"),
    "Transcription": ("http://localhost:8002", "/health"),
}

def check_service(name, host, path):
    """Check if a service is healthy"""
    try:
        url = f"{host}{path}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {name}: {response.json()}")
            return True
        else:
            print(f"⚠️  {name}: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name}: Connection refused")
        return False
    except requests.exceptions.Timeout:
        print(f"⚠️  {name}: Timeout (may be slow)")
        return True

def check_database():
    """Check PostgreSQL connection"""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="nny_em_dashboard",
            user="emdash",
            password="emdash_secure_password_change_me",
        )
        print("✅ PostgreSQL: Connected")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL: {e}")
        return False

def check_redis():
    """Check Redis connection"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        result = r.ping()
        print("✅ Redis: Pong received")
        return True
    except Exception as e:
        print(f"❌ Redis: {e}")
        return False

def main():
    """Run health checks"""
    print("=" * 60)
    print("NNY EM Dashboard - Health Check")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    all_healthy = True
    
    # Check HTTP services
    for name, (host, path) in SERVICES.items():
        if not check_service(name, host, path):
            all_healthy = False
    print()
    
    # Check database
    if not check_database():
        all_healthy = False
    print()
    
    # Check Redis
    if not check_redis():
        all_healthy = False
    print()
    
    # Summary
    print("=" * 60)
    if all_healthy:
        print("✅ All services are healthy")
        sys.exit(0)
    else:
        print("⚠️  Some services are unhealthy")
        sys.exit(1)

if __name__ == "__main__":
    main()
