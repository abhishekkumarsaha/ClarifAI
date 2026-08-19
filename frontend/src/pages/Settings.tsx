import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Moon,
  Sun,
  Monitor,
  Sliders,
  Activity,
  Shield,
  Trash2,
  Download,
  Check,
  Sparkles,
  Keyboard,
  Volume2,
  VolumeX,
  Bell,
  Palette,
  RefreshCw,
  Database,
  BrainCircuit,
  Newspaper,
  Server,
  HardDrive,
} from 'lucide-react';

import { useApp } from '../context/AppContext';
import { ThemeMode } from '../types';
import {
  playGlassClickSound,
  playSuccessChime,
} from '../utils/audio';

export const SettingsPage: React.FC = () => {
  const {
    theme,
    setTheme,
    soundEnabled,
    setSoundEnabled,
    maxArticlesLimit,
    setMaxArticlesLimit,
    health,
    refreshHealth,
    clearHistory,
    history,
    showToast,
  } = useApp();

  const [aiExplanationEnabled, setAiExplanationEnabled] =
    useState<boolean>(true);

  const [showClearConfirm, setShowClearConfirm] =
    useState<boolean>(false);

  const [clearedMsg, setClearedMsg] =
    useState<boolean>(false);

  const [refreshing, setRefreshing] =
    useState<boolean>(false);

  const themeOptions: Array<{
    id: ThemeMode;
    label: string;
    icon: React.FC<{ className?: string }>;
  }> = [
      {
        id: 'light',
        label: 'Light',
        icon: Sun,
      },
      {
        id: 'dark',
        label: 'Dark',
        icon: Moon,
      },
      {
        id: 'system',
        label: 'System',
        icon: Monitor,
      },
    ];

  const handleClearAllHistory = () => {
    playGlassClickSound();

    clearHistory();

    setClearedMsg(true);
    setShowClearConfirm(false);

    setTimeout(() => {
      setClearedMsg(false);
    }, 3000);
  };

  const handleExportHistoryJSON = () => {
    playGlassClickSound();

    if (!history.length) {
      showToast('No analysis history to export');
      return;
    }

    const exportData = {
      application: 'ClarifAI',
      export_type: 'verification_history',
      exported_at: new Date().toISOString(),
      total_records: history.length,
      records: history,
    };

    const jsonStr = JSON.stringify(
      exportData,
      null,
      2,
    );

    const blob = new Blob(
      [jsonStr],
      {
        type: 'application/json',
      },
    );

    const url = URL.createObjectURL(blob);

    const anchor = document.createElement('a');

    anchor.href = url;
    anchor.download =
      'clarifai_analysis_history.json';

    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();

    URL.revokeObjectURL(url);

    showToast(
      `${history.length} analysis record${history.length === 1 ? '' : 's'
      } exported`,
    );
  };

  const handleTestSound = () => {
    playGlassClickSound();

    setTimeout(() => {
      playSuccessChime();
    }, 150);

    showToast('Audio system tested successfully');
  };

  const handleRefreshHealth = async () => {
    playGlassClickSound();

    setRefreshing(true);

    try {
      await Promise.resolve(refreshHealth());

      setTimeout(() => {
        setRefreshing(false);
        showToast('Backend status refreshed');
      }, 500);
    } catch {
      setRefreshing(false);
      showToast('Unable to refresh backend status');
    }
  };

  const backendOperational =
    health.status === 'healthy';

  return (
    <div className="space-y-6 animate-in fade-in duration-200">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-3">

        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-7 h-7 rounded-xl bg-[#00C2FF]/10 border border-[#00C2FF]/30 flex items-center justify-center">
              <Sliders className="w-3.5 h-3.5 text-[#00C2FF]" />
            </div>

            <span className="text-[10px] font-black uppercase tracking-widest text-[#00C2FF]">
              Control Center
            </span>
          </div>

          <h1 className="text-3xl font-extrabold tracking-tight text-[#111827] dark:text-white">
            Settings
          </h1>

          <p className="text-sm text-[#475569] dark:text-[#A7A7A7] mt-1">
            Manage ClarifAI preferences, verification controls,
            services, and local data.
          </p>
        </div>

        {/* Backend status badge */}

        <div
          className={`inline-flex self-start md:self-auto items-center gap-2 px-3 py-1.5 rounded-full border text-[10px] font-black uppercase tracking-wider ${backendOperational
              ? 'bg-[#1DB954]/10 border-[#1DB954]/30 text-[#1DB954]'
              : 'bg-[#F5B942]/10 border-[#F5B942]/30 text-[#F5B942]'
            }`}
        >
          <span
            className={`w-1.5 h-1.5 rounded-full ${backendOperational
                ? 'bg-[#1DB954] animate-pulse'
                : 'bg-[#F5B942]'
              }`}
          />

          {backendOperational
            ? 'Backend Online'
            : 'Backend Degraded'}
        </div>
      </div>

      {/* =====================================================
          PREFERENCES
      ===================================================== */}

      <section className="p-5 glass-on-air rounded-3xl space-y-4 shadow-xl border border-black/15 dark:border-white/20">

        <div className="flex items-center justify-between border-b border-black/10 dark:border-white/10 pb-3">

          <div className="flex items-center gap-2">
            <Palette className="w-4 h-4 text-[#1DB954]" />

            <span className="text-sm font-bold text-[#111827] dark:text-white">
              Preferences
            </span>
          </div>

          <span
            className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full ${soundEnabled
                ? 'bg-[#1DB954]/15 text-[#1DB954] border border-[#1DB954]/40'
                : 'bg-gray-200 dark:bg-gray-800 text-gray-500'
              }`}
          >
            {soundEnabled
              ? 'AUDIO ON'
              : 'MUTED'}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          {/* Appearance */}

          <div className="space-y-2">

            <label className="text-xs font-bold text-[#111827] dark:text-white flex items-center gap-1.5">
              <Sun className="w-3.5 h-3.5 text-[#F5B942]" />
              Appearance
            </label>

            <div className="relative grid grid-cols-3 gap-1 p-1 bg-black/5 dark:bg-black/40 rounded-full border border-black/15 dark:border-white/20">

              {themeOptions.map((option) => {
                const Icon = option.icon;
                const active = theme === option.id;

                return (
                  <button
                    key={option.id}
                    type="button"
                    onClick={() => {
                      playGlassClickSound();
                      setTheme(option.id);
                      showToast(
                        `Theme: ${option.label}`,
                      );
                    }}
                    className={`relative flex items-center justify-center gap-1.5 py-2 px-2 rounded-full text-xs font-bold transition-all cursor-pointer ${active
                        ? 'text-[#1DB954]'
                        : 'text-[#475569] dark:text-[#A7A7A7]'
                      }`}
                  >

                    {active && (
                      <motion.div
                        layoutId="clarifai-theme-thumb"
                        transition={{
                          type: 'spring',
                          stiffness: 400,
                          damping: 30,
                        }}
                        className="absolute inset-0 bg-white dark:bg-[#1A1A1A] border border-black/15 dark:border-white/20 rounded-full shadow-md"
                      />
                    )}

                    <Icon className="w-3.5 h-3.5 relative z-10" />

                    <span className="relative z-10 text-[11px]">
                      {option.label}
                    </span>

                  </button>
                );
              })}

            </div>
          </div>

          {/* Sound */}

          <div className="space-y-2 md:border-l md:border-black/10 md:dark:border-white/10 md:pl-5">

            <div className="flex items-center justify-between">

              <div className="flex items-center gap-1.5 text-xs font-bold text-[#111827] dark:text-white">

                {soundEnabled ? (
                  <Volume2 className="w-3.5 h-3.5 text-[#1DB954]" />
                ) : (
                  <VolumeX className="w-3.5 h-3.5 text-[#64748B]" />
                )}

                Sound Effects

              </div>

              <button
                type="button"
                aria-label="Toggle sound effects"
                onClick={() => {
                  const next =
                    !soundEnabled;

                  setSoundEnabled(next);

                  if (next) {
                    playGlassClickSound();
                  }

                  showToast(
                    next
                      ? 'Audio enabled'
                      : 'Audio muted',
                  );
                }}
                className={`w-10 h-5 rounded-full p-0.5 transition-colors cursor-pointer ${soundEnabled
                    ? 'bg-[#1DB954]'
                    : 'bg-gray-300 dark:bg-gray-700'
                  }`}
              >
                <div
                  className={`w-4 h-4 rounded-full bg-white transition-transform shadow-md ${soundEnabled
                      ? 'translate-x-5'
                      : 'translate-x-0'
                    }`}
                />
              </button>

            </div>

            <div className="flex items-center justify-between">

              <span className="text-[11px] text-[#475569] dark:text-[#A7A7A7]">
                Glass click and verification chimes
              </span>

              {soundEnabled && (
                <button
                  type="button"
                  onClick={handleTestSound}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full glass-interactive border border-black/15 dark:border-white/20 text-[10px] font-bold text-[#00C2FF] hover:scale-105 transition-transform cursor-pointer"
                >
                  <Bell className="w-3 h-3" />
                  Test
                </button>
              )}

            </div>
          </div>
        </div>
      </section>

      {/* =====================================================
          VERIFICATION CONFIGURATION
      ===================================================== */}

      <section className="p-5 glass-on-air rounded-3xl space-y-4 shadow-xl border border-black/15 dark:border-white/20">

        <div className="flex items-center gap-2 border-b border-black/10 dark:border-white/10 pb-3">

          <Sliders className="w-4 h-4 text-[#00C2FF]" />

          <span className="text-sm font-bold text-[#111827] dark:text-white">
            Verification Configuration
          </span>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          {/* Evidence limit */}

          <div className="space-y-2">

            <div className="flex items-center justify-between">

              <span className="text-xs font-bold text-[#111827] dark:text-white">
                Evidence Articles
              </span>

              <span className="text-xs font-black text-[#1DB954]">
                {maxArticlesLimit}
              </span>

            </div>

            <input
              type="range"
              min={1}
              max={10}
              value={maxArticlesLimit}
              onChange={(event) => {
                setMaxArticlesLimit(
                  Number(event.target.value),
                );
              }}
              className="w-full glass-slider accent-[#1DB954]"
            />

            <div className="flex justify-between text-[10px] text-[#64748B] dark:text-[#666666]">
              <span>1</span>
              <span>5</span>
              <span>10</span>
            </div>

            <p className="text-[10px] text-[#64748B] dark:text-[#777777]">
              Controls how many evidence articles are
              analyzed per verification.
            </p>

          </div>

          {/* AI */}

          <div className="flex items-center justify-between md:border-l md:border-black/10 md:dark:border-white/10 md:pl-5">

            <div className="space-y-1">

              <div className="flex items-center gap-1.5 text-xs font-bold text-[#111827] dark:text-white">

                <BrainCircuit className="w-3.5 h-3.5 text-[#00C2FF]" />

                AI Explanation Synthesis

              </div>

              <p className="text-[11px] text-[#475569] dark:text-[#A7A7A7]">
                Generate evidence-grounded explanations.
              </p>

              <span className="inline-flex items-center gap-1 text-[9px] font-black uppercase tracking-wider text-[#1DB954]">
                <Sparkles className="w-3 h-3" />
                OpenRouter Layer
              </span>

            </div>

            <button
              type="button"
              aria-label="Toggle AI explanations"
              onClick={() => {
                playGlassClickSound();

                const next =
                  !aiExplanationEnabled;

                setAiExplanationEnabled(next);

                showToast(
                  next
                    ? 'AI explanations enabled'
                    : 'AI explanations disabled',
                );
              }}
              className={`w-10 h-5 rounded-full p-0.5 transition-colors cursor-pointer flex-shrink-0 ${aiExplanationEnabled
                  ? 'bg-[#1DB954]'
                  : 'bg-gray-300 dark:bg-gray-700'
                }`}
            >
              <div
                className={`w-4 h-4 rounded-full bg-white transition-transform shadow-md ${aiExplanationEnabled
                    ? 'translate-x-5'
                    : 'translate-x-0'
                  }`}
              />
            </button>

          </div>
        </div>
      </section>

      {/* =====================================================
          KEYBOARD SHORTCUTS
      ===================================================== */}

      <section className="p-5 glass-on-air rounded-3xl space-y-4 shadow-xl border border-black/15 dark:border-white/20">

        <div className="flex items-center gap-2">
          <Keyboard className="w-4 h-4 text-[#F5B942]" />

          <span className="text-sm font-bold text-[#111827] dark:text-white">
            Keyboard Shortcuts
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">

          {[
            ['Focus Search Bar', 'Ctrl + K'],
            ['Open History', 'Ctrl + H'],
            ['Submit Verification', 'Enter'],
            ['Close Modal / Popover', 'Esc'],
          ].map(([label, key]) => (
            <div
              key={label}
              className="flex items-center justify-between p-2.5 bg-black/5 dark:bg-black/40 rounded-xl border border-black/10 dark:border-white/10"
            >

              <span className="text-xs text-[#475569] dark:text-[#A7A7A7]">
                {label}
              </span>

              <kbd className="px-2 py-0.5 bg-white dark:bg-[#1E1E1E] border border-black/10 dark:border-white/10 rounded-md font-mono font-bold text-[#111827] dark:text-white text-[10px]">
                {key}
              </kbd>

            </div>
          ))}

        </div>
      </section>

      {/* =====================================================
          SERVICES STATUS
      ===================================================== */}

      <section className="p-5 glass-on-air rounded-3xl space-y-4 shadow-xl border border-black/15 dark:border-white/20">

        <div className="flex items-center justify-between">

          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-[#1DB954]" />

            <span className="text-sm font-bold text-[#111827] dark:text-white">
              Services & Environment
            </span>
          </div>

          <button
            type="button"
            onClick={handleRefreshHealth}
            disabled={refreshing}
            className="p-2 rounded-full glass-interactive cursor-pointer disabled:opacity-50"
            title="Refresh backend status"
          >
            <RefreshCw
              className={`w-3.5 h-3.5 text-[#00C2FF] ${refreshing
                  ? 'animate-spin'
                  : ''
                }`}
            />
          </button>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">

          {/* Backend */}

          <div className="p-3 rounded-2xl bg-black/5 dark:bg-black/30 border border-black/10 dark:border-white/10">

            <div className="flex items-center gap-2 mb-2">

              <Server className="w-4 h-4 text-[#00C2FF]" />

              <span className="text-xs font-bold text-[#111827] dark:text-white">
                Backend
              </span>

            </div>

            <div className="flex items-center gap-1.5">

              <span
                className={`w-1.5 h-1.5 rounded-full ${backendOperational
                    ? 'bg-[#1DB954]'
                    : 'bg-[#F5B942]'
                  }`}
              />

              <span className="text-[10px] font-bold text-[#475569] dark:text-[#A7A7A7]">
                {backendOperational
                  ? 'Operational'
                  : 'Degraded'}
              </span>

            </div>

          </div>

          {/* News */}

          <div className="p-3 rounded-2xl bg-black/5 dark:bg-black/30 border border-black/10 dark:border-white/10">

            <div className="flex items-center gap-2 mb-2">

              <Newspaper className="w-4 h-4 text-[#1DB954]" />

              <span className="text-xs font-bold text-[#111827] dark:text-white">
                News Search
              </span>

            </div>

            <div className="flex items-center gap-1.5">

              <span className="w-1.5 h-1.5 rounded-full bg-[#1DB954]" />

              <span className="text-[10px] font-bold text-[#475569] dark:text-[#A7A7A7]">
                Available
              </span>

            </div>

          </div>

          {/* AI */}

          <div className="p-3 rounded-2xl bg-black/5 dark:bg-black/30 border border-black/10 dark:border-white/10">

            <div className="flex items-center gap-2 mb-2">

              <BrainCircuit className="w-4 h-4 text-[#F5B942]" />

              <span className="text-xs font-bold text-[#111827] dark:text-white">
                AI Layer
              </span>

            </div>

            <div className="flex items-center gap-1.5">

              <span className="w-1.5 h-1.5 rounded-full bg-[#1DB954]" />

              <span className="text-[10px] font-bold text-[#475569] dark:text-[#A7A7A7]">
                Configured
              </span>

            </div>

          </div>

        </div>

        {health.version && (
          <div className="text-[10px] text-[#64748B] dark:text-[#666666] flex items-center gap-1.5">
            <Activity className="w-3 h-3" />
            Backend version: {health.version}
          </div>
        )}

      </section>

      {/* =====================================================
          DATA MANAGEMENT
      ===================================================== */}

      <section className="p-5 glass-on-air rounded-3xl space-y-4 shadow-xl border border-black/15 dark:border-white/20">

        <div className="flex items-center gap-2">

          <Shield className="w-4 h-4 text-[#F5B942]" />

          <span className="text-sm font-bold text-[#111827] dark:text-white">
            Data & Storage
          </span>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">

          <div className="p-3 rounded-2xl bg-black/5 dark:bg-black/30 border border-black/10 dark:border-white/10">

            <div className="flex items-center gap-2">

              <HardDrive className="w-4 h-4 text-[#00C2FF]" />

              <span className="text-xs font-bold text-[#111827] dark:text-white">
                Local Storage
              </span>

            </div>

            <p className="text-[10px] text-[#64748B] dark:text-[#777777] mt-1">
              History and preferences stay in your browser.
            </p>

          </div>

          <div className="p-3 rounded-2xl bg-black/5 dark:bg-black/30 border border-black/10 dark:border-white/10">

            <div className="flex items-center gap-2">

              <Database className="w-4 h-4 text-[#1DB954]" />

              <span className="text-xs font-bold text-[#111827] dark:text-white">
                History Records
              </span>

            </div>

            <p className="text-lg font-black text-[#1DB954] mt-1">
              {history.length}
            </p>

          </div>

          <div className="p-3 rounded-2xl bg-black/5 dark:bg-black/30 border border-black/10 dark:border-white/10">

            <div className="flex items-center gap-2">

              <Activity className="w-4 h-4 text-[#F5B942]" />

              <span className="text-xs font-bold text-[#111827] dark:text-white">
                Storage Mode
              </span>

            </div>

            <p className="text-[10px] font-bold text-[#475569] dark:text-[#A7A7A7] mt-2">
              Browser LocalStorage
            </p>

          </div>

        </div>

        {clearedMsg && (
          <div className="p-3 bg-[#1DB954]/15 border border-[#1DB954]/30 text-[#1DB954] font-bold text-xs rounded-xl flex items-center gap-2">

            <Check className="w-4 h-4" />

            Local analysis history cleared successfully.

          </div>
        )}

        <div className="flex flex-wrap items-center gap-3">

          <button
            type="button"
            onClick={handleExportHistoryJSON}
            disabled={!history.length}
            className="flex items-center gap-2 px-3.5 py-2 glass-interactive rounded-full text-xs font-bold text-[#111827] dark:text-white disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-[#00C2FF]" />

            Export JSON

            <span className="text-[#64748B]">
              ({history.length})
            </span>

          </button>

          <button
            type="button"
            onClick={() => {
              playGlassClickSound();
              setShowClearConfirm(true);
            }}
            disabled={!history.length}
            className="flex items-center gap-2 px-3.5 py-2 glass-interactive rounded-full text-xs font-bold text-[#FF4D5A] disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
          >
            <Trash2 className="w-3.5 h-3.5" />
            Clear History
          </button>

        </div>

      </section>

      {/* =====================================================
          CLEAR CONFIRMATION
      ===================================================== */}

      <AnimatePresence>
        {showClearConfirm && (

          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">

            <motion.div
              initial={{
                opacity: 0,
                scale: 0.95,
              }}
              animate={{
                opacity: 1,
                scale: 1,
              }}
              exit={{
                opacity: 0,
                scale: 0.95,
              }}
              className="w-full max-w-sm glass-on-air rounded-3xl p-6 space-y-4 shadow-2xl text-[#111827] dark:text-white border border-black/15 dark:border-white/20"
            >

              <div className="flex items-center gap-3">

                <div className="w-10 h-10 rounded-2xl bg-[#FF4D5A]/10 border border-[#FF4D5A]/30 flex items-center justify-center">
                  <Trash2 className="w-5 h-5 text-[#FF4D5A]" />
                </div>

                <div>
                  <h4 className="text-lg font-bold">
                    Clear Local History?
                  </h4>

                  <p className="text-[10px] text-[#64748B] dark:text-[#777777]">
                    {history.length} record
                    {history.length === 1
                      ? ''
                      : 's'} will be removed
                  </p>
                </div>

              </div>

              <p className="text-xs text-[#475569] dark:text-[#A7A7A7]">
                This permanently removes verification history
                stored in this browser. Export your history first
                if you want to keep a copy.
              </p>

              <div className="flex justify-end gap-3 pt-2">

                <button
                  type="button"
                  onClick={() => {
                    playGlassClickSound();
                    setShowClearConfirm(false);
                  }}
                  className="px-4 py-2 text-xs font-bold glass-interactive rounded-full cursor-pointer"
                >
                  Cancel
                </button>

                <button
                  type="button"
                  onClick={handleClearAllHistory}
                  className="px-4 py-2 text-xs font-bold bg-[#FF4D5A] text-white rounded-full shadow-md hover:bg-[#e04350] cursor-pointer"
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