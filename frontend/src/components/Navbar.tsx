import React from 'react';
import { Menu, X, Settings, LogOut } from 'lucide-react';
import { useState } from 'react';

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-primary-600">💰 Finance PWA</h1>
          </div>
          
          <div className="hidden md:flex items-center space-x-8">
            <a href="/" className="hover:text-primary-600">Dashboard</a>
            <a href="/transactions" className="hover:text-primary-600">Transactions</a>
            <a href="/budgets" className="hover:text-primary-600">Budgets</a>
            <a href="/forecasts" className="hover:text-primary-600">Forecasts</a>
            <a href="/analytics" className="hover:text-primary-600">Analytics</a>
            <a href="/settings" className="text-gray-600"><Settings size={20} /></a>
          </div>

          <button
            className="md:hidden"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {isOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <a href="/" className="block hover:text-primary-600">Dashboard</a>
            <a href="/transactions" className="block hover:text-primary-600">Transactions</a>
            <a href="/budgets" className="block hover:text-primary-600">Budgets</a>
            <a href="/forecasts" className="block hover:text-primary-600">Forecasts</a>
            <a href="/analytics" className="block hover:text-primary-600">Analytics</a>
            <a href="/settings" className="block hover:text-primary-600">Settings</a>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
