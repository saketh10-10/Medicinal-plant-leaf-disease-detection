/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
        colors: {
        primary: {
          DEFAULT: '#4ade80', // bright green for accents
          foreground: '#022c22', // dark green for text on primary
        },
        accent: {
          DEFAULT: '#fbbf24', // amber/yellow for "Detection"
          foreground: '#022c22',
        },
        background: '#022c22', // very dark green
        foreground: '#ecfdf5', // very light green/white
        muted: {
          DEFAULT: 'rgba(255, 255, 255, 0.1)',
          foreground: '#a7f3d0', // light green text
        },
        destructive: {
          DEFAULT: '#ef4444',
          foreground: '#ffffff',
        },
      },
      fontFamily: {
        sans: ['system-ui', 'sans-serif'],
        heading: ['Inter', 'sans-serif'],
      },
      animation: {
        'slide-up': 'slideUp 0.6s ease-out forwards',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'glow-accent': 'glowAccent 2s ease-in-out infinite alternate',
      },
      keyframes: {
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(16, 185, 129, 0.3)' },
          '100%': { boxShadow: '0 0 30px rgba(16, 185, 129, 0.6)' },
        },
        glowAccent: {
          '0%': { boxShadow: '0 0 20px rgba(139, 92, 246, 0.3)' },
          '100%': { boxShadow: '0 0 30px rgba(139, 92, 246, 0.6)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
