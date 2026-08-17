import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BookOpen,
  HelpCircle,
  Shield,
  ChevronDown,
  ChevronUp,
  Cpu,
  Search,
  Sparkles,
  Layers,
  FileCheck,
  CheckCircle2,
  Info,
} from 'lucide-react';

export const AboutPage: React.FC = () => {
  const [expandedFaq, setExpandedFaq] = useState<number | null>(0);

  const toggleFaq = (index: number) => {
    setExpandedFaq(expandedFaq === index ? null : index);
  };

  const steps = [
    {
      num: '01',
      title: 'Claim Analysis & Query Generation',
      icon: Search,
      color: 'text-[#00C2FF]',
      bgColor: 'bg-[#00C2FF]/10',
      borderColor: 'border-[#00C2FF]/30',
      desc: 'ClarifAI parses the claim, extracts core entities, removes stop words, and constructs focused search queries.',
    },
    {
      num: '02',
      title: 'Live News Retrieval',
      icon: Layers,
      color: 'text-[#1DB954]',
      bgColor: 'bg-[#1DB954]/10',
      borderColor: 'border-[#1DB954]/30',
      desc: 'Queries live news indexes from Currents API to retrieve recent published reports from verified news publishers.',
    },
    {
      num: '03',
      title: 'Evidence Extraction',
      icon: FileCheck,
      color: 'text-[#F5B942]',
      bgColor: 'bg-[#F5B942]/10',
      borderColor: 'border-[#F5B942]/30',
      desc: 'Article bodies are scraped and extracted to identify specific findings supporting or contradicting the claim.',
    },
    {
      num: '04',
      title: 'Machine Learning Classification',
      icon: Cpu,
      color: 'text-[#00C2FF]',
      bgColor: 'bg-[#00C2FF]/10',
      borderColor: 'border-[#00C2FF]/30',
      desc: 'A calibrated Linear SVM model evaluates TF-IDF structural token frequencies to score linguistic patterns.',
    },
    {
      num: '05',
      title: 'AI Explanation Synthesis',
      icon: Sparkles,
      color: 'text-[#1DB954]',
      bgColor: 'bg-[#1DB954]/10',
      borderColor: 'border-[#1DB954]/30',
      desc: 'An LLM synthesizes evidence articles, ML signals, and source consensus into a transparent natural-language explanation.',
    },
    {
      num: '06',
      title: 'Final Verification Result',
      icon: CheckCircle2,
      color: 'text-[#FF4D5A]',
      bgColor: 'bg-[#FF4D5A]/10',
      borderColor: 'border-[#FF4D5A]/30',
      desc: 'Renders the final verdict (Likely True, Likely False, Unverified), confidence score, evidence cards, and receipts.',
    },
  ];

  const faqs = [
    {
      q: 'What does LIKELY TRUE / LIKELY FALSE mean?',
      a: 'Verdicts represent the synthesis of published news evidence and linguistic pattern analysis. Likely True indicates high source agreement supporting the claim, while Likely False indicates clear source contradiction.',
    },
    {
      q: 'Why does a claim return UNVERIFIED?',
      a: 'UNVERIFIED means that insufficient recent published news articles were found in live indexes to confirm or refute the claim.',
    },
    {
      q: 'Is ClarifAI machine learning model factual authority?',
      a: 'No. Model predictions are analytical tools that describe structural TF-IDF linguistic patterns. They assist human research and are not absolute factual proof.',
    },
    {
      q: 'How does live news search protect API keys?',
      a: 'All news search requests pass through the secure Python FastAPI backend. Secrets like CURRENTS_API_KEY remain safely stored on the server and are never exposed to browser client code.',
    },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div>
        <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#111827] dark:text-white mb-2">
          Help & Documentation
        </h1>
        <p className="text-base text-[#475569] dark:text-[#A7A7A7] max-w-2xl leading-relaxed">
          Learn about ClarifAI's mission, verification architecture, FAQs, and safety disclosures.
        </p>
      </div>

      {/* SECTION 1: ABOUT CLARIFAI (TEXT SHIMMER & ISOLATED HOVER) */}
      <div className="p-6 help-card-interactive space-y-3 shadow-xl border border-black/15 dark:border-white/20">
        <div className="text-lg font-bold text-[#111827] dark:text-white flex items-center gap-2">
          <Info className="w-5 h-5 text-[#00C2FF]" />
          <span className="help-text-shine">About ClarifAI</span>
        </div>
        <p className="text-sm text-[#475569] dark:text-[#A7A7A7] leading-relaxed">
          ClarifAI is an analytical news verification engine designed to evaluate digital claims by searching live news coverage, assessing linguistic patterns with a calibrated Linear SVM model, and synthesizing transparent evidence summaries with AI.
        </p>
      </div>

      {/* SECTION 2: HOW CLARIFAI WORKS (6-STEP PIPELINE WITH ISOLATED TEXT SHIMMER) */}
      <div className="space-y-4">
        <div className="text-lg font-bold text-[#111827] dark:text-white flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-[#1DB954]" />
          <span>How ClarifAI Verifies a Claim (6-Step Pipeline)</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {steps.map((step, idx) => {
            const Icon = step.icon;

            return (
              <div
                key={idx}
                className="p-5 help-card-interactive space-y-3 border border-black/15 dark:border-white/20"
              >
                <div className="flex items-center justify-between">
                  <span
                    className={`w-8 h-8 rounded-xl ${step.bgColor} ${step.color} font-black text-sm flex items-center justify-center border ${step.borderColor}`}
                  >
                    {step.num}
                  </span>
                  <Icon className={`w-5 h-5 ${step.color}`} />
                </div>
                <h4 className="font-bold text-base text-[#111827] dark:text-white help-text-shine transition-colors">
                  {step.title}
                </h4>
                <p className="text-xs text-[#475569] dark:text-[#A7A7A7] leading-relaxed">
                  {step.desc}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* SECTION 3: FREQUENTLY ASKED QUESTIONS (INTERACTIVE ACCORDIONS WITH ISOLATED TEXT SHIMMER) */}
      <div className="space-y-4">
        <div className="text-lg font-bold text-[#111827] dark:text-white flex items-center gap-2">
          <HelpCircle className="w-5 h-5 text-[#F5B942]" />
          <span>Frequently Asked Questions</span>
        </div>

        <div className="space-y-3">
          {faqs.map((faq, idx) => {
            const isOpen = expandedFaq === idx;

            return (
              <div
                key={idx}
                className="help-card-interactive rounded-2xl overflow-hidden shadow-sm border border-black/15 dark:border-white/20"
              >
                <button
                  onClick={() => toggleFaq(idx)}
                  className="w-full p-4 flex items-center justify-between text-left font-bold text-sm text-[#111827] dark:text-white focus:outline-none hover:bg-black/5 dark:hover:bg-white/5 transition-colors cursor-pointer"
                >
                  <span className="help-text-shine">{faq.q}</span>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-[#1DB954] flex-shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-[#475569] dark:text-[#A7A7A7] flex-shrink-0" />
                  )}
                </button>

                <AnimatePresence>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      className="px-4 pb-4 text-xs text-[#475569] dark:text-[#A7A7A7] leading-relaxed border-t border-black/10 dark:border-white/10 pt-3"
                    >
                      {faq.a}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>
      </div>

      {/* SECTION 4: PRIVACY & EDITORIAL DISCLOSURES (TEXT SHIMMER & ISOLATED HOVER) */}
      <div className="p-6 help-card-interactive space-y-3 text-xs text-[#475569] dark:text-[#A7A7A7] shadow-xl border border-black/15 dark:border-white/20">
        <div className="text-sm font-bold text-[#111827] dark:text-white flex items-center gap-2 mb-2">
          <Shield className="w-4 h-4 text-[#FF4D5A]" />
          <span className="help-text-shine">Safety Disclosures & Privacy</span>
        </div>
        <ul className="space-y-2 list-disc pl-4">
          <li>ClarifAI queries published news coverage from verified online indexes.</li>
          <li>Extracted article findings are summarized to provide transparent evidence alignment.</li>
          <li>Machine Learning predictions are based on linguistic pattern frequencies.</li>
          <li>ClarifAI does not store user passwords or sensitive credentials on the browser.</li>
        </ul>
      </div>
    </div>
  );
};
