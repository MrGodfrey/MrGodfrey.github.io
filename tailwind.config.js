module.exports = {
  content: [
    "./templates/**/*.html",
    "./content/**/*.md",
    "./*.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#000666",
        "primary-container": "#1a237e",
        "on-primary": "#ffffff",
        "on-primary-container": "#8690ee",
        secondary: "#4c616c",
        "secondary-container": "#cfe6f2",
        "on-secondary-container": "#526772",
        "tertiary-container": "#3e2d00",
        "on-tertiary-container": "#ae945c",
        surface: "#fbf9f8",
        "surface-container-low": "#f6f3f2",
        "surface-container": "#f0eded",
        "surface-container-high": "#eae8e7",
        "surface-container-highest": "#e4e2e1",
        "surface-container-lowest": "#ffffff",
        "on-surface": "#1b1c1c",
        "on-surface-variant": "#454652",
        outline: "#767683",
        "outline-variant": "#c6c5d4",
        background: "#fbf9f8",
      },
      fontFamily: {
        headline: ["Noto Serif", "FangSong", "STFangsong", "serif"],
        body: ["Inter", "PingFang SC", "Helvetica Neue", "sans-serif"],
        label: ["Inter", "PingFang SC", "sans-serif"],
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/container-queries"),
  ],
};