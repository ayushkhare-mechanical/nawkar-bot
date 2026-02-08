import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { AnalyticsTrade } from '../types';

interface EquityChartProps {
    trades: AnalyticsTrade[];
    initialCapital: number;
}

export const EquityChart: React.FC<EquityChartProps> = ({ trades, initialCapital }) => {
    // Transform trades into equity data
    const data = React.useMemo(() => {
        let currentEquity = initialCapital;
        const points = trades.map(t => {
            currentEquity += t.pnl;
            return {
                time: t.exit_time,
                equity: currentEquity,
                pnl: t.pnl
            };
        });

        // Add start point
        return [{ time: 'Start', equity: initialCapital, pnl: 0 }, ...points];
    }, [trades, initialCapital]);

    if (trades.length === 0) return null;

    return (
        <div className="bg-white dark:bg-white/5 rounded-3xl border border-gray-200 dark:border-gray-800 p-6 h-80">
            <h3 className="text-sm font-bold uppercase text-gray-500 mb-4">Equity Curve</h3>
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                    <defs>
                        <linearGradient id="colorEquity" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" opacity={0.1} />
                    <XAxis dataKey="time" hide />
                    <YAxis
                        tick={{ fontSize: 10 }}
                        width={60}
                        axisLine={false}
                        tickLine={false}
                        tickFormatter={(val) => `₹${(val / 1000).toFixed(1)}k`}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                        itemStyle={{ color: '#fff' }}
                        formatter={(val: number) => [`₹${val.toLocaleString()}`, 'Equity']}
                        labelStyle={{ display: 'none' }}
                    />
                    <Area type="monotone" dataKey="equity" stroke="#6366f1" fillOpacity={1} fill="url(#colorEquity)" strokeWidth={2} />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};
