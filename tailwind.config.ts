import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './lib/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d'
        },
        ocean: '#0f766e',
        dusk: '#1f2937'
      },
      fontFamily: {
        sans: ['Inter', 'var(--font-sans)']
      },
      boxShadow: {
        soft: '0 18px 45px rgba(15, 118, 110, 0.12)'
      },
      keyframes: {
        flow: {
          '0%': { transform: 'translateX(0)' },
          '50%': { transform: 'translateX(12px)' },
          '100%': { transform: 'translateX(0)' }
        }
      },
      animation: {
        flow: 'flow 6s ease-in-out infinite'
      }
    }
  },
  plugins: []
};

export default config;
