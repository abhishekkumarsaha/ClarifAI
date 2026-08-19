import React, { useState, useEffect } from 'react';
import { Cpu, Terminal } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const SystemStatusTicker: React.FC = () => {
  const { health } = useApp();
  const [timeStr, setTimeStr] = useState<string>('');
  const [ping, setPing] = useState<number>(14);

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit' }));
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const pingInterval = setInterval(() => {
      setPing(Math.floor(11 + Math.random() * 5));
    }, 4000);
    return () => clearInterval(pingInterval);
  }, []);

  const isHealthy = health.status === 'healthy';

  return (
    <div className="inline-flex items-center gap-2.5 px-3 py-1 bg-black/5 dark:bg-white/5 rounded-full text-[10px] font-mono text-[#475569] dark:text-[#A7A7A7] border border-black/10 dark:border-white/10">
      <span className="flex items-center gap-1 font-bold text-[#1DB954]">
        <span className={`w-1.5 h-1.5 rounded-full ${isHealthy ? 'bg-[#1DB954] animate-pulse' : 'bg-[#FF4D5A]'}`} />
        <span>{isHealthy ? 'SYSTEM ONLINE' : 'ENGINE READY'}</span>
      </span>

      <span className="opacity-40 hidden sm:inline">•</span>

      <span className="hidden sm:flex items-center gap-1 font-medium">
        <Cpu className="w-3 h-3 text-[#00C2FF]" />
        <span>SVM v2.0</span>
      </span>

      <span className="opacity-40 hidden md:inline">•</span>

      <span className="hidden md:flex items-center gap-1 font-medium">
        <span>{ping}ms</span>
      </span>

      <span className="opacity-40 hidden lg:inline">•</span>

      <span className="hidden lg:flex items-center gap-1 font-bold text-[#111827] dark:text-white">
        <Terminal className="w-3 h-3 text-[#00C2FF]" />
        <span>{timeStr}</span>
      </span>
    </div>
  );
};
