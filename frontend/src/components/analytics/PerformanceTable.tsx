import React from 'react';
import type { AdvancedMetrics, MetricSet } from './types';

interface PerformanceTableProps {
    metrics: AdvancedMetrics;
}

export const PerformanceTable: React.FC<PerformanceTableProps> = ({ metrics }) => {

    // Helper to render a row
    const MetricRow = ({ label, data, isCurrency = true, isPercent = false }: { label: string, data: MetricSet, isCurrency?: boolean, isPercent?: boolean }) => {
        const format = (val: number | string) => {
            if (val === '-' || val === undefined) return '—';
            if (typeof val === 'string') return val;
            if (isPercent) return `${val.toFixed(2)}%`;
            if (isCurrency) return `₹${val.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
            return val;
        };

        return (
            <tr className="border-b border-gray-100 dark:border-white/5 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                <td className="py-3 px-4 text-sm font-medium text-gray-600 dark:text-gray-400">{label}</td>
                <td className="py-3 px-4 text-sm font-bold text-gray-900 dark:text-gray-100">{format(data.all)}</td>
                <td className="py-3 px-4 text-sm font-medium text-gray-600 dark:text-gray-400">{format(data.long)}</td>
                <td className="py-3 px-4 text-sm font-medium text-gray-600 dark:text-gray-400">{format(data.short)}</td>
            </tr>
        );
    };

    return (
        <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
                <thead>
                    <tr className="border-b-2 border-gray-200 dark:border-gray-800 text-xs uppercase text-gray-500">
                        <th className="py-3 px-4 font-bold">Metric</th>
                        <th className="py-3 px-4 font-bold">All</th>
                        <th className="py-3 px-4 font-bold">Long</th>
                        <th className="py-3 px-4 font-bold">Short</th>
                    </tr>
                </thead>
                <tbody>
                    <MetricRow label="Total Net Profit" data={metrics.net_pnl} />
                    <MetricRow label="Gross Profit" data={metrics.gross_profit} />
                    <MetricRow label="Gross Loss" data={metrics.gross_loss} />
                    <MetricRow label="Profit Factor" data={metrics.profit_factor} isCurrency={false} />
                    <MetricRow label="Commission Paid" data={metrics.commission} />
                    <MetricRow label="Expected Payoff" data={metrics.expected_payoff} />

                    {/* Separator for Return Metrics */}
                    <tr className="bg-gray-50 dark:bg-white/5"><td colSpan={4} className="py-1"></td></tr>

                    <MetricRow label="Sharpe Ratio" data={metrics.sharpe_ratio} isCurrency={false} />
                    <MetricRow label="Sortino Ratio" data={metrics.sortino_ratio} isCurrency={false} />
                    <MetricRow label="Total Trades" data={metrics.total_trades} isCurrency={false} />
                    <MetricRow label="Win Rate" data={metrics.win_rate} isCurrency={false} isPercent={true} />
                </tbody>
            </table>
        </div>
    );
};
