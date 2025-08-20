/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './templates/**/*.html',
    './**/templates/**/*.html',
    './frontend/templates/**/*.html',
    './frontend/templates/*.html',
    './**/templates/**/*.html',
    './**/static/**/*.js',
    './shared_templates/components/*.html'
  ],
  theme: {
    extend: {
      fontFamily: {
        'nunito-sans': ['Nunito Sans', 'sans-serif'],
        'inter': ['Inter', 'sans-serif']
      },
      height: {
        'calc-100-minus-100': 'calc(100% - 100px)',
        'calc-100-minus-130': 'calc(100% - 130px)',
        'calc-100-minus-150': 'calc(100% - 150px)',
        'calc-100-minus-180': 'calc(100% - 180px)',
        'calc-100-minus-200': 'calc(100% - 200px)',
        'calc-100-minus-50': 'calc(100% - 50px)',
        'calc-100-minus-30': 'calc(100% - 30px)',
      },
    },
  },
  plugins: [
    // Plugin temporaneamente disabilitati per la migrazione v4
    // require('daisyui'),
    // function({ addVariant }) {
    //   addVariant('my_light', '[data-theme="my_light"] &')
    //   addVariant('my_dark', '[data-theme="my_dark"] &')
    // }
  ],
  // Configurazione DaisyUI temporaneamente disabilitata
  // daisyui: {
  //   themes: false,
  //   darkTheme: "my_dark",
  //   base: true,
  //   styled: true,
  //   utils: true,
  // }
}