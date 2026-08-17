import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Search,
  ArrowRight,
  Sparkles,
  Bookmark,
  BookmarkCheck,
  Share2,
  RotateCcw,
  ExternalLink,
  ShieldAlert,
  Mic,
  MicOff,
  Printer,
  Newspaper,
  ChevronDown,
  Receipt,
  Cpu,
  Network,
  Globe,
  Radio,
  TrendingUp,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  BarChart3,
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { analyzeClaim, fetchLatestNews } from '../services/api';
import { EvidenceArticle } from '../types';
import { playGlassClickSound, playSuccessChime } from '../utils/audio';

export const VerifyPage: React.FC = () => {
  const {
    claimInput,
    setClaimInput,
    currentResult,
    setCurrentResult,
    addHistoryItem,
    savedItems,
    toggleSaveItem,
    maxArticlesLimit,
    setMaxArticlesLimit,
    resetVerification,
    showToast,
  } = useApp();

  const [loading, setLoading] = useState<boolean>(false);
  const [loadingStage, setLoadingStage] = useState<string>('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isListening, setIsListening] = useState<boolean>(false);
  const [showReceipt, setShowReceipt] = useState<boolean>(false);
  const [animatedConfidence, setAnimatedConfidence] = useState<number>(0);

  // Live News State
  const [newsArticles, setNewsArticles] = useState<EvidenceArticle[]>([]);
  const [newsLoading, setNewsLoading] = useState<boolean>(true);

  // Trending Radar Claims
  const radarClaims = [
    'CDC releases updated respiratory health guidance',
    'Federal Reserve benchmark rate decision update',
    'James Webb telescope detects atmosphere on rocky exoplanet',
    'Global renewable power generation crosses 35% milestone',
  ];

  // Quick Sample Presets
  const samplePresets = [
    { label: 'Health Policy', query: 'WHO updates global vaccination guidelines for 2026' },
    { label: 'Technology', query: 'Quantum computing milestone achieved by researchers' },
    { label: 'Climate Science', query: 'Global solar energy adoption breaks annual record' },
  ];

  // URL Auto Detection
  const isUrlDetected = claimInput.trim().startsWith('http://') || claimInput.trim().startsWith('https://');

  useEffect(() => {
    fetchLatestNews()
      .then((articles) => {
        setNewsArticles(articles);
        setNewsLoading(false);
      })
      .catch(() => setNewsLoading(false));
  }, []);

  // Radial Ring Confidence Entry Animation & Success Chime
  useEffect(() => {
    if (currentResult?.confidence) {
      playSuccessChime();
      setAnimatedConfidence(0);
      const target = currentResult.confidence;
      const duration = 1000;
      const steps = 30;
      const stepTime = duration / steps;
      let currentStep = 0;

      const timer = setInterval(() => {
        currentStep++;
        const progress = currentStep / steps;
        setAnimatedConfidence(target * Math.min(progress, 1));

        if (currentStep >= steps) {
          clearInterval(timer);
        }
      }, stepTime);

      return () => clearInterval(timer);
    }
  }, [currentResult]);

  // Voice Search Handler (Ultra-Short Alerts)
  const toggleVoiceInput = () => {
    playGlassClickSound();
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      showToast('Voice unavailable');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const SpeechRecognitionClass = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognitionClass();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
        showToast('Listening');
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setClaimInput(transcript);
        setIsListening(false);
        showToast('Captured');
      };

      recognition.onerror = () => {
        setIsListening(false);
        showToast('Voice error');
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } catch (e) {
      setIsListening(false);
    }
  };

  // Primary Verification Execution
  const handleVerify = async (claimToVerify?: string) => {
    const query = (claimToVerify || claimInput).trim();
    if (!query) {
      setErrorMsg('Please enter a valid news claim or article URL.');
      return;
    }

    playGlassClickSound();
    setErrorMsg(null);
    setLoading(true);
    setLoadingStage('Analyzing claim semantics & entities...');

    try {
      setTimeout(() => setLoadingStage('Querying live published news coverage...'), 600);
      setTimeout(() => setLoadingStage('Evaluating linguistic patterns with SVM model...'), 1200);
      setTimeout(() => setLoadingStage('Synthesizing evidence summary & verdict...'), 1800);

      const res = await analyzeClaim(query, maxArticlesLimit);
      setCurrentResult(res);
      addHistoryItem(res);
      setLoading(false);
    } catch (err: any) {
      setLoading(false);
      setErrorMsg(err.message || 'Failed to verify claim. Please check connection and try again.');
    }
  };

  const handleSelectNewsArticle = (art: EvidenceArticle) => {
    const titleText = art.title || art.headline || '';
    setClaimInput(titleText);
    handleVerify(titleText);
  };

  const handleCopySummary = () => {
    playGlassClickSound();
    if (!currentResult) return;
    const textToCopy = `ClarifAI Verification Receipt:\nClaim: "${currentResult.claim}"\nVerdict: ${currentResult.verdict} (${currentResult.confidence.toFixed(1)}% Confidence)\nSummary: ${currentResult.summary}`;
    navigator.clipboard.writeText(textToCopy);
    showToast('Receipt copied');
  };

  const isCurrentSaved = currentResult ? savedItems.has(currentResult.claim) : false;

  // Consensus Heatmap Ratio
  const supportingCount = currentResult?.supporting_evidence?.length || 0;
  const contradictingCount = currentResult?.contradicting_evidence?.length || 0;
  const totalArticles = Math.max(supportingCount + contradictingCount, 1);
  const supportingPct = (supportingCount / totalArticles) * 100;
  const contradictingPct = (contradictingCount / totalArticles) * 100;

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header & Mission Intro */}
      <div className="text-center max-w-2xl mx-auto space-y-3">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-content border border-[#00C2FF]/30 text-xs font-bold text-[#00C2FF] shadow-sm">
          <Sparkles className="w-3.5 h-3.5 text-[#00C2FF]" />
          <span>ClarifAI v2.0 Liquid Intelligence Engine</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-black tracking-tight text-[#111827] dark:text-white">
          Verify what you heard.
        </h1>

        <p className="text-base text-[#475569] dark:text-[#A7A7A7] leading-relaxed">
          Search live published news indexes, analyze structural linguistic patterns, and uncover evidence alignment in seconds.
        </p>
      </div>

      {/* SEARCH COMMAND BAR & BREAKING RADAR TICKER */}
      <div className="space-y-3 max-w-3xl mx-auto">
        {/* Real-time Misinformation Radar Ticker */}
        <div className="flex items-center gap-2 px-4 py-2.5 glass-content rounded-2xl border border-black/15 dark:border-white/20 text-xs text-[#475569] dark:text-[#A7A7A7] overflow-x-auto no-scrollbar">
          <span className="flex items-center gap-1.5 font-bold text-[#FF4D5A] flex-shrink-0">
            <Radio className="w-3.5 h-3.5 animate-pulse" />
            <span>BREAKING RADAR:</span>
          </span>
          <div className="flex items-center gap-3 overflow-x-auto no-scrollbar py-0.5">
            {radarClaims.map((item, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setClaimInput(item);
                  playGlassClickSound();
                }}
                className="whitespace-nowrap hover:text-[#00C2FF] transition-colors font-medium cursor-pointer text-left flex items-center gap-1"
              >
                <TrendingUp className="w-3 h-3 text-[#00C2FF]" />
                <span>"{item}"</span>
              </button>
            ))}
          </div>
        </div>

        {/* Liquid Glass Search Bar Instrument */}
        <div className="glass-on-air rounded-3xl p-3 shadow-2xl border border-black/15 dark:border-white/20 relative transition-all duration-200">
          <div className="flex items-center gap-3">
            <div className="pl-2 text-[#00C2FF] flex-shrink-0">
              <Search className="w-5 h-5" />
            </div>

            <input
              id="main-claim-search-input"
              type="text"
              value={claimInput}
              onChange={(e) => setClaimInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleVerify()}
              placeholder="Paste news claim or article URL..."
              className="flex-1 bg-transparent border-none text-sm md:text-base font-medium text-[#111827] dark:text-white placeholder-[#64748B] dark:placeholder-[#666666] focus:outline-none"
            />

            {/* URL Auto Detection Pill */}
            {isUrlDetected && (
              <span className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-[#00C2FF]/15 border border-[#00C2FF]/40 text-[10px] font-bold text-[#00C2FF]">
                <Globe className="w-3 h-3" />
                <span>URL</span>
              </span>
            )}

            {/* Ultra-Short Micro Voice Indicator Badge */}
            {isListening && (
              <span className="px-2 py-0.5 rounded-full bg-[#FF4D5A]/20 border border-[#FF4D5A]/50 text-[10px] font-black text-[#FF4D5A] flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-[#FF4D5A] animate-ping" />
                REC
              </span>
            )}

            {/* Voice Input Button */}
            <button
              onClick={toggleVoiceInput}
              className={`p-2.5 rounded-full border transition-all cursor-pointer active:scale-95 ${
                isListening
                  ? 'bg-[#FF4D5A]/20 border-[#FF4D5A] text-[#FF4D5A]'
                  : 'glass-interactive text-[#475569] dark:text-[#A7A7A7]'
              }`}
              title="Voice Search"
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </button>

            {/* Article Limit Dropdown */}
            <div className="relative hidden md:block">
              <select
                value={maxArticlesLimit}
                onChange={(e) => {
                  playGlassClickSound();
                  setMaxArticlesLimit(Number(e.target.value));
                }}
                className="glass-interactive appearance-none py-2.5 pl-3 pr-8 rounded-full text-xs font-bold text-[#111827] dark:text-white focus:outline-none cursor-pointer border border-black/15 dark:border-white/20"
              >
                <option value={3} className="bg-white dark:bg-[#121212]">3 articles</option>
                <option value={5} className="bg-white dark:bg-[#121212]">5 articles</option>
                <option value={8} className="bg-white dark:bg-[#121212]">8 articles</option>
                <option value={10} className="bg-white dark:bg-[#121212]">10 articles</option>
              </select>
              <ChevronDown className="w-3.5 h-3.5 text-[#475569] dark:text-[#A7A7A7] absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>

            {/* Analyze CTA Button */}
            <button
              onClick={() => handleVerify()}
              disabled={loading}
              className="flex items-center gap-2 px-5 py-3 bg-[#1DB954] text-black font-bold text-xs md:text-sm rounded-full shadow-lg hover:bg-[#1ed760] active:scale-98 transition-all cursor-pointer disabled:opacity-50"
            >
              <span>{loading ? 'Analyzing...' : 'Analyze Claim'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Quick Instant Sample Claim Presets */}
        <div className="flex items-center justify-center gap-2 pt-1 flex-wrap text-xs">
          <span className="text-[#475569] dark:text-[#A7A7A7] font-medium text-[11px]">Try sample:</span>
          {samplePresets.map((sp, idx) => (
            <button
              key={idx}
              onClick={() => {
                setClaimInput(sp.query);
                playGlassClickSound();
              }}
              className="px-3 py-1 rounded-full glass-interactive border border-black/15 dark:border-white/20 text-[11px] font-semibold text-[#475569] dark:text-[#A7A7A7] hover:text-[#00C2FF] transition-colors cursor-pointer"
            >
              {sp.label}
            </button>
          ))}
        </div>

        {/* Error Alert Box */}
        {errorMsg && (
          <div className="px-4 py-2.5 bg-[#FF4D5A]/15 border border-[#FF4D5A]/40 rounded-2xl text-xs font-bold text-[#FF4D5A] flex items-center justify-between shadow-md animate-in fade-in">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 flex-shrink-0" />
              <span>{errorMsg}</span>
            </div>
            <button
              onClick={() => setErrorMsg(null)}
              className="text-[#FF4D5A] hover:text-white text-[10px] uppercase font-extrabold cursor-pointer"
            >
              Dismiss
            </button>
          </div>
        )}
      </div>

      {/* LOADING SCANNING STATE WITH HOLOGRAPHIC PROGRESS BAR */}
      {loading && (
        <div className="max-w-2xl mx-auto p-8 glass-on-air rounded-3xl text-center space-y-5 shadow-2xl border border-[#00C2FF]/30">
          <div className="w-16 h-16 rounded-full bg-[#00C2FF]/10 border border-[#00C2FF]/40 flex items-center justify-center text-[#00C2FF] mx-auto animate-spin">
            <Cpu className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h3 className="text-base font-bold text-[#111827] dark:text-white">Analyzing News Authenticity</h3>
            <p className="text-xs text-[#00C2FF] font-semibold">{loadingStage}</p>
          </div>

          {/* Holographic Line Progress Bar */}
          <div className="w-full h-1.5 bg-black/10 dark:bg-white/10 rounded-full overflow-hidden relative">
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: '100%' }}
              transition={{ repeat: Infinity, duration: 1.4, ease: 'easeInOut' }}
              className="w-1/2 h-full bg-gradient-to-r from-[#00C2FF] via-[#1DB954] to-[#00C2FF] rounded-full"
            />
          </div>
        </div>
      )}

      {/* VERIFICATION RESULT VIEW */}
      {!loading && currentResult && (
        <div className="space-y-8 animate-in fade-in duration-300">
          {/* Action Toolbar */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-4 glass-content rounded-3xl border border-black/15 dark:border-white/20 shadow-lg">
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  playGlassClickSound();
                  resetVerification();
                }}
                className="flex items-center gap-1.5 px-3.5 py-2 glass-interactive rounded-full text-xs font-bold text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white"
              >
                <RotateCcw className="w-3.5 h-3.5 text-[#00C2FF]" />
                <span>Verify Another</span>
              </button>

              <button
                onClick={() => toggleSaveItem(currentResult.claim)}
                className="flex items-center gap-1.5 px-3.5 py-2 glass-interactive rounded-full text-xs font-bold"
              >
                {isCurrentSaved ? (
                  <>
                    <BookmarkCheck className="w-3.5 h-3.5 text-[#1DB954]" />
                    <span className="text-[#1DB954]">Saved</span>
                  </>
                ) : (
                  <>
                    <Bookmark className="w-3.5 h-3.5 text-[#475569] dark:text-[#A7A7A7]" />
                    <span className="text-[#475569] dark:text-[#A7A7A7]">Save</span>
                  </>
                )}
              </button>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleCopySummary}
                className="flex items-center gap-1.5 px-3.5 py-2 glass-interactive rounded-full text-xs font-bold text-[#00C2FF]"
              >
                <Share2 className="w-3.5 h-3.5" />
                <span>Share Receipt</span>
              </button>

              <button
                onClick={() => {
                  playGlassClickSound();
                  window.print();
                }}
                className="flex items-center gap-1.5 px-3.5 py-2 glass-interactive rounded-full text-xs font-bold text-[#1DB954]"
              >
                <Printer className="w-3.5 h-3.5" />
                <span>Print Report</span>
              </button>

              <button
                onClick={() => {
                  playGlassClickSound();
                  setShowReceipt(!showReceipt);
                }}
                className="flex items-center gap-1.5 px-3.5 py-2 glass-interactive rounded-full text-xs font-bold text-[#F5B942]"
              >
                <Receipt className="w-3.5 h-3.5" />
                <span>Receipt</span>
              </button>
            </div>
          </div>

          {/* VERDICT CARD WITH RADIAL PROGRESS RING & HEATMAP SPECTRUM */}
          <div className="p-8 glass-on-air rounded-3xl space-y-6 shadow-2xl border border-black/15 dark:border-white/20 relative overflow-hidden">
            <div className="flex flex-col md:flex-row items-center justify-between gap-6">
              {/* Left: Verdict Badge & Claim */}
              <div className="space-y-3 text-center md:text-left flex-1">
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full font-black text-sm tracking-wider uppercase shadow-md">
                  {currentResult.verdict === 'LIKELY_TRUE' && (
                    <span className="bg-[#1DB954]/15 text-[#1DB954] border border-[#1DB954]/40 px-4 py-1.5 rounded-full flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4" /> LIKELY TRUE
                    </span>
                  )}
                  {currentResult.verdict === 'LIKELY_FALSE' && (
                    <span className="bg-[#FF4D5A]/15 text-[#FF4D5A] border border-[#FF4D5A]/40 px-4 py-1.5 rounded-full flex items-center gap-2">
                      <AlertCircle className="w-4 h-4" /> LIKELY FALSE
                    </span>
                  )}
                  {currentResult.verdict === 'UNVERIFIED' && (
                    <span className="bg-[#F5B942]/15 text-[#F5B942] border border-[#F5B942]/40 px-4 py-1.5 rounded-full flex items-center gap-2">
                      <HelpCircle className="w-4 h-4" /> UNVERIFIED
                    </span>
                  )}
                </div>

                <h2 className="text-xl md:text-2xl font-bold text-[#111827] dark:text-white leading-snug">
                  "{currentResult.claim}"
                </h2>

                <p className="text-xs text-[#475569] dark:text-[#A7A7A7]">
                  Verified on {currentResult.timestamp || 'Today'} • Evaluated across {currentResult.articles_found || 0} live published reports.
                </p>
              </div>

              {/* Right: SVG Radial Progress Ring Score Meter */}
              <div className="flex flex-col items-center justify-center p-4 bg-black/5 dark:bg-white/5 rounded-3xl border border-black/10 dark:border-white/10 min-w-[160px]">
                <div className="relative w-24 h-24 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                    <path
                      className="text-black/10 dark:text-white/10"
                      strokeWidth="3.5"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className={`${
                        currentResult.verdict === 'LIKELY_TRUE'
                          ? 'text-[#1DB954]'
                          : currentResult.verdict === 'LIKELY_FALSE'
                          ? 'text-[#FF4D5A]'
                          : 'text-[#F5B942]'
                      } transition-all duration-1000 ease-out`}
                      strokeDasharray={`${animatedConfidence}, 100`}
                      strokeWidth="3.5"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>

                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-xl font-black text-[#111827] dark:text-white leading-none">
                      {animatedConfidence.toFixed(0)}%
                    </span>
                    <span className="text-[9px] font-bold text-[#475569] dark:text-[#A7A7A7] mt-0.5">
                      Confidence
                    </span>
                  </div>
                </div>

                <span className="text-[11px] font-bold text-[#1DB954] mt-2">
                  {currentResult.confidence_level || 'High Confidence'}
                </span>
              </div>
            </div>

            {/* Publisher Evidence Consensus Heatmap Spectrum Bar */}
            <div className="p-4 bg-black/5 dark:bg-white/5 rounded-2xl border border-black/10 dark:border-white/10 space-y-2">
              <div className="flex items-center justify-between text-xs font-bold text-[#111827] dark:text-white">
                <span className="flex items-center gap-1.5">
                  <BarChart3 className="w-4 h-4 text-[#00C2FF]" />
                  <span>Publisher Evidence Consensus Spectrum</span>
                </span>
                <span className="text-[11px] text-[#475569] dark:text-[#A7A7A7]">
                  {supportingCount} Supporting / {contradictingCount} Contradicting
                </span>
              </div>

              {/* Spectrum Heatmap Bar */}
              <div className="h-3 w-full bg-black/10 dark:bg-white/10 rounded-full overflow-hidden flex">
                <div
                  style={{ width: `${supportingPct}%` }}
                  className="bg-[#1DB954] h-full transition-all duration-700"
                  title={`${supportingCount} Supporting Reports`}
                />
                <div
                  style={{ width: `${contradictingPct}%` }}
                  className="bg-[#FF4D5A] h-full transition-all duration-700"
                  title={`${contradictingCount} Contradicting Reports`}
                />
              </div>

              <div className="flex items-center justify-between text-[10px] text-[#475569] dark:text-[#A7A7A7]">
                <span className="text-[#1DB954] font-bold">● {supportingPct.toFixed(0)}% Supporting Consensus</span>
                <span className="text-[#FF4D5A] font-bold">● {contradictingPct.toFixed(0)}% Contradicting</span>
              </div>
            </div>

            {/* AI Explanation Summary Box */}
            <div className="p-5 bg-black/5 dark:bg-white/5 rounded-2xl border border-black/10 dark:border-white/10 space-y-2">
              <div className="text-xs font-bold text-[#00C2FF] flex items-center gap-1.5">
                <Sparkles className="w-4 h-4" />
                <span>AI Evidence Synthesis Summary</span>
              </div>
              <p className="text-sm text-[#111827] dark:text-white leading-relaxed">
                {currentResult.summary}
              </p>
            </div>
          </div>

          {/* EVIDENCE SOURCE CARDS (SUPPORTING & CONTRADICTING) */}
          <div className="space-y-4">
            <div className="text-lg font-bold text-[#111827] dark:text-white flex items-center gap-2">
              <Network className="w-5 h-5 text-[#1DB954]" />
              <span>Evidence Articles & Publisher Consensus</span>
            </div>

            {currentResult.supporting_evidence && currentResult.supporting_evidence.length > 0 && (
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-[#1DB954] uppercase tracking-wider flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Supporting Evidence Reports ({currentResult.supporting_evidence.length})</span>
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {currentResult.supporting_evidence.map((art, idx) => (
                    <a
                      key={idx}
                      href={art.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-4 glass-content glass-content-hover rounded-2xl space-y-2 border border-black/15 dark:border-white/20 group"
                    >
                      <div className="flex items-center justify-between text-xs text-[#475569] dark:text-[#A7A7A7]">
                        <span className="font-bold text-[#1DB954]">{art.publisher || 'Verified News'}</span>
                        <ExternalLink className="w-3.5 h-3.5 group-hover:text-[#1DB954] transition-colors" />
                      </div>
                      <h5 className="font-bold text-sm text-[#111827] dark:text-white group-hover:text-[#1DB954] transition-colors line-clamp-2">
                        {art.title || art.headline}
                      </h5>
                      <p className="text-xs text-[#475569] dark:text-[#A7A7A7] line-clamp-2">
                        {art.snippet || art.finding || art.summary}
                      </p>
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* LIVE NEWS REPORTS GRID (WHEN NO RESULT IS ACTIVE) */}
      {!loading && !currentResult && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="text-lg font-bold text-[#111827] dark:text-white flex items-center gap-2">
              <Newspaper className="w-5 h-5 text-[#00C2FF]" />
              <span>Live News Reports</span>
            </div>
            <span className="text-xs text-[#475569] dark:text-[#A7A7A7]">Click any headline to verify</span>
          </div>

          {newsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[1, 2, 3, 4].map((n) => (
                <div key={n} className="p-5 glass-content rounded-2xl h-28 animate-pulse bg-black/5 dark:bg-white/5" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {newsArticles.slice(0, 4).map((art, idx) => (
                <div
                  key={idx}
                  onClick={() => handleSelectNewsArticle(art)}
                  className="p-5 glass-on-air rounded-2xl space-y-2 border border-black/15 dark:border-white/20 group cursor-pointer"
                >
                  <div className="flex items-center justify-between text-xs text-[#475569] dark:text-[#A7A7A7]">
                    <span className="font-bold text-[#00C2FF]">{art.publisher || 'Live Feed'}</span>
                    <span className="text-[10px] bg-[#00C2FF]/10 text-[#00C2FF] px-2 py-0.5 rounded-full font-bold">
                      Click to Verify
                    </span>
                  </div>

                  <h4 className="font-bold text-sm text-[#111827] dark:text-white group-hover:text-[#00C2FF] transition-colors line-clamp-2">
                    {art.title || art.headline}
                  </h4>

                  <p className="text-xs text-[#475569] dark:text-[#A7A7A7] line-clamp-2">
                    {art.snippet || art.finding || art.summary}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
