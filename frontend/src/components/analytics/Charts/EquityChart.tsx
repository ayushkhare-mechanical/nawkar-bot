import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { AnalyticsTrade } from '../types';

interface EquityChartProps {
    trades: AnalyticsTrade[];
    initialCapital?: number;
}

export const EquityChart: React.FC<EquityChartProps> = ({ trades, initialCapital = 100000 }) => {
    // Generate equity curve data points
    const data = React.useMemo(() => {
        let currentEquity = initialCapital;
        const points = [{ name: 'Start', equity: initialCapital, time: '' }];

        trades.forEach((t) => {
            currentEquity += t.pnl;
            points.push({
                name: `Trade #${t.id}`,
                equity: currentEquity,
                time: t.exit_time
            });
        });
        return points;
    }, [trades, initialCapital]);

    const minEquity = Math.min(...data.map(d => d.equity));
    const maxEquity = Math.max(...data.map(d => d.equity));
    const domainPadding = (maxEquity - minEquity) * 0.1;

    return (
        <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                    <defs>
                        <linearGradient id="colorEquity" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" opacity={0.1} />
                    <XAxis
                        dataKey="name"
                        hide
                    />
                    <YAxis
                        domain={[minEquity - domainPadding, maxEquity + domainPadding]}
                        tick={{ fontSize: 10 }}
                        width={60}
                        axisLine={false}
                        tickLine={false}
                        tickFormatter={(val) => `₹${(val / 1000).toFixed(1)}k`}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                        itemStyle={{ color: '#fff' }}
                        formatter={(val: any) => [`₹${Number(val).toFixed(2)}`, 'Equity']}
                        labelStyle={{ display: 'none' }}
                    />
                    <Area
                        type="monotone"
                        dataKey="equity"
                        stroke="#6366f1"
                        fillOpacity={1}
                        fill="url(#colorEquity)"
                        strokeWidth={2}
                        animationDuration={500}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};
