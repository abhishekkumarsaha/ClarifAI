import React, { useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { MoreVertical, Download, RefreshCw, Flag, BookOpen, RefreshCcw } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import { SystemStatusTicker } from '../SystemTicker/SystemTicker';

export const TopBar: React.FC = () => {
  const {
    activeNav,
    setActiveNav,
    health,
    refreshHealth,
    threeDotMenuOpen,
    setThreeDotMenuOpen,
    accountPopoverOpen,
    setAccountPopoverOpen,
    setActiveModal,
  } = useApp();

  const menuRef = useRef<HTMLDivElement>(null);

  // Close 3-dot menu on outside click or Escape key
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        const threeDotBtn = document.getElementById('three-dot-trigger-btn');
        if (threeDotBtn && threeDotBtn.contains(event.target as Node)) {
          return;
        }
        setThreeDotMenuOpen(false);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setThreeDotMenuOpen(false);
      }
    };

    if (threeDotMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [threeDotMenuOpen, setThreeDotMenuOpen]);

  const pageTitles: Record<string, string> = {
    verify: 'Verify Workspace',
    history: 'Analysis History',
    settings: 'Settings & Environment',
    about: 'Help & Documentation',
  };

  return (
    <header className="h-16 px-6 bg-white/80 dark:bg-[#080808]/80 backdrop-blur-xl border-b border-black/10 dark:border-white/10 flex items-center justify-between sticky top-0 z-20 transition-colors duration-300">
      {/* Left: Detailed 3D Glowing Prism Brand Logo */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => setActiveNav('verify')}
          className="flex items-center gap-3 group focus:outline-none cursor-pointer"
          title="ClarifAI Home"
        >
          <div className="relative flex items-center justify-center">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-[#00C2FF]/20 via-[#1DB954]/20 to-[#00C2FF]/10 border border-[#00C2FF]/40 flex items-center justify-center group-hover:scale-105 group-hover:shadow-[0_0_20px_rgba(0,194,255,0.5)] transition-all shadow-md">
              <svg className="w-5 h-5 text-[#00C2FF]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2" stroke="url(#logo-grad-1)" />
                <line x1="12" y1="2" x2="12" y2="22" stroke="url(#logo-grad-2)" opacity="0.6" />
                <polygon points="12 6 18 10 18 14 12 18 6 14 6 10 12 6" fill="url(#logo-grad-3)" opacity="0.3" />
                <defs>
                  <linearGradient id="logo-grad-1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#00C2FF" />
                    <stop offset="100%" stopColor="#1DB954" />
                  </linearGradient>
                  <linearGradient id="logo-grad-2" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#00C2FF" />
                    <stop offset="100%" stopColor="#FFFFFF" />
                  </linearGradient>
                  <linearGradient id="logo-grad-3" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#1DB954" />
                    <stop offset="100%" stopColor="#00C2FF" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>
          <div className="flex flex-col text-left">
            <span className="font-heading font-black text-xl tracking-tight text-[#111827] dark:text-white group-hover:text-[#00C2FF] transition-colors leading-none">
              Clarif<span className="text-[#00C2FF]">AI</span>
            </span>
            <span className="text-[9px] font-bold text-[#1DB954] uppercase tracking-wider leading-none mt-1">
              News Authenticity
            </span>
          </div>
        </button>

        <div className="w-[1px] h-5 bg-black/10 dark:bg-white/10 hidden sm:block" />

        <h2 className="text-xs font-semibold text-[#475569] dark:text-[#A7A7A7] tracking-tight hidden sm:block">
          {pageTitles[activeNav] || 'ClarifAI'}
        </h2>
      </div>

      {/* Center: System Telemetry Ticker Pill embedded right inside the top bar */}
      <div className="hidden md:block">
        <SystemStatusTicker />
      </div>

      {/* Right: Status Badge, 3-Dot Menu Trigger, and Account Trigger Avatar */}
      <div className="flex items-center gap-3">
        {/* Backend Online/Offline Status Badge */}
        <div className="flex items-center gap-2 px-3 py-1 rounded-full glass-content text-xs font-semibold border border-black/15 dark:border-white/20">
          <span
            className={`w-2 h-2 rounded-full ${
              health.status === 'healthy'
                ? 'bg-[#1DB954] animate-pulse'
                : 'bg-[#FF4D5A] animate-pulse'
            }`}
          />
          <span className={`hidden md:inline ${health.status === 'healthy' ? 'text-[#1DB954]' : 'text-[#FF4D5A]'}`}>
            {health.status === 'healthy' ? 'Backend Online' : 'Backend Offline'}
          </span>

          {health.status !== 'healthy' && (
            <button
              onClick={refreshHealth}
              className="p-1 text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors cursor-pointer"
              title="Retry Backend Connection"
            >
              <RefreshCcw className="w-3 h-3" />
            </button>
          )}
        </div>

        {/* 3-Dot Contextual Menu Trigger Button */}
        <button
          id="three-dot-trigger-btn"
          onClick={() => setThreeDotMenuOpen(!threeDotMenuOpen)}
          className="p-2 text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 rounded-full border border-black/15 dark:border-white/20 transition-all focus:outline-none cursor-pointer flex-shrink-0"
          title="Contextual Menu"
        >
          <MoreVertical className="w-4 h-4" />
        </button>

        {/* Safe Portal Rendering for 3-Dot Popover */}
        {threeDotMenuOpen &&
          ReactDOM.createPortal(
            <div
              ref={menuRef}
              className="fixed w-60 glass-interactive rounded-3xl shadow-2xl p-2 z-[9999] text-[#111827] dark:text-white border border-black/15 dark:border-white/20 animate-in fade-in slide-in-from-top-2 duration-150"
              style={{ position: 'fixed', top: '68px', right: '64px' }}
            >
              <button
                onClick={() => {
                  setActiveModal('export');
                  setThreeDotMenuOpen(false);
                }}
                className="w-full flex items-center gap-2.5 px-3.5 py-2.5 text-xs font-semibold text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 rounded-2xl transition-colors text-left cursor-pointer"
              >
                <Download className="w-4 h-4 text-[#1DB954]" />
                <span>Export Scan Data</span>
              </button>

              <button
                onClick={() => {
                  setActiveModal('cache');
                  setThreeDotMenuOpen(false);
                }}
                className="w-full flex items-center gap-2.5 px-3.5 py-2.5 text-xs font-semibold text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 rounded-2xl transition-colors text-left cursor-pointer"
              >
                <RefreshCw className="w-4 h-4 text-[#00C2FF]" />
                <span>Clear Cache</span>
              </button>

              <button
                onClick={() => {
                  setActiveModal('report');
                  setThreeDotMenuOpen(false);
                }}
                className="w-full flex items-center gap-2.5 px-3.5 py-2.5 text-xs font-semibold text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 rounded-2xl transition-colors text-left cursor-pointer"
              >
                <Flag className="w-4 h-4 text-[#FF4D5A]" />
                <span>Report Misclassification</span>
              </button>

              <button
                onClick={() => {
                  setActiveModal('doc');
                  setThreeDotMenuOpen(false);
                }}
                className="w-full flex items-center gap-2.5 px-3.5 py-2.5 text-xs font-semibold text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 rounded-2xl transition-colors text-left cursor-pointer"
              >
                <BookOpen className="w-4 h-4 text-[#F5B942]" />
                <span>Documentation</span>
              </button>
            </div>,
            document.body
          )}

        {/* ChatGPT-Style Circular Account Avatar Trigger Button */}
        <button
          id="account-trigger-btn"
          onClick={() => setAccountPopoverOpen(!accountPopoverOpen)}
          className="w-8 h-8 rounded-full bg-[#1DB954]/20 border border-[#1DB954]/40 flex items-center justify-center text-[#1DB954] font-bold text-xs shadow-sm hover:scale-105 transition-all cursor-pointer flex-shrink-0"
          title="Account Profile"
        >
          A
        </button>
      </div>
    </header>
  );
};
