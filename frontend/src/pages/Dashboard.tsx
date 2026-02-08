import { useEffect, useState } from 'react';
import { Layout } from '../Layout';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
interface MonitorData {
    authenticated: boolean;
    user_profile?: {
        name: string;
        fy_id: string;
        email: string;
        mobile_number: string;
    };
    funds?: {
        fund_limit: Array<{ id: number; title: string; equityAmount: number; commodityAmount: number }>;
    };
    holdings?: {
        overall?: {
            count_total: number;
            total_pl: number;
        };
    };
    positions?: {
        overall?: {
            count_open: number;
            pl_total: number;
        };
    };
    last_linked?: string;
    active_trades_count?: number;
    total_trades_count?: number;
    features: Array<{ name: string; status: string; icon: string }>;
}

interface Strategy {
    name: string;
    symbol: string;
    timeframe: string;
    indicators: any[];
}

interface Trade {
    symbol: string;
    entry_price: number;
    exit_price?: number;
    entry_time: string;
    exit_time?: string;
    sl_price: number;
    target_price: number;
    status: string;
    exit_reason?: string;
    pnl?: number;
}

export const Dashboard = () => {
    const [data, setData] = useState<MonitorData | null>(null);
    const [strategies, setStrategies] = useState<Strategy[]>([]);
    const [activeTrades, setActiveTrades] = useState<Trade[]>([]);
    const [history, setHistory] = useState<Trade[]>([]);
    const [activeTab, setActiveTab] = useState<'overview' | 'strategies' | 'trades' | 'backtest'>('overview');
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        try {
            const [monRes, stratRes, activeRes, histRes] = await Promise.all([
                fetch('/api/v1/monitor/data'),
                fetch('/api/v1/monitor/strategies'),
                fetch('/api/v1/monitor/trades/active'),
                fetch('/api/v1/monitor/trades/history')
            ]);

            const monData = await monRes.json();
            const stratData = await stratRes.json();
            const activeData = await activeRes.json();
            const histData = await histRes.json();

            setData(monData);
            setStrategies(stratData.active_strategies || []);
            setActiveTrades(activeData.active_trades || []);
            setHistory(histData.history || []);
        } catch (error) {
            console.error("Error fetching dashboard data:", error);
        } finally {
            setLoading(false);
        }
    };

    const reloadStrategies = async () => {
        await fetch('/api/v1/monitor/strategies/reload', { method: 'POST' });
        fetchData();
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000);
        return () => clearInterval(interval);
    }, []);

    // Format Timestamp
    const formatTimestamp = (isoString?: string) => {
        if (!isoString) return "Never";
        try {
            const date = new Date(isoString);
            return date.toLocaleString('en-IN', {
                day: '2-digit',
                month: 'short',
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
            });
        } catch {
            return "Invalid Date";
        }
    };

    // Get Balance with robust fallbacks
    const getBalance = () => {
        if (!data?.funds?.fund_limit) return 0;
        const limits = data.funds.fund_limit;
        const total = limits.find(f => f.title === "Total Balance");
        if (total && total.equityAmount > 0) return total.equityAmount;
        const available = limits.find(f => f.title === "Available Balance");
        if (available && available.equityAmount > 0) return available.equityAmount;
        return total?.equityAmount || 0;
    };

    const totalBalance = getBalance();
    const displayPnL = data?.positions?.overall?.pl_total !== 0
        ? (data?.positions?.overall?.pl_total || 0)
        : (data?.holdings?.overall?.total_pl || 0);

    const pnlColor = displayPnL > 0 ? "text-green-500" : displayPnL < 0 ? "text-red-500" : "text-gray-400";

    if (loading) return (
        <Layout>
            <div className="flex items-center justify-center h-[80vh]">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-scandi-accents"></div>
            </div>
        </Layout>
    );

    if (!data?.authenticated) {
        return (
            <Layout>
                <div className="text-center py-20">
                    <h2 className="text-2xl font-bold mb-4">Authentication Required</h2>
                    <a href="/api/v1/auth/login" className="px-6 py-2 bg-indigo-600 text-white rounded-full">Connect Fyers</a>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="max-w-7xl mx-auto px-4 py-12">
                <header className="mb-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                    <div>
                        <h1 className="text-3xl font-bold mb-2">Bot Console</h1>
                        <p className="text-scandi-muted">Welcome back, {data.user_profile?.name}</p>
                        <p className="text-xs text-scandi-muted mt-1">
                            <span className="opacity-60">Last Linked:</span> {formatTimestamp(data.last_linked)}
                        </p>
                    </div>

                    <nav className="flex bg-gray-100 dark:bg-white/5 rounded-2xl p-1 border border-gray-200 dark:border-white/10">
                        <button
                            onClick={() => setActiveTab('overview')}
                            className={`px-6 py-2 rounded-xl text-sm font-medium transition-all ${activeTab === 'overview' ? 'bg-white dark:bg-scandi-accents text-black dark:text-white shadow-sm' : 'text-scandi-muted hover:text-black dark:hover:text-white'}`}
                        >Overview</button>
                        <button
                            onClick={() => setActiveTab('strategies')}
                            className={`px-6 py-2 rounded-xl text-sm font-medium transition-all ${activeTab === 'strategies' ? 'bg-white dark:bg-scandi-accents text-black dark:text-white shadow-sm' : 'text-scandi-muted hover:text-black dark:hover:text-white'}`}
                        >Strategies</button>
                        <button
                            onClick={() => setActiveTab('trades')}
                            className={`px-6 py-2 rounded-xl text-sm font-medium transition-all ${activeTab === 'trades' ? 'bg-white dark:bg-scandi-accents text-black dark:text-white shadow-sm' : 'text-scandi-muted hover:text-black dark:hover:text-white'}`}
                        >Trades</button>
                        <button
                            onClick={() => setActiveTab('backtest')}
                            className={`px-6 py-2 rounded-xl text-sm font-medium transition-all ${activeTab === 'backtest' ? 'bg-white dark:bg-scandi-accents text-black dark:text-white shadow-sm' : 'text-scandi-muted hover:text-black dark:hover:text-white'}`}
                        >Backtesting</button>
                    </nav>
                </header>

                {activeTab === 'overview' && (
                    <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
                        <div className="grid md:grid-cols-3 gap-6">
                            <div className="bg-white dark:bg-white/5 p-6 rounded-3xl border border-gray-200 dark:border-gray-800">
                                <h3 className="text-sm font-bold uppercase text-scandi-muted mb-4">Account Balance</h3>
                                <div className="text-3xl font-bold">₹{totalBalance.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</div>
                            </div>
                            <div className="bg-white dark:bg-white/5 p-6 rounded-3xl border border-gray-200 dark:border-gray-800">
                                <h3 className="text-sm font-bold uppercase text-scandi-muted mb-4">Live Performance</h3>
                                <div className={`text-3xl font-bold ${pnlColor}`}>
                                    {displayPnL >= 0 ? '+' : ''}₹{displayPnL.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                                </div>
                            </div>
                            <div className="bg-white dark:bg-white/5 p-6 rounded-3xl border border-gray-200 dark:border-gray-800">
                                <h3 className="text-sm font-bold uppercase text-scandi-muted mb-4">Active Engine</h3>
                                <div className="text-3xl font-bold">{strategies.length} Strategies</div>
                            </div>
                        </div>

                        <div className="grid md:grid-cols-3 gap-8">
                            <div className="md:col-span-2 space-y-6">
                                <h2 className="text-xl font-bold">Latest Price Action</h2>
                                <div className="bg-white dark:bg-white/5 p-12 rounded-3xl border border-gray-200 dark:border-gray-800 flex items-center justify-center text-scandi-muted italic">
                                    [Interactive Chart Engine - Linking Pending]
                                </div>
                            </div>
                            <div className="space-y-6">
                                <h2 className="text-xl font-bold">Fyers Status</h2>
                                <div className="space-y-4">
                                    {data.features?.map((f: any, i: number) => (
                                        <div key={i} className="flex items-center gap-4 bg-white dark:bg-white/5 p-4 rounded-xl border border-gray-200 dark:border-gray-800">
                                            <div className="p-2 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 rounded-lg">⚡</div>
                                            <div>
                                                <div className="font-semibold">{f.name}</div>
                                                <div className="text-xs text-green-500 font-medium">● {f.status}</div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'strategies' && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="flex justify-between items-center">
                            <h2 className="text-2xl font-bold">Available Strategies</h2>
                            <button onClick={reloadStrategies} className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-sm font-medium hover:bg-indigo-700 transition-all">
                                Reload Engine
                            </button>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {strategies.map((s: Strategy, i: number) => (
                                <div key={i} className="bg-white dark:bg-white/5 p-6 rounded-3xl border border-gray-200 dark:border-gray-800">
                                    <div className="flex justify-between items-start mb-6">
                                        <div>
                                            <h3 className="font-bold text-xl mb-1">{s.name}</h3>
                                            <p className="text-sm text-scandi-muted">{s.symbol} • {s.timeframe}</p>
                                        </div>
                                        <div className="px-3 py-1 bg-green-100 dark:bg-green-900/20 text-green-600 text-xs font-bold rounded-full uppercase tracking-wider border border-green-200 dark:border-green-800">Active</div>
                                    </div>
                                    <div className="space-y-3">
                                        <p className="text-xs font-bold text-scandi-muted uppercase tracking-widest">Indicators</p>
                                        <div className="flex gap-2 flex-wrap">
                                            {s.indicators.map((ind: any, j: number) => (
                                                <span key={j} className="text-xs bg-gray-100 dark:bg-white/5 px-3 py-1 rounded-lg border border-gray-200 dark:border-white/10">{ind.type} ({ind.params.period})</span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {activeTab === 'trades' && (
                    <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <section>
                            <h2 className="text-2xl font-bold mb-6">Active Signals</h2>
                            <div className="bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-gray-800 overflow-hidden">
                                <table className="w-full text-left border-collapse">
                                    <thead className="bg-gray-50 dark:bg-white/5 text-[10px] font-bold text-scandi-muted uppercase tracking-widest">
                                        <tr>
                                            <th className="px-8 py-4">Symbol</th>
                                            <th className="px-8 py-4">Entry Price</th>
                                            <th className="px-8 py-4">SL / Target</th>
                                            <th className="px-8 py-4">Current PnL</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-100 dark:divide-white/5">
                                        {activeTrades.map((t: Trade, i: number) => (
                                            <tr key={i} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                                                <td className="px-8 py-6 font-bold text-lg">{t.symbol}</td>
                                                <td className="px-8 py-6">₹{t.entry_price.toLocaleString()}</td>
                                                <td className="px-8 py-6 font-mono text-xs">
                                                    <span className="text-red-500">SL: ₹{t.sl_price.toFixed(2)}</span><br />
                                                    <span className="text-green-500">TG: ₹{t.target_price.toFixed(2)}</span>
                                                </td>
                                                <td className="px-8 py-6 font-bold text-indigo-600">-- Tracking --</td>
                                            </tr>
                                        ))}
                                        {activeTrades.length === 0 && (
                                            <tr><td colSpan={4} className="px-8 py-20 text-center text-scandi-muted italic">No active tactical positions</td></tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section>
                            <h2 className="text-2xl font-bold mb-6">Trade History</h2>
                            <div className="bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-gray-800 overflow-hidden">
                                <table className="w-full text-left border-collapse">
                                    <thead className="bg-gray-50 dark:bg-white/5 text-[10px] font-bold text-scandi-muted uppercase tracking-widest">
                                        <tr>
                                            <th className="px-8 py-4">Symbol</th>
                                            <th className="px-8 py-4">Reason</th>
                                            <th className="px-8 py-4">PnL</th>
                                            <th className="px-8 py-4">Final Price</th>
                                            <th className="px-8 py-4">Exit Time</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-100 dark:divide-white/5">
                                        {history.map((t: Trade, i: number) => (
                                            <tr key={i} className="hover:bg-gray-50 dark:hover:bg-white/10 transition-colors">
                                                <td className="px-8 py-6 font-bold">{t.symbol}</td>
                                                <td className="px-8 py-6 text-sm italic">{t.exit_reason}</td>
                                                <td className={`px-8 py-6 font-bold ${(t.pnl || 0) >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                                                    {(t.pnl || 0) >= 0 ? '+' : ''}₹{t.pnl?.toFixed(2)}
                                                </td>
                                                <td className="px-8 py-6 text-scandi-muted">₹{t.exit_price?.toLocaleString()}</td>
                                                <td className="px-8 py-6 text-xs text-scandi-muted">{formatTimestamp(t.exit_time)}</td>
                                            </tr>
                                        ))}
                                        {history.length === 0 && (
                                            <tr><td colSpan={5} className="px-8 py-20 text-center text-scandi-muted italic">No closed trades yet</td></tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </section>
                    </div>
                )}

                {activeTab === 'backtest' && (
                    <BacktestPlayground strategies={strategies} />
                )}
            </div>
        </Layout>
    );
};

// --- New Component for Backtest Tab ---
const BacktestPlayground = ({ strategies }: { strategies: Strategy[] }) => {
    const [selectedStrat, setSelectedStrat] = useState<Strategy | null>(strategies[0] || null);
    const [symbol, setSymbol] = useState("NSE:SBIN-EQ");
    const [overrides, setOverrides] = useState<Record<string, any>>({});
    const [results, setResults] = useState<any>(null);
    const [running, setRunning] = useState(false);
    const [btHistory, setBtHistory] = useState<any[]>([]);

    useEffect(() => {
        fetch('/api/v1/monitor/backtest/history').then(res => res.json()).then(data => setBtHistory(data.history || []));
    }, []);

    const [startDate, setStartDate] = useState(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]);
    const [endDate, setEndDate] = useState(new Date().toISOString().split('T')[0]);

    const runBacktest = async () => {
        if (!selectedStrat) return;
        setRunning(true);
        try {
            const res = await fetch('/api/v1/monitor/backtest/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    strategy_name: selectedStrat.name,
                    symbol: symbol,
                    parameters: overrides,
                    from_date: startDate,
                    to_date: endDate
                })
            });
            const data = await res.json();

            if (res.ok) {
                setResults(data);
                // Refresh history
                fetch('/api/v1/monitor/backtest/history').then(res => res.json()).then(data => setBtHistory(data.history || []));
            } else {
                alert(`Backtest Failed: ${data.detail || 'Unknown Error'}`);
                setResults(null);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setRunning(false);
        }
    };

    const handleParamChange = (indId: string, param: string, val: number) => {
        setOverrides(prev => ({
            ...prev,
            [indId]: { ...(prev[indId] || {}), [param]: val }
        }));
    };

    return (
        <div className="grid lg:grid-cols-3 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="space-y-6">
                <div className="bg-white dark:bg-white/5 p-6 rounded-3xl border border-gray-200 dark:border-gray-800 space-y-6">
                    <h2 className="text-xl font-bold">Playground Controls</h2>

                    <div>
                        <label className="text-xs font-bold text-scandi-muted block mb-2 uppercase">Strategy</label>
                        <select
                            className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl p-3 text-sm"
                            onChange={(e) => setSelectedStrat(strategies.find(s => s.name === e.target.value) || null)}
                        >
                            {strategies.map(s => <option key={s.name} value={s.name}>{s.name}</option>)}
                        </select>
                    </div>

                    <div>
                        <label className="text-xs font-bold text-scandi-muted block mb-2 uppercase">Symbol</label>
                        <input
                            type="text"
                            className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl p-3 text-sm"
                            value={symbol}
                            onChange={(e) => setSymbol(e.target.value)}
                        />
                    </div>

                    {selectedStrat?.indicators.map((ind: any) => (
                        <div key={ind.id} className="space-y-4 pt-4 border-t border-gray-100 dark:border-white/5">
                            <p className="text-[10px] font-bold text-scandi-muted uppercase">{ind.id} Parameters</p>
                            {Object.entries(ind.params).map(([key, val]: [string, any]) => (
                                <div key={key}>
                                    <div className="flex justify-between text-xs mb-2">
                                        <span className="capitalize">{key}</span>
                                        <span className="font-bold text-indigo-600">{overrides[ind.id]?.[key] || val}</span>
                                    </div>
                                    <input
                                        type="range" min="1" max="200"
                                        value={overrides[ind.id]?.[key] || val}
                                        onChange={(e) => handleParamChange(ind.id, key, parseInt(e.target.value))}
                                        className="w-full transition-all accent-indigo-600"
                                    />
                                </div>
                            ))}
                        </div>
                    ))}

                    <div className="space-y-4">
                        <label className="text-xs font-bold uppercase text-scandi-muted">Date Range</label>
                        <div className="grid grid-cols-2 gap-2">
                            <input
                                type="date"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                className="w-full bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                            />
                            <input
                                type="date"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className="w-full bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                            />
                        </div>
                    </div>
                </div>
            </div>

            <button
                onClick={runBacktest}
                disabled={running}
                className={`w-full py-4 rounded-2xl font-bold text-white transition-all ${running ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-500/20'}`}
            >
                {running ? 'Simulating Engine...' : 'Run Backtest'}
            </button>
            <div className="lg:col-span-2">
                <AnalyticsDashboard rawTrades={results?.trades || []} />

                <section className="mt-8">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-xl font-bold">Saved Research Logs</h2>
                        {btHistory.length > 0 && (
                            <button
                                onClick={async () => {
                                    if (confirm("Delete all backtest history? This cannot be undone.")) {
                                        await fetch('/api/v1/monitor/backtest/clear', { method: 'DELETE' });
                                        setBtHistory([]);
                                        setResults(null);
                                    }
                                }}
                                className="text-xs font-bold text-red-500 hover:text-red-600 uppercase tracking-widest"
                            >
                                Clear All
                            </button>
                        )}
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {btHistory.map((run: any) => (
                            <div key={run.id} className="bg-white dark:bg-white/5 p-4 rounded-2xl border border-gray-200 dark:border-gray-800 text-xs">
                                <div className="flex justify-between items-center mb-2">
                                    <span className="font-bold">{run.strategy_name}</span>
                                    <div className="flex items-center gap-3">
                                        <span className={`font-bold ${run.total_pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                                            ₹{run.total_pnl.toFixed(1)}
                                        </span>
                                        <a
                                            href={`/api/v1/monitor/backtest/export/${run.id}`}
                                            download
                                            className="text-indigo-600 hover:text-indigo-700 font-bold underline"
                                        >
                                            CSV
                                        </a>
                                    </div>
                                </div>
                                <div className="text-[10px] text-scandi-muted flex justify-between">
                                    <span>{run.symbol} • {run.win_rate.toFixed(0)}% WR</span>
                                    <p className="text-[10px] text-scandi-muted">
                                        {new Date(run.timestamp).toLocaleString('en-IN', {
                                            day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
                                        })}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            </div>
        </div>
    );
};
