// tailwind.config.js
module.exports = {
  content: [
    "./theme/templates/**/*.html",
    "./templates/**/*.html",
    "./**/*.html"
  ],
  safelist: [
    // Couleurs bg et text utilisées dynamiquement
    "bg-gray-100", "bg-white", "bg-green-100", "bg-amber-100", "bg-red-100",
    "text-gray-500", "text-gray-600", "text-gray-700",
    "text-green-800", "text-amber-800", "text-red-800",
    "border-green-300", "border-amber-300", "border-red-300",

    // Classes utilitaires
    "shadow-md", "shadow-lg", "rounded-lg", "rounded",
    "p-8", "p-6", "px-3", "py-2", "max-w-md", "w-full",
    "flex", "flex-col", "items-center", "justify-center",
    "space-y-4", "text-2xl", "text-4xl", "text-lg",
    "font-bold", "font-semibold", "font-medium", "text-center",
    "bg-blue-600", "bg-blue-500", "hover:bg-blue-700",
    "focus:ring-2", "focus:ring-blue-500", "focus:outline-none",
    "select-all", "gap-2", "gap-4", "gap-6", "container",
    "mx-auto", "mt-auto", "mt-8", "min-h-screen", "grid",
    "grid-cols-1", "md:grid-cols-2", "lg:grid-cols-3",
    "text-blue-700", "text-blue-600"
  ],
  theme: {
    extend: {
      colors: {
        pastelblue: "#DBDFFD",
        amber: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        green: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        },
        red: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
        },
      },
      keyframes: {
        barAnim: {
          '0%, 100%': { transform: 'scaleY(0.6)' },
          '50%': { transform: 'scaleY(1)' },
        },
        draw: {
          '0%': { strokeDashoffset: '120' },
          '50%': { strokeDashoffset: '0' },
          '100%': { strokeDashoffset: '120' },
        },
        progress: {
          '0%': { marginLeft: '-40%' },
          '50%': { marginLeft: '100%' },
          '100%': { marginLeft: '-40%' },
        },
      },
      animation: {
        barAnim: 'barAnim 1.2s infinite ease-in-out',
        draw: 'draw 2s infinite ease-in-out',
        progress: 'progress 1.5s infinite ease-in-out',
      },
    },
  },
  plugins: [],
};