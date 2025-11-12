/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Galaxy/Universe Neon Theme
        'space-dark': '#0a0e27',
        'surface-dark': '#1a1f3a',
        'surface-light': '#252d4a',
        'neon-cyan': '#00f0ff',
        'energy-red': '#ff1744',
        'nebula-purple': '#b24bff',
        'success-green': '#00e676',
        'plasma-yellow': '#ffeb3b',
        'text-primary': '#e0e8ff',
        'text-secondary': '#a0aff0',
      },
      boxShadow: {
        'neon-cyan': '0 0 10px #00f0ff, 0 0 20px rgba(0, 240, 255, 0.5)',
        'neon-red': '0 0 10px #ff1744, 0 0 20px rgba(255, 23, 68, 0.5)',
        'neon-purple': '0 0 10px #b24bff, 0 0 20px rgba(178, 75, 255, 0.5)',
        'neon-cyan-lg': '0 0 15px #00f0ff, 0 0 30px rgba(0, 240, 255, 0.6), 0 0 45px rgba(0, 240, 255, 0.4)',
      },
      animation: {
        'pulse-neon': 'pulse-neon 2s ease-in-out infinite',
        'glow': 'glow 1.5s ease-in-out infinite alternate',
      },
      keyframes: {
        'pulse-neon': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        'glow': {
          'from': { filter: 'brightness(1) drop-shadow(0 0 5px currentColor)' },
          'to': { filter: 'brightness(1.2) drop-shadow(0 0 10px currentColor)' },
        },
      },
    },
  },
  plugins: [],
}
