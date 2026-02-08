import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';
import type { AnalyticsTrade } from '../types';

interface PnLChartProps {
    trades: AnalyticsTrade[];
}

export const PnLChart: React.FC<PnLChartProps> = ({ trades }) => {
    return (
        <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trades}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" opacity={0.1} />
                    <XAxis dataKey="id" hide />
                    <YAxis
                        tick={{ fontSize: 10 }}
                        width={40}
                        axisLine={false}
                        tickLine={false}
                    />
                    <Tooltip
                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                        contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                        formatter={(val: any) => [`₹${Number(val).toFixed(2)}`, 'PnL']}
                        labelFormatter={(label) => `Trade #${label}`}
                    />
                    <ReferenceLine y={0} stroke="#4b5563" />
                    <Bar dataKey="pnl" radius={[2, 2, 0, 0]}>
                        {trades.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.pnl >= 0 ? '#22c55e' : '#ef4444'} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};
