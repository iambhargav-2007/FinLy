import React, { useState } from 'react';

const Tabs = ({ financeData, addItem, removeItem }) => {
    const [activeTab, setActiveTab] = useState('salaries');

    // Local state for inputs
    const [formData, setFormData] = useState({
        name: '', amount: '', days: ''
    });

    const handleAdd = () => {
        if (formData.name && formData.amount && formData.days) {
            if (activeTab === 'salaries') {
                addItem('salaries', {
                    employee: formData.name,
                    amount: parseInt(formData.amount),
                    due_in_days: parseInt(formData.days)
                });
            } else if (activeTab === 'bills') {
                addItem('fixed_bills', {
                    type: formData.name,
                    amount: parseInt(formData.amount),
                    due_in_days: parseInt(formData.days)
                });
            } else {
                addItem('receivables', {
                    client: formData.name,
                    amount: parseInt(formData.amount),
                    due_in_days: parseInt(formData.days)
                });
            }
            setFormData({ name: '', amount: '', days: '' });
        }
    };

    const getList = () => {
        if (activeTab === 'salaries') return financeData.salaries;
        if (activeTab === 'bills') return financeData.fixed_bills;
        return financeData.receivables;
    };

    const getBadges = (item) => {
        if (activeTab === 'salaries') return 'badge-amber';
        if (activeTab === 'bills') return 'badge-blue';
        return 'badge-emerald';
    };

    const getItemName = (item) => item.employee || item.type || item.client;

    return (
        <div className="card mb-6">
            <div className="p-4 bg-gray-50 rounded-t-xl">
                <div className="grid grid-cols-3 gap-1 bg-slate-200 p-1 rounded-lg">
                    {['salaries', 'bills', 'receivables'].map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`py-2 px-4 rounded-md text-sm font-medium transition-all ${activeTab === tab ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
                                }`}
                        >
                            {tab.charAt(0).toUpperCase() + tab.slice(1)}
                        </button>
                    ))}
                </div>
            </div>

            <div className="p-5">
                <div className="mb-4">
                    <h3 className="text-lg font-bold text-slate-900 capitalize">{activeTab.replace('_', ' ')}</h3>
                    <p className="text-sm text-slate-500">Manage your {activeTab} entries</p>
                </div>

                {/* Form */}
                <div className="grid grid-cols-[2fr_1fr_1fr_auto] gap-3 bg-slate-50 p-4 rounded-lg mb-4">
                    <div>
                        <label>Name / Type</label>
                        <input
                            value={formData.name}
                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                            placeholder="Name"
                        />
                    </div>
                    <div>
                        <label>Amount (₹)</label>
                        <input
                            type="number"
                            value={formData.amount}
                            onChange={e => setFormData({ ...formData, amount: e.target.value })}
                            placeholder="0.00"
                        />
                    </div>
                    <div>
                        <label>Due (Days)</label>
                        <input
                            type="number"
                            value={formData.days}
                            onChange={e => setFormData({ ...formData, days: e.target.value })}
                            placeholder="0"
                        />
                    </div>
                    <button
                        onClick={handleAdd}
                        className="self-end bg-blue-500 text-white w-10 h-10 rounded-md flex items-center justify-center hover:bg-blue-600"
                    >
                        +
                    </button>
                </div>

                {/* List */}
                <div className="flex flex-col gap-2">
                    {getList().map((item, i) => (
                        <div key={i} className="flex items-center justify-between p-3 border rounded-lg hover:border-slate-300 transition-colors">
                            <div>
                                <h4 className="text-sm font-bold text-slate-800">{getItemName(item)}</h4>
                                <p className="text-xs text-slate-500">₹{item.amount.toLocaleString()} • Due in {item.due_in_days} days</p>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className={`badge ${getBadges(item)}`}>Day {item.due_in_days}</span>
                                <button
                                    onClick={() => removeItem(activeTab === 'bills' ? 'fixed_bills' : activeTab, i)}
                                    className="text-slate-300 hover:text-rose-500 p-1"
                                >
                                    🗑️
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Tabs;
