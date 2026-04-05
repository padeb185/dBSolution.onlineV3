// tailwind.config.js
module.exports = {
  content: [
    "./theme/templates/**/*.html",
    "./templates/**/*.html",
    "./theme/static/src/**/*.js",
  ],

  safelist: [

      'bg-[#FFF9C4]',
    'text-[#FFEB3B]',
    'border-[#FFEB3B]',
    // Backgrounds
    "bg-gray-100", "bg-white",
    "bg-green-100", "bg-lime-100", "bg-red-100",
    "bg-yellow-100", "bg-amber-100",
    "bg-blue-500", "bg-blue-600", "hover:bg-blue-700",

    // Custom yellow
    "bg-customyellow-100",
    "text-customyellow-800",
    "border-customyellow-500",

    // Text
    "text-gray-500", "text-gray-600", "text-gray-700",
    "text-green-800", "text-lime-800", "text-red-800",
    "text-yellow-800", "text-amber-800",
    "text-blue-600", "text-blue-700",

    // Borders
    "border-green-300", "border-lime-300", "border-red-300",
    "border-yellow-500", "border-amber-500",

    // Layout / spacing
    "shadow-md", "shadow-lg", "rounded", "rounded-lg",
    "p-6", "p-8", "px-3", "py-2",
    "max-w-md", "w-full",
    "flex", "flex-col", "items-center", "justify-center",
    "space-y-4", "gap-2", "gap-4", "gap-6",
    "container", "mx-auto", "mt-8", "mt-auto", "min-h-screen",

    // Grid
    "grid", "grid-cols-1", "md:grid-cols-2", "lg:grid-cols-3",

    // Typography
    "text-center", "text-lg", "text-2xl", "text-4xl",
    "font-medium", "font-semibold", "font-bold",

    // Interaction
    "focus:ring-2", "focus:ring-blue-500", "focus:outline-none",
    "select-all",
  ],

  theme: {
    extend: {
      colors: {
        pastelblue: "#DBDFFD",

        customyellow: {
          100: "#fef3c7",
          500: "#f59e0b",
          800: "#92400e",
        },

        customamber: {
          100: "#fef08a",
          500: "#d97706",
          800: "#78350f",
        },

        customlime: {
          100: "#d9f99d",
          500: "#65a30d",
          800: "#365314",
        },
      },

      keyframes: {
        barAnim: {
          "0%, 100%": { transform: "scaleY(0.6)" },
          "50%": { transform: "scaleY(1)" },
        },
        draw: {
          "0%": { strokeDashoffset: "120" },
          "50%": { strokeDashoffset: "0" },
          "100%": { strokeDashoffset: "120" },
        },
        progress: {
          "0%": { marginLeft: "-40%" },
          "50%": { marginLeft: "100%" },
          "100%": { marginLeft: "-40%" },
        },
      },

      animation: {
        barAnim: "barAnim 1.2s infinite ease-in-out",
        draw: "draw 2s infinite ease-in-out",
        progress: "progress 1.5s infinite ease-in-out",
      },
    },
  },

  plugins: [],
};