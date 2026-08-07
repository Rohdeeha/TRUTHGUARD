import { useState } from 'react';
import {
    Shield,
    Share2,
    AlertTriangle,
    CheckCircle2,
    XCircle,
    Search,
    Filter,
    Clock,
    FileText,
    Radio
} from 'lucide-react';
import BroadcastModal from '../components/BroadcastModal';

export interface DashboardReport {
    id: string;
    title: string;
    claim: string;
    verdict: 'FALSE' | 'MISLEADING' | 'VERIFIED' | 'PENDING';
    category: 'INEC' | 'Election Day' | 'Candidates' | 'Security';
    location: string;
    timestamp: string;
    summary: string;
    broadcasted?: boolean;
}

const INITIAL_REPORTS: DashboardReport[] = [
    {
        id: '101',
        title: 'INEC Postpones Osun 2026 Election Date Due to Security Concerns',
        claim: 'Viral audio claims voting has been delayed by 2 weeks.',
        verdict: 'FALSE',
        category: 'INEC',
        location: 'Osogbo LGA',
        timestamp: '10 mins ago',
        summary: 'INEC Resident Electoral Commissioner confirmed the official election timetable remains unchanged.',
        broadcasted: true,
    },
    {
        id: '102',
        title: 'Video Showing Supposed BVAS Malfunction at Ward 4',
        claim: 'Social media video shows BVAS rejecting all voter cards at Ward 4.',
        verdict: 'MISLEADING',
        category: 'Election Day',
        location: 'Ilesa East',
        timestamp: '25 mins ago',
        summary: 'The video was recorded during a routine technician test run 3 days prior to polling day.',
        broadcasted: false,
    },
    {
        id: '103',
        title: 'Security Agent Blocking Access to Polling Station 008',
        claim: 'Voters reporting armed men preventing entry at Ward 2, Polling Unit 008.',
        verdict: 'PENDING',
        category: 'Security',
        location: 'Ede North',
        timestamp: '40 mins ago',
        summary: 'Verification team currently contacting ground monitors and police liaison in Ede North.',
        broadcasted: false,
    },
    {
        id: '104',
        title: 'Official List of Accredited Election Observers Published',
        claim: 'Document listing 45 international and local observer groups for Osun 2026.',
        verdict: 'VERIFIED',
        category: 'Candidates',
        location: 'Statewide',
        timestamp: '1 hour ago',
        summary: 'INEC officially released the verified registry of accredited domestic and international monitoring organizations.',
        broadcasted: true,
    },
];

