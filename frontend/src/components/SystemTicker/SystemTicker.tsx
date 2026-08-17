import React, { useState, useEffect } from 'react';
import { Activity, Terminal, ShieldCheck, Cpu } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const SystemStatusTicker: React.FC = () => {
  const { health } = useApp();
  const [timeStr, setTimeStr] = useState<string>('');
  const [ping, setPing] = useState<number>(14);

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Jitter ping slightly for kinetic telemetry feel
  useEffect(() => {
    const pingInterval = setInterval(() => {
      setPing(Math.floor(11 + Math.random() * 6));
    }, 4000);
    return () => clearInterval(pingInterval);
  }, []);

  return (
    <div className="flex items-center justify-between px-4 py-1.5 glass-content rounded-full text-[10px] font-mono text-[#475569] dark:text-[#A7A7A7] border border-black/10 dark:border-white/10 shadow-sm max-w-3xl mx-auto my-2 overflow-x-auto no-scrollbar">
      <div className="flex items-center gap-3 flex-shrink-0">
        <span className="flex items-center gap-1 font-bold text-[#1DB954]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#1DB954] animate-pulse" />
          <span>MATRIX ONLINE</span>
        </span>

        <span className="opacity-40">•</span>

        <span className="flex items-center gap-1 font-medium">
          <Cpu className="w-3 h-3 text-[#00C2FF]" />
          <span>SVM ENGINE v2.0</span>
        </span>

        <span className="opacity-40">•</span>

        <span className="flex items-center gap-1 font-medium">
          <Activity className="w-3 h-3 text-[#F5B942]" />
          <span>PING: {ping}ms</span>
        </span>
      </div>

      <div className="flex items-center gap-3 flex-shrink-0 font-bold text-[#111827] dark:text-white hidden sm:flex">
        <span className="flex items-center gap-1">
          <Terminal className="w-3 h-3 text-[#00C2FF]" />
          <span>UTC {timeStr}</span>
        </span>
        <span className="text-[9px] bg-[#00C2FF]/10 text-[#00C2FF] px-2 py-0.5 rounded-full font-bold border border-[#00C2FF]/30">
          LOCAL PRIVACY
        </span>
      </div>
    </div>
  );
};
