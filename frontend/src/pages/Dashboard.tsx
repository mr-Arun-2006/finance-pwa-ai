import React from 'react';
import StatCard from '../components/StatCard';
import FinancialChart from '../components/FinancialChart';

const Dashboard: React.FC = () => {
  const mockData = [
    { name: 'Jan', value: 4000 },
    { name: 'Feb', value: 3000 },
    { name: 'Mar', value: 2000 },
    { name: 'Apr', value: 2780 },
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Balance" value="$12,450" icon="💰" trend="+5.2%" />
        <StatCard title="Monthly Spending" value="$3,240" icon="📊" trend="-2.1%" />
        <StatCard title="Savings Goal" value="$8,000" icon="🎯" trend="+12.5%" />
        <StatCard title="Alerts" value="3" icon="🔔" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <FinancialChart data={mockData} title="Monthly Spending" />
        <FinancialChart data={mockData} title="Income vs Spending" />
      </div>
    </div>
  );
};

export default Dashboard;
