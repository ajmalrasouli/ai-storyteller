const { } = require('tailwindcss/defaultTheme');

module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      keyframes: {
        drift: {
          '0%': { transform: 'translateY(0px) translateX(0px) scale(1)', opacity: '0.5' },
          '50%': { transform: 'translateY(-15px) translateX(10px) scale(1.05)', opacity: '0.7' },
          '100%': { transform: 'translateY(5px) translateX(-5px) scale(1)', opacity: '0.5' },
        },
        'drift-slow': {
          from: { transform: 'translate(0, 0) rotate(0deg)' },
          to: { transform: 'translate(10px, -15px) rotate(5deg)' },
        },
        'drift-alt': {
          from: { transform: 'translate(0, 0) scale(1)' },
          to: { transform: 'translate(-10px, 10px) scale(1.03)' },
        },
        'spin-subtle': {
          from: { transform: 'rotate(0deg) scale(1)' },
          to: { transform: 'rotate(20deg) scale(1.02)' },
        },
        'spin-bounce': {
          '0%, 100%': { transform: 'rotate(0deg) translateY(0)' },
          '25%': { transform: 'rotate(10deg) translateY(-8px)' },
          '50%': { transform: 'rotate(-5deg) translateY(0)' },
          '75%': { transform: 'rotate(5deg) translateY(-4px)' },
        },
        bounce: {
          '0%, 20%, 50%, 80%, 100%': { transform: 'translateY(0)' },
          '40%': { transform: 'translateY(-15px)' },
          '60%': { transform: 'translateY(-7px)' },
        },
        spin: {
          from: { transform: 'rotate(0deg)' },
          to: { transform: 'rotate(360deg)' },
        }
      },
      animation: {
        drift: 'drift var(--anim-duration, 15s) ease-in-out infinite alternate',
        'drift-slow': 'drift-slow var(--anim-duration, 20s) ease-in-out infinite alternate',
        'drift-alt': 'drift-alt var(--anim-duration, 18s) ease-in-out infinite alternate',
        'spin-subtle': 'spin-subtle var(--anim-duration, 25s) ease-in-out infinite alternate',
        'spin-bounce': 'spin-bounce var(--anim-duration, 12s) ease-in-out infinite',
        bounce: 'bounce 2s infinite ease-in-out',
        spin: 'spin 1s linear infinite',
      }
    },
  },
  plugins: [
  ],
};