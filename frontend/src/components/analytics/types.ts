export interface AnalyticsTrade {
    id: number;
    symbol: string;
    type: 'LONG' | 'SHORT';
    entry_time: string;
    exit_time: string;
    entry_price: number;
    exit_price: number;
    quantity: number;
    pnl: number;
    exit_reason: string;
    duration_bars: number;
    max_favorable_excursion?: number;
    max_adverse_excursion?: number;
    cumulative_pnl?: number;
}

export interface MetricSet {
    all: number | string;
    long: number | string;
    short: number | string;
}

export interface AdvancedMetrics {
    total_trades: MetricSet;
    win_rate: MetricSet;
    avg_pnl: MetricSet;
    profit_factor: MetricSet;
    sharpe_ratio: MetricSet;
    sortino_ratio: MetricSet;
    max_drawdown: MetricSet;
    net_pnl: MetricSet;
    gross_profit: MetricSet;
    gross_loss: MetricSet;
    commission: MetricSet;
    expected_payoff: MetricSet;
    cagr: MetricSet;
    return_on_capital: MetricSet;
}

export interface WidgetState {
    showEquityChart: boolean;
    showPerformance: boolean;
    showTradesAnalysis: boolean;
    showCapitalEfficiency: boolean;
    showRunupsDrawdowns: boolean;
}

// Helper to init default empty metrics
export const defaultMetrics: AdvancedMetrics = {
    total_trades: { all: 0, long: 0, short: 0 },
    win_rate: { all: 0, long: 0, short: 0 },
    avg_pnl: { all: 0, long: 0, short: 0 },
    profit_factor: { all: '-', long: '-', short: '-' },
    sharpe_ratio: { all: '-', long: '-', short: '-' },
    sortino_ratio: { all: '-', long: '-', short: '-' },
    max_drawdown: { all: 0, long: 0, short: 0 },
    net_pnl: { all: 0, long: 0, short: 0 },
    gross_profit: { all: 0, long: 0, short: 0 },
    gross_loss: { all: 0, long: 0, short: 0 },
    commission: { all: 0, long: 0, short: 0 },
    expected_payoff: { all: 0, long: 0, short: 0 },
    cagr: { all: 0, long: 0, short: 0 },
    return_on_capital: { all: 0, long: 0, short: 0 },
};
