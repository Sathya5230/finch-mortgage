/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*.html',
    './blog/*.html',
    './calculators/*.html',
    './guides/*.html',
    './lenders/*.html',
    './services/*.html',
    './testimonials/*.html',
    './weekly-reports/*.html',
    './script.js',
  ],
  safelist: [],
  theme: {
    extend: {
      colors: {
        'finch-forest': '#10443e','finch-sage': '#62a29a','finch-medium': '#32745c',
        'finch-teal': '#62a29a','finch-gold': '#b29361','finch-mist': '#f3ede5',
        'finch-cream': '#ede4d6','brand-gold': '#b29361','brand-amber': '#10443e',
        'neutral-black': '#10443e','neutral-medGray': '#3a5c56','neutral-warmGray': '#7a9490','neutral-lightGray': '#aec8c4',
      },
    },
  },
  plugins: [],
};
