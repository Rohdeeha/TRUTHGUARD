import { useState } from 'react';
import { DragDropContext, Droppable, Draggable, type DropResult } from '@hello-pangea/dnd';
import { Shield, Clock, Filter, Search, UserCheck } from 'lucide-react';
import toast from 'react-hot-toast';

export interface IncidentTicket {
    id: string;
    reference: string;
    incident_type: 'fake_news' | 'doctored_media' | 'tfgbv' | 'hate_speech';
    description: string;
    status: 'new' | 'investigating' | 'verified' | 'debunked' | 'dismissed';
    language: string;
    timestamp: string;
    assigned_to?: string;
    is_anonymous: boolean;
}

const initialTickets: IncidentTicket[] = [
    {
        id: 't-1',
        reference: 'TG-849201',
        incident_type: 'fake_news',
        description: 'WhatsApp voice note claiming voters without PVC can use National ID at Osogbo Ward 4.',
        status: 'new',
        language: 'en',
        timestamp: '10 mins ago',
        is_anonymous: true,
    },
    {
        id: 't-2',
        reference: 'TG-301928',
        incident_type: 'doctored_media',
        description: 'Doctored video showing ballot box tampering in Ede North.',
        status: 'investigating',
        language: 'yo',
        timestamp: '25 mins ago',
        assigned_to: 'Agent Kunle',
        is_anonymous: false,
    },
    {
        id: 't-3',
        reference: 'TG-102938',
        incident_type: 'tfgbv',
        description: 'Targeted online harassment campaign against a female election observer in Ife East.',
        status: 'investigating',
        language: 'en',
        timestamp: '1 hour ago',
        assigned_to: 'Agent Amina',
        is_anonymous: true,
    },
    {
        id: 't-4',
        reference: 'TG-509211',
        incident_type: 'fake_news',
        description: 'Claim that INEC servers went down across Osun State.',
        status: 'debunked',
        language: 'pcm',
        timestamp: '2 hours ago',
        assigned_to: 'Agent Bode',
        is_anonymous: false,
    },
];

const COLUMNS: { id: IncidentTicket['status']; label: string; color: string }[] = [
    { id: 'new', label: 'New Reports', color: 'border-blue-500 text-blue-400' },
    { id: 'investigating', label: 'Under Investigation', color: 'border-amber-500 text-amber-400' },
    { id: 'verified', label: 'Verified True', color: 'border-emerald-500 text-emerald-400' },
    { id: 'debunked', label: 'Debunked / Fake', color: 'border-rose-500 text-rose-400' },
    { id: 'dismissed', label: 'Dismissed', color: 'border-gray-600 text-gray-400' },
];

