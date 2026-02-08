import React from 'react';
import type { AdvancedMetrics } from './types';

interface SummaryCardsProps {
    metrics: AdvancedMetrics;
}

export const SummaryCards: React.FC<SummaryCardsProps> = ({ metrics }) => {

    const formatCurrency = (val: number | string) => {
        if (typeof val === 'string') return val;
        return `₹${val.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    };

    return (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {/* 1. Total P&L */}
            <div className="bg-white dark:bg-white/5 p-4 rounded-2xl border border-gray-200 dark:border-gray-800">
                <p className="text-[10px] uppercase text-gray-500 font-bold mb-1">Total P&L</p>
                <div className="flex items-baseline gap-2">
                    <span className={`text-lg font-bold ${Number(metrics.net_pnl.all) >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                        {formatCurrency(metrics.net_pnl.all)}
                    </span>
                    {/* Add percentage return calculation later */}
                </div>
            </div>

            {/* 2. Max Drawdown */}
            <div className="bg-white dark:bg-white/5 p-4 rounded-2xl border border-gray-200 dark:border-gray-800">
                <p className="text-[10px] uppercase text-gray-500 font-bold mb-1">Max Drawdown</p>
                <span className="text-lg font-bold text-red-500">
                    {formatCurrency(metrics.max_drawdown.all)}
                </span>
            </div>

            {/* 3. Total Trades */}
            <div className="bg-white dark:bg-white/5 p-4 rounded-2xl border border-gray-200 dark:border-gray-800">
                <p className="text-[10px] uppercase text-gray-500 font-bold mb-1">Total Trades</p>
                <span className="text-lg font-bold text-gray-900 dark:text-gray-100">
                    {metrics.total_trades.all}
                </span>
            </div>

            {/* 4. Profitable Trades */}
            <div className="bg-white dark:bg-white/5 p-4 rounded-2xl border border-gray-200 dark:border-gray-800">
                <p className="text-[10px] uppercase text-gray-500 font-bold mb-1">Profitable Trades</p>
                <span className="text-lg font-bold text-green-500">
                    {/* Placeholder logic for count of winners */}
                    {metrics.win_rate.all !== 0 ? Math.round(Number(metrics.total_trades.all) * (Number(metrics.win_rate.all) / 100)) : '—'}
                </span>
            </div>

            {/* 5. Profit Factor */}
            <div className="bg-white dark:bg-white/5 p-4 rounded-2xl border border-gray-200 dark:border-gray-800">
                <p className="text-[10px] uppercase text-gray-500 font-bold mb-1">Profit Factor</p>
                <span className="text-lg font-bold text-indigo-500">
                    {metrics.profit_factor.all}
                </span>
            </div>
        </div>
    );
};
