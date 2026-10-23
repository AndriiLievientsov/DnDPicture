// Локальный рендер Homebrewery V3 (5ePHB): node render.mjs brew.md style.css out.html
// Повторяет brewRenderer.jsx: деление на страницы, \page{...}, искусственный \column в конце страницы.
import fs from 'fs';
import { hbfm } from 'marked-hbfm';

const [,, mdPath, cssPath, outPath, theme = '5ePHB'] = process.argv;
const text = fs.readFileSync(mdPath, 'utf8');
const style = cssPath && fs.existsSync(cssPath) ? fs.readFileSync(cssPath, 'utf8') : '';
const PAGEBREAK = /^(?=\\page(?:break)?(?: *{[^\n{}]*})?$)/m;
const pages = text.split(PAGEBREAK);
const out = pages.map((pageText, index) => {
  let classes = 'page', attrs = '', st = '';
  if (pageText.startsWith('\\page')) {
    const first = hbfm.marked.lexer(pageText.split('\n', 1)[0])[0].tokens;
    const tags = first?.find(o => o.injectedTags !== undefined)?.injectedTags;
    if (tags) {
      classes = [classes, tags.classes].join(' ').trim();
      st = Object.entries(tags.styles || {}).map(([k, v]) => `${k}:${v}`).join(';');
      attrs = Object.entries(tags.attributes || {}).map(([k, v]) => ` ${k}="${v}"`).join('');
    }
    pageText = pageText.includes('\n') ? pageText.substring(pageText.indexOf('\n') + 1) : '';
  }
  pageText += `\n\n&nbsp;\n\\column\n&nbsp;`;
  const html = hbfm.render(pageText, index);
  return `<div class="${classes}" id="p${index + 1}" data-index="${index}" style="${st}"${attrs}><div class="columnWrapper">${html}</div></div>`;
}).join('\n');
const B = '';
const doc = `<!doctype html><html lang="ru"><head><meta charset="utf-8">
<link rel="stylesheet" href="${B}/themes/V3/Blank/style.css">
${theme !== 'Blank' ? `<link rel="stylesheet" href="${B}/themes/V3/${theme}/style.css">` : ''}
<style>
body{margin:0;background:#555}
.pages{padding:20px 0}
.pages > .page{width:215.9mm;height:279.4mm;margin:0 auto 20px;box-shadow:1px 4px 14px #000}
@media print{body{background:none}.pages{padding:0}.pages>.page{margin:0;box-shadow:none;break-after:page}}
@page{size:215.9mm 279.4mm;margin:0}
</style>
<style>${style}</style></head>
<body><div class="brewRenderer"><div class="pages" lang="ru">${out}</div></div></body></html>`;
// абсолютные пути /assets → локальные
fs.writeFileSync(outPath, doc);
console.log('pages:', pages.length);
