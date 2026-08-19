import React, { useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, X, UserCheck, Server, Activity, Megaphone, Sparkles } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const AccountPopover: React.FC = () => {
  const { accountPopoverOpen, setAccountPopoverOpen, health } = useApp();
  const popoverRef = useRef<HTMLDivElement>(null);

  // Close on outside click or Escape key
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(event.target as Node)) {
        const accountButton = document.getElementById('account-trigger-btn');
        if (accountButton && accountButton.contains(event.target as Node)) {
          return; // Handled by trigger button toggle
        }
        setAccountPopoverOpen(false);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setAccountPopoverOpen(false);
      }
    };

    if (accountPopoverOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [accountPopoverOpen, setAccountPopoverOpen]);

  const announcements = [
    {
      id: 1,
      tag: 'News Authenticity v2.0',
      title: 'Multi-Source Fact Checking Engine',
      desc: 'Queries published news coverage & scores linguistic evidence alignment.',
    },
    {
      id: 2,
      tag: 'Security & Privacy',
      title: 'Zero Data Retention Session',
      desc: 'News claim queries are analyzed in real-time with local privacy protection.',
    },
  ];

  if (!accountPopoverOpen) return null;

  return ReactDOM.createPortal(
    <AnimatePresence>
      <motion.div
        ref={popoverRef}
        initial={{ opacity: 0, scale: 0.95, y: -8 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: -8 }}
        transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
        className="fixed top-16 right-6 w-72 glass-content rounded-3xl shadow-2xl p-4 z-[9999] text-[#111827] dark:text-white border border-black/15 dark:border-white/20 flex flex-col space-y-3.5"
        style={{ position: 'fixed', top: '68px', right: '24px' }}
      >
        {/* Top Profile Header */}
        <div className="flex items-center justify-between pb-3 border-b border-black/10 dark:border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-[#1DB954]/20 border border-[#1DB954]/40 flex items-center justify-center text-[#1DB954] font-extrabold text-sm flex-shrink-0 shadow-sm">
              A
            </div>
            <div className="flex flex-col min-w-0">
              <span className="text-sm font-bold leading-tight text-[#111827] dark:text-white truncate">Abhi</span>
              <span className="text-xs text-[#475569] dark:text-[#A7A7A7] leading-tight mt-0.5 font-medium">Free / Local Mode</span>
            </div>
          </div>
          <button
            onClick={() => setAccountPopoverOpen(false)}
            className="text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white p-1 rounded-full hover:bg-black/5 dark:hover:bg-white/10 transition-colors cursor-pointer"
            title="Close panel"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Account & Workspace Status Details */}
        <div className="space-y-2 text-xs text-[#475569] dark:text-[#A7A7A7] bg-black/5 dark:bg-white/5 p-3 rounded-2xl border border-black/5 dark:border-white/5">
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-medium">
              <UserCheck className="w-3.5 h-3.5 text-[#1DB954]" />
              <span>Workspace:</span>
            </span>
            <span className="font-bold text-[#111827] dark:text-white">Local Workspace</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-medium">
              <Server className="w-3.5 h-3.5 text-[#00C2FF]" />
              <span>Session:</span>
            </span>
            <span className="font-bold text-[#1DB954]">Active</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-medium">
              <Activity className="w-3.5 h-3.5 text-[#F5B942]" />
              <span>API Connection:</span>
            </span>
            <span className={`font-bold ${health.status === 'healthy' ? 'text-[#1DB954]' : 'text-[#FF4D5A]'}`}>
              {health.status === 'healthy' ? 'Connected' : 'Offline'}
            </span>
          </div>
        </div>

        {/* Announcements & Platform Updates Section */}
        <div className="space-y-2 pt-1">
          <div className="flex items-center gap-1.5 text-xs font-bold text-[#111827] dark:text-white">
            <Megaphone className="w-3.5 h-3.5 text-[#00C2FF]" />
            <span>Announcements</span>
          </div>

          <div className="space-y-2">
            {announcements.map((ann) => (
              <div key={ann.id} className="p-2.5 bg-black/5 dark:bg-white/5 rounded-2xl border border-black/5 dark:border-white/5 space-y-1">
                <div className="flex items-center justify-between text-[10px]">
                  <span className="font-bold text-[#00C2FF] uppercase tracking-wider">{ann.tag}</span>
                  <Sparkles className="w-3 h-3 text-[#1DB954]" />
                </div>
                <div className="text-xs font-bold text-[#111827] dark:text-white leading-tight">{ann.title}</div>
                <div className="text-[11px] text-[#475569] dark:text-[#A7A7A7] leading-snug">{ann.desc}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Authentication Footer Status */}
        <div className="pt-2 border-t border-black/10 dark:border-white/10 flex items-center justify-between text-xs text-[#475569] dark:text-[#A7A7A7]">
          <span className="flex items-center gap-1.5">
            <Shield className="w-3.5 h-3.5 text-[#F5B942]" />
            <span>Authentication</span>
          </span>
          <span className="font-bold text-[#F5B942]">Coming Soon</span>
        </div>
      </motion.div>
    </AnimatePresence>,
    document.body
  );
};