export default function DashboardPage() {
    const [reports, setReports] = useState<DashboardReport[]>(INITIAL_REPORTS);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedFilter, setSelectedFilter] = useState<string>('ALL');
    const [selectedReportForBroadcast, setSelectedReportForBroadcast] = useState<DashboardReport | null>(null);

    // Update verdict dynamically from admin control
    const handleVerdictChange = (id: string, newVerdict: DashboardReport['verdict']) => {
        setReports((prev) =>
            prev.map((item) => (item.id === id ? { ...item, verdict: newVerdict } : item))
        );
    };

    // Filtered reports logic
    const filteredReports = reports.filter((item) => {
        const matchesSearch =
            item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.claim.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.location.toLowerCase().includes(searchQuery.toLowerCase());

        const matchesFilter =
            selectedFilter === 'ALL' ||
            (selectedFilter === 'PENDING' && item.verdict === 'PENDING') ||
            (selectedFilter === 'VERIFIED' && item.verdict !== 'PENDING');

        return matchesSearch && matchesFilter;
    });

    // Analytics Counters
    const totalCount = reports.length;
    const pendingCount = reports.filter((r) => r.verdict === 'PENDING').length;
    const debunkedCount = reports.filter((r) => r.verdict === 'FALSE' || r.verdict === 'MISLEADING').length;
    const broadcastedCount = reports.filter((r) => r.broadcasted).length;

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-8">

            {/* Control Room Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#1A3352] pb-6">
                <div>
                    <div className="flex items-center gap-2 text-[#1CB5BE] font-bold text-xs uppercase tracking-wider mb-1">
                        <Radio className="w-4 h-4 animate-pulse text-emerald-400" />
                        <span>Situation Room Control Panel</span>
                    </div>
                    <h1 className="text-2xl sm:text-3xl font-black text-white">
                        Incident Verification & Social Dispatch
                    </h1>
                </div>

                <div className="flex items-center gap-3">
                    <span className="bg-[#061528] border border-[#1A3352] text-gray-300 text-xs px-3 py-2 rounded-xl flex items-center gap-2">
                        <Clock className="w-3.5 h-3.5 text-[#1CB5BE]" />
                        Live Syncing
                    </span>
                </div>
            </div>

            {/* Analytics KPI Cards */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-[#0E243F] border border-[#1A3352] p-4 rounded-2xl flex items-center justify-between shadow-lg">
                    <div>
                        <p className="text-xs text-gray-400 font-bold uppercase">Total Incident Reports</p>
                        <h3 className="text-2xl font-black text-white mt-1">{totalCount}</h3>
                    </div>
                    <div className="p-3 bg-[#061528] rounded-xl text-[#1CB5BE]">
                        <FileText className="w-5 h-5" />
                    </div>
                </div>

                <div className="bg-[#0E243F] border border-[#1A3352] p-4 rounded-2xl flex items-center justify-between shadow-lg">
                    <div>
                        <p className="text-xs text-gray-400 font-bold uppercase">Pending Verification</p>
                        <h3 className="text-2xl font-black text-amber-400 mt-1">{pendingCount}</h3>
                    </div>
                    <div className="p-3 bg-[#061528] rounded-xl text-amber-400">
                        <Clock className="w-5 h-5" />
                    </div>
                </div>

                <div className="bg-[#0E243F] border border-[#1A3352] p-4 rounded-2xl flex items-center justify-between shadow-lg">
                    <div>
                        <p className="text-xs text-gray-400 font-bold uppercase">Debunked Claims</p>
                        <h3 className="text-2xl font-black text-rose-400 mt-1">{debunkedCount}</h3>
                    </div>
                    <div className="p-3 bg-[#061528] rounded-xl text-rose-400">
                        <Shield className="w-5 h-5" />
                    </div>
                </div>

                <div className="bg-[#0E243F] border border-[#1A3352] p-4 rounded-2xl flex items-center justify-between shadow-lg">
                    <div>
                        <p className="text-xs text-gray-400 font-bold uppercase">Multi-Broadcasted</p>
                        <h3 className="text-2xl font-black text-emerald-400 mt-1">{broadcastedCount}</h3>
                    </div>
                    <div className="p-3 bg-[#061528] rounded-xl text-emerald-400">
                        <Share2 className="w-5 h-5" />
                    </div>
                </div>
            </div>

            {/* Search & Status Filters */}
            <div className="bg-[#0E243F] border border-[#1A3352] p-4 rounded-2xl shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
                <div className="relative w-full md:w-96">
                    <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search reports by ID, claim, location..."
                        className="w-full bg-[#061528] border border-[#1A3352] rounded-xl pl-10 pr-4 py-2.5 text-xs text-white focus:outline-none focus:border-[#1CB5BE] placeholder-gray-500"
                    />
                </div>

                <div className="flex items-center gap-2 w-full md:w-auto overflow-x-auto text-xs">
                    <Filter className="w-4 h-4 text-[#1CB5BE] shrink-0" />
                    {[
                        { id: 'ALL', label: 'All Reports' },
                        { id: 'PENDING', label: 'Pending Review' },
                        { id: 'VERIFIED', label: 'Fact-Checked' },
                    ].map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setSelectedFilter(tab.id)}
                            className={`px-3 py-2 rounded-xl font-bold whitespace-nowrap transition-all cursor-pointer ${selectedFilter === tab.id
                                    ? 'bg-[#1CB5BE] text-[#061528]'
                                    : 'bg-[#061528] text-gray-300 border border-[#1A3352] hover:text-white'
                                }`}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Reports Table / Management Cards */}
            <div className="space-y-4">
                {filteredReports.map((report) => (
                    <div
                        key={report.id}
                        className="bg-[#0E243F] border border-[#1A3352] rounded-2xl p-5 hover:border-[#1CB5BE]/40 transition-all shadow-lg flex flex-col lg:flex-row lg:items-center justify-between gap-6"
                    >
                        {/* Report Content Details */}
                        <div className="space-y-2 max-w-3xl">
                            <div className="flex flex-wrap items-center gap-2">
                                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-[#061528] text-[#1CB5BE] border border-[#1A3352]">
                                    #{report.id} • {report.category}
                                </span>

                                <span className="text-xs text-gray-400 font-medium">
                                    {report.location} • {report.timestamp}
                                </span>

                                {/* Status Indicator */}
                                {report.verdict === 'FALSE' && (
                                    <span className="inline-flex items-center gap-1 text-[10px] font-black px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 border border-rose-500/30">
                                        <XCircle className="w-3 h-3" /> FALSE
                                    </span>
                                )}
                                {report.verdict === 'MISLEADING' && (
                                    <span className="inline-flex items-center gap-1 text-[10px] font-black px-2 py-0.5 rounded bg-[#E55322]/20 text-[#E55322] border border-[#E55322]/30">
                                        <AlertTriangle className="w-3 h-3" /> MISLEADING
                                    </span>
                                )}
                                {report.verdict === 'VERIFIED' && (
                                    <span className="inline-flex items-center gap-1 text-[10px] font-black px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                                        <CheckCircle2 className="w-3 h-3" /> VERIFIED TRUE
                                    </span>
                                )}
                                {report.verdict === 'PENDING' && (
                                    <span className="inline-flex items-center gap-1 text-[10px] font-black px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">
                                        <Clock className="w-3 h-3" /> PENDING REVIEW
                                    </span>
                                )}
                            </div>

                            <h3 className="text-base font-bold text-white leading-snug">
                                {report.title}
                            </h3>

                            <p className="text-xs text-gray-300 leading-relaxed">
                                <strong className="text-gray-400">Summary:</strong> {report.summary}
                            </p>
                        </div>

                        {/* Admin Controls & Actions */}
                        <div className="flex flex-wrap lg:flex-col items-end justify-between gap-3 border-t lg:border-t-0 border-[#1A3352] pt-4 lg:pt-0 shrink-0">

                            {/* Change Verdict Select */}
                            <div className="flex items-center gap-2">
                                <span className="text-[11px] font-bold text-gray-400 uppercase">Verdict:</span>
                                <select
                                    value={report.verdict}
                                    onChange={(e) => handleVerdictChange(report.id, e.target.value as DashboardReport['verdict'])}
                                    className="bg-[#061528] border border-[#1A3352] rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-[#1CB5BE] font-bold cursor-pointer"
                                >
                                    <option value="PENDING">PENDING</option>
                                    <option value="FALSE">FALSE</option>
                                    <option value="MISLEADING">MISLEADING</option>
                                    <option value="VERIFIED">VERIFIED</option>
                                </select>
                            </div>

                            {/* Broadcast to Socials Trigger Button */}
                            <button
                                onClick={() => setSelectedReportForBroadcast(report)}
                                disabled={report.verdict === 'PENDING'}
                                className={`px-4 py-2 rounded-xl text-xs font-black flex items-center gap-2 transition-all cursor-pointer shadow-md ${report.verdict === 'PENDING'
                                        ? 'bg-[#061528] text-gray-500 border border-[#1A3352] cursor-not-allowed'
                                        : 'bg-[#E55322] hover:bg-[#d44819] text-white'
                                    }`}
                                title={report.verdict === 'PENDING' ? 'Set a verdict before broadcasting' : 'Publish to official social channels'}
                            >
                                <Share2 className="w-4 h-4" />
                                <span>Broadcast to Socials</span>
                            </button>

                        </div>
                    </div>
                ))}
            </div>

            {/* Social Media Broadcast Modal Integration */}
            {selectedReportForBroadcast && (
                <BroadcastModal
                    report={selectedReportForBroadcast}
                    onClose={() => {
                        // Update state to mark as broadcasted locally when modal closes
                        setReports((prev) =>
                            prev.map((item) =>
                                item.id === selectedReportForBroadcast.id ? { ...item, broadcasted: true } : item
                            )
                        );
                        setSelectedReportForBroadcast(null);
                    }}
                />
            )}

        </div>
    );
}