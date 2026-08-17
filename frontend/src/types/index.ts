export type NavigationPage = 'verify' | 'history' | 'settings' | 'about';

export type ThemeMode = 'dark' | 'light' | 'system';

export interface EvidenceArticle {
  publisher?: string;
  source_domain?: string;
  headline?: string;
  title?: string;
  publication_date?: string;
  finding?: string;
  snippet?: string;
  summary?: string;
  url?: string;
}

export interface SignalItem {
  feature?: string;
  contribution?: number;
  [key: string]: unknown;
}

export interface VerificationResult {
  success: boolean;
  claim: string;
  verdict: 'LIKELY_TRUE' | 'LIKELY_FALSE' | 'UNVERIFIED' | string;
  confidence: number;
  confidence_level: string;
  summary?: string;
  why?: string[];
  supporting_evidence?: EvidenceArticle[];
  contradicting_evidence?: EvidenceArticle[];
  source_assessment?: string;
  ml_interpretation?: string;
  ml_results?: Array<{ signals?: SignalItem[] }>;
  limitations?: string[];
  user_safety?: string;
  articles_found?: number;
  timestamp?: string;
  error?: string;
}

export interface HistoryItem {
  id: string;
  claim: string;
  verdict: string;
  confidence: number;
  confidence_level: string;
  summary: string;
  timestamp: string;
  date_obj: string;
  supporting_count: number;
  contradicting_count: number;
  full_result: VerificationResult;
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unavailable' | string;
  version?: string;
  timestamp?: string;
}
