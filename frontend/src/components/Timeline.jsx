import React from 'react';

const formatCurrency = (amount) => '₹' + amount.toLocaleString('en-IN');

const Timeline = ({ financeData }) => {
    const events = [
        ...financeData.salaries.map(s => ({
            day: s.due_in_days,
            type: 'outflow',
            description: s.employee,
            amount: s.amount
        })),
        ...financeData.fixed_bills.map(b => ({
            day: b.due_in_days,
            type: 'outflow',
            description: b.type,
            amount: b.amount
        })),
        ...financeData.receivables.map(r => ({
            day: r.due_in_days,
            type: 'inflow',
            description: r.client,
            amount: r.amount
        }))
    ].sort((a, b) => a.day - b.day);

    let balance = financeData.cash_balance;

    return (
        <div className="card mt-6">
            <div className="card-header">
                <div className="card-title">
                    <span>📅</span> Cash Flow Timeline
                </div>
                <div className="card-description">30-day projection</div>
            </div>
            <div className="card-content">
                <div className="timeline">
                    {/* Initial State */}
                    <div className="timeline-item">
                        <div className="timeline-dot current"></div>
                        <div className="timeline-card current">
                            <div className="flex items-center gap-2 mb-2">
                                <span className="badge bg-slate-100 text-slate-600 border-slate-300">Day 0</span>
                            </div>
                            <div className="flex justify-between items-start">
                                <div>
                                    <h4 className="text-sm font-bold">Current Balance</h4>
                                    <p className="text-xs text-slate-500">Today</p>
                                </div>
                                <div className="text-right font-bold text-sm">
                                    {formatCurrency(balance)}
                                </div>
                            </div>
                        </div>
                    </div>

                    {events.map((event, i) => {
                        balance += event.type === 'inflow' ? event.amount : -event.amount;
                        const isCritical = balance < 0;
                        return (
                            <div key={i} className="timeline-item">
                                <div className={`timeline-dot ${event.type}`}></div>
                                <div className={`timeline-card ${isCritical ? 'critical' : ''}`}>
                                    <div className="flex items-center gap-2 mb-2">
                                        <span className="badge badge-amber">Day {event.day}</span>
                                        <span>{event.type === 'inflow' ? '↗️' : '↘️'}</span>
                                    </div>
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <h4 className="text-sm font-bold">{event.description}</h4>
                                            <p className={`text-xs ${event.type === 'inflow' ? 'text-emerald' : 'text-rose'}`}>
                                                {event.type === 'inflow' ? '+' : '-'}{formatCurrency(event.amount)}
                                            </p>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-xs text-slate-500">Projected</div>
                                            <div className={`text-sm font-bold ${balance < 0 ? 'text-rose' : ''}`}>
                                                {formatCurrency(balance)}
                                            </div>
                                        </div>
                                    </div>
                                    {isCritical && (
                                        <div className="mt-2 pt-2 border-t border-rose-200 text-xs font-bold text-rose-700">
                                            ⚠️ Critical: Negative balance projected
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default Timeline;
