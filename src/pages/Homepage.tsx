import { useState } from 'react';
import { AlertTriangle, Share2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export default function HomePage() {
    const [filter, setFilter] = useState('ALL');
    const { t } = useTranslation();

    const debunks = [
        {
            id: '1',
            claim: 'Viral WhatsApp audio claiming INEC postponed Osun governorship election to August 22.',
            fact: 'INEC confirms the Osun governorship election remains strictly scheduled for August 15, 2026. The audio is doctored.',
            verdict: 'FAKE NEWS',
            source: 'WhatsApp Forward',
            date: 'Aug 4, 2026',
        },
        {
            id: '2',
            claim: 'Image showing alleged violence at a campaign rally in Osogbo.',
            fact: 'Reverse image search proves the photo was taken during an election event in 2018, not 2026.',
            verdict: 'MISLEADING',
            source: 'X (Twitter)',
            date: 'Aug 3, 2026',
        }
    ];

    return (
        <div className="max-w-6xl mx-auto px-4 py-8">
            {/* Banner */}
            <div className="bg-gradient-to-r from-[#0E243F] to-[#071D38] border border-[#00B8C4]/30 rounded-2xl p-6 md:p-8 mb-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
                <div className="space-y-2 max-w-2xl">
                    <div className="inline-flex items-center gap-2 px-3 py-1 bg-[#E05A2B]/10 border border-[#E05A2B] rounded-full text-[#E05A2B] text-xs font-semibold">
                        <AlertTriangle className="w-3.5 h-3.5" />
                        {t('home.badge')}
                    </div>
                    <h1 className="text-2xl md:text-4xl font-extrabold text-white tracking-tight">
                        {t('home.title')}
                    </h1>
                    <p className="text-gray-300 text-sm md:text-base">
                        {t('home.subtitle')}
                    </p>
                </div>
            </div>

            {/* Filter Tabs */}
            <div className="flex items-center gap-2 overflow-x-auto w-full pb-2 mb-6">
                {['ALL', 'FAKE NEWS', 'MISLEADING', 'TFGBV'].map((tag) => (
                    <button
                        key={tag}
                        onClick={() => setFilter(tag)}
                        className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${filter === tag
                                ? 'bg-[#00B8C4] text-[#071D38]'
                                : 'bg-[#0E243F] text-gray-300 hover:bg-gray-800 border border-gray-700'
                            }`}
                    >
                        {tag}
                    </button>
                ))}
            </div>

            {/* Debunk Cards Grid */}
            <div className="grid md:grid-cols-2 gap-6">
                {debunks.map((card) => (
                    <div key={card.id} className="bg-[#0E243F] border border-gray-800 hover:border-[#00B8C4]/40 rounded-xl overflow-hidden shadow-lg flex flex-col justify-between">
                        <div className="p-6 space-y-4">
                            <div className="flex items-center justify-between">
                                <span className="px-2.5 py-1 bg-[#E05A2B]/20 text-[#E05A2B] border border-[#E05A2B]/40 text-xs font-bold rounded">
                                    {card.verdict}
                                </span>
                                <span className="text-xs text-gray-400">{card.date}</span>
                            </div>

                            <div>
                                <h4 className="text-xs font-bold uppercase tracking-wider text-[#E05A2B] mb-1">{t('home.claimed')}</h4>
                                <p className="text-white font-medium text-sm leading-relaxed">{card.claim}</p>
                            </div>

                            <div className="p-3 bg-[#071D38] rounded-lg border border-gray-800">
                                <h4 className="text-xs font-bold uppercase tracking-wider text-[#00B8C4] mb-1">{t('home.fact')}</h4>
                                <p className="text-gray-300 text-xs leading-relaxed">{card.fact}</p>
                            </div>
                        </div>

                        <div className="px-6 py-3 bg-[#071D38]/50 border-t border-gray-800/60 flex items-center justify-between">
                            <span className="text-xs text-gray-400">Source: <strong className="text-gray-200">{card.source}</strong></span>
                            <button
                                onClick={() => alert(`Share debunk #${card.id}`)}
                                className="inline-flex items-center gap-1.5 text-xs text-[#00B8C4] hover:underline font-semibold cursor-pointer"
                            >
                                <Share2 className="w-3.5 h-3.5" /> {t('home.share')}
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}