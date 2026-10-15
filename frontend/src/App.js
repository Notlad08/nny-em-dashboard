import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import './index.css';

function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/incidents" element={<Dashboard />} />
        <Route path="/units" element={<Dashboard />} />
        <Route path="/timeline" element={<Dashboard />} />
        <Route path="/settings" element={<Dashboard />} />
      </Routes>
    </div>
  );
}

export default App;
