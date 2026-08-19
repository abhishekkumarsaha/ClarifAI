import React, { useEffect, useRef, useState } from 'react';
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
  Cpu,
  Globe,
  Radio,
  TrendingUp,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  SlidersHorizontal,
  Brain,
  FileCheck2,
  XCircle,
  Info,
} from 'lucide-react';

import { useApp } from '../context/AppContext';
import { analyzeClaim, fetchLatestNews } from '../services/api';
import { EvidenceArticle } from '../types';
import {
  playGlassClickSound,
  playSuccessChime,
} from '../utils/audio';

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

  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [animatedConfidence, setAnimatedConfidence] = useState(0);

  const [newsArticles, setNewsArticles] = useState<EvidenceArticle[]>([]);
  const [newsLoading, setNewsLoading] = useState(true);

  const headlineRef = useRef<HTMLHeadingElement>(null);
  const [headlineStyle, setHeadlineStyle] =
    useState<React.CSSProperties>({});

  const isUrlDetected =
    claimInput.trim().startsWith('http://') ||
    claimInput.trim().startsWith('https://');

  const radarClaims = [
    'India announces a new technology initiative',
    'Federal Reserve benchmark rate decision update',
    'James Webb space telescope discovery',
    'Global renewable energy milestone',
  ];

  const samplePresets = [
    {
      label: 'Health',
      query:
        'WHO updates global vaccination guidelines for 2026',
    },
    {
      label: 'Tech',
      query:
        'Quantum computing milestone achieved by researchers',
    },
    {
      label: 'Climate',
      query:
        'Global solar energy adoption breaks annual record',
    },
  ];

  const handleMouseMoveHeadline = (
    e: React.MouseEvent<HTMLHeadingElement>,
  ) => {
    if (!headlineRef.current) return;

    const rect =
      headlineRef.current.getBoundingClientRect();

    const x =
      e.clientX -
      rect.left -
      rect.width / 2;

    const y =
      e.clientY -
      rect.top -
      rect.height / 2;

    setHeadlineStyle({
      transform: `
        perspective(600px)
        rotateX(${(-y / rect.height) * 10}deg)
        rotateY(${(x / rect.width) * 10}deg)
        translateY(-3px)
      `,
    });
  };

  const handleMouseLeaveHeadline = () => {
    setHeadlineStyle({
      transform:
        'perspective(600px) rotateX(0deg) rotateY(0deg)',
    });
  };

  useEffect(() => {
    fetchLatestNews()
      .then((articles) => {
        setNewsArticles(articles);
      })
      .finally(() => {
        setNewsLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!currentResult) {
      setAnimatedConfidence(0);
      return;
    }

    playSuccessChime();

    const target = Number(
      currentResult.confidence || 0,
    );

    setAnimatedConfidence(0);

    const duration = 900;
    const steps = 30;
    const stepTime = duration / steps;

    let step = 0;

    const timer = window.setInterval(() => {
      step++;

      setAnimatedConfidence(
        target * Math.min(step / steps, 1),
      );

      if (step >= steps) {
        window.clearInterval(timer);
      }
    }, stepTime);

    return () =>
      window.clearInterval(timer);
  }, [currentResult]);

  const toggleVoiceInput = () => {
    playGlassClickSound();

    const SpeechRecognitionClass =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognitionClass) {
      showToast('Voice input is unavailable.');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const recognition =
        new SpeechRecognitionClass();

      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
        showToast('Listening...');
      };

      recognition.onresult = (event: any) => {
        const transcript =
          event.results?.[0]?.[0]?.transcript || '';

        setClaimInput(transcript);
        setIsListening(false);
        showToast('Claim captured.');
      };

      recognition.onerror = () => {
        setIsListening(false);
        showToast('Voice input failed.');
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } catch {
      setIsListening(false);
      showToast('Voice input failed.');
    }
  };

  const handleVerify = async (
    claimToVerify?: string,
  ) => {
    const query = (
      claimToVerify || claimInput
    ).trim();

    if (!query) {
      setErrorMsg(
        'Please enter a news claim or article URL.',
      );
      return;
    }

    playGlassClickSound();

    setErrorMsg(null);
    setCurrentResult(null);
    setLoading(true);

    setLoadingStage(
      'Searching live news and collecting evidence...',
    );

    const stage1 = window.setTimeout(() => {
      setLoadingStage(
        'Comparing independent sources...',
      );
    }, 1000);

    const stage2 = window.setTimeout(() => {
      setLoadingStage(
        'Running ML and AI verification...',
      );
    }, 2200);

    const stage3 = window.setTimeout(() => {
      setLoadingStage(
        'Preparing evidence-backed verdict...',
      );
    }, 3500);

    try {
      const result = await analyzeClaim(
        query,
        maxArticlesLimit,
      );

      setCurrentResult(result);
      addHistoryItem(result);
    } catch (error: any) {
      setErrorMsg(
        error?.message ||
        'Verification failed. Please try again.',
      );
    } finally {
      window.clearTimeout(stage1);
      window.clearTimeout(stage2);
      window.clearTimeout(stage3);
      setLoading(false);
    }
  };

  const handleSelectNewsArticle = (
    article: EvidenceArticle,
  ) => {
    const title =
      article.title ||
      article.headline ||
      '';

    if (!title) return;

    setClaimInput(title);
    handleVerify(title);
  };

  const handleCopySummary = async () => {
    if (!currentResult) return;

    playGlassClickSound();

    const verdict =
      currentResult.verdict || 'UNVERIFIED';

    const text = [
      'ClarifAI Verification',
      '',
      `Claim: ${currentResult.claim}`,
      `Verdict: ${verdict}`,
      `Confidence: ${Number(
        currentResult.confidence || 0,
      ).toFixed(1)}%`,
      '',
      currentResult.summary || '',
    ].join('\n');

    try {
      await navigator.clipboard.writeText(text);
      showToast('Verification receipt copied.');
    } catch {
      showToast('Unable to copy receipt.');
    }
  };

  const isCurrentSaved = currentResult
    ? savedItems.has(currentResult.claim)
    : false;

  const verdict =
    currentResult?.verdict || 'UNVERIFIED';

  const confidence =
    Number(currentResult?.confidence || 0);

  const supporting =
    currentResult?.supporting_evidence || [];

  const contradicting =
    currentResult?.contradicting_evidence || [];

  const mlResults =
    currentResult?.ml_results || [];

  const limitations =
    currentResult?.limitations || [];

  const getVerdictIcon = () => {
    if (verdict === 'LIKELY_TRUE') {
      return (
        <CheckCircle2 className="w-4 h-4" />
      );
    }

    if (verdict === 'LIKELY_FALSE') {
      return (
        <AlertCircle className="w-4 h-4" />
      );
    }

    return (
      <HelpCircle className="w-4 h-4" />
    );
  };

  const getVerdictClass = () => {
    if (verdict === 'LIKELY_TRUE') {
      return 'bg-[#1DB954]/15 text-[#1DB954] border-[#1DB954]/40';
    }

    if (verdict === 'LIKELY_FALSE') {
      return 'bg-[#FF4D5A]/15 text-[#FF4D5A] border-[#FF4D5A]/40';
    }

    return 'bg-[#F5B942]/15 text-[#F5B942] border-[#F5B942]/40';
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <div className="text-center max-w-2xl mx-auto space-y-2">

        <h1
          ref={headlineRef}
          onMouseMove={handleMouseMoveHeadline}
          onMouseLeave={handleMouseLeaveHeadline}
          style={headlineStyle}
          className="
            text-4xl md:text-5xl
            font-black tracking-tight
            text-[#111827] dark:text-white
            cursor-pointer select-none
            headline-neon-wave
            inline-block
          "
        >
          Is this NEWS true?
        </h1>

        <p className="text-sm font-medium text-[#475569] dark:text-[#A7A7A7]">
          Verify claims against live sources,
          independent evidence, ML signals and AI analysis.
        </p>

      </div>

      {/* ======================================================
          SEARCH
      ====================================================== */}

      <div className="space-y-3 max-w-3xl mx-auto">

        <div className="
          glass-on-air
          rounded-3xl
          p-2.5
          shadow-xl
          border border-black/15 dark:border-white/20
        ">

          <div className="flex items-center gap-3">

            <div className="pl-3 text-[#00C2FF]">
              <Search className="w-5 h-5" />
            </div>

            <input
              id="main-claim-search-input"
              type="text"
              value={claimInput}
              onChange={(e) =>
                setClaimInput(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleVerify();
                }
              }}
              placeholder="Enter news claim or paste article URL..."
              className="
                flex-1 bg-transparent border-none
                text-sm md:text-base font-medium
                text-[#111827] dark:text-white
                placeholder-[#64748B]
                focus:outline-none
              "
            />

            {isListening && (
              <span className="
                px-2 py-0.5 rounded-full
                bg-[#FF4D5A]/20
                border border-[#FF4D5A]/50
                text-[10px] font-bold
                text-[#FF4D5A]
                flex items-center gap-1
              ">
                <span className="
                  w-1.5 h-1.5 rounded-full
                  bg-[#FF4D5A] animate-ping
                " />
                REC
              </span>
            )}

            <button
              onClick={toggleVoiceInput}
              className={`
                p-2.5 rounded-full border
                transition-all cursor-pointer
                flex-shrink-0
                ${isListening
                  ? 'bg-[#FF4D5A]/20 border-[#FF4D5A] text-[#FF4D5A]'
                  : 'glass-interactive text-[#475569] dark:text-[#A7A7A7]'
                }
              `}
            >
              {isListening ? (
                <MicOff className="w-4 h-4" />
              ) : (
                <Mic className="w-4 h-4" />
              )}
            </button>

            <button
              onClick={() => handleVerify()}
              disabled={loading}
              className="
                flex items-center gap-2
                px-5 py-2.5
                bg-[#1DB954]
                text-black
                font-bold text-xs md:text-sm
                rounded-full
                shadow-md
                hover:bg-[#1ed760]
                active:scale-95
                transition-all
                cursor-pointer
                disabled:opacity-50
              "
            >
              <span>
                {loading
                  ? 'Checking...'
                  : 'Check Claim'}
              </span>

              <ArrowRight className="w-4 h-4" />
            </button>

          </div>
        </div>

        {/* Controls */}

        <div className="
          flex items-center
          justify-between
          gap-2 px-2 flex-wrap
          text-xs text-[#475569]
          dark:text-[#A7A7A7]
        ">

          <div className="flex items-center gap-2">

            {isUrlDetected && (
              <span className="
                inline-flex items-center gap-1
                px-2.5 py-0.5 rounded-full
                bg-[#00C2FF]/15
                border border-[#00C2FF]/40
                text-[11px] font-bold
                text-[#00C2FF]
              ">
                <Globe className="w-3 h-3" />
                Link Detected
              </span>
            )}

            <div className="
              relative inline-flex
              items-center gap-1
              px-2.5 py-1
              glass-interactive
              rounded-full
              border border-black/15
              dark:border-white/20
              text-[11px] font-bold
            ">

              <SlidersHorizontal
                className="
                  w-3 h-3
                  text-[#1DB954]
                "
              />

              <span>Evidence:</span>

              <select
                value={maxArticlesLimit}
                onChange={(e) => {
                  playGlassClickSound();

                  setMaxArticlesLimit(
                    Number(e.target.value),
                  );
                }}
                className="
                  bg-transparent
                  text-[#111827]
                  dark:text-white
                  font-bold
                  focus:outline-none
                  cursor-pointer
                  appearance-none
                  pr-4
                "
              >
                <option value={3}>
                  3
                </option>
                <option value={5}>
                  5
                </option>
                <option value={8}>
                  8
                </option>
              </select>

              <ChevronDown
                className="
                  w-3 h-3
                  absolute right-2
                  pointer-events-none
                "
              />

            </div>

          </div>

          <div className="
            flex items-center gap-1.5
          ">
            <span className="text-[11px] opacity-70">
              Try sample:
            </span>

            {samplePresets.map(
              (preset) => (
                <button
                  key={preset.label}
                  onClick={() => {
                    setClaimInput(
                      preset.query,
                    );
                    playGlassClickSound();
                  }}
                  className="
                    px-2.5 py-0.5
                    rounded-full
                    glass-interactive
                    border
                    border-black/10
                    dark:border-white/10
                    text-[10px]
                    font-semibold
                    cursor-pointer
                    hover:text-[#00C2FF]
                  "
                >
                  {preset.label}
                </button>
              ),
            )}
          </div>

        </div>

        {/* Radar */}

        <div className="
          flex items-center gap-2
          px-3 py-1.5
          glass-content
          rounded-2xl
          border
          border-black/10
          dark:border-white/10
          text-xs
          overflow-x-auto
        ">

          <span className="
            flex items-center gap-1
            font-bold
            text-[#FF4D5A]
            flex-shrink-0
            text-[11px]
          ">
            <Radio className="w-3 h-3 animate-pulse" />
            LIVE RADAR
          </span>

          <div className="
            flex items-center gap-3
            overflow-x-auto
          ">

            {radarClaims.map(
              (item, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setClaimInput(item);
                    playGlassClickSound();
                  }}
                  className="
                    whitespace-nowrap
                    hover:text-[#00C2FF]
                    transition-colors
                    font-medium
                    cursor-pointer
                    text-[11px]
                    flex items-center gap-1
                  "
                >
                  <TrendingUp
                    className="
                      w-3 h-3
                      text-[#00C2FF]
                    "
                  />

                  {item}
                </button>
              ),
            )}

          </div>
        </div>

        {/* Error */}

        {errorMsg && (
          <div className="
            px-4 py-2
            bg-[#FF4D5A]/15
            border border-[#FF4D5A]/40
            rounded-2xl
            text-xs font-bold
            text-[#FF4D5A]
            flex items-center
            justify-between
          ">

            <div className="
              flex items-center gap-2
            ">
              <ShieldAlert className="w-4 h-4" />
              {errorMsg}
            </div>

            <button
              onClick={() =>
                setErrorMsg(null)
              }
              className="uppercase text-[10px]"
            >
              Dismiss
            </button>

          </div>
        )}

      </div>

      {/* ======================================================
          LOADING
      ====================================================== */}

      {loading && (
        <div className="
          max-w-md mx-auto
          p-6
          glass-on-air
          rounded-3xl
          text-center
          space-y-4
          shadow-xl
          border border-[#00C2FF]/30
        ">

          <div className="
            w-12 h-12
            rounded-full
            bg-[#00C2FF]/10
            border border-[#00C2FF]/40
            flex items-center justify-center
            text-[#00C2FF]
            mx-auto
            animate-spin
          ">
            <Cpu className="w-6 h-6" />
          </div>

          <div>
            <h3 className="
              text-sm font-bold
              text-[#111827]
              dark:text-white
            ">
              Verifying News Claim
            </h3>

            <p className="
              text-xs
              text-[#00C2FF]
              font-semibold
              mt-1
            ">
              {loadingStage}
            </p>
          </div>

          <div className="
            w-full h-1
            bg-black/10
            dark:bg-white/10
            rounded-full
            overflow-hidden
          ">
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: '100%' }}
              transition={{
                repeat: Infinity,
                duration: 1.4,
              }}
              className="
                w-1/2 h-full
                bg-[#1DB954]
                rounded-full
              "
            />
          </div>

        </div>
      )}

      {/* ======================================================
          RESULT
      ====================================================== */}

      {!loading && currentResult && (
        <div className="
          max-w-5xl mx-auto
          space-y-6
          animate-in
          fade-in
          duration-300
        ">

          {/* Toolbar */}

          <div className="
            flex flex-wrap
            items-center
            justify-between
            gap-3
            p-3
            glass-content
            rounded-2xl
            border border-black/15
            dark:border-white/20
          ">

            <div className="
              flex items-center gap-2
            ">

              <button
                onClick={() => {
                  playGlassClickSound();
                  resetVerification();
                }}
                className="
                  flex items-center gap-1.5
                  px-3 py-1.5
                  glass-interactive
                  rounded-full
                  text-xs font-bold
                "
              >
                <RotateCcw
                  className="
                    w-3.5 h-3.5
                    text-[#00C2FF]
                  "
                />
                Check Another
              </button>

              <button
                onClick={() =>
                  toggleSaveItem(
                    currentResult.claim,
                  )
                }
                className="
                  flex items-center gap-1.5
                  px-3 py-1.5
                  glass-interactive
                  rounded-full
                  text-xs font-bold
                "
              >
                {isCurrentSaved ? (
                  <>
                    <BookmarkCheck
                      className="
                        w-3.5 h-3.5
                        text-[#1DB954]
                      "
                    />
                    <span className="text-[#1DB954]">
                      Saved
                    </span>
                  </>
                ) : (
                  <>
                    <Bookmark
                      className="w-3.5 h-3.5"
                    />
                    Save
                  </>
                )}
              </button>

            </div>

            <div className="
              flex items-center gap-2
            ">

              <button
                onClick={handleCopySummary}
                className="
                  flex items-center gap-1.5
                  px-3 py-1.5
                  glass-interactive
                  rounded-full
                  text-xs font-bold
                  text-[#00C2FF]
                "
              >
                <Share2 className="w-3.5 h-3.5" />
                Share
              </button>

              <button
                onClick={() => {
                  playGlassClickSound();
                  window.print();
                }}
                className="
                  flex items-center gap-1.5
                  px-3 py-1.5
                  glass-interactive
                  rounded-full
                  text-xs font-bold
                  text-[#1DB954]
                "
              >
                <Printer className="w-3.5 h-3.5" />
                Print
              </button>

            </div>

          </div>

          {/* Main verdict */}

          <div className="
            glass-on-air
            rounded-3xl
            p-6 md:p-8
            space-y-6
            border border-black/15
            dark:border-white/20
            shadow-xl
          ">

            <div className="
              flex flex-col
              md:flex-row
              items-center
              justify-between
              gap-8
            ">

              <div className="
                flex-1
                space-y-4
                text-center
                md:text-left
              ">

                <span className={`
                  inline-flex
                  items-center gap-2
                  px-4 py-1.5
                  rounded-full
                  border
                  text-sm
                  font-black
                  tracking-wider
                  ${getVerdictClass()}
                `}>
                  {getVerdictIcon()}
                  {verdict.replace(
                    /_/g,
                    ' ',
                  )}
                </span>

                <h2 className="
                  text-xl md:text-2xl
                  font-bold
                  text-[#111827]
                  dark:text-white
                  leading-snug
                ">
                  "{currentResult.claim}"
                </h2>

                {currentResult.confidence_level && (
                  <p className="
                    text-xs
                    font-semibold
                    text-[#64748B]
                  ">
                    Confidence level:{' '}
                    {currentResult.confidence_level}
                  </p>
                )}

              </div>

              {/* Confidence */}

              <div className="
                flex flex-col
                items-center
                justify-center
                p-4
                bg-black/5
                dark:bg-white/5
                rounded-2xl
                border
                border-black/10
                dark:border-white/10
                min-w-[150px]
              ">

                <div className="
                  relative
                  w-24 h-24
                ">

                  <svg
                    className="
                      w-full h-full
                      -rotate-90
                    "
                    viewBox="0 0 36 36"
                  >

                    <path
                      className="
                        text-black/10
                        dark:text-white/10
                      "
                      strokeWidth="3.5"
                      stroke="currentColor"
                      fill="none"
                      d="
                        M18 2.0845
                        a15.9155 15.9155 0 0 1
                        0 31.831
                        a15.9155 15.9155 0 0 1
                        0 -31.831
                      "
                    />

                    <path
                      className={
                        verdict === 'LIKELY_TRUE'
                          ? 'text-[#1DB954]'
                          : verdict === 'LIKELY_FALSE'
                            ? 'text-[#FF4D5A]'
                            : 'text-[#F5B942]'
                      }
                      strokeDasharray={`
                        ${animatedConfidence},100
                      `}
                      strokeWidth="3.5"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="
                        M18 2.0845
                        a15.9155 15.9155 0 0 1
                        0 31.831
                        a15.9155 15.9155 0 0 1
                        0 -31.831
                      "
                    />

                  </svg>

                  <div className="
                    absolute inset-0
                    flex flex-col
                    items-center
                    justify-center
                  ">
                    <span className="
                      text-xl
                      font-black
                      text-[#111827]
                      dark:text-white
                    ">
                      {animatedConfidence.toFixed(0)}%
                    </span>
                  </div>

                </div>

                <span className="
                  text-[11px]
                  font-bold
                  text-[#00C2FF]
                  mt-2
                ">
                  Confidence Score
                </span>

              </div>

            </div>

            {/* Summary */}

            <div className="
              p-5
              bg-black/5
              dark:bg-white/5
              rounded-2xl
              border
              border-black/10
              dark:border-white/10
              space-y-2
            ">

              <div className="
                text-xs font-bold
                text-[#00C2FF]
                flex items-center gap-1.5
              ">
                <Sparkles className="w-4 h-4" />
                Evidence Summary
              </div>

              <p className="
                text-sm
                text-[#111827]
                dark:text-white
                leading-relaxed
              ">
                {currentResult.summary ||
                  'No summary was generated.'}
              </p>

            </div>

          </div>

          {/* ==================================================
              EVIDENCE OVERVIEW
          ================================================== */}

          <div className="
            grid
            grid-cols-1
            md:grid-cols-3
            gap-4
          ">

            <div className="
              glass-content
              rounded-2xl
              p-4
              border
              border-black/10
              dark:border-white/10
            ">
              <div className="
                flex items-center
                justify-between
              ">
                <span className="
                  text-xs font-bold
                  text-[#64748B]
                ">
                  Sources Found
                </span>

                <Newspaper
                  className="
                    w-4 h-4
                    text-[#00C2FF]
                  "
                />
              </div>

              <p className="
                text-2xl
                font-black
                mt-2
                text-[#111827]
                dark:text-white
              ">
                {currentResult.articles_found ??
                  supporting.length +
                  contradicting.length}
              </p>
            </div>

            <div className="
              glass-content
              rounded-2xl
              p-4
              border
              border-black/10
              dark:border-white/10
            ">
              <div className="
                flex items-center
                justify-between
              ">
                <span className="
                  text-xs font-bold
                  text-[#64748B]
                ">
                  Supporting
                </span>

                <FileCheck2
                  className="
                    w-4 h-4
                    text-[#1DB954]
                  "
                />
              </div>

              <p className="
                text-2xl
                font-black
                mt-2
                text-[#1DB954]
              ">
                {supporting.length}
              </p>
            </div>

            <div className="
              glass-content
              rounded-2xl
              p-4
              border
              border-black/10
              dark:border-white/10
            ">
              <div className="
                flex items-center
                justify-between
              ">
                <span className="
                  text-xs font-bold
                  text-[#64748B]
                ">
                  Contradicting
                </span>

                <XCircle
                  className="
                    w-4 h-4
                    text-[#FF4D5A]
                  "
                />
              </div>

              <p className="
                text-2xl
                font-black
                mt-2
                text-[#FF4D5A]
              ">
                {contradicting.length}
              </p>
            </div>

          </div>

          {/* ==================================================
              AI + SOURCE ASSESSMENT
          ================================================== */}

          <div className="
            grid
            grid-cols-1
            md:grid-cols-2
            gap-4
          ">

            <div className="
              glass-content
              rounded-2xl
              p-5
              border
              border-[#00C2FF]/20
              space-y-3
            ">

              <div className="
                flex items-center gap-2
                text-[#00C2FF]
                font-bold text-sm
              ">
                <Brain className="w-4 h-4" />
                AI Interpretation
              </div>

              <p className="
                text-sm
                leading-relaxed
                text-[#111827]
                dark:text-white
              ">
                {currentResult.ml_interpretation ||
                  'AI interpretation unavailable.'}
              </p>

            </div>

            <div className="
              glass-content
              rounded-2xl
              p-5
              border
              border-[#1DB954]/20
              space-y-3
            ">

              <div className="
                flex items-center gap-2
                text-[#1DB954]
                font-bold text-sm
              ">
                <Globe className="w-4 h-4" />
                Source Assessment
              </div>

              <p className="
                text-sm
                leading-relaxed
                text-[#111827]
                dark:text-white
              ">
                {currentResult.source_assessment ||
                  'No source assessment available.'}
              </p>

            </div>

          </div>

          {/* ==================================================
              WHY
          ================================================== */}

          {currentResult.why &&
            currentResult.why.length > 0 && (
              <div className="
                glass-content
                rounded-2xl
                p-5
                border
                border-black/10
                dark:border-white/10
              ">

                <div className="
                  flex items-center gap-2
                  text-sm font-bold
                  text-[#111827]
                  dark:text-white
                  mb-3
                ">
                  <Info className="
                    w-4 h-4
                    text-[#00C2FF]
                  " />
                  Why ClarifAI reached this result
                </div>

                <ul className="
                  space-y-2
                  text-sm
                  text-[#475569]
                  dark:text-[#A7A7A7]
                ">
                  {currentResult.why.map(
                    (reason, index) => (
                      <li
                        key={index}
                        className="
                          flex gap-2
                        "
                      >
                        <span className="
                          text-[#00C2FF]
                          font-bold
                        ">
                          •
                        </span>
                        <span>
                          {reason}
                        </span>
                      </li>
                    ),
                  )}
                </ul>

              </div>
            )}

          {/* ==================================================
              SUPPORTING EVIDENCE
          ================================================== */}

          {supporting.length > 0 && (
            <EvidenceSection
              title="Supporting Evidence"
              icon={
                <CheckCircle2
                  className="
                    w-4 h-4
                    text-[#1DB954]
                  "
                />
              }
              articles={supporting}
              accent="green"
            />
          )}

          {/* ==================================================
              CONTRADICTING EVIDENCE
          ================================================== */}

          {contradicting.length > 0 && (
            <EvidenceSection
              title="Contradicting Evidence"
              icon={
                <AlertCircle
                  className="
                    w-4 h-4
                    text-[#FF4D5A]
                  "
                />
              }
              articles={contradicting}
              accent="red"
            />
          )}

          {/* ==================================================
              ML SIGNALS
          ================================================== */}

          {mlResults.length > 0 && (
            <div className="
              glass-content
              rounded-2xl
              p-5
              border
              border-black/10
              dark:border-white/10
              space-y-4
            ">

              <div className="
                flex items-center gap-2
                text-sm font-bold
                text-[#111827]
                dark:text-white
              ">
                <Brain className="
                  w-4 h-4
                  text-[#00C2FF]
                " />
                ML Signals
              </div>

              <div className="
                grid
                grid-cols-1
                md:grid-cols-2
                gap-3
              ">

                {mlResults
                  .flatMap(
                    (result) =>
                      result.signals || [],
                  )
                  .slice(0, 12)
                  .map(
                    (signal, index) => (
                      <div
                        key={`${signal.feature}-${index}`}
                        className="
                          flex
                          items-center
                          justify-between
                          px-3 py-2
                          rounded-xl
                          bg-black/5
                          dark:bg-white/5
                        "
                      >
                        <span className="
                          text-xs
                          font-semibold
                          text-[#475569]
                          dark:text-[#A7A7A7]
                        ">
                          {signal.feature ||
                            'Signal'}
                        </span>

                        <span className={`
                          text-xs
                          font-black
                          ${Number(
                          signal.contribution ||
                          0,
                        ) >= 0
                            ? 'text-[#1DB954]'
                            : 'text-[#FF4D5A]'
                          }
                        `}>
                          {Number(
                            signal.contribution || 0,
                          ).toFixed(4)}
                        </span>
                      </div>
                    ),
                  )}

              </div>

            </div>
          )}

          {/* ==================================================
              LIMITATIONS
          ================================================== */}

          {limitations.length > 0 && (
            <div className="
              p-4
              rounded-2xl
              bg-[#F5B942]/10
              border border-[#F5B942]/30
            ">

              <div className="
                flex items-center gap-2
                text-sm font-bold
                text-[#F5B942]
                mb-2
              ">
                <ShieldAlert className="w-4 h-4" />
                Limitations
              </div>

              <ul className="
                space-y-1
                text-xs
                text-[#475569]
                dark:text-[#A7A7A7]
              ">
                {limitations.map(
                  (item, index) => (
                    <li key={index}>
                      • {item}
                    </li>
                  ),
                )}
              </ul>

            </div>
          )}

        </div>
      )}

      {/* ======================================================
          TRENDING
      ====================================================== */}

      {!loading && !currentResult && (
        <div className="
          max-w-5xl mx-auto
          space-y-4
        ">

          <div className="
            flex items-center
            justify-between
          ">

            <div className="
              text-sm font-bold
              text-[#111827]
              dark:text-white
              flex items-center gap-2
            ">
              <Newspaper
                className="
                  w-4 h-4
                  text-[#00C2FF]
                "
              />
              Verified Trending News Reports
            </div>

            <span className="
              text-[11px]
              font-bold
              text-[#1DB954]
              bg-[#1DB954]/10
              px-2.5 py-0.5
              rounded-full
              border
              border-[#1DB954]/30
            ">
              Live Feed
            </span>

          </div>

          {newsLoading ? (
            <div className="
              grid
              grid-cols-1
              md:grid-cols-2
              gap-4
            ">
              {[1, 2, 3, 4].map(
                (item) => (
                  <div
                    key={item}
                    className="
                      p-5
                      glass-content
                      rounded-2xl
                      h-24
                      animate-pulse
                    "
                  />
                ),
              )}
            </div>
          ) : (

            <motion.div
              initial="hidden"
              animate="show"
              variants={{
                hidden: {
                  opacity: 0,
                },
                show: {
                  opacity: 1,
                  transition: {
                    staggerChildren: 0.1,
                  },
                },
              }}
              className="
                grid
                grid-cols-1
                md:grid-cols-2
                gap-4
              "
            >

              {newsArticles
                .slice(0, 4)
                .map(
                  (article, index) => (
                    <motion.button
                      key={index}
                      variants={{
                        hidden: {
                          opacity: 0,
                          y: 12,
                        },
                        show: {
                          opacity: 1,
                          y: 0,
                        },
                      }}
                      onClick={() =>
                        handleSelectNewsArticle(
                          article,
                        )
                      }
                      className="
                        text-left
                        p-4
                        glass-on-air
                        rounded-2xl
                        space-y-2
                        border
                        border-black/15
                        dark:border-white/20
                        group
                        cursor-pointer
                      "
                    >

                      <div className="
                        flex
                        items-center
                        justify-between
                        text-xs
                      ">

                        <span className="
                          font-bold
                          text-[#00C2FF]
                        ">
                          {article.publisher ||
                            'Verified Feed'}
                        </span>

                        <span className="
                          text-[10px]
                          bg-[#00C2FF]/10
                          text-[#00C2FF]
                          px-2 py-0.5
                          rounded-full
                          font-bold
                        ">
                          Check
                        </span>

                      </div>

                      <h4 className="
                        font-bold
                        text-sm
                        text-[#111827]
                        dark:text-white
                        group-hover:text-[#00C2FF]
                        transition-colors
                      ">
                        {article.title ||
                          article.headline ||
                          'Untitled report'}
                      </h4>

                      {article.snippet && (
                        <p className="
                          text-xs
                          text-[#64748B]
                          dark:text-[#A7A7A7]
                          line-clamp-2
                        ">
                          {article.snippet}
                        </p>
                      )}

                    </motion.button>
                  ),
                )}

            </motion.div>
          )}

        </div>
      )}

    </div>
  );
};

/* ============================================================
   EVIDENCE SECTION
============================================================ */

interface EvidenceSectionProps {
  title: string;
  icon: React.ReactNode;
  articles: EvidenceArticle[];
  accent: 'green' | 'red';
}

const EvidenceSection: React.FC<
  EvidenceSectionProps
> = ({
  title,
  icon,
  articles,
  accent,
}) => {
    const border =
      accent === 'green'
        ? 'border-[#1DB954]/20'
        : 'border-[#FF4D5A]/20';

    return (
      <div className="
      space-y-3
    ">

        <div className="
        flex items-center gap-2
        text-sm font-bold
        text-[#111827]
        dark:text-white
      ">
          {icon}
          {title}
          <span className="
          text-[10px]
          px-2 py-0.5
          rounded-full
          bg-black/5
          dark:bg-white/5
        ">
            {articles.length}
          </span>
        </div>

        <div className="
        grid
        grid-cols-1
        md:grid-cols-2
        gap-4
      ">

          {articles.map(
            (article, index) => (
              <a
                key={`${article.url}-${index}`}
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`
                glass-content
                rounded-2xl
                p-4
                border
                ${border}
                group
                hover:translate-y-[-2px]
                transition-all
              `}
              >

                <div className="
                flex
                items-center
                justify-between
                gap-3
                text-xs
              ">

                  <span className="
                  font-bold
                  text-[#00C2FF]
                ">
                    {article.publisher ||
                      article.source_domain ||
                      'Verified Source'}
                  </span>

                  <ExternalLink
                    className="
                    w-3.5 h-3.5
                    opacity-60
                    group-hover:opacity-100
                  "
                  />

                </div>

                <h4 className="
                mt-2
                font-bold
                text-sm
                text-[#111827]
                dark:text-white
                group-hover:text-[#00C2FF]
                transition-colors
                line-clamp-3
              ">
                  {article.title ||
                    article.headline ||
                    'Untitled article'}
                </h4>

                {article.publication_date && (
                  <p className="
                  mt-2
                  text-[10px]
                  text-[#64748B]
                ">
                    {article.publication_date}
                  </p>
                )}

                {(article.snippet ||
                  article.summary ||
                  article.finding) && (
                    <p className="
                  mt-2
                  text-xs
                  text-[#64748B]
                  dark:text-[#A7A7A7]
                  line-clamp-3
                ">
                      {article.finding ||
                        article.summary ||
                        article.snippet}
                    </p>
                  )}

              </a>
            ),
          )}

        </div>

      </div>
    );
  };