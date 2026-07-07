/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#09090b",
        surface: "rgba(24, 24, 27, 0.7)",
        border: "rgba(255, 255, 255, 0.1)",
        primary: "#3b82f6",
        accent: "#10b981",
        danger: "#ef4444",
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}
