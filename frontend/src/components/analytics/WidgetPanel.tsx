import React from 'react';
import type { WidgetState } from './types';

interface WidgetPanelProps {
    widgets: WidgetState;
    setWidgets: (w: WidgetState) => void;
}

export const WidgetPanel: React.FC<WidgetPanelProps> = ({ widgets, setWidgets }) => {
    const toggle = (key: keyof WidgetState) => {
        setWidgets({ ...widgets, [key]: !widgets[key] });
    };

    return (
        <div className="bg-white dark:bg-white/5 p-4 rounded-2xl border border-gray-200 dark:border-gray-800 mb-6">
            <h3 className="text-xs font-bold uppercase text-scandi-muted mb-3 flex items-center gap-2">
                Customize Widgets
            </h3>
            <div className="flex flex-wrap gap-4">
                <label className="flex items-center gap-2 cursor-pointer select-none text-sm font-medium">
                    <input
                        type="checkbox"
                        checked={widgets.showEquityChart}
                        onChange={() => toggle('showEquityChart')}
                        className="rounded text-indigo-600 focus:ring-indigo-500 bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-700"
                    />
                    Equity Chart
                </label>
                <label className="flex items-center gap-2 cursor-pointer select-none text-sm font-medium">
                    <input
                        type="checkbox"
                        checked={widgets.showPerformance}
                        onChange={() => toggle('showPerformance')}
                        className="rounded text-indigo-600 focus:ring-indigo-500 bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-700"
                    />
                    Performance
                </label>
                <label className="flex items-center gap-2 cursor-pointer select-none text-sm font-medium">
                    <input
                        type="checkbox"
                        checked={widgets.showTradesAnalysis}
                        onChange={() => toggle('showTradesAnalysis')}
                        className="rounded text-indigo-600 focus:ring-indigo-500 bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-700"
                    />
                    Trades Analysis
                </label>
                <label className="flex items-center gap-2 cursor-pointer select-none text-sm font-medium">
                    <input
                        type="checkbox"
                        checked={widgets.showCapitalEfficiency}
                        onChange={() => toggle('showCapitalEfficiency')}
                        className="rounded text-indigo-600 focus:ring-indigo-500 bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-700"
                    />
                    Capital Efficiency
                </label>
                <label className="flex items-center gap-2 cursor-pointer select-none text-sm font-medium">
                    <input
                        type="checkbox"
                        checked={widgets.showRunupsDrawdowns}
                        onChange={() => toggle('showRunupsDrawdowns')}
                        className="rounded text-indigo-600 focus:ring-indigo-500 bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-700"
                    />
                    Run-ups & Drawdowns
                </label>
            </div>
        </div>
    );
};
