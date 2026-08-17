import * as React from "react";

export interface LiquidButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'emerald' | 'cyan' | 'destructive' | 'outline' | 'ghost';
  size?: 'default' | 'sm' | 'lg' | 'xl' | 'icon';
  children?: React.ReactNode;
}

export function GlassFilter() {
  return (
    <svg className="hidden" aria-hidden>
      <defs>
        <filter
          id="liquid-glass-filter"
          x="0%"
          y="0%"
          width="100%"
          height="100%"
          colorInterpolationFilters="sRGB"
        >
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.05 0.05"
            numOctaves="1"
            seed="1"
            result="turbulence"
          />
          <feGaussianBlur in="turbulence" stdDeviation="2" result="blurredNoise" />
          <feDisplacementMap
            in="SourceGraphic"
            in2="blurredNoise"
            scale="70"
            xChannelSelector="R"
            yChannelSelector="B"
            result="displaced"
          />
          <feGaussianBlur in="displaced" stdDeviation="4" result="finalBlur" />
          <feComposite in="finalBlur" in2="finalBlur" operator="over" />
        </filter>
      </defs>
    </svg>
  );
}

export const LiquidButton = React.forwardRef<HTMLButtonElement, LiquidButtonProps>(
  ({ className = '', variant = 'default', size = 'default', children, ...props }, ref) => {
    let variantStyles = "bg-transparent text-[#111827] dark:text-white hover:scale-[1.03] active:scale-[0.97]";
    
    if (variant === 'emerald') {
      variantStyles = "bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold shadow-lg hover:scale-[1.03] active:scale-[0.97]";
    } else if (variant === 'cyan') {
      variantStyles = "bg-[#00C2FF]/15 border border-[#00C2FF]/40 text-[#00C2FF] hover:bg-[#00C2FF]/25 hover:scale-[1.03] active:scale-[0.97]";
    } else if (variant === 'destructive') {
      variantStyles = "bg-[#FF4D5A]/15 border border-[#FF4D5A]/40 text-[#FF4D5A] hover:bg-[#FF4D5A]/25 hover:scale-[1.03] active:scale-[0.97]";
    } else if (variant === 'outline') {
      variantStyles = "border border-black/15 dark:border-white/20 bg-white/60 dark:bg-[#161616]/60 hover:bg-black/5 dark:hover:bg-white/10 text-[#111827] dark:text-white hover:scale-[1.02] active:scale-[0.98]";
    } else if (variant === 'ghost') {
      variantStyles = "hover:bg-black/5 dark:hover:bg-white/10 text-[#111827] dark:text-white";
    }

    let sizeStyles = "h-9 px-4 py-2 text-xs font-bold";
    if (size === 'sm') sizeStyles = "h-8 text-xs gap-1.5 px-3.5 font-bold";
    else if (size === 'lg') sizeStyles = "h-11 px-6 text-sm font-bold";
    else if (size === 'xl') sizeStyles = "h-12 px-8 text-base font-bold";
    else if (size === 'icon') sizeStyles = "size-9 rounded-full flex items-center justify-center";

    return (
      <button
        ref={ref}
        data-slot="liquid-button"
        className={`relative inline-flex items-center justify-center cursor-pointer gap-2 whitespace-nowrap rounded-full font-bold transition-all disabled:pointer-events-none disabled:opacity-50 shrink-0 outline-none ${variantStyles} ${sizeStyles} ${className}`}
        {...props}
      >
        {/* Glass shadow layer */}
        <div
          className="absolute top-0 left-0 z-0 h-full w-full rounded-full transition-all pointer-events-none"
          style={{
            boxShadow: `
              0 0 6px rgba(0,0,0,0.03),
              0 2px 6px rgba(0,0,0,0.08),
              inset 3px 3px 0.5px -3.5px rgba(255,255,255,0.15),
              inset -3px -3px 0.5px -3.5px rgba(255,255,255,0.85),
              inset 1px 1px 1px -0.5px rgba(255,255,255,0.6),
              inset -1px -1px 1px -0.5px rgba(255,255,255,0.6),
              inset 0 0 6px 6px rgba(255,255,255,0.12),
              inset 0 0 2px 2px rgba(255,255,255,0.06),
              0 0 12px rgba(0,0,0,0.12)
            `,
          }}
        />

        {/* Backdrop distortion layer */}
        <div
          className="absolute top-0 left-0 isolate -z-10 h-full w-full overflow-hidden rounded-full pointer-events-none"
          style={{ backdropFilter: 'blur(8px) url("#liquid-glass-filter")' }}
        />

        {/* Content */}
        <div className="pointer-events-none z-10 flex items-center justify-center gap-2">
          {children}
        </div>

        {/* Inline SVG filter */}
        <GlassFilter />
      </button>
    );
  }
);

LiquidButton.displayName = "LiquidButton";
