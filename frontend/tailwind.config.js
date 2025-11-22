/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'zain-red': '#E60012',
        'zain-dark': '#1a1a1a',
        'zain-gray': '#f5f5f5',
      },
    },
  },
  plugins: [],
}

