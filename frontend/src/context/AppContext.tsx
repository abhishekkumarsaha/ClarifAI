import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { NavigationPage, ThemeMode, VerificationResult, HistoryItem, HealthStatus } from '../types';
import { fetchHealthStatus } from '../services/api';

interface AppContextType {
  activeNav: NavigationPage;
  setActiveNav: (page: NavigationPage) => void;
  theme: ThemeMode;
  setTheme: (theme: ThemeMode) => void;
  claimInput: string;
  setClaimInput: (input: string) => void;
  currentResult: VerificationResult | null;
  setCurrentResult: (result: VerificationResult | null) => void;
  history: HistoryItem[];
  addHistoryItem: (result: VerificationResult) => void;
  deleteHistoryItem: (id: string) => void;
  clearHistory: () => void;
  savedItems: Set<string>;
  toggleSaveItem: (claim: string) => void;
  maxArticlesLimit: number;
  setMaxArticlesLimit: (limit: number) => void;
  sidebarCollapsed: boolean;
  setSidebarCollapsed: (collapsed: boolean | ((prev: boolean) => boolean)) => void;
  accountPopoverOpen: boolean;
  setAccountPopoverOpen: (open: boolean) => void;
  threeDotMenuOpen: boolean;
  setThreeDotMenuOpen: (open: boolean) => void;
  activeModal: 'export' | 'report' | 'doc' | 'cache' | null;
  setActiveModal: (modal: 'export' | 'report' | 'doc' | 'cache' | null) => void;
  health: HealthStatus;
  refreshHealth: () => void;
  resetVerification: () => void;
  toastMsg: string | null;
  showToast: (msg: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const LOCAL_STORAGE_HISTORY_KEY = 'clarifai_history_v2';
const LOCAL_STORAGE_SAVED_KEY = 'clarifai_saved_v2';
const LOCAL_STORAGE_THEME_KEY = 'clarifai_theme_v2';

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activeNav, setActiveNav] = useState<NavigationPage>('verify');
  const [theme, setThemeState] = useState<ThemeMode>(() => {
    const saved = localStorage.getItem(LOCAL_STORAGE_THEME_KEY) as ThemeMode;
    return saved || 'dark';
  });

  const [claimInput, setClaimInput] = useState<string>('');
  const [currentResult, setCurrentResult] = useState<VerificationResult | null>(null);
  const [toastMsg, setToastMsg] = useState<string | null>(null);
  
  const [history, setHistory] = useState<HistoryItem[]>(() => {
    try {
      const saved = localStorage.getItem(LOCAL_STORAGE_HISTORY_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [savedItems, setSavedItems] = useState<Set<string>>(() => {
    try {
      const saved = localStorage.getItem(LOCAL_STORAGE_SAVED_KEY);
      return saved ? new Set(JSON.parse(saved)) : new Set();
    } catch {
      return new Set();
    }
  });

  const [maxArticlesLimit, setMaxArticlesLimit] = useState<number>(5);
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(false);
  const [accountPopoverOpen, setAccountPopoverOpen] = useState<boolean>(false);
  const [threeDotMenuOpen, setThreeDotMenuOpen] = useState<boolean>(false);
  const [activeModal, setActiveModal] = useState<'export' | 'report' | 'doc' | 'cache' | null>(null);
  const [health, setHealth] = useState<HealthStatus>({ status: 'healthy' });

  const showToast = (msg: string) => {
    setToastMsg(msg);
    setTimeout(() => {
      setToastMsg((prev) => (prev === msg ? null : prev));
    }, 3000);
  };

  // Sync Theme to HTML Root Element
  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_THEME_KEY, theme);
    const root = document.documentElement;
    
    if (theme === 'light') {
      root.classList.remove('dark');
    } else if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        root.classList.add('dark');
      } else {
        root.classList.remove('dark');
      }
    }
  }, [theme]);

  // Global Keyboard Shortcuts (Ctrl+K, Ctrl+H, Escape)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setActiveNav('verify');
        const input = document.getElementById('main-claim-search-input');
        if (input) input.focus();
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'h') {
        e.preventDefault();
        setActiveNav('history');
      } else if (e.key === 'Escape') {
        setActiveModal(null);
        setAccountPopoverOpen(false);
        setThreeDotMenuOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Sync History to LocalStorage
  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_HISTORY_KEY, JSON.stringify(history));
  }, [history]);

  // Sync Saved Items to LocalStorage
  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_SAVED_KEY, JSON.stringify(Array.from(savedItems)));
  }, [savedItems]);

  // Fetch Health on Mount
  useEffect(() => {
    refreshHealth();
  }, []);

  const refreshHealth = () => {
    fetchHealthStatus().then(setHealth);
  };

  const setTheme = (mode: ThemeMode) => {
    setThemeState(mode);
  };

  const addHistoryItem = (res: VerificationResult) => {
    const newItem: HistoryItem = {
      id: crypto.randomUUID(),
      claim: res.claim,
      verdict: res.verdict,
      confidence: res.confidence,
      confidence_level: res.confidence_level || 'Unknown',
      summary: res.summary || '',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      date_obj: new Date().toISOString().split('T')[0],
      supporting_count: res.supporting_evidence?.length || 0,
      contradicting_count: res.contradicting_evidence?.length || 0,
      full_result: res,
    };

    setHistory((prev) => {
      const exists = prev.some((item) => item.claim === res.claim);
      if (exists) return prev;
      return [newItem, ...prev];
    });

    showToast('Verification result saved to local history');
  };

  const deleteHistoryItem = (id: string) => {
    setHistory((prev) => prev.filter((item) => item.id !== id));
    showToast('History item deleted');
  };

  const clearHistory = () => {
    setHistory([]);
    showToast('Local history cleared');
  };

  const toggleSaveItem = (claim: string) => {
    setSavedItems((prev) => {
      const next = new Set(prev);
      if (next.has(claim)) {
        next.delete(claim);
        showToast('Claim removed from bookmarks');
      } else {
        next.add(claim);
        showToast('Claim saved to bookmarks');
      }
      return next;
    });
  };

  const resetVerification = () => {
    setCurrentResult(null);
    setClaimInput('');
    setActiveNav('verify');
  };

  return (
    <AppContext.Provider
      value={{
        activeNav,
        setActiveNav,
        theme,
        setTheme,
        claimInput,
        setClaimInput,
        currentResult,
        setCurrentResult,
        history,
        addHistoryItem,
        deleteHistoryItem,
        clearHistory,
        savedItems,
        toggleSaveItem,
        maxArticlesLimit,
        setMaxArticlesLimit,
        sidebarCollapsed,
        setSidebarCollapsed,
        accountPopoverOpen,
        setAccountPopoverOpen,
        threeDotMenuOpen,
        setThreeDotMenuOpen,
        activeModal,
        setActiveModal,
        health,
        refreshHealth,
        resetVerification,
        toastMsg,
        showToast,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
