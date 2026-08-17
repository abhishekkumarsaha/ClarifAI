import React from 'react';
import { motion } from 'framer-motion';
import {
  Plus,
  Search,
  History,
  Settings,
  HelpCircle,
  PanelLeftClose,
  PanelLeftOpen,
  Activity,
} from 'lucide-react';
import { useApp } from '../../context/AppContext';
import { AccountPopover } from '../AccountPopover/AccountPopover';
import { NavigationPage } from '../../types';

export const Sidebar: React.FC = () => {
  const {
    activeNav,
    setActiveNav,
    sidebarCollapsed,
    setSidebarCollapsed,
    accountPopoverOpen,
    setAccountPopoverOpen,
    resetVerification,
    health,
  } = useApp();

  const handleLogoClick = () => {
    // Logo button means "Open / collapse navigation", NOT "Always go Home"
    setSidebarCollapsed((prev) => !prev);
  };

  const handleNewVerificationClick = () => {
    // Fresh verification session: clear claim & result state, focus search
    resetVerification();
    const searchInput = document.getElementById('main-claim-search-input');
    if (searchInput) {
      searchInput.focus();
    }
  };

  const handleNavClick = (page: NavigationPage) => {
    setActiveNav(page);
    setAccountPopoverOpen(false);
  };

  const navItems: Array<{ id: NavigationPage; label: string; icon: React.FC<{ className?: string }> }> = [
    { id: 'verify', label: 'Verify', icon: Search },
    { id: 'history', label: 'History', icon: History },
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'about', label: 'Help & About', icon: HelpCircle },
  ];

  return (
    <motion.aside
      animate={{ width: sidebarCollapsed ? 72 : 260 }}
      transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
      className="relative flex flex-col h-screen glass-content border-r border-black/10 dark:border-white/10 z-30 select-none flex-shrink-0 transition-colors duration-300"
    >
      {/* Top Branding Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-black/10 dark:border-white/10">
        <button
          onClick={handleLogoClick}
          className="flex items-center gap-3 group focus:outline-none relative cursor-pointer"
          title={sidebarCollapsed ? 'Open sidebar' : 'Collapse sidebar'}
        >
          <div className="w-8 h-8 rounded-2xl bg-[#00C2FF]/10 border border-[#00C2FF]/30 flex items-center justify-center text-[#00C2FF] group-hover:scale-105 group-hover:shadow-[0_0_12px_rgba(0,194,255,0.4)] transition-all">
            <span className="font-extrabold text-lg leading-none">◈</span>
          </div>
          {!sidebarCollapsed && (
            <span className="font-heading font-extrabold text-xl tracking-tight text-[#111827] dark:text-white group-hover:text-[#00C2FF] transition-colors">
              ClarifAI
            </span>
          )}
        </button>

        <button
          onClick={() => setSidebarCollapsed((prev) => !prev)}
          className="p-1.5 text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 rounded-2xl transition-colors relative group cursor-pointer"
          title={sidebarCollapsed ? 'Open sidebar' : 'Collapse sidebar'}
        >
          {sidebarCollapsed ? <PanelLeftOpen className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
          {sidebarCollapsed && (
            <span className="absolute left-12 top-1/2 -translate-y-1/2 bg-[#121212] text-white text-[10px] font-bold px-2 py-1 rounded-xl shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50">
              Open sidebar
            </span>
          )}
        </button>
      </div>

      {/* Main Action + Navigation */}
      <div className="flex-1 px-3 py-4 space-y-4 overflow-y-auto">
        {/* + New Verification Primary CTA Button (Curved Liquid Glass) */}
        <button
          onClick={handleNewVerificationClick}
          className={`w-full flex items-center justify-center gap-2 py-2.5 px-3 rounded-2xl font-bold text-sm bg-[#1DB954] hover:bg-[#1ed760] text-black shadow-lg shadow-[#1DB954]/20 hover:scale-[1.02] active:scale-[0.97] transition-all group cursor-pointer ${
            sidebarCollapsed ? 'px-0' : ''
          }`}
          title="New verification"
        >
          <Plus className="w-4 h-4 stroke-[3] group-hover:rotate-90 transition-transform duration-300" />
          {!sidebarCollapsed && <span>New Verification</span>}
        </button>

        {/* Primary Nav List with Sliding Glass Indicator */}
        <div className="space-y-1 relative">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeNav === item.id;

            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`relative w-full flex items-center gap-3 px-3 py-2.5 rounded-2xl font-semibold text-sm transition-all text-left z-10 cursor-pointer ${
                  isActive
                    ? 'text-[#1DB954] font-bold'
                    : 'text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white'
                }`}
                title={item.label}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeNavPill"
                    transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                    className="absolute inset-0 bg-[#1DB954]/15 border-l-4 border-[#1DB954] rounded-2xl z-0 shadow-sm"
                  />
                )}
                <Icon className="w-4 h-4 flex-shrink-0 z-10" />
                {!sidebarCollapsed && <span className="z-10">{item.label}</span>}
              </button>
            );
          })}
        </div>
      </div>

      {/* Static System Status Rows (FIRM & IMMOVABLE) */}
      {!sidebarCollapsed && (
        <div className="px-4 py-3 border-t border-black/10 dark:border-white/10 bg-white/40 dark:bg-[#0A0A0A]/40 text-xs text-[#475569] dark:text-[#A7A7A7] space-y-1.5">
          <div className="font-bold text-[#111827] dark:text-white mb-1 flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5 text-[#1DB954]" />
            <span>System Status</span>
          </div>
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${health.status === 'healthy' ? 'bg-[#1DB954] animate-pulse' : 'bg-[#F5B942]'}`} />
            <span>Backend: {health.status === 'healthy' ? 'Operational' : 'Degraded'}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#1DB954]" />
            <span>News Search: Operational</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#1DB954]" />
            <span>AI Explanation: Operational</span>
          </div>
        </div>
      )}

      {/* Bottom ChatGPT-Style Account Control Trigger Button */}
      <div className="p-3 border-t border-black/10 dark:border-white/10 bg-[#F8F9FA] dark:bg-[#0D0D0D] relative">
        <button
          id="account-trigger-btn"
          onClick={() => setAccountPopoverOpen(!accountPopoverOpen)}
          className={`w-full flex items-center gap-3 px-2.5 py-2 rounded-2xl hover:bg-black/5 dark:hover:bg-white/10 transition-colors text-left focus:outline-none cursor-pointer ${
            sidebarCollapsed ? 'justify-center px-0' : ''
          }`}
          title={sidebarCollapsed ? 'Account' : 'Account Profile'}
        >
          <div className="w-8 h-8 rounded-full bg-[#1DB954]/20 border border-[#1DB954]/40 flex items-center justify-center text-[#1DB954] font-bold text-xs flex-shrink-0 shadow-sm">
            A
          </div>
          {!sidebarCollapsed && (
            <div className="flex-1 truncate">
              <div className="text-xs font-semibold leading-none text-[#111827] dark:text-white truncate">Abhi</div>
              <div className="text-[10px] text-[#475569] dark:text-[#A7A7A7] mt-1 leading-none">Free / Local Mode</div>
            </div>
          )}
        </button>

        {/* Render Account Popover Fixed Overlay */}
        <AccountPopover />
      </div>
    </motion.aside>
  );
};
