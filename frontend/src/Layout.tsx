import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';

export const Layout = ({ children }: { children: React.ReactNode }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <div className="min-h-screen bg-scandi-bg dark:bg-scandi-dark text-scandi-text dark:text-gray-100 font-poppins transition-colors duration-300">
            <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-white/70 dark:bg-black/50 border-b border-gray-200/50 dark:border-gray-800/50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">

                        {/* Logo */}
                        <Link to="/" className="text-2xl font-bold tracking-tight">
                            NAWKAR<span className="text-scandi-accents">.</span>
                        </Link>

                        {/* Desktop Menu */}
                        <div className="hidden md:flex items-center space-x-8">
                            <Link to="/" className="text-sm font-medium hover:text-scandi-accents transition-colors">Features</Link>
                            <Link to="/" className="text-sm font-medium hover:text-scandi-accents transition-colors">Pricing</Link>
                            <Link to="/api/v1/auth/login" className="btn-pill bg-scandi-text text-white hover:bg-black dark:bg-white dark:text-black dark:hover:bg-gray-200">
                                Connect Fyers
                            </Link>
                        </div>

                        {/* Mobile Menu Button */}
                        <div className="md:hidden flex items-center">
                            <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="p-2">
                                {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Mobile Menu */}
                {isMenuOpen && (
                    <div className="md:hidden bg-white/95 dark:bg-black/95 backdrop-blur-xl absolute top-16 w-full border-b border-gray-200 dark:border-gray-800">
                        <div className="px-4 pt-2 pb-6 space-y-4">
                            <Link to="/" className="block py-2 font-medium">Features</Link>
                            <Link to="/" className="block py-2 font-medium">Pricing</Link>
                            <a href="/api/v1/auth/login" className="block w-full text-center btn-pill bg-scandi-text text-white">
                                Connect Broker
                            </a>
                        </div>
                    </div>
                )}
            </nav>

            <main className="pt-20">
                {children}
            </main>
        </div>
    );
};
