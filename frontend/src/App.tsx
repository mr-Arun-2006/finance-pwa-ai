import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Budgets from './pages/Budgets';
import Forecasts from './pages/Forecasts';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import Toaster from 'react-hot-toast';

const App: React.FC = () => {
  return (
    <Router>
      <div className="flex flex-col h-screen bg-gray-50">
        <Navbar />
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/budgets" element={<Budgets />} />
            <Route path="/forecasts" element={<Forecasts />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
      <Toaster position="top-right" />
    </Router>
  );
};

export default App;
