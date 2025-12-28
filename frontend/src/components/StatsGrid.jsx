import React from 'react';

const formatCurrency = (amount) => {
  return '₹' + amount.toLocaleString('en-IN');
};

const StatsGrid = ({ financeData, updateCashBalance }) => {
  const totalInflow = financeData.receivables.reduce((sum, r) => sum + r.amount, 0);
  const totalOutflow = 
    financeData.salaries.reduce((sum, s) => sum + s.amount, 0) +
    financeData.fixed_bills.reduce((sum, b) => sum + b.amount, 0);
  
  const netPosition = financeData.cash_balance + totalInflow - totalOutflow;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div className="card p-5">
        <div className="text-gray-500 text-xs mb-2">Current Balance</div>
        <div className="flex items-center gap-2 text-2xl font-bold">
          <span>💰</span>
          <input 
            type="number" 
            value={financeData.cash_balance}
            onChange={(e) => updateCashBalance(Number(e.target.value))}
            className="border-none text-2xl font-bold w-full outline-none p-0 focus:ring-0"
          />
        </div>
      </div>

      <div className="card p-5">
        <div className="text-gray-500 text-xs mb-2">Expected Inflow</div>
        <div className="text-emerald text-2xl font-bold flex items-center gap-2">
          <span>↗️</span>
          <span>{formatCurrency(totalInflow)}</span>
        </div>
      </div>

      <div className="card p-5">
        <div className="text-gray-500 text-xs mb-2">Expected Outflow</div>
        <div className="text-rose text-2xl font-bold flex items-center gap-2">
          <span>↘️</span>
          <span>{formatCurrency(totalOutflow)}</span>
        </div>
      </div>

      <div className="card p-5">
        <div className="text-gray-500 text-xs mb-2">Net Position</div>
        <div className={`text-2xl font-bold flex items-center gap-2 ${netPosition >= 0 ? 'text-emerald' : 'text-rose'}`}>
          <span>{formatCurrency(netPosition)}</span>
        </div>
      </div>
    </div>
  );
};

export default StatsGrid;
