/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './theme/templates/**/*.html',
    './theme/static/theme/js/**/*.js',
  ],
  theme: {
    extend: { colors: {
        pastelblue: "#DDEBFF", // bleu pastel clair
      },
    },
  },
  plugins: [],
}
