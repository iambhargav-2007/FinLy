import React from 'react';

const RiskCard = ({ riskData }) => {
    // riskData shape: { risk_score, critical_window, dominant_risk, confidence, sub_goal }
    if (!riskData) return null;

    const { risk_score, critical_window, dominant_risk, confidence, sub_goal } = riskData;

    const getRiskLevel = (score) => {
        if (score > 70) return 'high';
        if (score > 40) return 'medium';
        return 'low';
    };

    const level = getRiskLevel(risk_score);
    const cardClass = level === 'high' ? 'bg-rose-50 border-rose-200' :
        level === 'medium' ? 'bg-yellow-50 border-yellow-200' : 'bg-emerald-50 border-emerald-200';

    return (
        <div className={`card risk-card mb-4 border-2 ${cardClass}`}>
            <div className="card-header">
                <div className="card-title">
                    <span>⚠️</span> Risk Analysis
                </div>
                <div className="card-description">Agent 1: Scenario simulation</div>
            </div>
            <div className="card-content">
                <div className="mb-4">
                    <div className="flex justify-between mb-1">
                        <span className="text-sm font-semibold">Risk Score</span>
                        <span className="font-bold">{risk_score}/100</span>
                    </div>
                    <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-gradient-to-r from-emerald-400 to-rose-500 transition-all duration-500"
                            style={{ width: `${risk_score}%` }}
                        ></div>
                    </div>
                </div>

                <div className="bg-white border rounded-lg p-3 mb-3">
                    <div className="text-xs text-slate-500 mb-1">Critical Time Window</div>
                    <div className="text-sm font-bold text-slate-900">{critical_window}</div>
                </div>

                <div className="bg-white border rounded-lg p-3 mb-3">
                    <div className="text-xs text-slate-500 mb-1">Dominant Risk</div>
                    <div className="text-sm font-bold text-slate-900">{dominant_risk}</div>
                </div>

                <div className="flex justify-between items-center mb-4">
                    <span className="text-xs text-slate-500">Confidence Level</span>
                    <span className="badge bg-blue-100 text-blue-800 border-blue-200">{confidence}</span>
                </div>

                {sub_goal && (
                    <div className="bg-gradient-to-br from-purple-100 to-blue-50 border border-purple-200 rounded-lg p-3">
                        <div className="text-xs font-bold text-purple-700 mb-1 flex items-center gap-1">
                            <span>🎯</span> AI-Generated Sub-Goal
                        </div>
                        <div className="text-sm font-semibold text-purple-900">
                            {/* Handle differing sub_goal structures (string vs object) */}
                            {typeof sub_goal === 'string' ? sub_goal :
                                sub_goal.intent ? `${sub_goal.intent} (₹${sub_goal.required_amount})` :
                                    JSON.stringify(sub_goal)}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default RiskCard;
