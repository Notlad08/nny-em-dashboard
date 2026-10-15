-- Drop existing tables
DROP TABLE IF EXISTS incidents CASCADE;
DROP TABLE IF EXISTS timeline CASCADE;
DROP TABLE IF EXISTS units CASCADE;
DROP TABLE IF EXISTS weather_data CASCADE;
DROP TABLE IF EXISTS outage_data CASCADE;
DROP TABLE IF EXISTS ingestion_metadata CASCADE;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Incidents table (core)
CREATE TABLE incidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    units TEXT[],
    address TEXT,
    incident_type TEXT,
    location TEXT,
    transcription TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create index for timestamp-based queries
CREATE INDEX ON incidents (timestamp DESC);

-- Incident timeline
CREATE TABLE timeline (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_id UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type TEXT NOT NULL,
    message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX ON timeline (incident_id, timestamp DESC);

-- Units tracking
CREATE TABLE units (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unit_id TEXT UNIQUE NOT NULL,
    callsign TEXT,
    status TEXT DEFAULT 'available',
    last_known_location TEXT,
    last_transmission TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ON units (unit_id);
CREATE INDEX ON units (status);

-- External data - Weather
CREATE TABLE weather_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source TEXT NOT NULL,
    data JSONB NOT NULL,
    location TEXT
);

CREATE INDEX ON weather_data (timestamp DESC);

-- External data - Outages
CREATE TABLE outage_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source TEXT NOT NULL,
    data JSONB NOT NULL,
    location TEXT
);

CREATE INDEX ON outage_data (timestamp DESC);

-- Ingestion metadata (for tracking chunks)
CREATE TABLE ingestion_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stream_id TEXT NOT NULL,
    chunk_start TIMESTAMPTZ NOT NULL,
    chunk_end TIMESTAMPTZ NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    transcription_status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ON ingestion_metadata (stream_id);
CREATE INDEX ON ingestion_metadata (processed);

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for automatic timestamp updates
CREATE TRIGGER set_updated_at_incidents BEFORE UPDATE ON incidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER set_updated_at_units BEFORE UPDATE ON units
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
