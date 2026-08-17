/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#080808',
        sidebar: '#0D0D0D',
        surface: '#121212',
        'surface-hover': '#1A1A1A',
        border: '#222222',
        'border-light': '#333333',
        spotify: {
          green: '#1DB954',
          'green-hover': '#1ed760',
        },
        clarifai: {
          cyan: '#00C2FF',
          mint: '#00E5A8',
        },
        verdict: {
          true: '#1DB954',
          false: '#FF4D5A',
          unverified: '#F5B942',
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Text"', '"SF Pro Display"', '"Helvetica Neue"', 'sans-serif'],
        display: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Display"', '"SF Pro Text"', '"Helvetica Neue"', 'sans-serif'],
        heading: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Display"', '"SF Pro Text"', '"Helvetica Neue"', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'anti-gravity': 'antiGravity 5s ease-in-out infinite',
      },
      keyframes: {
        antiGravity: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-3px)' },
        }
      }
    },
  },
  plugins: [],
}
