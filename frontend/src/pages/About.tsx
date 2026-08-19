import React from 'react';
import {
  ShieldCheck,
  BrainCircuit,
  Newspaper,
  Search,
  Database,
  Cpu,
  Globe,
  CheckCircle2,
  ExternalLink,
  Github,
  Activity,
} from 'lucide-react';

import { useApp } from '../context/AppContext';
import { playGlassClickSound } from '../utils/audio';

export const AboutPage: React.FC = () => {
  const { setActiveNav, health } = useApp();

  const backendOnline = health.status === 'healthy';

  return (
    <div className="space-y-6 animate-in fade-in duration-200">

      {/* HEADER */}

      <div className="text-center max-w-2xl mx-auto">

        <div className="w-16 h-16 mx-auto rounded-3xl bg-[#00C2FF]/10 border border-[#00C2FF]/30 flex items-center justify-center shadow-lg">
          <ShieldCheck className="w-8 h-8 text-[#00C2FF]" />
        </div>

        <div className="mt-4 text-[10px] font-black uppercase tracking-[0.2em] text-[#00C2FF]">
          ClarifAI Intelligence System
        </div>

        <h1 className="mt-2 text-4xl font-black tracking-tight text-[#111827] dark:text-white">
          About ClarifAI
        </h1>

        <p className="mt-3 text-sm leading-relaxed text-[#475569] dark:text-[#A7A7A7]">
          An evidence-driven news verification platform designed
          to help users evaluate claims using live news evidence,
          article extraction, ML analysis, and AI-generated
          explanations.
        </p>

      </div>

      {/* STATUS */}

      <div className="max-w-3xl mx-auto p-4 glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-xl">

        <div className="flex items-center justify-between gap-4">

          <div className="flex items-center gap-3">

            <div className="w-10 h-10 rounded-2xl bg-[#1DB954]/10 border border-[#1DB954]/30 flex items-center justify-center">
              <Activity className="w-5 h-5 text-[#1DB954]" />
            </div>

            <div>
              <div className="text-sm font-bold text-[#111827] dark:text-white">
                System Status
              </div>

              <div className="text-[10px] text-[#64748B] dark:text-[#777777]">
                ClarifAI verification infrastructure
              </div>
            </div>

          </div>

          <div
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-[10px] font-black ${backendOnline
                ? 'text-[#1DB954] bg-[#1DB954]/10 border-[#1DB954]/30'
                : 'text-[#F5B942] bg-[#F5B942]/10 border-[#F5B942]/30'
              }`}
          >
            <span
              className={`w-1.5 h-1.5 rounded-full ${backendOnline
                  ? 'bg-[#1DB954] animate-pulse'
                  : 'bg-[#F5B942]'
                }`}
            />

            {backendOnline ? 'ONLINE' : 'DEGRADED'}
          </div>

        </div>

      </div>

      {/* ARCHITECTURE */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        <div className="p-5 glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-xl">

          <div className="w-10 h-10 rounded-2xl bg-[#00C2FF]/10 border border-[#00C2FF]/25 flex items-center justify-center">
            <Search className="w-5 h-5 text-[#00C2FF]" />
          </div>

          <h2 className="mt-4 text-base font-bold text-[#111827] dark:text-white">
            Claim Verification
          </h2>

          <p className="mt-2 text-xs leading-relaxed text-[#64748B] dark:text-[#888888]">
            Natural-language claims and direct article URLs are
            processed through the ClarifAI verification pipeline.
          </p>

        </div>

        <div className="p-5 glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-xl">

          <div className="w-10 h-10 rounded-2xl bg-[#1DB954]/10 border border-[#1DB954]/25 flex items-center justify-center">
            <Newspaper className="w-5 h-5 text-[#1DB954]" />
          </div>

          <h2 className="mt-4 text-base font-bold text-[#111827] dark:text-white">
            Live News Evidence
          </h2>

          <p className="mt-2 text-xs leading-relaxed text-[#64748B] dark:text-[#888888]">
            Current news sources are discovered and ranked before
            article evidence is extracted and analyzed.
          </p>

        </div>

        <div className="p-5 glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-xl">

          <div className="w-10 h-10 rounded-2xl bg-[#F5B942]/10 border border-[#F5B942]/25 flex items-center justify-center">
            <BrainCircuit className="w-5 h-5 text-[#F5B942]" />
          </div>

          <h2 className="mt-4 text-base font-bold text-[#111827] dark:text-white">
            ML + AI Analysis
          </h2>

          <p className="mt-2 text-xs leading-relaxed text-[#64748B] dark:text-[#888888]">
            Extracted evidence can be evaluated using the ML
            layer and synthesized into an evidence-grounded
            explanation.
          </p>

        </div>

        <div className="p-5 glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-xl">

          <div className="w-10 h-10 rounded-2xl bg-[#FF4D5A]/10 border border-[#FF4D5A]/25 flex items-center justify-center">
            <Database className="w-5 h-5 text-[#FF4D5A]" />
          </div>

          <h2 className="mt-4 text-base font-bold text-[#111827] dark:text-white">
            Evidence Preservation
          </h2>

          <p className="mt-2 text-xs leading-relaxed text-[#64748B] dark:text-[#888888]">
            Verification results preserve source information,
            evidence summaries, confidence, and analysis history
            for later review.
          </p>

        </div>

      </div>

      {/* PIPELINE */}

      <section className="p-5 glass-on-air rounded-3xl border border-black/15 dark:border-white/20 shadow-xl">

        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-[#00C2FF]" />

          <h2 className="text-sm font-bold text-[#111827] dark:text-white">
            Verification Pipeline
          </h2>
        </div>

        <div className="mt-5 grid grid-cols-2 md:grid-cols-5 gap-3">

          {[
            ['01', 'Claim', Search],
            ['02', 'News Search', Newspaper],
            ['03', 'Extraction', Globe],
            ['04', 'ML Analysis', BrainCircuit],
            ['05', 'Verdict', CheckCircle2],
          ].map(([number, label, Icon]) => {

            const PipelineIcon =
              Icon as React.FC<{
                className?: string;
              }>;

            return (
              <div
                key={number as string}
                className="relative p-3 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10"
              >

                <div className="text-[9px] font-black text-[#00C2FF]">
                  {number as string}
                </div>

                <PipelineIcon className="w-4 h-4 mt-2 text-[#1DB954]" />

                <div className="mt-2 text-[10px] font-bold text-[#111827] dark:text-white">
                  {label as string}
                </div>

              </div>
            );
          })}

        </div>

      </section>

      {/* SAFETY */}

      <section className="p-5 rounded-3xl bg-[#F5B942]/10 border border-[#F5B942]/25">

        <div className="flex items-start gap-3">

          <ShieldCheck className="w-5 h-5 flex-shrink-0 text-[#F5B942]" />

          <div>

            <h2 className="text-sm font-bold text-[#111827] dark:text-white">
              Verification Disclaimer
            </h2>

            <p className="mt-1 text-xs leading-relaxed text-[#475569] dark:text-[#A7A7A7]">
              ClarifAI provides evidence-based assessments rather
              than absolute guarantees of truth. A result should
              be interpreted alongside the cited sources and the
              available evidence.
            </p>

          </div>

        </div>

      </section>

      {/* ACTIONS */}

      <div className="flex flex-wrap justify-center gap-3">

        <button
          type="button"
          onClick={() => {
            playGlassClickSound();
            setActiveNav('verify');
          }}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#1DB954] text-black text-xs font-bold shadow-md cursor-pointer"
        >
          <Search className="w-3.5 h-3.5" />
          Start Verification
        </button>

        <button
          type="button"
          onClick={() => {
            playGlassClickSound();
            setActiveNav('history');
          }}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full glass-interactive text-xs font-bold text-[#111827] dark:text-white cursor-pointer"
        >
          <Database className="w-3.5 h-3.5 text-[#00C2FF]" />
          View History
        </button>

      </div>

      {/* FOOTER */}

      <div className="text-center pt-3 pb-4">

        <div className="flex items-center justify-center gap-2 text-[10px] text-[#64748B] dark:text-[#666666]">
          <span>ClarifAI</span>
          <span>•</span>
          <span>News Verification System</span>
          <span>•</span>
          <span>v{health.version || '1.0.0'}</span>
        </div>

      </div>

    </div>
  );
};