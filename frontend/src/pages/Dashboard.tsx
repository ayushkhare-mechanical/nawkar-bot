import { useEffect, useState } from 'react';
import { Layout } from '../Layout';

// Define interface for API response
interface MonitorData {
    authenticated: boolean;
    user_profile?: {
        name: string;
        fy_id: string;
        email: string;
        mobile_number: string;
    };
    features: Array<{ name: string; status: string; icon: string }>;
}

export const Dashboard = () => {
    const [data, setData] = useState<MonitorData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/v1/monitor/data')
            .then(res => res.json())
            .then(data => {
                setData(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    if (loading) return (
        <Layout>
            <div className="flex items-center justify-center h-[80vh]">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-scandi-accents"></div>
            </div>
        </Layout>
    );

    if (!data?.authenticated) {
        return (
            <Layout>
                <div className="text-center py-20">
                    <h2 className="text-2xl font-bold mb-4">Authentication Required</h2>
                    <a href="/api/v1/auth/login" className="btn-pill bg-scandi-accents text-white">Connect Fyers</a>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="max-w-7xl mx-auto px-4 py-12">
                <header className="mb-12 flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
                        <p className="text-scandi-muted">Welcome back, {data.user_profile?.name}</p>
                    </div>
                    <div className="flex gap-4">
                        <div className="bg-green-100 text-green-700 px-4 py-1 rounded-full text-sm font-medium">
                            {data.user_profile?.fy_id}
                        </div>
                    </div>
                </header>

                <div className="grid md:grid-cols-3 gap-6">
                    {/* Status Card 1 */}
                    <div className="bg-white dark:bg-white/5 p-6 rounded-3xl border border-gray-200 dark:border-gray-800">
                        <h3 className="text-sm font-bold uppercase text-scandi-muted mb-4">Account Balance</h3>
                        <div className="text-3xl font-bold">₹0.00</div>
                    </div>

                    {/* Status Card 2 */}
                    <div className="bg-white dark:bg-white/5 p-6 rounded-3xl border border-gray-200 dark:border-gray-800">
                        <h3 className="text-sm font-bold uppercase text-scandi-muted mb-4">Active Strategies</h3>
                        <div className="text-3xl font-bold">0</div>
                    </div>

                    {/* Status Card 3 */}
                    <div className="bg-white dark:bg-white/5 p-6 rounded-3xl border border-gray-200 dark:border-gray-800">
                        <h3 className="text-sm font-bold uppercase text-scandi-muted mb-4">Today's P&L</h3>
                        <div className="text-3xl font-bold text-green-500">+₹0.00</div>
                    </div>
                </div>

                <div className="mt-12">
                    <h2 className="text-xl font-bold mb-6">System Status</h2>
                    <div className="grid md:grid-cols-3 gap-6">
                        {data.features?.map((f, i) => (
                            <div key={i} className="flex items-center gap-4 bg-white dark:bg-white/5 p-4 rounded-xl border border-gray-200 dark:border-gray-800">
                                <div className="p-2 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 rounded-lg">
                                    {/* Icon placeholder logic could go here */}
                                    ⚡
                                </div>
                                <div>
                                    <div className="font-semibold">{f.name}</div>
                                    <div className="text-xs text-green-500 font-medium">● {f.status}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </Layout>
    );
};
