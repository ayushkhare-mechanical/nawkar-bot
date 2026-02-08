import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { AnalyticsTrade } from '../types';

interface PnLDistributionProps {
    trades: AnalyticsTrade[];
}

export const PnLDistribution: React.FC<PnLDistributionProps> = ({ trades }) => {
    // Generate buckets for PnL
    const data = React.useMemo(() => {
        if (trades.length === 0) return [];

        // Simple bucketing logic - sort trades by PnL
        const sorted = [...trades].sort((a, b) => a.pnl - b.pnl);

        // Just return individual trade bars for now, specialized by color
        return sorted.map((t, i) => ({
            id: t.id,
            pnl: t.pnl,
            color: t.pnl >= 0 ? '#22c55e' : '#ef4444'
        }));
    }, [trades]);

    if (trades.length === 0) return null;

    return (
        <div className="bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-gray-800 p-6 h-80">
            <h3 className="text-sm font-bold uppercase text-gray-500 mb-4">PnL Distribution</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" opacity={0.1} />
                    <XAxis dataKey="id" hide />
                    <YAxis
                        tick={{ fontSize: 10 }}
                        width={40}
                        axisLine={false}
                        tickLine={false}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                        itemStyle={{ color: '#fff' }}
                        formatter={(val: number) => [`₹${val.toFixed(2)}`, 'PnL']}
                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                    />
                    <Bar dataKey="pnl">
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};
