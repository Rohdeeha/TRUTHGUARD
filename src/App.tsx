import { useState } from 'react';
import { Shield, FileText, Globe, LayoutDashboard } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import HomePage from './pages/Homepage';
import ReportPage from './pages/ReportPage';
import DashboardPage from './pages/DashboardPage';

export default function App() {
    const [activeTab, setActiveTab] = useState<'home' | 'report' | 'dashboard'>('home');
    const { t, i18n } = useTranslation();

    const changeLanguage = (lang: string) => {
        i18n.changeLanguage(lang);
    };

    return (
        <div className="min-h-screen bg-[#071D38] text-white flex flex-col font-sans">
            {/* Header */}
            <header className="border-b border-gray-800 bg-[#0E243F] sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2 cursor-pointer shrink-0" onClick={() => setActiveTab('home')}>
                        <div className="w-9 h-9 bg-[#0B131D] border-2 border-[#00B8C4] rounded-lg flex items-center justify-center">
                            <Shield className="w-5 h-5 text-[#00B8C4]" />
                        </div>
                        <div>
                            <span className="text-base sm:text-lg font-black tracking-wider text-[#00B8C4]">TRUTH<span className="text-white">GUARD</span></span>
                            <span className="text-[9px] block text-gray-400 font-semibold uppercase tracking-widest -mt-1">{t('nav.tagline')}</span>
                        </div>
                    </div>

                    <div className="flex items-center gap-2 overflow-x-auto">
                        <nav className="flex items-center gap-1 bg-[#071D38] p-1 rounded-lg border border-gray-800 shrink-0">
                            <button
                                onClick={() => setActiveTab('home')}
                                className={`px-2.5 py-1.5 text-xs font-semibold rounded-md transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${activeTab === 'home' ? 'bg-[#00B8C4] text-[#071D38]' : 'text-gray-300 hover:text-white'
                                    }`}
                            >
                                <FileText className="w-3.5 h-3.5" /> {t('nav.debunks')}
                            </button>
                            <button
                                onClick={() => setActiveTab('report')}
                                className={`px-2.5 py-1.5 text-xs font-semibold rounded-md transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${activeTab === 'report' ? 'bg-[#E05A2B] text-white' : 'text-gray-300 hover:text-white'
                                    }`}
                            >
                                <Shield className="w-3.5 h-3.5" /> {t('nav.report')}
                            </button>
                            <button
                                onClick={() => setActiveTab('dashboard')}
                                className={`px-2.5 py-1.5 text-xs font-semibold rounded-md transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${activeTab === 'dashboard' ? 'bg-[#00B8C4] text-[#071D38]' : 'text-gray-300 hover:text-white'
                                    }`}
                            >
                                <LayoutDashboard className="w-3.5 h-3.5" /> Situation Room
                            </button>
                        </nav>

                        {/* Language Selector */}
                        <div className="flex items-center gap-1 bg-[#071D38] px-2 py-1 rounded border border-gray-800 text-xs shrink-0">
                            <Globe className="w-3.5 h-3.5 text-[#00B8C4]" />
                            {[
                                { code: 'en', label: 'EN' },
                                { code: 'yo', label: 'YO' },
                                { code: 'pcm', label: 'PCM' }
                            ].map((lang) => (
                                <button
                                    key={lang.code}
                                    onClick={() => changeLanguage(lang.code)}
                                    className={`px-1.5 py-0.5 rounded font-bold cursor-pointer transition-colors ${i18n.language === lang.code ? 'bg-[#00B8C4] text-[#071D38]' : 'text-gray-400 hover:text-white'
                                        }`}
                                >
                                    {lang.label}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </header>
            {/* Main View Area */}
            <main className="flex-1">
                {activeTab === 'home' && <HomePage />}
                {activeTab === 'report' && <ReportPage />}
                {activeTab === 'dashboard' && <DashboardPage />}
            </main>

            {/* Footer */}
            <footer className="border-t border-gray-800 bg-[#0E243F] py-6 text-center text-xs text-gray-400">
                <p>© 2026 TruthGuard Initiative · FactCheck Africa / BallotEyes Working Group</p>
            </footer>
        </div>
    );
}