// Ship the browser runtime and CHTML font files with the static site.
// No CDN is needed, including for lazily loaded TeX and accessibility modules.
const { cpSync, mkdirSync, rmSync } = require('node:fs');
const { join } = require('node:path');
const root = join(__dirname, '..');

function copyPackage(packageName, targetName, files) {
  const source = join(root, 'node_modules', packageName);
  const target = join(root, 'assets', 'vendor', targetName);
  rmSync(target, { recursive: true, force: true });
  mkdirSync(target, { recursive: true });
  for (const file of files) {
    cpSync(join(source, file), join(target, file), { recursive: true });
  }
}

copyPackage('mathjax', 'mathjax', [
  'tex-chtml.js', 'input/tex', 'ui', 'a11y', 'sre', 'LICENSE', 'package.json',
]);
copyPackage('@mathjax/mathjax-newcm-font', 'mathjax-newcm-font', [
  'chtml.js', 'chtml', 'package.json',
]);
console.log('Copied MathJax and CHTML fonts to assets/vendor/');
