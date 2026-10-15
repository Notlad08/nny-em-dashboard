import React from 'react';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import './App.css';

const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = React.useState(
    !!localStorage.getItem('auth_token'),
  );

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    setIsAuthenticated(false);
  };

  return (
    <div className="app">
      {isAuthenticated ? <Dashboard /> : <Login />}
    </div>
  );
};

export default App;
