import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
  ReactNode,
} from 'react';

import {
  NavigationPage,
  ThemeMode,
  VerificationResult,
  HistoryItem,
  HealthStatus,
} from '../types';

import {
  fetchHealthStatus,
} from '../services/api';

interface AppContextType {
  activeNav: NavigationPage;
  setActiveNav: (page: NavigationPage) => void;

  theme: ThemeMode;
  setTheme: (theme: ThemeMode) => void;

  soundEnabled: boolean;
  setSoundEnabled: (enabled: boolean) => void;

  claimInput: string;
  setClaimInput: (input: string) => void;

  currentResult: VerificationResult | null;
  setCurrentResult: (
    result: VerificationResult | null
  ) => void;

  history: HistoryItem[];
  addHistoryItem: (
    result: VerificationResult
  ) => void;
  deleteHistoryItem: (id: string) => void;
  clearHistory: () => void;

  savedItems: Set<string>;
  toggleSaveItem: (claim: string) => void;

  maxArticlesLimit: number;
  setMaxArticlesLimit: (limit: number) => void;

  sidebarCollapsed: boolean;
  setSidebarCollapsed: (
    collapsed:
      | boolean
      | ((prev: boolean) => boolean)
  ) => void;

  accountPopoverOpen: boolean;
  setAccountPopoverOpen: (open: boolean) => void;

  threeDotMenuOpen: boolean;
  setThreeDotMenuOpen: (open: boolean) => void;

  activeModal:
    | 'export'
    | 'report'
    | 'doc'
    | 'cache'
    | null;

  setActiveModal: (
    modal:
      | 'export'
      | 'report'
      | 'doc'
      | 'cache'
      | null
  ) => void;

  health: HealthStatus;

  refreshHealth: () => Promise<void>;

  resetVerification: () => void;

  toastMsg: string | null;
  showToast: (msg: string) => void;
}

const AppContext =
  createContext<AppContextType | undefined>(
    undefined
  );

const LOCAL_STORAGE_HISTORY_KEY = 'clarifai_history_v2';
const SESSION_STORAGE_HISTORY_KEY = 'clarifai_history_backup_v2';

const LOCAL_STORAGE_SAVED_KEY = 'clarifai_saved_v2';
const LOCAL_STORAGE_THEME_KEY = 'clarifai_theme_v2';
const LOCAL_STORAGE_SOUND_KEY = 'clarifai_sound_enabled';

// In-Memory Fallback Cache to Prevent Storage Reset During HMR
let inMemoryHistoryBackup: HistoryItem[] | null = null;

// Helper to sanitize VerificationResult so history objects stay ultra-lightweight (< 2KB)
function sanitizeResultForHistory(res: VerificationResult): VerificationResult {
  return {
    success: res.success ?? true,
    claim: res.claim,
    verdict: res.verdict,
    confidence: res.confidence,
    confidence_level: res.confidence_level || 'Unknown',
    summary: res.summary || '',
    articles_found: res.articles_found || 0,
    supporting_evidence: (res.supporting_evidence || []).map((art) => ({
      title: art.title || art.headline || '',
      headline: art.headline || art.title || '',
      publisher: art.publisher || 'Source',
      url: art.url || '#',
      snippet: (art.snippet || '').slice(0, 150),
    })),
    contradicting_evidence: (res.contradicting_evidence || []).map((art) => ({
      title: art.title || art.headline || '',
      headline: art.headline || art.title || '',
      publisher: art.publisher || 'Source',
      url: art.url || '#',
      snippet: (art.snippet || '').slice(0, 150),
    })),
  };
}

