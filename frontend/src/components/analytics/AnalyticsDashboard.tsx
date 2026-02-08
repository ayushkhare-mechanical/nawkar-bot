import { useState, useEffect } from 'react';
import type { WidgetState, AnalyticsTrade, AdvancedMetrics } from './types';
import { defaultMetrics } from './types';
import { WidgetPanel } from './WidgetPanel';
import { SummaryCards } from './SummaryCards';
import { PerformanceTable } from './PerformanceTable';
import { TradeList } from './TradeList';
import { EquityChart } from './Charts/EquityChart';
import { PnLChart } from './Charts/PnLChart';

interface AnalyticsDashboardProps {
    rawTrades: any[]; // Raw trades from backtest engine
    initialCapital?: number;
}

export const AnalyticsDashboard: React.FC<AnalyticsDashboardProps> = ({ rawTrades, initialCapital = 100000 }) => {
    // 1. State for Widget Customization
    const [widgets, setWidgets] = useState<WidgetState>({
        showEquityChart: true,
        showPerformance: true,
        showTradesAnalysis: true,
        showCapitalEfficiency: true,
        showRunupsDrawdowns: true
    });

    // 2. State for Calculated Metrics
    const [metrics, setMetrics] = useState<AdvancedMetrics>(defaultMetrics);
    const [trades, setTrades] = useState<AnalyticsTrade[]>([]);
    const [activeTab, setActiveTab] = useState<'metrics' | 'trades'>('metrics');

    // 3. Process Data Effect
    useEffect(() => {
        if (!rawTrades || rawTrades.length === 0) {
            setMetrics(defaultMetrics);
            setTrades([]);
            return;
        }

        // --- A. Process Trades List ---
        const processedTrades: AnalyticsTrade[] = rawTrades.map((t, index) => ({
            id: index + 1,
            symbol: t.symbol,
            type: t.entry_price < t.exit_price && t.pnl > 0 ? 'LONG' : (t.entry_price > t.exit_price ? 'SHORT' : 'LONG'), // Heuristic for now
            entry_time: t.entry_time,
            exit_time: t.exit_time,
            entry_price: t.entry_price,
            exit_price: t.exit_price,
            quantity: 1, // Placeholder
            pnl: t.pnl,
            exit_reason: t.exit_reason,
            duration_bars: 0,
            cumulative_pnl: 0
        }));

        setTrades(processedTrades);

        // --- B. Calculate Metrics for All / Long / Short ---

        // Helper to calculate Standard Deviation
        const calculateStdDev = (values: number[]) => {
            if (values.length < 2) return 0;
            const mean = values.reduce((a, b) => a + b, 0) / values.length;
            const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (values.length - 1);
            return Math.sqrt(variance);
        };

        // Helper to calculate fields for All/Long/Short
        const calcField = (selector: (t: AnalyticsTrade) => number, mode: 'sum' | 'avg' | 'count' | 'pf' | 'sharpe' | 'sortino' | 'dd') => {
            const compute = (items: AnalyticsTrade[]) => {
                if (items.length === 0) return 0;

                if (mode === 'count') return items.length;

                if (mode === 'pf') {
                    const wins = items.filter(t => t.pnl > 0).reduce((a, b) => a + b.pnl, 0);
                    const losses = Math.abs(items.filter(t => t.pnl <= 0).reduce((a, b) => a + b.pnl, 0));
                    return losses === 0 ? (wins > 0 ? 99.99 : 0) : wins / losses;
                }

                if (mode === 'sharpe') {
                    const pnls = items.map(t => t.pnl);
                    const avgPnl = pnls.reduce((a, b) => a + b, 0) / pnls.length;
                    const stdDev = calculateStdDev(pnls);
                    return stdDev === 0 ? 0 : (avgPnl / stdDev); // Simplified Sharpe
                }

                if (mode === 'sortino') {
                    const pnls = items.map(t => t.pnl);
                    const avgPnl = pnls.reduce((a, b) => a + b, 0) / pnls.length;
                    const downsidePnls = pnls.filter(p => p < 0);
                    // Downside Deviation: Std Dev of ONLY negative returns, but using N (not N-1) relative to 0 or target 
                    // Standard approach: sqrt(sum(min(0, returns)^2) / N)
                    if (downsidePnls.length === 0) return avgPnl > 0 ? 99.99 : 0;

                    const sumSqDownside = pnls.reduce((acc, p) => acc + (p < 0 ? p * p : 0), 0);
                    const downsideDev = Math.sqrt(sumSqDownside / pnls.length);

                    return downsideDev === 0 ? 0 : (avgPnl / downsideDev);
                }

                if (mode === 'dd') {
                    // Maximum Dradown
                    let peak = initialCapital;
                    let maxDd = 0;
                    let equity = initialCapital;

                    for (const t of items) {
                        equity += t.pnl;
                        if (equity > peak) peak = equity;
                        const dd = peak - equity;
                        if (dd > maxDd) maxDd = dd;
                    }
                    return maxDd;
                }

                const sum = items.reduce((acc, item) => acc + selector(item), 0);
                return mode === 'avg' ? sum / items.length : sum;
            };

            const longT = processedTrades.filter(t => t.type === 'LONG');
            const shortT = processedTrades.filter(t => t.type === 'SHORT');

            return {
                all: compute(processedTrades),
                long: compute(longT),
                short: compute(shortT)
            };
        };

        // Gross Profit/Loss Selectors
        const grossProfitSel = (t: AnalyticsTrade) => t.pnl > 0 ? t.pnl : 0;
        const grossLossSel = (t: AnalyticsTrade) => t.pnl <= 0 ? Math.abs(t.pnl) : 0;

        const formatRatio = (val: number) => val.toFixed(2);

        const calculatedMetrics: AdvancedMetrics = {
            total_trades: calcField(() => 1, 'count'),
            net_pnl: calcField(t => t.pnl, 'sum'),
            avg_pnl: calcField(t => t.pnl, 'avg'),
            gross_profit: calcField(grossProfitSel, 'sum'),
            gross_loss: calcField(grossLossSel, 'sum'),
            profit_factor: {
                all: calcField(() => 0, 'pf').all.toFixed(2),
                long: calcField(() => 0, 'pf').long.toFixed(2),
                short: calcField(() => 0, 'pf').short.toFixed(2),
            },
            win_rate: {
                all: (processedTrades.filter(t => t.pnl > 0).length / processedTrades.length * 100) || 0,
                long: (processedTrades.filter(t => t.type === 'LONG' && t.pnl > 0).length / processedTrades.filter(t => t.type === 'LONG').length * 100) || 0,
                short: (processedTrades.filter(t => t.type === 'SHORT' && t.pnl > 0).length / processedTrades.filter(t => t.type === 'SHORT').length * 100) || 0,
            },
            sharpe_ratio: {
                all: formatRatio(calcField(() => 0, 'sharpe').all),
                long: formatRatio(calcField(() => 0, 'sharpe').long),
                short: formatRatio(calcField(() => 0, 'sharpe').short)
            },
            sortino_ratio: {
                all: formatRatio(calcField(() => 0, 'sortino').all),
                long: formatRatio(calcField(() => 0, 'sortino').long),
                short: formatRatio(calcField(() => 0, 'sortino').short)
            },
            max_drawdown: calcField(() => 0, 'dd'),
            commission: { all: 0, long: 0, short: 0 },
            expected_payoff: calcField(t => t.pnl, 'avg'), // Same as Avg PnL
            cagr: { all: 0, long: 0, short: 0 },
            return_on_capital: { all: 0, long: 0, short: 0 }
        };

        setMetrics(calculatedMetrics);

    }, [rawTrades, initialCapital]);

    if (!rawTrades || rawTrades.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center py-20 bg-white dark:bg-white/5 rounded-3xl border border-dashed border-gray-300 dark:border-gray-700">
                <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-full mb-4 text-4xl">🕵️</div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">Not enough data to display</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 max-w-sm text-center">
                    Run a backtest to generate trading data for this analysis.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <WidgetPanel widgets={widgets} setWidgets={setWidgets} />

            {/* Dashboard Controls */}
            <div className="flex justify-end mb-4">
                <button
                    onClick={() => {
                        const headers = ['ID', 'Symbol', 'Type', 'Entry Time', 'Exit Time', 'Entry Price', 'Exit Price', 'PnL', 'Exit Reason'];
                        const csvContent = [
                            headers.join(','),
                            ...trades.map(t => [
                                t.id,
                                t.symbol,
                                t.type,
                                t.entry_time,
                                t.exit_time,
                                t.entry_price,
                                t.exit_price,
                                t.pnl,
                                `"${t.exit_reason}"`
                            ].join(','))
                        ].join('\n');

                        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                        const link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.setAttribute('download', `trades_export_${new Date().toISOString().slice(0, 10)}.csv`);
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    }}
                    className="flex items-center gap-2 px-4 py-2 text-sm font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-900/20 dark:hover:bg-indigo-900/40 rounded-xl transition-colors"
                >
                    📥 Export CSV
                </button>
            </div>

            {/* Tab Navigation */}
            <div className="flex border-b border-gray-200 dark:border-gray-800">
                <button
                    onClick={() => setActiveTab('metrics')}
                    className={`px-6 py-3 text-sm font-bold border-b-2 transition-colors ${activeTab === 'metrics'
                        ? 'border-indigo-600 text-indigo-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                        }`}
                >
                    Metrics
                </button>
                <button
                    onClick={() => setActiveTab('trades')}
                    className={`px-6 py-3 text-sm font-bold border-b-2 transition-colors ${activeTab === 'trades'
                        ? 'border-indigo-600 text-indigo-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                        }`}
                >
                    List of trades
                </button>
            </div>

            {activeTab === 'metrics' ? (
                <div className="space-y-6 animate-in fade-in duration-500">
                    {/* Summary Cards */}
                    <SummaryCards metrics={metrics} />

                    {/* 1. Equity Curve Chart */}
                    {widgets.showEquityChart && (
                        <div className="bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-gray-800 p-6">
                            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                                📈 Equity Curve
                            </h2>
                            <EquityChart trades={trades} initialCapital={initialCapital} />
                        </div>
                    )}

                    {/* 2. Performance Section */}
                    {widgets.showPerformance && (
                        <div className="bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-gray-800 p-6">
                            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                                📊 Performance
                            </h2>
                            <PerformanceTable metrics={metrics} />
                        </div>
                    )}

                    {/* 3. Trades PnL Analysis */}
                    {widgets.showTradesAnalysis && (
                        <div className="bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-gray-800 p-6">
                            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                                💸 Trade P&L Distribution
                            </h2>
                            <PnLChart trades={trades} />
                        </div>
                    )}
                </div>
            ) : (
                <div className="bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-gray-800 overflow-hidden">
                    <TradeList trades={trades} />
                </div>
            )}
        </div>
    );
};
