import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../config/api';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeIncidents, setActiveIncidents] = useState<any[]>([]);
  const [unitCounts, setUnitCounts] = useState({ available: 0, active: 0 });

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    try {
      const response = await api.get('/incidents');
      setIncidents(response.data.incidents);
      setActiveIncidents(response.data.incidents.filter((i: any) => i.status === 'active'));
    } catch (error: any) {
      console.error('Failed to fetch incidents:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUnits = async () => {
    try {
      const response = await api.get('/units');
      setUnitCounts({
        available: response.data.units.filter((u: any) => u.status === 'available').length,
        active: response.data.units.filter((u: any) => u.status === 'active').length,
      });
    } catch (error: any) {
      console.error('Failed to fetch units:', error);
    }
  };

  useEffect(() => {
    fetchUnits();
  }, []);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <div className="nav-title">NNY Emergency Dashboard</div>
        <div className="nav-links">
          <Link to="/incidents">Incidents</Link>
          <Link to="/units">Units</Link>
          <Link to="/timeline">Timeline</Link>
          <Link to="/settings">Settings</Link>
          <Link to="/logout" className="logout-link">Logout</Link>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header">
          <h1>Active Incidents</h1>
          <span className="incident-count">{activeIncidents.length} active</span>
        </div>

        <div className="incidents-grid">
          {activeIncidents.length === 0 ? (
            <div className="no-incidents">
              <h2>No active incidents</h2>
              <p>Radio traffic is being monitored. Incidents will appear here when detected.</p>
            </div>
          ) : (
            activeIncidents.map((incident) => (
              <div key={incident.id} className="incident-card">
                <div className="incident-header">
                  <h3>{incident.incident_type || 'Unknown Incident'}</h3>
                  <span className="status-badge active">Active</span>
                </div>
                <div className="incident-info">
                  <p><strong>Location:</strong> {incident.address || 'Unknown'}</p>
                  <p><strong>Units:</strong> {incident.units?.join(', ') || 'None'}</p>
                  <p><strong>Timestamp:</strong> {new Date(incident.timestamp).toLocaleTimeString()}</p>
                </div>
                <div className="incident-actions">
                  <Link to={`/incidents/${incident.id}`}>View Details</Link>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
