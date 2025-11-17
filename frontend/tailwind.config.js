/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'scam-red': '#dc2626',
        'subito-blue': '#0066ff',
      },
    },
  },
  plugins: [],
}
