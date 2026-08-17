import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Moon, Sun, Monitor, Sliders, Activity, Shield, Trash2, Download, Check, Sparkles, Keyboard } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { ThemeMode } from '../types';
import { playGlassClickSound } from '../utils/audio';

export const SettingsPage: React.FC = () => {
  const {
    theme,
    setTheme,
    maxArticlesLimit,
    setMaxArticlesLimit,
    health,
    clearHistory,
    history,
    showToast,
  } = useApp();

  const [aiExplanationEnabled, setAiExplanationEnabled] = useState<boolean>(true);
  const [showClearConfirm, setShowClearConfirm] = useState<boolean>(false);
  const [clearedMsg, setClearedMsg] = useState<boolean>(false);

  const themeOptions: Array<{ id: ThemeMode; label: string; icon: React.FC<{ className?: string }> }> = [
    { id: 'light', label: 'Light', icon: Sun },
    { id: 'dark', label: 'Dark', icon: Moon },
    { id: 'system', label: 'System', icon: Monitor },
  ];

  const handleClearAllHistory = () => {
    playGlassClickSound();
    clearHistory();
    setClearedMsg(true);
    setShowClearConfirm(false);
    setTimeout(() => setClearedMsg(false), 3000);
  };

  const handleExportHistoryJSON = () => {
    playGlassClickSound();
    const jsonStr = JSON.stringify(history, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'clarifai_analysis_history.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('Analysis history exported to JSON');
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-[#111827] dark:text-white">Settings</h1>
        <p className="text-sm text-[#475569] dark:text-[#A7A7A7] mt-1">Manage application preferences, theme, and verification options.</p>
      </div>

      {/* WIDGET 1: APPEARANCE & THEME CONTROL (LIQUID GLASS FLOATING INSTRUMENT TILE) */}
      <div className="p-6 glass-on-air rounded-3xl space-y-4 shadow-xl">
        <div className="text-base font-bold text-[#111827] dark:text-white flex items-center gap-2">
          <Sun className="w-5 h-5 text-[#1DB954]" />
          <span>Appearance</span>
        </div>

        <div className="space-y-3">
          <label className="text-xs font-semibold text-[#475569] dark:text-[#A7A7A7]">
            Theme Mode (Sole Source of Truth)
          </label>
          
          {/* Segmented Liquid Glass Theme Switcher */}
          <div className="relative grid grid-cols-3 gap-2 p-1.5 bg-black/5 dark:bg-black/40 rounded-full border border-black/15 dark:border-white/20 max-w-md">
            {themeOptions.map((opt) => {
              const Icon = opt.icon;
              const isActive = theme === opt.id;

              return (
                <button
                  key={opt.id}
                  onClick={() => {
                    playGlassClickSound();
                    setTheme(opt.id);
                    showToast(`Theme changed to ${opt.label}`);
                  }}
                  className={`relative flex items-center justify-center gap-2 py-2.5 px-4 rounded-full text-xs font-bold transition-all z-10 cursor-pointer ${
                    isActive
                      ? 'text-[#1DB954]'
                      : 'text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white'
                  }`}
                >
                  {isActive && (
                    <motion.div
                      layoutId="themeThumb"
                      transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                      className="absolute inset-0 bg-white dark:bg-[#1A1A1A] border border-black/15 dark:border-white/20 rounded-full shadow-md z-0"
                    />
                  )}
                  <Icon className="w-4 h-4 z-10" />
                  <span className="z-10">{opt.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* WIDGET 2: VERIFICATION CONFIGURATION (LIQUID GLASS RANGE SLIDER) */}
      <div className="p-6 glass-on-air rounded-3xl space-y-5 shadow-xl">
        <div className="text-base font-bold text-[#111827] dark:text-white flex items-center gap-2">
          <Sliders className="w-5 h-5 text-[#00C2FF]" />
          <span>Verification Configuration</span>
        </div>

        {/* Evidence Limit Liquid Glass Range Slider */}
        <div className="space-y-3 max-w-md">
          <div className="flex items-center justify-between text-xs font-semibold">
            <span className="text-[#475569] dark:text-[#A7A7A7]">Evidence Articles Limit</span>
            <span className="text-[#1DB954] font-bold text-sm">{maxArticlesLimit} articles</span>
          </div>
          <input
            type="range"
            min={1}
            max={10}
            value={maxArticlesLimit}
            onChange={(e) => setMaxArticlesLimit(Number(e.target.value))}
            className="w-full glass-slider accent-[#1DB954]"
          />
          <div className="flex justify-between text-[10px] text-[#64748B] dark:text-[#666666]">
            <span>1 article</span>
            <span>5 articles</span>
            <span>10 articles</span>
          </div>
        </div>

        {/* AI Explanation Toggle */}
        <div className="pt-3 border-t border-black/10 dark:border-white/10 flex items-center justify-between max-w-md">
          <div className="space-y-0.5">
            <div className="text-xs font-bold text-[#111827] dark:text-white flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-[#00C2FF]" />
              <span>AI Explanation Synthesis</span>
            </div>
            <div className="text-[11px] text-[#475569] dark:text-[#A7A7A7]">
              Synthesize natural-language evidence summaries
            </div>
          </div>

          <button
            onClick={() => {
              playGlassClickSound();
              setAiExplanationEnabled(!aiExplanationEnabled);
            }}
            className={`w-12 h-6 rounded-full p-1 transition-colors cursor-pointer ${
              aiExplanationEnabled ? 'bg-[#1DB954]' : 'bg-gray-300 dark:bg-gray-700'
            }`}
          >
            <div
              className={`w-4 h-4 rounded-full bg-white transition-transform ${
                aiExplanationEnabled ? 'translate-x-6' : 'translate-x-0'
              }`}
            />
          </button>
        </div>
      </div>

      {/* WIDGET 3: KEYBOARD SHORTCUTS CHEAT SHEET */}
      <div className="p-6 glass-on-air rounded-3xl space-y-4 shadow-xl">
        <div className="text-base font-bold text-[#111827] dark:text-white flex items-center gap-2">
          <Keyboard className="w-5 h-5 text-[#F5B942]" />
          <span>Keyboard Shortcuts</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-[#475569] dark:text-[#A7A7A7]">
          <div className="flex items-center justify-between p-3 bg-black/5 dark:bg-black/40 rounded-xl">
            <span>Focus Search Bar</span>
            <kbd className="px-2 py-1 bg-white dark:bg-[#1E1E1E] border border-black/10 dark:border-white/10 rounded-md font-mono font-bold text-[#111827] dark:text-white text-[11px]">
              Ctrl + K
            </kbd>
          </div>

          <div className="flex items-center justify-between p-3 bg-black/5 dark:bg-black/40 rounded-xl">
            <span>Open History</span>
            <kbd className="px-2 py-1 bg-white dark:bg-[#1E1E1E] border border-black/10 dark:border-white/10 rounded-md font-mono font-bold text-[#111827] dark:text-white text-[11px]">
              Ctrl + H
            </kbd>
          </div>

          <div className="flex items-center justify-between p-3 bg-black/5 dark:bg-black/40 rounded-xl">
            <span>Submit Verification</span>
            <kbd className="px-2 py-1 bg-white dark:bg-[#1E1E1E] border border-black/10 dark:border-white/10 rounded-md font-mono font-bold text-[#111827] dark:text-white text-[11px]">
              Enter
            </kbd>
          </div>

          <div className="flex items-center justify-between p-3 bg-black/5 dark:bg-black/40 rounded-xl">
            <span>Close Modal / Popover</span>
            <kbd className="px-2 py-1 bg-white dark:bg-[#1E1E1E] border border-black/10 dark:border-white/10 rounded-md font-mono font-bold text-[#111827] dark:text-white text-[11px]">
              Esc
            </kbd>
          </div>
        </div>
      </div>

      {/* WIDGET 4: SERVICES STATUS */}
      <div className="p-6 glass-on-air rounded-3xl space-y-4 shadow-xl">
        <div className="text-base font-bold text-[#111827] dark:text-white flex items-center gap-2">
          <Activity className="w-5 h-5 text-[#1DB954]" />
          <span>Services & Environment Status</span>
        </div>

        <div className="space-y-2 text-xs text-[#475569] dark:text-[#A7A7A7]">
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${health.status === 'healthy' ? 'bg-[#1DB954]' : 'bg-[#F5B942]'}`} />
            <span>Backend Verification Engine: <strong className="text-[#111827] dark:text-white">{health.status === 'healthy' ? 'Operational' : 'Degraded'}</strong></span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#1DB954]" />
            <span>Live News Indexing Service: <strong className="text-[#111827] dark:text-white">Operational</strong></span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#1DB954]" />
            <span>AI Verification Explanation Layer: <strong className="text-[#111827] dark:text-white">Operational</strong></span>
          </div>
        </div>
      </div>

      {/* WIDGET 5: DATA & EXPORT */}
      <div className="p-6 glass-on-air rounded-3xl space-y-4 shadow-xl">
        <div className="text-base font-bold text-[#111827] dark:text-white flex items-center gap-2">
          <Shield className="w-5 h-5 text-[#F5B942]" />
          <span>Data & Storage Management</span>
        </div>

        {clearedMsg && (
          <div className="p-3 bg-[#1DB954]/15 text-[#1DB954] font-bold text-xs rounded-xl flex items-center gap-2">
            <Check className="w-4 h-4" />
            <span>Local analysis history cleared successfully.</span>
          </div>
        )}

        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={handleExportHistoryJSON}
            disabled={history.length === 0}
            className="flex items-center gap-2 px-4 py-2.5 glass-interactive rounded-2xl text-xs font-bold text-[#111827] dark:text-white disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <Download className="w-4 h-4 text-[#00C2FF]" />
            <span>Export History JSON ({history.length})</span>
          </button>

          <button
            onClick={() => {
              playGlassClickSound();
              setShowClearConfirm(true);
            }}
            disabled={history.length === 0}
            className="flex items-center gap-2 px-4 py-2.5 glass-interactive rounded-2xl text-xs font-bold text-[#FF4D5A] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <Trash2 className="w-4 h-4" />
            <span>Clear Local History</span>
          </button>
        </div>
      </div>

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
                  className="px-4 py-2 text-xs font-bold glass-interactive rounded-full cursor-pointer"
                >
                  Cancel
                </button>
                <button
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
