module.exports = {
  content: [
    "./theme/templates/**/*.html",
    "./templates/**/*.html",
    "./**/*.html"
  ],
  safelist: [
    "bg-gray-100", "bg-white", "shadow-md", "shadow-lg", "rounded-lg", "rounded",
    "p-8", "p-6", "px-3", "py-2", "max-w-md", "w-full", "flex", "flex-col",
    "items-center", "justify-center", "space-y-4", "text-2xl", "text-4xl", "text-lg",
    "font-bold", "font-semibold", "font-medium", "text-center", "text-gray-500",
    "text-gray-600", "text-gray-700", "text-red-500", "text-white", "bg-blue-600",
    "bg-blue-500", "hover:bg-blue-700", "focus:ring-2", "focus:ring-blue-500",
    "focus:outline-none", "select-all", "gap-2", "gap-4", "gap-6", "container",
    "mx-auto", "mt-auto", "mt-8", "min-h-screen", "grid", "grid-cols-1",
    "md:grid-cols-2", "lg:grid-cols-3", "text-blue-700", "text-blue-600"
  ],
  theme: {
    extend: {
      colors: {
        pastelblue: "#e8f0ff"
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
    }
  },
  plugins: [],
};