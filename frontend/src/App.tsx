import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { useApp } from './context/AppContext';
import { TopBar } from './components/TopBar/TopBar';
import { SystemStatusTicker } from './components/SystemTicker/SystemTicker';
import { BottomDock } from './components/Dock/Dock';
import { AccountPopover } from './components/AccountPopover/AccountPopover';
import { Modals } from './components/Modals/Modals';
import { VerifyPage } from './pages/Verify';
import { HistoryPage } from './pages/History';
import { SettingsPage } from './pages/Settings';
import { AboutPage } from './pages/About';

export const MainContent: React.FC = () => {
  const { activeNav, toastMsg } = useApp();

  return (
    <div className="flex-1 flex flex-col min-w-0 bg-transparent text-[#111827] dark:text-white h-screen overflow-y-auto relative">
      {/* Background Cinematic Ambient Lighting Mist */}
      <div className="cinematic-glow-cyan top-[-100px] left-[-100px]" />
      <div className="cinematic-glow-emerald top-[300px] right-[-100px]" />

      {/* Top Floating Header with Brand Logo & Account Trigger */}
      <TopBar />

      {/* Kinetic Creative Telemetry Ticker (Inspired by aio.engineer) */}
      <SystemStatusTicker />

      {/* Primary Workspace Content */}
      <main className="flex-1 p-6 md:p-10 max-w-5xl w-full mx-auto pb-32 relative z-10">
        {activeNav === 'verify' && <VerifyPage />}
        {activeNav === 'history' && <HistoryPage />}
        {activeNav === 'settings' && <SettingsPage />}
        {activeNav === 'about' && <AboutPage />}
      </main>

      {/* Footer */}
      <footer className="py-8 border-t border-black/10 dark:border-white/10 text-center text-xs text-[#64748B] dark:text-[#666666] pb-28 relative z-10">
        <div>ClarifAI • News Authenticity & Pattern Analysis Engine</div>
        <div className="text-[10px] opacity-70 mt-1">
          Evidence analysis, not absolute factual authority.
        </div>
      </footer>

      {/* Floating Bottom Liquid Glass Navigation Dock */}
      <BottomDock />

      {/* Top-Level Independent Account Popover Overlay */}
      <AccountPopover />

      {/* Toast Notification Container */}
      <AnimatePresence>
        {toastMsg && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="fixed bottom-24 right-6 z-[500] glass-content border border-[#1DB954]/40 px-4 py-3 rounded-2xl shadow-2xl flex items-center gap-2.5 text-xs font-bold text-[#111827] dark:text-white"
          >
            <Sparkles className="w-4 h-4 text-[#1DB954]" />
            <span>{toastMsg}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Global Modals Container */}
      <Modals />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <div className="flex h-screen overflow-hidden bg-gradient-to-br from-[#F8F9FA] via-[#F1F3F5] to-[#E9ECEF] dark:from-[#080808] dark:via-[#0D0D0D] dark:to-[#050505] text-[#111827] dark:text-white">
      <MainContent />
    </div>
  );
};
