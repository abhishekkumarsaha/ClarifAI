import React from 'react';
import { motion } from 'framer-motion';
import { Search, History, Settings, HelpCircle, Plus } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import { NavigationPage } from '../../types';
import { playGlassClickSound } from '../../utils/audio';

export const BottomDock: React.FC = () => {
  const { activeNav, setActiveNav, setAccountPopoverOpen, resetVerification } = useApp();

  const handleNavClick = (page: NavigationPage) => {
    playGlassClickSound();
    setActiveNav(page);
    setAccountPopoverOpen(false);
  };

  const handleNewVerification = () => {
    playGlassClickSound();
    resetVerification();
    const searchInput = document.getElementById('main-claim-search-input');
    if (searchInput) {
      searchInput.focus();
    }
  };

  const dockItems: Array<{ id: NavigationPage; label: string; icon: React.FC<{ className?: string }> }> = [
    { id: 'verify', label: 'Verify', icon: Search },
    { id: 'history', label: 'History', icon: History },
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'about', label: 'Help', icon: HelpCircle },
  ];

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] max-w-xl w-[92%] sm:w-auto">
      {/* Liquid Glass Bottom Dock Container */}
      <div className="relative flex items-center justify-between gap-1 sm:gap-2 px-3 py-2 bg-white/80 dark:bg-[#161616]/90 backdrop-blur-2xl border border-black/15 dark:border-white/20 rounded-full shadow-2xl">
        
        {/* + New Verification Quick Action Pill */}
        <button
          onClick={handleNewVerification}
          className="flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-[#1DB954] hover:bg-[#1ed760] text-black font-bold text-xs shadow-md transition-all hover:scale-105 active:scale-95 cursor-pointer flex-shrink-0"
          title="New Verification"
        >
          <Plus className="w-4 h-4 stroke-[3]" />
          <span className="hidden sm:inline">New</span>
        </button>

        {/* Divider */}
        <div className="w-[1px] h-6 bg-black/10 dark:bg-white/10 mx-1 flex-shrink-0" />

        {/* Navigation Items with Shared Liquid Active Pill */}
        <div className="flex items-center gap-1 sm:gap-1.5 relative">
          {dockItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeNav === item.id;

            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`relative flex items-center gap-2 px-3 sm:px-4 py-2 rounded-full text-xs font-bold transition-all z-10 cursor-pointer ${
                  isActive
                    ? 'text-[#1DB954]'
                    : 'text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white'
                }`}
                title={item.label}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeDockPill"
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                    className="absolute inset-0 bg-[#1DB954]/15 border border-[#1DB954]/40 rounded-full z-0 shadow-sm"
                  />
                )}
                <Icon className="w-4 h-4 z-10" />
                <span className="hidden sm:inline z-10">{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