export const AppProvider: React.FC<{
  children: ReactNode;
}> = ({ children }) => {

  // ==========================================================
  // NAVIGATION
  // ==========================================================

  const [activeNav, setActiveNav] =
    useState<NavigationPage>('verify');

  // ==========================================================
  // THEME
  // ==========================================================

  const [theme, setThemeState] =
    useState<ThemeMode>(() => {
      try {
        const saved = localStorage.getItem(LOCAL_STORAGE_THEME_KEY) as ThemeMode | null;
        if (saved === 'dark' || saved === 'light' || saved === 'system') {
          return saved;
        }
      } catch {
        // Ignore storage errors
      }
      return 'dark';
    });

  // ==========================================================
  // SOUND
  // ==========================================================

  const [soundEnabled, setSoundEnabledState] =
    useState<boolean>(() => {
      try {
        const saved = localStorage.getItem(LOCAL_STORAGE_SOUND_KEY);
        return saved !== 'false';
      } catch {
        return true;
      }
    });

  const setSoundEnabled = (enabled: boolean) => {
    setSoundEnabledState(enabled);
    try {
      localStorage.setItem(LOCAL_STORAGE_SOUND_KEY, enabled ? 'true' : 'false');
    } catch {
      // Ignore storage errors
    }
  };

  // ==========================================================
  // VERIFICATION
  // ==========================================================

  const [claimInput, setClaimInput] = useState<string>('');
  const [currentResult, setCurrentResult] = useState<VerificationResult | null>(null);

  // ==========================================================
  // TOAST
  // ==========================================================

  const [toastMsg, setToastMsg] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMsg(msg);
    window.setTimeout(() => {
      setToastMsg((prev) => (prev === msg ? null : prev));
    }, 3000);
  };

  // ==========================================================
  // RESILIENT DUAL-LAYER HISTORY PERSISTENCE
  // ==========================================================

  const isHistoryLoadedRef = useRef<boolean>(false);

  const [history, setHistory] = useState<HistoryItem[]>(() => {
    // Priority 1: In-Memory Backup
    if (inMemoryHistoryBackup && inMemoryHistoryBackup.length > 0) {
      return inMemoryHistoryBackup;
    }

    // Priority 2: LocalStorage
    try {
      const savedLocal = localStorage.getItem(LOCAL_STORAGE_HISTORY_KEY);
      if (savedLocal) {
        const parsed = JSON.parse(savedLocal);
        if (Array.isArray(parsed) && parsed.length > 0) {
          inMemoryHistoryBackup = parsed;
          return parsed;
        }
      }
    } catch {
      // Ignore storage read errors
    }

    // Priority 3: SessionStorage Backup
    try {
      const savedSession = sessionStorage.getItem(SESSION_STORAGE_HISTORY_KEY);
      if (savedSession) {
        const parsed = JSON.parse(savedSession);
        if (Array.isArray(parsed) && parsed.length > 0) {
          inMemoryHistoryBackup = parsed;
          return parsed;
        }
      }
    } catch {
      // Ignore session storage read errors
    }

    return [];
  });

  // Mark Initial History Load Complete
  useEffect(() => {
    isHistoryLoadedRef.current = true;
  }, []);

  // Sync History to LocalStorage & SessionStorage Safely (with Quota Overflow Protection)
  useEffect(() => {
    if (!isHistoryLoadedRef.current) return;

    inMemoryHistoryBackup = history;

    const historyJson = JSON.stringify(history);

    // Save to LocalStorage
    try {
      localStorage.setItem(LOCAL_STORAGE_HISTORY_KEY, historyJson);
    } catch {
      // QuotaExceededError handling: slice to 20 items and retry
      try {
        const trimmed = history.slice(0, 20);
        localStorage.setItem(LOCAL_STORAGE_HISTORY_KEY, JSON.stringify(trimmed));
      } catch {
        // Fallback
      }
    }

    // Save to SessionStorage Backup
    try {
      sessionStorage.setItem(SESSION_STORAGE_HISTORY_KEY, historyJson);
    } catch {
      // Ignore session storage errors
    }
  }, [history]);

  // ==========================================================
  // SAVED ITEMS PERSISTENCE
  // ==========================================================

  const [savedItems, setSavedItems] = useState<Set<string>>(() => {
    try {
      const saved = localStorage.getItem(LOCAL_STORAGE_SAVED_KEY);
      if (!saved) return new Set<string>();
      const parsed = JSON.parse(saved);
      return Array.isArray(parsed) ? new Set<string>(parsed) : new Set<string>();
    } catch {
      return new Set<string>();
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(
        LOCAL_STORAGE_SAVED_KEY,
        JSON.stringify(Array.from(savedItems))
      );
    } catch {
      // Ignore storage errors
    }
  }, [savedItems]);

  // ==========================================================
  // UI STATE
  // ==========================================================

  const [maxArticlesLimit, setMaxArticlesLimit] = useState<number>(5);
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(false);
  const [accountPopoverOpen, setAccountPopoverOpen] = useState<boolean>(false);
  const [threeDotMenuOpen, setThreeDotMenuOpen] = useState<boolean>(false);
  const [activeModal, setActiveModal] = useState<
    'export' | 'report' | 'doc' | 'cache' | null
  >(null);

  // ==========================================================
  // BACKEND HEALTH MONITOR
  // ==========================================================

  const [health, setHealth] = useState<HealthStatus>({ status: 'unavailable' });

  const refreshHealth = async () => {
    try {
      const result = await fetchHealthStatus();
      if (result && result.status) {
        setHealth(result);
      } else {
        setHealth({ status: 'degraded' });
      }
    } catch {
      setHealth({ status: 'unavailable' });
    }
  };

  useEffect(() => {
    let mounted = true;
    const checkHealth = async () => {
      try {
        const result = await fetchHealthStatus();
        if (!mounted) return;
        if (result && result.status) {
          setHealth(result);
        } else {
          setHealth({ status: 'degraded' });
        }
      } catch {
        if (mounted) {
          setHealth({ status: 'unavailable' });
        }
      }
    };

    checkHealth();
    const interval = window.setInterval(checkHealth, 15000);
    return () => {
      mounted = false;
      window.clearInterval(interval);
    };
  }, []);

  // ==========================================================
  // THEME SYNC
  // ==========================================================

  useEffect(() => {
    try {
      localStorage.setItem(LOCAL_STORAGE_THEME_KEY, theme);
    } catch {
      // Ignore storage errors
    }

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

  // ==========================================================
  // KEYBOARD SHORTCUTS
  // ==========================================================

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setActiveNav('verify');
        const input = document.getElementById('main-claim-search-input') as HTMLInputElement | null;
        input?.focus();
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

  // ==========================================================
  // THEME SETTER
  // ==========================================================

  const setTheme = (mode: ThemeMode) => {
    setThemeState(mode);
  };

  // ==========================================================
  // ADD HISTORY ITEM (WITH AUTOMATIC DUP CHECK & DUAL BACKUP)
  // ==========================================================

  const addHistoryItem = (res: VerificationResult) => {
    const sanitizedResult = sanitizeResultForHistory(res);

    const newItem: HistoryItem = {
      id: crypto.randomUUID(),
      claim: sanitizedResult.claim,
      verdict: sanitizedResult.verdict,
      confidence: sanitizedResult.confidence,
      confidence_level: sanitizedResult.confidence_level || 'Unknown',
      summary: sanitizedResult.summary || '',
      timestamp: new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      }),
      date_obj: new Date().toISOString().split('T')[0],
      supporting_count: sanitizedResult.supporting_evidence?.length || 0,
      contradicting_count: sanitizedResult.contradicting_evidence?.length || 0,
      full_result: sanitizedResult,
    };

    setHistory((prev) => {
      const existsIndex = prev.findIndex(
        (item) => item.claim.toLowerCase().trim() === res.claim.toLowerCase().trim()
      );

      let nextHistory: HistoryItem[];
      if (existsIndex !== -1) {
        // Update existing entry with new scan results and move to top
        const updated = [...prev];
        updated.splice(existsIndex, 1);
        nextHistory = [newItem, ...updated];
      } else {
        nextHistory = [newItem, ...prev];
      }

      // Keep max 50 history items to prevent browser storage bloat
      const trimmedHistory = nextHistory.slice(0, 50);

      // Instantly update backups
      inMemoryHistoryBackup = trimmedHistory;
      try {
        const json = JSON.stringify(trimmedHistory);
        localStorage.setItem(LOCAL_STORAGE_HISTORY_KEY, json);
        sessionStorage.setItem(SESSION_STORAGE_HISTORY_KEY, json);
      } catch {
        // Storage failover
      }

      return trimmedHistory;
    });

    showToast('Verification result saved to local history');
  };

  // ==========================================================
  // DELETE HISTORY
  // ==========================================================

  const deleteHistoryItem = (id: string) => {
    setHistory((prev) => {
      const next = prev.filter((item) => item.id !== id);
      inMemoryHistoryBackup = next;
      try {
        const json = JSON.stringify(next);
        localStorage.setItem(LOCAL_STORAGE_HISTORY_KEY, json);
        sessionStorage.setItem(SESSION_STORAGE_HISTORY_KEY, json);
      } catch {
        // Failover
      }
      return next;
    });

    showToast('History item deleted');
  };

  // ==========================================================
  // CLEAR HISTORY
  // ==========================================================

  const clearHistory = () => {
    setHistory([]);
    inMemoryHistoryBackup = [];
    try {
      localStorage.removeItem(LOCAL_STORAGE_HISTORY_KEY);
      sessionStorage.removeItem(SESSION_STORAGE_HISTORY_KEY);
    } catch {
      // Failover
    }
    showToast('Local history cleared');
  };

  // ==========================================================
  // SAVED ITEMS
  // ==========================================================

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

  // ==========================================================
  // RESET
  // ==========================================================

  const resetVerification = () => {
    setCurrentResult(null);
    setClaimInput('');
    setActiveNav('verify');
  };

  // ==========================================================
  // PROVIDER
  // ==========================================================

  return (
    <AppContext.Provider
      value={{
        activeNav,
        setActiveNav,

        theme,
        setTheme,

        soundEnabled,
        setSoundEnabled,

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

// ============================================================
// HOOK
// ============================================================

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};