export default function DashboardPage() {
    const [tickets, setTickets] = useState<IncidentTicket[]>(initialTickets);
    const [searchQuery, setSearchQuery] = useState('');
    const [typeFilter, setTypeFilter] = useState<string>('ALL');

    const onDragEnd = (result: DropResult) => {
        const { destination, source, draggableId } = result;

        if (!destination) return;
        if (destination.droppableId === source.droppableId && destination.index === source.index) return;

        const newStatus = destination.droppableId as IncidentTicket['status'];

        setTickets((prev) =>
            prev.map((t) => (t.id === draggableId ? { ...t, status: newStatus } : t))
        );

        toast.success(`Ticket moved to ${newStatus.toUpperCase()}`);
    };

    const filteredTickets = tickets.filter((ticket) => {
        const matchesSearch = ticket.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
            ticket.reference.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesType = typeFilter === 'ALL' || ticket.incident_type === typeFilter;
        return matchesSearch && matchesType;
    });

    return (
        <div className="max-w-[1600px] mx-auto px-4 py-6 space-y-6">
            {/* Top Situation Room Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#0E243F] border border-gray-800 p-5 rounded-2xl shadow-xl">
                <div>
                    <h1 className="text-xl font-bold text-white flex items-center gap-2">
                        <Shield className="w-5 h-5 text-[#00B8C4]" /> Situation Room Triage Hub
                    </h1>
                    <p className="text-xs text-gray-400 mt-0.5">
                        Real-Time Ticket Management & Fact-Checking Queue · #OsunDecides2026
                    </p>
                </div>

                {/* Quick Stats */}
                <div className="flex items-center gap-3">
                    <div className="px-3 py-1.5 bg-[#071D38] border border-gray-800 rounded-lg text-center">
                        <span className="text-[10px] text-gray-400 block font-semibold">Total Incoming</span>
                        <span className="text-sm font-bold text-white">{tickets.length}</span>
                    </div>
                    <div className="px-3 py-1.5 bg-[#071D38] border border-blue-500/40 rounded-lg text-center">
                        <span className="text-[10px] text-blue-400 block font-semibold">New</span>
                        <span className="text-sm font-bold text-blue-400">
                            {tickets.filter((t) => t.status === 'new').length}
                        </span>
                    </div>
                    <div className="px-3 py-1.5 bg-[#071D38] border border-amber-500/40 rounded-lg text-center">
                        <span className="text-[10px] text-amber-400 block font-semibold">Investigating</span>
                        <span className="text-sm font-bold text-amber-400">
                            {tickets.filter((t) => t.status === 'investigating').length}
                        </span>
                    </div>
                </div>
            </div>

            {/* Filter Controls */}
            <div className="flex flex-col sm:flex-row gap-3 justify-between items-center bg-[#0E243F]/60 p-3 rounded-xl border border-gray-800">
                <div className="relative w-full sm:w-72">
                    <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
                    <input
                        type="text"
                        placeholder="Search reference or keywords..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full bg-[#071D38] border border-gray-700 text-xs text-white pl-9 pr-3 py-2 rounded-lg focus:border-[#00B8C4] focus:outline-none"
                    />
                </div>

                <div className="flex items-center gap-2 w-full sm:w-auto overflow-x-auto">
                    <Filter className="w-4 h-4 text-gray-400 shrink-0" />
                    {['ALL', 'fake_news', 'doctored_media', 'tfgbv', 'hate_speech'].map((type) => (
                        <button
                            key={type}
                            onClick={() => setTypeFilter(type)}
                            className={`px-3 py-1 rounded-md text-[11px] font-bold uppercase cursor-pointer whitespace-nowrap transition-colors ${typeFilter === type
                                    ? 'bg-[#00B8C4] text-[#071D38]'
                                    : 'bg-[#071D38] text-gray-400 hover:text-white border border-gray-700'
                                }`}
                        >
                            {type.replace('_', ' ')}
                        </button>
                    ))}
                </div>
            </div>

            {/* Kanban Board */}
            <DragDropContext onDragEnd={onDragEnd}>
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 overflow-x-auto pb-4">
                    {COLUMNS.map((col) => {
                        const colTickets = filteredTickets.filter((t) => t.status === col.id);

                        return (
                            <div key={col.id} className="bg-[#0E243F] border border-gray-800 rounded-xl p-3 flex flex-col min-h-[500px]">
                                {/* Column Header */}
                                <div className={`border-b-2 pb-2 mb-3 flex items-center justify-between ${col.color}`}>
                                    <span className="text-xs font-bold uppercase tracking-wider">{col.label}</span>
                                    <span className="px-2 py-0.5 bg-[#071D38] rounded-full text-[10px] font-bold border border-gray-700 text-gray-300">
                                        {colTickets.length}
                                    </span>
                                </div>

                                {/* Droppable Area */}
                                <Droppable droppableId={col.id}>
                                    {(provided, snapshot) => (
                                        <div
                                            ref={provided.innerRef}
                                            {...provided.droppableProps}
                                            className={`flex-1 space-y-3 transition-colors rounded-lg p-1 ${snapshot.isDraggingOver ? 'bg-[#071D38]/80 border border-dashed border-[#00B8C4]' : ''
                                                }`}
                                        >
                                            {colTickets.map((ticket, index) => (
                                                <Draggable key={ticket.id} draggableId={ticket.id} index={index}>
                                                    {(provided, snapshot) => (
                                                        <div
                                                            ref={provided.innerRef}
                                                            {...provided.draggableProps}
                                                            {...provided.dragHandleProps}
                                                            className={`bg-[#071D38] border border-gray-800 hover:border-[#00B8C4]/60 p-3.5 rounded-lg shadow-md space-y-2.5 transition-all ${snapshot.isDragging ? 'rotate-2 shadow-2xl border-[#00B8C4]' : ''
                                                                }`}
                                                        >
                                                            <div className="flex items-center justify-between text-[11px]">
                                                                <span className="font-mono font-bold text-[#E05A2B]">{ticket.reference}</span>
                                                                <span className="text-gray-500 uppercase font-bold text-[9px] px-1.5 py-0.5 bg-[#0E243F] rounded border border-gray-800">
                                                                    {ticket.language}
                                                                </span>
                                                            </div>

                                                            <p className="text-xs text-gray-200 line-clamp-3 leading-relaxed">
                                                                {ticket.description}
                                                            </p>

                                                            <div className="flex items-center justify-between pt-1 border-t border-gray-800/60 text-[10px] text-gray-400">
                                                                <span className="inline-flex items-center gap-1">
                                                                    <Clock className="w-3 h-3" /> {ticket.timestamp}
                                                                </span>
                                                                {ticket.assigned_to ? (
                                                                    <span className="inline-flex items-center gap-1 text-[#00B8C4]">
                                                                        <UserCheck className="w-3 h-3" /> {ticket.assigned_to}
                                                                    </span>
                                                                ) : (
                                                                    <span className="text-gray-500 italic">Unassigned</span>
                                                                )}
                                                            </div>
                                                        </div>
                                                    )}
                                                </Draggable>
                                            ))}
                                            {provided.placeholder}
                                        </div>
                                    )}
                                </Droppable>
                            </div>
                        );
                    })}
                </div>
            </DragDropContext>
        </div>
    );
}