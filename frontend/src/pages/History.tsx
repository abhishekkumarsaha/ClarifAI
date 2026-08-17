import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  History as HistoryIcon,
  Trash2,
  Download,
  RotateCcw,
  Bookmark,
  BookmarkCheck,
  Search,
  SlidersHorizontal,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  FileText,
  List,
  GitCommit,
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { playGlassClickSound } from '../utils/audio';

export const HistoryPage: React.FC = () => {
  const {
    history,
    deleteHistoryItem,
    clearHistory,
    setCurrentResult,
    setActiveNav,
    savedItems,
    toggleSaveItem,
  } = useApp();

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [filterVerdict, setFilterVerdict] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'list' | 'timeline'>('list');
  const [showClearConfirm, setShowClearConfirm] = useState<boolean>(false);

  const filteredHistory = history.filter((item) => {
    const matchesSearch = item.claim.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesVerdict = filterVerdict === 'all' || item.verdict === filterVerdict;
    return matchesSearch && matchesVerdict;
  });

  const handleRestore = (item: any) => {
    playGlassClickSound();
    setCurrentResult(item.full_result);
    setActiveNav('verify');
  };

  const handleExportSingleJSON = (item: any) => {
    playGlassClickSound();
    const jsonStr = JSON.stringify(item.full_result, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `clarifai_scan_${item.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleExportSingleCSV = (item: any) => {
    playGlassClickSound();
    const res = item.full_result;
    const csvRows = [
      ['Field', 'Value'],
      ['Claim', `"${res.claim.replace(/"/g, '""')}"`],
      ['Verdict', res.verdict],
      ['Confidence', res.confidence],
      ['Confidence Level', res.confidence_level],
      ['Summary', `"${(res.summary || '').replace(/"/g, '""')}"`],
      ['Articles Found', res.articles_found || 0],
    ];

    const csvContent = csvRows.map((e) => e.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `clarifai_scan_${item.id}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-[#111827] dark:text-white">
            Analysis History
          </h1>
          <p className="text-sm text-[#475569] dark:text-[#A7A7A7] mt-1">
            Review past claim verifications, export records, or restore analysis sessions.
          </p>
        </div>

        {history.length > 0 && (
          <div className="flex items-center gap-2">
            {/* View Mode Segmented Switcher */}
            <div className="flex items-center p-1 bg-black/5 dark:bg-white/5 rounded-2xl border border-black/10 dark:border-white/10 text-xs font-bold">
              <button
                onClick={() => {
                  playGlassClickSound();
                  setViewMode('list');
                }}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition-all cursor-pointer ${
                  viewMode === 'list'
                    ? 'bg-white dark:bg-[#1E1E1E] text-[#1DB954] shadow-sm'
                    : 'text-[#475569] dark:text-[#A7A7A7]'
                }`}
              >
                <List className="w-3.5 h-3.5" />
                <span>List</span>
              </button>

              <button
                onClick={() => {
                  playGlassClickSound();
                  setViewMode('timeline');
                }}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition-all cursor-pointer ${
                  viewMode === 'timeline'
                    ? 'bg-white dark:bg-[#1E1E1E] text-[#00C2FF] shadow-sm'
                    : 'text-[#475569] dark:text-[#A7A7A7]'
                }`}
              >
                <GitCommit className="w-3.5 h-3.5" />
                <span>Timeline</span>
              </button>
            </div>

            <button
              onClick={() => {
                playGlassClickSound();
                setShowClearConfirm(true);
              }}
              className="flex items-center gap-2 px-4 py-2 glass-interactive rounded-xl text-xs font-bold text-[#FF4D5A]"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear History</span>
            </button>
          </div>
        )}
      </div>

      {/* Filter & Search Bar */}
      {history.length > 0 && (
        <div className="flex flex-col sm:flex-row items-center gap-4">
          <div className="relative flex-1 w-full">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#475569] dark:text-[#A7A7A7]" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search history claims..."
              className="w-full glass-interactive rounded-xl py-2.5 pl-10 pr-4 text-xs text-[#111827] dark:text-white placeholder-[#64748B] dark:placeholder-[#666666]"
            />
          </div>

          <div className="flex items-center gap-2 text-xs text-[#475569] dark:text-[#A7A7A7] glass-content px-3 py-2 rounded-xl w-full sm:w-auto">
            <SlidersHorizontal className="w-3.5 h-3.5 text-[#1DB954]" />
            <span>Filter Verdict:</span>
            <select
              value={filterVerdict}
              onChange={(e) => setFilterVerdict(e.target.value)}
              className="bg-transparent text-[#111827] dark:text-white font-bold focus:outline-none cursor-pointer"
            >
              <option value="all" className="bg-white dark:bg-[#121212]">All Verdicts</option>
              <option value="LIKELY_TRUE" className="bg-white dark:bg-[#121212]">Likely True</option>
              <option value="LIKELY_FALSE" className="bg-white dark:bg-[#121212]">Likely False</option>
              <option value="UNVERIFIED" className="bg-white dark:bg-[#121212]">Unverified</option>
            </select>
          </div>
        </div>
      )}

      {/* History Items List / Timeline View */}
      {filteredHistory.length > 0 ? (
        viewMode === 'list' ? (
          <div className="space-y-4">
            {filteredHistory.map((item) => {
              const isSaved = savedItems.has(item.claim);

              return (
                <div
                  key={item.id}
                  className="p-5 glass-content glass-content-hover rounded-3xl space-y-3 transition-all border border-black/15 dark:border-white/20"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2 border-b border-black/10 dark:border-white/10 pb-3">
                    <div className="flex items-center gap-2 text-xs font-bold">
                      {item.verdict === 'LIKELY_TRUE' && (
                        <span className="text-[#1DB954] flex items-center gap-1">
                          <CheckCircle2 className="w-4 h-4" /> LIKELY TRUE
                        </span>
                      )}
                      {item.verdict === 'LIKELY_FALSE' && (
                        <span className="text-[#FF4D5A] flex items-center gap-1">
                          <AlertCircle className="w-4 h-4" /> LIKELY FALSE
                        </span>
                      )}
                      {item.verdict === 'UNVERIFIED' && (
                        <span className="text-[#F5B942] flex items-center gap-1">
                          <HelpCircle className="w-4 h-4" /> UNVERIFIED
                        </span>
                      )}
                      <span className="text-[#475569] dark:text-[#A7A7A7]">
                        • {item.confidence.toFixed(1)}% Confidence ({item.confidence_level})
                      </span>
                    </div>

                    <span className="text-xs text-[#64748B] dark:text-[#666666]">{item.timestamp}</span>
                  </div>

                  <div className="text-sm font-bold text-[#111827] dark:text-white leading-snug">
                    "{item.claim}"
                  </div>

                  <div className="text-xs text-[#475569] dark:text-[#A7A7A7] line-clamp-2">
                    {item.summary}
                  </div>

                  {/* Actions Bar */}
                  <div className="pt-2 flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleRestore(item)}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-[#1DB954] text-black font-bold text-xs rounded-xl shadow-md hover:bg-[#1ed760] transition-all cursor-pointer"
                      >
                        <RotateCcw className="w-3.5 h-3.5" />
                        <span>Open Workspace</span>
                      </button>

                      <button
                        onClick={() => toggleSaveItem(item.claim)}
                        className="flex items-center gap-1.5 px-3 py-1.5 glass-interactive rounded-xl text-xs cursor-pointer"
                      >
                        {isSaved ? (
                          <>
                            <BookmarkCheck className="w-3.5 h-3.5 text-[#1DB954]" />
                            <span className="text-[#1DB954]">Saved</span>
                          </>
                        ) : (
                          <>
                            <Bookmark className="w-3.5 h-3.5 text-[#475569] dark:text-[#A7A7A7]" />
                            <span>Save</span>
                          </>
                        )}
                      </button>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleExportSingleJSON(item)}
                        className="flex items-center gap-1 px-2.5 py-1.5 glass-interactive rounded-xl text-xs text-[#00C2FF] cursor-pointer"
                        title="Export JSON"
                      >
                        <Download className="w-3 h-3" />
                        <span>JSON</span>
                      </button>

                      <button
                        onClick={() => handleExportSingleCSV(item)}
                        className="flex items-center gap-1 px-2.5 py-1.5 glass-interactive rounded-xl text-xs text-[#1DB954] cursor-pointer"
                        title="Export CSV"
                      >
                        <FileText className="w-3 h-3" />
                        <span>CSV</span>
                      </button>

                      <button
                        onClick={() => {
                          playGlassClickSound();
                          deleteHistoryItem(item.id);
                        }}
                        className="p-1.5 text-[#FF4D5A] hover:bg-[#FF4D5A]/10 rounded-xl transition-colors cursor-pointer"
                        title="Delete entry"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          /* TIMELINE NODE GRAPH VIEW */
          <div className="relative pl-6 border-l-2 border-[#1DB954]/30 space-y-6">
            {filteredHistory.map((item) => {
              const isSaved = savedItems.has(item.claim);

              return (
                <div key={item.id} className="relative group">
                  {/* Timeline Node Point */}
                  <div className="absolute -left-[31px] top-4 w-4 h-4 rounded-full bg-[#1DB954] border-4 border-white dark:border-[#080808] shadow-[0_0_12px_rgba(29,185,84,0.6)] group-hover:scale-125 transition-transform" />

                  <div className="p-5 glass-content glass-content-hover rounded-3xl space-y-3 border border-black/15 dark:border-white/20">
                    <div className="flex flex-wrap items-center justify-between gap-2 border-b border-black/10 dark:border-white/10 pb-2">
                      <span className="text-xs font-bold text-[#00C2FF]">{item.timestamp}</span>
                      <span className="text-xs font-bold text-[#1DB954]">{item.verdict} ({item.confidence.toFixed(0)}%)</span>
                    </div>

                    <h4 className="text-sm font-bold text-[#111827] dark:text-white">"{item.claim}"</h4>
                    <p className="text-xs text-[#475569] dark:text-[#A7A7A7] line-clamp-2">{item.summary}</p>

                    <div className="flex items-center gap-2 pt-1">
                      <button
                        onClick={() => handleRestore(item)}
                        className="px-3 py-1 bg-[#1DB954] text-black font-bold text-xs rounded-xl shadow-sm hover:bg-[#1ed760] cursor-pointer"
                      >
                        Restore Session
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )
      ) : (
        <div className="p-12 glass-content rounded-3xl text-center space-y-3 shadow-xl border border-black/15 dark:border-white/20">
          <HistoryIcon className="w-12 h-12 text-[#64748B] dark:text-[#666666] mx-auto" />
          <h3 className="text-base font-bold text-[#111827] dark:text-white">No history records found</h3>
          <p className="text-xs text-[#475569] dark:text-[#A7A7A7] max-w-sm mx-auto">
            {searchTerm || filterVerdict !== 'all'
              ? 'No verification records match your active search or filter criteria.'
              : 'Verifications you perform will automatically be saved locally in your history.'}
          </p>
        </div>
      )}

      {/* Confirmation Dialog for Clearing History */}
      <AnimatePresence>
        {showClearConfirm && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="w-full max-w-sm glass-on-air rounded-3xl p-6 space-y-4 shadow-2xl text-[#111827] dark:text-white"
            >
              <h4 className="text-lg font-bold">Clear Local History?</h4>
              <p className="text-xs text-[#475569] dark:text-[#A7A7A7]">
                This will delete all saved scan items from your browser local storage. This action cannot be undone.
              </p>
              <div className="flex justify-end gap-3 pt-2">
                <button
                  onClick={() => {
                    playGlassClickSound();
                    setShowClearConfirm(false);
                  }}
                  className="px-4 py-2 text-xs font-bold glass-interactive rounded-xl cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    playGlassClickSound();
                    clearHistory();
                    setShowClearConfirm(false);
                  }}
                  className="px-4 py-2 text-xs font-bold bg-[#FF4D5A] text-white rounded-xl shadow-md hover:bg-[#e04350] cursor-pointer"
                >
                  Confirm Clear
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};
