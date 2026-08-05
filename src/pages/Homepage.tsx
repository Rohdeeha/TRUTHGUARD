import { useState } from 'react';
import { Search, Filter, AlertTriangle, CheckCircle, HelpCircle, Share2, ArrowRight } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface DebunkItem {
    id: string;
    claim: string;
    verdict: 'FALSE' | 'MISLEADING' | 'VERIFIED' | 'UNVERIFIED';
    explanation: string;
    category: string;
    date: string;
    lga: string;
}

export default function HomePage() {
    const { t } = useTranslation();
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('All');

    // Dynamically pull translated debunk cards from i18n
    const debunksList = (t('debunkList', { returnObjects: true }) as DebunkItem[]) || [];

    const getVerdictBadge = (verdict: DebunkItem['verdict']) => {
        switch (verdict) {
            case 'FALSE':
                return (
                    <span className="inline-flex items-center gap-1 bg-rose-500/10 border border-rose-500/30 text-rose-400 font-black text-[10px] px-2.5 py-1 rounded-full uppercase tracking-wider">
                        <AlertTriangle className="w-3 h-3" /> {t('home.verdictFalse')}
                    </span>
                );
            case 'MISLEADING':
                return (
                    <span className="inline-flex items-center gap-1 bg-amber-500/10 border border-amber-500/30 text-amber-400 font-black text-[10px] px-2.5 py-1 rounded-full uppercase tracking-wider">
                        <AlertTriangle className="w-3 h-3" /> {t('home.verdictMisleading')}
                    </span>
                );
            case 'VERIFIED':
                return (
                    <span className="inline-flex items-center gap-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-black text-[10px] px-2.5 py-1 rounded-full uppercase tracking-wider">
                        <CheckCircle className="w-3 h-3" /> {t('home.verdictVerified')}
                    </span>
                );
            default:
                return (
                    <span className="inline-flex items-center gap-1 bg-gray-500/10 border border-gray-500/30 text-gray-400 font-black text-[10px] px-2.5 py-1 rounded-full uppercase tracking-wider">
                        <HelpCircle className="w-3 h-3" /> {t('home.verdictUnverified')}
                    </span>
                );
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
            {/* Hero Header */}
            <div className="text-center max-w-3xl mx-auto space-y-4">
                <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                    {t('home.heroTitle')}
                </h1>
                <p className="text-gray-400 text-sm sm:text-base leading-relaxed">
                    {t('home.heroSubtitle')}
                </p>
            </div>

            {/* Search & Filter Section */}
            <div className="bg-[#0E243F] border border-gray-800 rounded-2xl p-4 sm:p-6 space-y-4 shadow-xl">
                <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder={t('home.searchPlaceholder')}
                        className="w-full bg-[#071D38] border border-gray-700 text-white pl-12 pr-4 py-3 rounded-xl focus:border-[#00B8C4] focus:ring-1 focus:ring-[#00B8C4] outline-none text-sm transition-all"
                    />
                </div>

                {/* Categories */}
                <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
                    <Filter className="w-4 h-4 text-[#00B8C4] shrink-0" />
                    {[
                        { id: 'All', label: t('home.filterAll') },
                        { id: 'Election Day', label: t('home.filterElectionDay') },
                        { id: 'Candidates', label: t('home.filterCandidates') },
                        { id: 'INEC & BVAS', label: t('home.filterINEC') },
                        { id: 'Security', label: t('home.filterSecurity') },
                    ].map((cat) => (
                        <button
                            key={cat.id}
                            onClick={() => setSelectedCategory(cat.id)}
                            className={`px-3 py-1.5 rounded-lg font-bold transition-all whitespace-nowrap cursor-pointer ${selectedCategory === cat.id
                                    ? 'bg-[#00B8C4] text-[#071D38]'
                                    : 'bg-[#071D38] text-gray-400 hover:text-white border border-gray-800'
                                }`}
                        >
                            {cat.label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Debunks List - 100% Multilingual */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Array.isArray(debunksList) && debunksList.map((item) => (
                    <div
                        key={item.id}
                        className="bg-[#0E243F] border border-gray-800 hover:border-gray-700 rounded-2xl p-6 flex flex-col justify-between transition-all hover:shadow-xl space-y-4"
                    >
                        <div className="space-y-3">
                            <div className="flex items-center justify-between text-xs text-gray-400">
                                <span className="font-semibold text-[#00B8C4] bg-[#071D38] px-2.5 py-1 rounded-md border border-gray-800">
                                    {item.lga}
                                </span>
                                <span>{item.date}</span>
                            </div>

                            <div>{getVerdictBadge(item.verdict)}</div>

                            <h3 className="text-base font-bold text-white leading-snug">
                                "{item.claim}"
                            </h3>

                            <p className="text-xs text-gray-300 leading-relaxed border-t border-gray-800/60 pt-3">
                                {item.explanation}
                            </p>
                        </div>

                        <div className="pt-2 flex items-center justify-between border-t border-gray-800/80 text-xs">
                            <button className="text-[#00B8C4] hover:underline font-bold flex items-center gap-1">
                                {t('home.shareDebunk')} <Share2 className="w-3.5 h-3.5" />
                            </button>
                            <button className="text-gray-400 hover:text-white flex items-center gap-1 font-semibold">
                                {t('home.readFullAnalysis')} <ArrowRight className="w-3.5 h-3.5" />
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}