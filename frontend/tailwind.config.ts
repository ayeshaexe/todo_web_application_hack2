import type { Config } from 'tailwindcss';

export default {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1C352D',
        secondary: '#A6B28B',
        accent: '#F5C9B0',
        background: '#F9F6F3',
      },
    },
  },
  plugins: [],
} satisfies Config;