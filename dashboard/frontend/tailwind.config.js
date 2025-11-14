/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Galaxy Theme Colors
        'bg-primary': '#0a0e27',
        'bg-surface': '#1a1f3a',
        'bg-surface-hover': '#252b47',
        'text-primary': '#e0e8ff',
        'text-secondary': '#a0aff0',
        'neon-cyan': '#00f0ff',
        'neon-red': '#ff1744',
        'neon-purple': '#b24bf3',
        'neon-green': '#00e676',
        'neon-yellow': '#ffeb3b',
      },
      boxShadow: {
        'neon-cyan': '0 0 10px #00f0ff, 0 0 20px rgba(0, 240, 255, 0.5)',
        'neon-cyan-intense': '0 0 15px #00f0ff, 0 0 30px rgba(0, 240, 255, 0.7), 0 0 45px rgba(0, 240, 255, 0.4)',
        'neon-red': '0 0 10px #ff1744, 0 0 20px rgba(255, 23, 68, 0.5)',
        'neon-purple': '0 0 10px #b24bf3, 0 0 20px rgba(178, 75, 243, 0.5)',
        'neon-green': '0 0 10px #00e676, 0 0 20px rgba(0, 230, 118, 0.5)',
        'neon-yellow': '0 0 10px #ffeb3b, 0 0 20px rgba(255, 235, 59, 0.5)',
      },
      animation: {
        'glow-cyan': 'glow-cyan 2s ease-in-out infinite',
        'glow-red': 'glow-red 2s ease-in-out infinite',
        'spin-slow': 'spin 3s linear infinite',
        'fade-in-up': 'fade-in-up 0.5s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        'glow-cyan': {
          '0%, 100%': { boxShadow: '0 0 10px #00f0ff, 0 0 20px rgba(0, 240, 255, 0.5)' },
          '50%': { boxShadow: '0 0 20px #00f0ff, 0 0 40px rgba(0, 240, 255, 0.7), 0 0 60px rgba(0, 240, 255, 0.4)' },
        },
        'glow-red': {
          '0%, 100%': { boxShadow: '0 0 10px #ff1744, 0 0 20px rgba(255, 23, 68, 0.5)' },
          '50%': { boxShadow: '0 0 20px #ff1744, 0 0 40px rgba(255, 23, 68, 0.7), 0 0 60px rgba(255, 23, 68, 0.4)' },
        },
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
