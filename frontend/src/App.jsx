import React, { useState } from 'react';
import StatsGrid from './components/StatsGrid';
import Tabs from './components/Tabs';
import Timeline from './components/Timeline';
import AgentPanel from './components/AgentPanel';
import RiskCard from './components/RiskCard';
import DecisionCard from './components/DecisionCard';
import ActionCard from './components/ActionCard';

const API_URL = "http://localhost:8000/run-analysis";

const App = () => {
  // Initial demo data
  const [financeData, setFinanceData] = useState({
    cash_balance: 150000,
    salaries: [
      { employee: "Dev", amount: 60000, due_in_days: 15 },
      { employee: "Designer", amount: 40000, due_in_days: 15 }
    ],
    fixed_bills: [
      { type: "AWS", amount: 20000, due_in_days: 10 },
      { type: "Office Rent", amount: 30000, due_in_days: 18 }
    ],
    receivables: [
      { client: "Client A", amount: 120000, due_in_days: 12 },
      { client: "Client B", amount: 80000, due_in_days: 20 }
    ],
    preferences: {
      dont_delay_salaries: true,
      avoid_vendor_damage: true
    }
  });

  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // --- Actions ---
  const updateCashBalance = (val) => {
    setFinanceData(prev => ({ ...prev, cash_balance: val }));
  };

  const addItem = (key, item) => {
    setFinanceData(prev => ({
      ...prev,
      [key]: [...prev[key], item]
    }));
  };

  const removeItem = (key, index) => {
    setFinanceData(prev => ({
      ...prev,
      [key]: prev[key].filter((_, i) => i !== index)
    }));
  };

  const runAnalysis = async () => {
    setLoading(true);
    try {
      // Mock initial call if backend isn't ready, or real call
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(financeData)
      });

      if (!response.ok) throw new Error("API call failed");

      const data = await response.json();
      setAnalysisResult(data);

    } catch (error) {
      console.error("Analysis failed:", error);
      alert("Failed to connect to agent backend. Make sure the Python server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-xl shadow-lg">
              📊
            </div>
            Autonomous Finance Agent
          </h1>
          <p className="text-slate-500 ml-14">AI-powered cashflow management & risk analysis</p>
        </div>
        <button
          onClick={runAnalysis}
          disabled={loading}
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <span className="animate-spin">🔄</span> Running Agents...
            </>
          ) : (
            <>
              <span>📈</span> Run Analysis
            </>
          )}
        </button>
      </div>

      {/* Stats Grid */}
      <StatsGrid financeData={financeData} updateCashBalance={updateCashBalance} />

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">

        {/* Left Column: Inputs & Data */}
        <div>
          <Tabs financeData={financeData} addItem={addItem} removeItem={removeItem} />
          <Timeline financeData={financeData} />
        </div>

        {/* Right Column: Agent Outputs */}
        {/* Right Column: Agent Outputs */}
        <div className="flex flex-col gap-6">
          <AgentPanel status={analysisResult ? "complete" : "ready"} />

          {/* Agents Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <RiskCard riskData={analysisResult?.risk_analysis} />
            <DecisionCard decisionData={analysisResult?.decision} />
            <ActionCard actionLog={analysisResult?.action_log} />
          </div>
        </div>

      </div>
    </div>
  );
};

export default App;
