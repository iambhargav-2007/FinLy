import React from 'react';

const DecisionCard = ({ decisionData }) => {
    if (!decisionData) return null;

    const { strategy, target, amount_goal, rationale } = decisionData;

    return (
        <div className="card decision-card mb-4 bg-gradient-to-br from-indigo-50 to-white border-indigo-200">
            <div className="card-header">
                <div className="card-title">
                    <span>🎯</span> Agent Decision
                </div>
                <div className="card-description">Agent 2: Strategic choice</div>
            </div>
            <div className="card-content">
                <div className="grid gap-3">
                    <div className="bg-white border rounded-lg p-3">
                        <div className="text-xs text-slate-500 mb-1">Strategy</div>
                        <div className="text-sm font-bold text-slate-900">{strategy}</div>
                    </div>

                    <div className="bg-white border rounded-lg p-3">
                        <div className="text-xs text-slate-500 mb-1">Target</div>
                        <div className="text-sm font-bold text-slate-900">{target}</div>
                    </div>

                    <div className="bg-white border rounded-lg p-3">
                        <div className="text-xs text-slate-500 mb-1">Amount Goal</div>
                        <div className="text-sm font-bold text-emerald-600">
                            ₹{amount_goal ? amount_goal.toLocaleString() : '0'}
                        </div>
                    </div>

                    <div className="bg-gradient-to-br from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-3">
                        <div className="text-xs font-bold text-purple-700 mb-1">💡 Reasoning</div>
                        <div className="text-sm text-purple-900 italic">
                            "{rationale}"
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DecisionCard;
