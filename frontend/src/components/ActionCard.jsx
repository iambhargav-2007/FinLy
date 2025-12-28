import React from 'react';

const ActionCard = ({ actionLog }) => {
    // actionLog shape: { action_taken, target, tone_used, content_draft, result }

    const hasAction = actionLog && actionLog.action_taken && actionLog.action_taken !== "NO_ACTION";

    return (
        <div className="card">
            <div className="card-header">
                <div className="card-title">
                    <span>⚡</span> Recent Actions
                </div>
                <div className="card-description">Agent 3: Autonomous execution</div>
            </div>
            <div className="card-content">
                {!hasAction ? (
                    <div className="text-center py-8 text-slate-400">
                        <div className="text-5xl mb-2 grayscale opacity-50">⏰</div>
                        <p className="text-sm">No actions executed yet</p>
                        <p className="text-xs mt-1">Run analysis to see agent actions</p>
                    </div>
                ) : (
                    <div className="bg-gradient-to-br from-emerald-50 to-white border border-emerald-100 rounded-lg p-4">
                        <div className="flex justify-between items-start mb-2">
                            <span className="badge badge-emerald">ACTION EXECUTED</span>
                            <span className="text-xs text-slate-400">Just now (v2.0)</span>
                        </div>

                        <h4 className="font-bold text-slate-900 mb-3">{actionLog.action_taken}</h4>

                        {/* Multi-Target Support */}
                        {actionLog.targets_processed ? (
                            <div className="space-y-3">
                                {actionLog.targets_processed.map((item, index) => (
                                    <div key={index} className="bg-white border border-slate-200 rounded p-3">
                                        <div className="text-sm text-slate-700 font-semibold mb-1">
                                            To: {item.target}
                                            <span className="text-xs font-normal text-slate-500 ml-1">
                                                ({item.email || "No Email"})
                                            </span>
                                        </div>
                                        <div className="text-xs text-emerald-600 font-semibold">
                                            Result: {item.result?.status || "SENT"}
                                        </div>
                                    </div>
                                ))}
                                <div className="mt-2 text-xs font-semibold text-slate-500">
                                    Tone: {actionLog.tone_used}
                                </div>
                            </div>
                        ) : (
                            /* Single Target Fallback (e.g. for STATUS_QUO) */
                            <>
                                <div className="text-sm text-slate-600 mb-3">
                                    Target: <span className="font-semibold">{actionLog.target}</span>
                                </div>

                                {actionLog.content_draft && (
                                    <div className="bg-white border rounded p-3 text-xs text-slate-600 italic">
                                        "{actionLog.content_draft}"
                                    </div>
                                )}

                                <div className="mt-3 flex gap-2">
                                    <span className="text-xs font-semibold text-slate-500">Tone: {actionLog.tone_used}</span>
                                    {actionLog.result && (
                                        <span className="text-xs font-semibold text-emerald-600">
                                            Result: {actionLog.result?.status || "SENT"}
                                        </span>
                                    )}
                                </div>
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default ActionCard;
