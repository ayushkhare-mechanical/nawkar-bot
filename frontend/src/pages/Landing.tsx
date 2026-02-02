import { useEffect, useState } from 'react';
import { ArrowRight, Zap, Shield, LayoutDashboard } from 'lucide-react';
import { Layout } from '../Layout';

export const Landing = () => {
    const [authenticated, setAuthenticated] = useState(false);

    useEffect(() => {
        // Check auth status
        fetch('/api/v1/auth/status')
            .then(res => res.json())
            .then(data => setAuthenticated(data.authenticated))
            .catch(err => console.error("Auth check failed", err));
    }, []);

    return (
        <Layout>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">

                {/* Hero Section */}
                <section className="text-center max-w-3xl mx-auto mb-24">
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-8">
                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                        System Online v2.4
                    </div>

                    <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6 leading-tight">
                        Algo Trading, <br />
                        <span className="text-scandi-accents">Simplified.</span>
                    </h1>

                    <p className="text-lg text-scandi-muted dark:text-gray-400 mb-10 leading-relaxed">
                        Professional-grade execution engine for retail traders.
                        Automate your strategies on Fyers with ultra-low latency and built-in risk management.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        {authenticated ? (
                            <a href="/dashboard" className="btn-pill bg-scandi-accents text-white hover:bg-indigo-600 shadow-lg shadow-indigo-500/20 inline-flex items-center justify-center gap-2 text-lg px-8 py-3">
                                Launch Dashboard <ArrowRight size={20} />
                            </a>
                        ) : (
                            <a href="/api/v1/auth/login" target="_blank" rel="noopener noreferrer" className="btn-pill bg-scandi-accents text-white hover:bg-indigo-600 shadow-lg shadow-indigo-500/20 inline-flex items-center justify-center gap-2 text-lg px-8 py-3">
                                Connect Fyers <Zap size={20} />
                            </a>
                        )}

                    </div>
                </section>



                {/* Manual Token Entry (Local Dev Helper) - Only show if NOT authenticated */}
                {!authenticated && (
                    <div className="max-w-md mx-auto mb-20 p-6 bg-gray-50 dark:bg-white/5 rounded-2xl border border-dashed border-gray-300 dark:border-gray-700">
                        <h3 className="text-sm font-semibold text-scandi-muted uppercase tracking-wider mb-4 text-center">
                            Local Authentication
                        </h3>
                        <form onSubmit={(e) => {
                            e.preventDefault();
                            const input = (e.target as any).elements.tokenParams.value;
                            if (!input) return;

                            fetch('/api/v1/auth/manual', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ access_token: input })
                            })
                                .then(res => res.json())
                                .then(data => {
                                    if (data.success) {
                                        window.location.reload();
                                    } else {
                                        alert("Error: " + data.message);
                                    }
                                })
                                .catch(err => {
                                    console.error(err);
                                    alert("Failed to save token");
                                });
                        }}>
                            <div className="flex gap-2">
                                <input
                                    name="tokenParams"
                                    type="text"
                                    placeholder="Paste Redirect URL (auth_code=...)"
                                    className="flex-1 px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-black text-sm focus:outline-none focus:ring-2 focus:ring-scandi-accents"
                                />
                                <button type="submit" className="px-4 py-2 bg-gray-900 dark:bg-white text-white dark:text-black rounded-lg text-sm font-medium hover:bg-gray-800 dark:hover:bg-gray-200">
                                    Save
                                </button>
                            </div>
                            <p className="text-xs text-center mt-3 text-scandi-muted">
                                1. Click "Connect Fyers" (opens new tab). <br />
                                2. Login & Copy the resulting URL. <br />
                                3. Paste it here to auth locally.
                            </p>
                        </form>
                    </div>
                )}

                {/* Features */}
                <section className="grid md:grid-cols-3 gap-8">
                    <FeatureCard
                        icon={<Zap className="text-yellow-500" />}
                        title="Smart Execution"
                        desc="Intelligent order slicing to minimize impact cost. Our engine detects liquidity pockets automatically."
                    />
                    <FeatureCard
                        icon={<Shield className="text-green-500" />}
                        title="Risk Guard"
                        desc="Automated circuit breakers. Set your daily max loss and let the system protect your capital."
                    />
                    <FeatureCard
                        icon={<LayoutDashboard className="text-pink-500" />}
                        title="Strategy Hub"
                        desc="Deploy multiple Python strategies. Monitor signals and P&L in real-time from one unified dashboard."
                    />
                </section>

            </div>

            <footer className="border-t border-gray-200 dark:border-gray-800 py-12 text-center text-sm text-scandi-muted">
                &copy; 2026 Nawkar Systems. Scandinavian Design by Antigravity.
            </footer>
        </Layout>
    );
};

const FeatureCard = ({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) => (
    <div className="p-8 rounded-3xl bg-white dark:bg-white/5 border border-gray-100 dark:border-gray-800 hover:shadow-xl transition-shadow duration-300">
        <div className="w-12 h-12 rounded-2xl bg-gray-50 dark:bg-white/10 flex items-center justify-center mb-6 text-2xl">
            {icon}
        </div>
        <h3 className="text-xl font-bold mb-3">{title}</h3>
        <p className="text-scandi-muted leading-relaxed">
            {desc}
        </p>
    </div>
);
