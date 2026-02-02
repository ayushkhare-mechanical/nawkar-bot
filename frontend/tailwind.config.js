/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                poppins: ['Poppins', 'sans-serif'],
            },
            colors: {
                scandi: {
                    bg: '#f9fafb', // Off-white
                    dark: '#121212', // Matte Black
                    text: '#1f2937', // Charcoal
                    accents: '#6366f1', // Soft Indigo
                    muted: '#9ca3af', // Gray
                }
            },
            borderRadius: {
                'pill': '9999px',
            }
        },
    },
    plugins: [],
}
