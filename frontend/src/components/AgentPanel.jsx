import React from 'react';

const AgentPanel = ({ status }) => {
    // Status can be 'active', 'standby', 'learning'
    const agents = [
        { name: 'Risk Agent', icon: '🧠', state: 'active' },
        { name: 'Decision Agent', icon: '🎯', state: 'active' },
        { name: 'Action Agent', icon: '⚡', state: 'standby' },
        { name: 'Memory Agent', icon: '💾', state: 'learning' },
    ];

    const getBadgeClass = (state) => {
        if (state === 'active') return 'badge-active';
        return 'badge-standby';
    };

    return (
        <div className="card agent-card mb-4 bg-gradient-to-br from-purple-50 to-white border-purple-200">
            <div className="card-header">
                <div className="card-title">
                    <span>🤖</span> Agent System
                </div>
                <div className="card-description">AI-powered autonomous analysis</div>
            </div>
            <div className="card-content">
                <div className="flex flex-col gap-3">
                    {agents.map((agent, i) => (
                        <div key={i} className="flex items-center justify-between p-3 bg-white border rounded-lg">
                            <div className="flex items-center gap-2 font-semibold text-sm">
                                <span>{agent.icon}</span>
                                {agent.name}
                            </div>
                            <span className={`badge ${agent.state === 'active' ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : 'bg-slate-100 text-slate-600 border-slate-200'}`}>
                                {agent.state === 'active' ? '⚡ Active' : agent.state}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AgentPanel;
