window.MathJax = {
  loader: { paths: { mathjax: '/assets/vendor/mathjax' } },
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']],
    processEscapes: true,
    tags: 'ams',
  },
  options: {
    ignoreHtmlClass: '.*',
    processHtmlClass: 'arithmatex',
  },
  output: {
    font: 'mathjax-newcm',
    fontPath: '/assets/vendor/mathjax-newcm-font',
    displayOverflow: 'scroll',
  },
};
