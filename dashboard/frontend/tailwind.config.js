/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Neon Theme Colors
        'neon-cyan': '#00f0ff',
        'energy-red': '#ff1744',
        'nebula-purple': '#b24bff',
        'deep-space': '#0a0e27',
        'surface-dark': '#1a1f3a',
        'text-primary': '#e0e8ff',
      },
      boxShadow: {
        'neon-cyan': '0 0 10px #00f0ff',
        'neon-cyan-strong': '0 0 20px #00f0ff',
        'energy-red': '0 0 10px #ff1744',
        'nebula-purple': '0 0 10px #b24bff',
      }
    },
  },
  plugins: [],
}
