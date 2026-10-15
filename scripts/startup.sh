#!/usr/bin/env python3
"""
Startup script for NNY EM Dashboard
Initializes database and starts all services
"""

import subprocess
import sys
import time
import signal
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_URL = "postgresql://emdash:emdash_secure_password_change_me@localhost:5432/nny_em_dashboard"

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n🚀 {description}")
    print(f"   {cmd}")
    print()
    subprocess.run(cmd, shell=True, check=True)

def check_database():
    """Check if PostgreSQL is running"""
    print("Checking PostgreSQL...")
    result = subprocess.run(
        "docker ps --format '{{.Names}}' | grep -q nny_em_pg && echo 'running' || echo 'not running'",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip() == "running"

def setup_database():
    """Set up PostgreSQL database"""
    print("\n📦 Setting up database...")
    
    # Create database if it doesn't exist
    run_command(
        f"docker exec -i nny_em_pg psql -U emdash -d postgres -c \"CREATE DATABASE nny_em_dashboard;\"",
        "Creating database"
    )
    
    # Create tables
    schema_file = PROJECT_ROOT / "database" / "schema.sql"
    run_command(
        f"docker exec -i nny_em_pg psql -U emdash -d nny_em_dashboard < {schema_file}",
        "Running schema migrations"
    )
    
    print("✅ Database setup complete")

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "audio", "models"]
    for dir_path in directories:
        path = PROJECT_ROOT / dir_path
        if not path.exists():
            path.mkdir()
            print(f"Created directory: {dir_path}/")

def main():
    """Main startup function"""
    print("=" * 60)
    print("NNY EM Dashboard - Startup")
    print("=" * 60)
    
    # Check if running in Docker
    if check_database():
        print("\n✅ PostgreSQL is running (Docker)")
        
        # Setup database if needed
        setup_database()
    else:
        print("\n⚠️  PostgreSQL not running in Docker")
        print("Please start with: docker-compose up -d")
        return
    
    # Create directories
    create_directories()
    
    # Show status
    print("\n" + "=" * 60)
    print("📊 Service Status")
    print("=" * 60)
    
    # Check services
    services = ["api", "ingestion", "transcription"]
    for service in services:
        result = subprocess.run(
            f"docker ps --format '{{.Names}}' | grep -q {service} && echo 'running' || echo 'stopped'",
            shell=True,
            capture_output=True,
            text=True
        )
        status = "running" if result.stdout.strip() == "running" else "stopped"
        print(f"   {service}: {status}")
    
    print()
    print("✅ Startup complete!")
    print()
    print("Access points:")
    print("   API Docs:    http://localhost:8000/docs")
    print("   Frontend:    http://localhost:3000")
    print()
    print("Run 'make health' to check all services")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during startup: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Startup interrupted")
        sys.exit(0)
