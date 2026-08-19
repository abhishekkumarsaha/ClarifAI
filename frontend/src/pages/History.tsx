import React, { useMemo, useState } from 'react';
import {
  Search,
  Trash2,
  RotateCcw,
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Clock3,
  Database,
  X,
} from 'lucide-react';

import { useApp } from '../context/AppContext';
import { HistoryItem } from '../types';
import { playGlassClickSound } from '../utils/audio';

export const HistoryPage: React.FC = () => {
  const {
    history,
    deleteHistoryItem,
    clearHistory,
    setClaimInput,
    setCurrentResult,
    setActiveNav,
    showToast,
  } = useApp();

  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<
    'ALL' | 'LIKELY_TRUE' | 'LIKELY_FALSE' | 'UNVERIFIED'
  >('ALL');

  const [selectedItem, setSelectedItem] =
    useState<HistoryItem | null>(null);

  const filteredHistory = useMemo(() => {
    const query = search.trim().toLowerCase();

    return history.filter((item) => {
      const matchesSearch =
        !query ||
        item.claim.toLowerCase().includes(query) ||
        item.summary.toLowerCase().includes(query);

      const matchesFilter =
        filter === 'ALL' ||
        item.verdict === filter;

      return matchesSearch && matchesFilter;
    });
  }, [history, search, filter]);

  const getVerdictConfig = (verdict: string) => {
    if (verdict === 'LIKELY_TRUE') {
      return {
        label: 'LIKELY TRUE',
        icon: CheckCircle2,
        className:
          'text-[#1DB954] bg-[#1DB954]/10 border-[#1DB954]/30',
      };
    }

    if (verdict === 'LIKELY_FALSE') {
      return {
        label: 'LIKELY FALSE',
        icon: AlertCircle,
        className:
          'text-[#FF4D5A] bg-[#FF4D5A]/10 border-[#FF4D5A]/30',
      };
    }

    return {
      label: 'UNVERIFIED',
      icon: HelpCircle,
      className:
        'text-[#F5B942] bg-[#F5B942]/10 border-[#F5B942]/30',
    };
  };

  const handleOpenResult = (item: HistoryItem) => {
    playGlassClickSound();

    setClaimInput(item.claim);
    setCurrentResult(item.full_result);
    setActiveNav('verify');

    showToast('Previous verification restored');
  };

  const handleDelete = (
    event: React.MouseEvent,
    id: string,
  ) => {
    event.stopPropagation();

    playGlassClickSound();
    deleteHistoryItem(id);
  };

  const handleClearHistory = () => {
    if (!history.length) return;

    playGlassClickSound();

    const confirmed = window.confirm(
      'Clear all ClarifAI verification history?',
    );

    if (!confirmed) return;

    clearHistory();
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">

      {/* HEADER */}

      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">

        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-7 h-7 rounded-xl bg-[#00C2FF]/10 border border-[#00C2FF]/30 flex items-center justify-center">
              <Clock3 className="w-3.5 h-3.5 text-[#00C2FF]" />
            </div>

            <span className="text-[10px] font-black uppercase tracking-widest text-[#00C2FF]">
              Verification Archive
            </span>
          </div>

          <h1 className="text-3xl font-extrabold tracking-tight text-[#111827] dark:text-white">
            History
          </h1>

          <p className="text-sm text-[#475569] dark:text-[#A7A7A7] mt-1">
            Review and restore your previous ClarifAI analyses.
          </p>
        </div>

        <div className="flex items-center gap-2">

          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#00C2FF]/10 border border-[#00C2FF]/25 text-[#00C2FF] text-[10px] font-black">
            <Database className="w-3 h-3" />
            {history.length} RECORD
            {history.length === 1 ? '' : 'S'}
          </div>

          {history.length > 0 && (
            <button
              type="button"
              onClick={handleClearHistory}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full glass-interactive border border-[#FF4D5A]/25 text-[#FF4D5A] text-[10px] font-bold cursor-pointer"
            >
              <Trash2 className="w-3 h-3" />
              Clear
            </button>
          )}

        </div>
      </div>

      {/* SEARCH + FILTER */}

      <div className="glass-on-air rounded-3xl p-3 border border-black/15 dark:border-white/20 shadow-xl">

        <div className="flex flex-col md:flex-row gap-3">

          <div className="relative flex-1">

            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#64748B]" />

            <input
              type="text"
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
              placeholder="Search verification history..."
              className="w-full h-10 pl-10 pr-9 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#111827] dark:text-white placeholder-[#64748B] focus:outline-none focus:border-[#00C2FF]/50"
            />

            {search && (
              <button
                type="button"
                onClick={() => setSearch('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 cursor-pointer"
              >
                <X className="w-3.5 h-3.5 text-[#64748B]" />
              </button>
            )}

          </div>

          <div className="flex gap-1 overflow-x-auto">

            {[
              ['ALL', 'All'],
              ['LIKELY_TRUE', 'True'],
              ['LIKELY_FALSE', 'False'],
              ['UNVERIFIED', 'Unverified'],
            ].map(([value, label]) => (
              <button
                key={value}
                type="button"
                onClick={() =>
                  setFilter(
                    value as
                    | 'ALL'
                    | 'LIKELY_TRUE'
                    | 'LIKELY_FALSE'
                    | 'UNVERIFIED',
                  )
                }
                className={`px-3 py-2 rounded-full text-[10px] font-bold whitespace-nowrap cursor-pointer transition-all ${filter === value
                    ? 'bg-[#00C2FF]/15 text-[#00C2FF] border border-[#00C2FF]/30'
                    : 'glass-interactive text-[#64748B] dark:text-[#A7A7A7]'
                  }`}
              >
                {label}
              </button>
            ))}

          </div>
        </div>
      </div>

      {/* EMPTY STATE */}

      {history.length === 0 && (
        <div className="glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-xl p-10 text-center">

          <div className="w-16 h-16 mx-auto rounded-3xl bg-[#00C2FF]/10 border border-[#00C2FF]/25 flex items-center justify-center">
            <Database className="w-7 h-7 text-[#00C2FF]" />
          </div>

          <h2 className="mt-5 text-lg font-bold text-[#111827] dark:text-white">
            No verification history yet
          </h2>

          <p className="mt-2 max-w-md mx-auto text-sm text-[#64748B] dark:text-[#888888]">
            Your completed news verifications will automatically
            appear here.
          </p>

          <button
            type="button"
            onClick={() => {
              playGlassClickSound();
              setActiveNav('verify');
            }}
            className="mt-5 inline-flex items-center gap-2 px-4 py-2.5 rounded-full bg-[#1DB954] text-black text-xs font-bold cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Start Verification
          </button>

        </div>
      )}

      {/* NO SEARCH RESULTS */}

      {history.length > 0 &&
        filteredHistory.length === 0 && (
          <div className="glass-on-air rounded-3xl border border-black/15 dark:border-white/20 p-10 text-center">

            <Search className="w-8 h-8 mx-auto text-[#64748B]" />

            <h2 className="mt-4 text-base font-bold text-[#111827] dark:text-white">
              No matching analyses
            </h2>

            <p className="mt-1 text-xs text-[#64748B] dark:text-[#888888]">
              Try another search term or filter.
            </p>

          </div>
        )}

      {/* HISTORY LIST */}

      {filteredHistory.length > 0 && (
        <div className="space-y-3">

          {filteredHistory.map((item) => {

            const config =
              getVerdictConfig(item.verdict);

            const VerdictIcon =
              config.icon;

            return (
              <div
                key={item.id}
                onClick={() =>
                  handleOpenResult(item)
                }
                className="group glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-lg p-4 md:p-5 cursor-pointer hover:border-[#00C2FF]/30 hover:shadow-xl transition-all"
              >

                <div className="flex flex-col md:flex-row md:items-start gap-4">

                  {/* VERDICT */}

                  <div
                    className={`flex-shrink-0 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-[9px] font-black w-fit ${config.className}`}
                  >
                    <VerdictIcon className="w-3 h-3" />
                    {config.label}
                  </div>

                  {/* CONTENT */}

                  <div className="flex-1 min-w-0">

                    <h3 className="text-sm md:text-base font-bold text-[#111827] dark:text-white leading-snug line-clamp-2 group-hover:text-[#00C2FF] transition-colors">
                      {item.claim}
                    </h3>

                    {item.summary && (
                      <p className="mt-2 text-xs text-[#475569] dark:text-[#A7A7A7] line-clamp-2 leading-relaxed">
                        {item.summary}
                      </p>
                    )}

                    <div className="flex flex-wrap items-center gap-3 mt-3 text-[10px] text-[#64748B] dark:text-[#777777]">

                      <span className="flex items-center gap-1">
                        <Clock3 className="w-3 h-3" />
                        {item.date_obj} · {item.timestamp}
                      </span>

                      <span>
                        Confidence:{' '}
                        <strong className="text-[#111827] dark:text-white">
                          {Number(
                            item.confidence ?? 0,
                          ).toFixed(0)}
                          %
                        </strong>
                      </span>

                      <span>
                        Evidence:{' '}
                        <strong className="text-[#111827] dark:text-white">
                          {(item.supporting_count || 0) +
                            (item.contradicting_count || 0)}
                        </strong>
                      </span>

                    </div>

                  </div>

                  {/* ACTIONS */}

                  <div className="flex items-center gap-2 md:self-center">

                    <button
                      type="button"
                      title="Restore analysis"
                      onClick={(event) => {
                        event.stopPropagation();
                        handleOpenResult(item);
                      }}
                      className="p-2 rounded-full glass-interactive text-[#00C2FF] cursor-pointer"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                    </button>

                    <button
                      type="button"
                      title="Delete analysis"
                      onClick={(event) =>
                        handleDelete(
                          event,
                          item.id,
                        )
                      }
                      className="p-2 rounded-full glass-interactive text-[#FF4D5A] cursor-pointer"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>

                  </div>

                </div>
              </div>
            );
          })}

        </div>
      )}

      {/* DETAIL MODAL */}

      {selectedItem && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">

          <div className="w-full max-w-2xl max-h-[85vh] overflow-y-auto glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-2xl p-6">

            <div className="flex items-start justify-between gap-4">

              <div>
                <span
                  className={`inline-flex px-2.5 py-1 rounded-full border text-[9px] font-black ${getVerdictConfig(
                    selectedItem.verdict,
                  ).className
                    }`}
                >
                  {
                    getVerdictConfig(
                      selectedItem.verdict,
                    ).label
                  }
                </span>

                <h2 className="mt-3 text-lg font-bold text-[#111827] dark:text-white">
                  {selectedItem.claim}
                </h2>
              </div>

              <button
                type="button"
                onClick={() =>
                  setSelectedItem(null)
                }
                className="p-2 rounded-full glass-interactive cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>

            </div>

            <div className="mt-5 p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10">

              <div className="text-[10px] font-black uppercase tracking-wider text-[#00C2FF]">
                Evidence Summary
              </div>

              <p className="mt-2 text-sm text-[#111827] dark:text-white leading-relaxed">
                {selectedItem.summary ||
                  'No summary available.'}
              </p>

            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-4">

              <div className="p-3 rounded-2xl bg-black/5 dark:bg-white/5">
                <div className="text-[9px] text-[#64748B]">
                  Confidence
                </div>
                <div className="mt-1 text-lg font-black text-[#00C2FF]">
                  {Number(
                    selectedItem.confidence ?? 0,
                  ).toFixed(0)}
                  %
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-black/5 dark:bg-white/5">
                <div className="text-[9px] text-[#64748B]">
                  Confidence Level
                </div>
                <div className="mt-1 text-xs font-bold text-[#111827] dark:text-white">
                  {selectedItem.confidence_level ||
                    'Unknown'}
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-black/5 dark:bg-white/5">
                <div className="text-[9px] text-[#64748B]">
                  Supporting
                </div>
                <div className="mt-1 text-lg font-black text-[#1DB954]">
                  {selectedItem.supporting_count ||
                    0}
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-black/5 dark:bg-white/5">
                <div className="text-[9px] text-[#64748B]">
                  Contradicting
                </div>
                <div className="mt-1 text-lg font-black text-[#FF4D5A]">
                  {selectedItem.contradicting_count ||
                    0}
                </div>
              </div>

            </div>

            {selectedItem.full_result
              ?.supporting_evidence &&
              selectedItem.full_result
                .supporting_evidence.length > 0 && (

                <div className="mt-5">

                  <h3 className="text-xs font-black uppercase tracking-wider text-[#111827] dark:text-white">
                    Supporting Evidence
                  </h3>

                  <div className="mt-2 space-y-2">

                    {selectedItem.full_result.supporting_evidence.map(
                      (article, index) => (
                        <a
                          key={index}
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center justify-between gap-3 p-3 rounded-2xl glass-interactive border border-black/10 dark:border-white/10 group"
                        >

                          <div className="min-w-0">

                            <div className="text-[10px] font-bold text-[#1DB954]">
                              {article.publisher ||
                                article.source_domain ||
                                'Source'}
                            </div>

                            <div className="mt-1 text-xs font-bold text-[#111827] dark:text-white line-clamp-2">
                              {article.title ||
                                article.headline ||
                                'Evidence article'}
                            </div>

                          </div>

                          <ExternalLink className="w-3.5 h-3.5 flex-shrink-0 text-[#64748B] group-hover:text-[#00C2FF]" />

                        </a>
                      ),
                    )}

                  </div>

                </div>
              )}

            <div className="flex justify-end gap-2 mt-6">

              <button
                type="button"
                onClick={() =>
                  setSelectedItem(null)
                }
                className="px-4 py-2 rounded-full glass-interactive text-xs font-bold cursor-pointer"
              >
                Close
              </button>

              <button
                type="button"
                onClick={() => {
                  setSelectedItem(null);
                  handleOpenResult(selectedItem);
                }}
                className="px-4 py-2 rounded-full bg-[#1DB954] text-black text-xs font-bold cursor-pointer flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                Restore Analysis
              </button>

            </div>

          </div>
        </div>
      )}

    </div>
  );
};