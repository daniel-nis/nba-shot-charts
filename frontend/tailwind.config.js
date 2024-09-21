/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'background': '#1c1c1e',
        'gray-800': '#2c2c2e',
        'gray-700': '#3a3a3c',
        'blue-500': '#0a84ff',
      },
      fontFamily: {
        'arvo': ['Arvo', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

