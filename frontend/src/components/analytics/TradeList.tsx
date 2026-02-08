import React, { useState, useMemo } from 'react';
import type { AnalyticsTrade } from './types';

interface TradeListProps {
    trades: AnalyticsTrade[];
}

type SortField = 'id' | 'type' | 'entry_time' | 'pnl' | 'entry_price' | 'exit_price';

export const TradeList: React.FC<TradeListProps> = ({ trades }) => {
    const [sortField, setSortField] = useState<SortField>('id');
    const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

    const handleSort = (field: SortField) => {
        if (sortField === field) {
            setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
        } else {
            setSortField(field);
            setSortDirection('desc');
        }
    };

    const sortedTrades = useMemo(() => {
        return [...trades].sort((a, b) => {
            const valA = a[sortField];
            const valB = b[sortField];

            // Handle strings (dates/types)
            if (typeof valA === 'string' && typeof valB === 'string') {
                return sortDirection === 'asc'
                    ? valA.localeCompare(valB)
                    : valB.localeCompare(valA);
            }

            // Handle numbers
            if (valA < valB) return sortDirection === 'asc' ? -1 : 1;
            if (valA > valB) return sortDirection === 'asc' ? 1 : -1;
            return 0;
        });
    }, [trades, sortField, sortDirection]);

    const SortIcon = ({ field }: { field: SortField }) => {
        if (sortField !== field) return <span className="text-gray-300 ml-1">⇅</span>;
        return <span className="text-indigo-600 ml-1">{sortDirection === 'asc' ? '↑' : '↓'}</span>;
    };

    return (
        <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
                <thead>
                    <tr className="bg-gray-50 dark:bg-white/5 text-xs font-bold text-gray-500 uppercase border-b border-gray-200 dark:border-gray-800">
                        <th
                            className="px-6 py-4 cursor-pointer hover:text-indigo-600 transition-colors"
                            onClick={() => handleSort('id')}
                        >
                            Trade # <SortIcon field="id" />
                        </th>
                        <th
                            className="px-6 py-4 cursor-pointer hover:text-indigo-600 transition-colors"
                            onClick={() => handleSort('type')}
                        >
                            Type <SortIcon field="type" />
                        </th>
                        <th
                            className="px-6 py-4 cursor-pointer hover:text-indigo-600 transition-colors"
                            onClick={() => handleSort('entry_time')}
                        >
                            Date & Time <SortIcon field="entry_time" />
                        </th>
                        <th className="px-6 py-4">
                            Signal
                        </th>
                        <th
                            className="px-6 py-4 cursor-pointer hover:text-indigo-600 transition-colors text-right"
                            onClick={() => handleSort('entry_price')}
                        >
                            Price <SortIcon field="entry_price" />
                        </th>
                        <th className="px-6 py-4 text-right">
                            Size
                        </th>
                        <th
                            className="px-6 py-4 cursor-pointer hover:text-indigo-600 transition-colors text-right"
                            onClick={() => handleSort('pnl')}
                        >
                            Net P&L <SortIcon field="pnl" />
                        </th>
                        <th className="px-6 py-4 text-right hidden md:table-cell">
                            Cum. P&L
                        </th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-white/5">
                    {sortedTrades.map((t) => (
                        <tr key={t.id} className="text-sm hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                            <td className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">{t.id}</td>
                            <td className="px-6 py-4">
                                <span className={`px-2 py-1 rounded text-xs font-bold ${t.type === 'LONG'
                                        ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                                        : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                                    }`}>
                                    {t.type}
                                </span>
                            </td>
                            <td className="px-6 py-4 text-gray-600 dark:text-gray-400 whitespace-nowrap">
                                {t.entry_time.replace('T', ' ')}
                            </td>
                            <td className="px-6 py-4 text-xs italic text-gray-500">
                                {t.exit_reason}
                            </td>
                            <td className="px-6 py-4 text-right font-mono">
                                <div className="text-gray-900 dark:text-gray-100">₹{t.entry_price.toFixed(2)}</div>
                                <div className="text-xs text-gray-400">→ ₹{t.exit_price.toFixed(2)}</div>
                            </td>
                            <td className="px-6 py-4 text-right font-mono">
                                {t.quantity}
                            </td>
                            <td className={`px-6 py-4 text-right font-bold font-mono ${t.pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                                {t.pnl >= 0 ? '+' : ''}{t.pnl.toFixed(2)}
                            </td>
                            <td className="px-6 py-4 text-right font-mono text-gray-400 hidden md:table-cell">
                                —
                            </td>
                        </tr>
                    ))}
                    {sortedTrades.length === 0 && (
                        <tr>
                            <td colSpan={8} className="px-6 py-12 text-center text-gray-500 italic">
                                No trades found matching criteria.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};
