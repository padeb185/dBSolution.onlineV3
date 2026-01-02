module.exports = {
  content: [
    "./theme/templates/**/*.html",
    "./templates/**/*.html",
    "./**/*.html"
  ],
  safelist: [
    "bg-gray-100","bg-white","shadow-md","rounded-lg","p-8","max-w-md","w-full",
    "text-2xl","font-bold","mb-6","text-center","text-red-500",
    "border","px-3","py-2","rounded","space-y-4",
    "bg-blue-600","text-white","hover:bg-blue-700","py-2",
    "flex","items-center","justify-center","flex-col",
    "min-h-screen",
    "container","mx-auto","mt-auto","p-6","flex-1","text-gray-500",
    "focus:ring-2","focus:outline-none","select-all",
    "text-blue-700","text-lg","font-semibold","gap-6","grid","grid-cols-1","md:grid-cols-2","lg:grid-cols-3"
  ],
  theme: {
    extend: {
      colors: {
        pastelblue: "#e8f0ff"
      }
    }
  },
  plugins: []
};
