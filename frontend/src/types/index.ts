export type NavigationPage =
  | 'verify'
  | 'history'
  | 'settings'
  | 'about';

export type ThemeMode =
  | 'dark'
  | 'light'
  | 'system';

/* ============================================================
   EVIDENCE
   ============================================================ */

export interface EvidenceArticle {
  id?: string | number;

  publisher?: string;
  source?: string;
  source_domain?: string;
  provider?: string;

  headline?: string;
  title?: string;
  article_title?: string;

  publication_date?: string;
  published_at?: string;
  pubDate?: string;

  finding?: string;
  snippet?: string;
  summary?: string;
  description?: string;
  content?: string;

  url?: string;
  original_url?: string;
  final_url?: string;

  input_method?: string;

  extraction_success?: boolean;
  extraction_method?: string;
  evidence_quality?: string;
  extraction_error?: string;

  ml_analysis?: MLAnalysis | null;
}

/* ============================================================
   ML ANALYSIS
   ============================================================ */

export interface SignalItem {
  feature?: string;
  contribution?: number;
  [key: string]: unknown;
}

export interface MLAnalysis {
  prediction?: string;
  confidence?: number;
  signals?: SignalItem[];
  [key: string]: unknown;
}

/* ============================================================
   EVIDENCE SUMMARY
   ============================================================ */

export interface EvidenceSummary {
  articles_found?: number;
  articles_extracted?: number;

  independent_domains?: number;
  domains?: string[];

  ml_real_count?: number;
  ml_fake_count?: number;
  ml_neutral_count?: number;

  average_ml_confidence?: number;

  source_details?: unknown[];
  evidence_articles?: EvidenceArticle[];

  error?: string;

  [key: string]: unknown;
}

/* ============================================================
   VERIFICATION RESULT
   ============================================================ */

export interface VerificationResult {
  success: boolean;

  /* Input information */
  claim: string;
  input_type?: 'claim' | 'url' | string;

  source_url?: string;
  source_domain?: string;
  article_title?: string;

  /* Final verdict */
  verdict:
  | 'LIKELY_TRUE'
  | 'LIKELY_FALSE'
  | 'UNVERIFIED'
  | string;

  confidence: number;
  confidence_level: string;

  /* AI explanation */
  summary?: string;

  why?: string[];

  supporting_evidence?: EvidenceArticle[];

  contradicting_evidence?: EvidenceArticle[];

  ml_interpretation?: string;

  source_assessment?: string;

  limitations?: string[];

  user_safety?: string;

  /* Full evidence pipeline */
  evidence?: EvidenceArticle[];

  evidence_summary?: EvidenceSummary;

  /* Article counts */
  articles_found?: number;
  articles_extracted?: number;

  /* ML results */
  ml_results?: MLAnalysis[];

  /* AI availability */
  ai_available?: boolean;

  /* Extraction information */
  extraction_method?: string;
  evidence_quality?: string;

  /* Error information */
  error?: string;

  /* Timestamp */
  timestamp?: string;

  [key: string]: unknown;
}

/* ============================================================
   HISTORY
   ============================================================ */

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

/* ============================================================
   HEALTH
   ============================================================ */

export interface HealthStatus {
  status:
  | 'healthy'
  | 'degraded'
  | 'unavailable'
  | string;

  version?: string;

  timestamp?: string;

  [key: string]: unknown;
}